import json
import httpx
import urllib
import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CallbackQueryHandler
from ..config import SERVERS
from ..localization import STRINGS

from ..utils import get_access_token, ssl_certificate


def get_conference_running(server):
    try:
        url = f"https://{server['ip']}/api/v3.3/logs/calls"

        data = {
            "access_token": server["access_token"],
            "sort_field": "end_time",
            "sort_order": 1,
            "page_size": 200,
        }

        with httpx.Client(verify=ssl_certificate(server), timeout=5) as client:
            response = client.get(url=url, params=data)
        response.raise_for_status()  # проверка статуса ответа
        run_list = []
        for i in response.json()["list"]:
            if i["end_time"] is None and i["class"] > 1:
                if i["topic"] is None:
                    topic = "Без названия"
                else:
                    topic = i["topic"]
                run_list.append(
                    {
                        "conf_id": urllib.request.pathname2url(i["conference_id"]),
                        "named_id": i["named_conf_id"],
                        "participant_count": i["participant_count"],
                        "topic": topic,
                        "owner": i["owner"],
                        "duration": str(datetime.timedelta(seconds=i["duration"])),
                    }
                )
        return run_list
    except httpx.HTTPError:
        if 'response' in locals():
            if response and response.status_code == 403:
                if response.json()["error"]["errors"][0]["reason"] == "accessTokenInvalid":
                    if get_access_token(server):
                        return get_conference_running(server)
                    else:
                        return None
            elif response.status_code == 404:
                return "ConnectionError"
    except httpx.ConnectTimeout:
        return "ConnectionError"


def get_conference_button(
    update: Update, context: CallbackContext, server=None
) -> None:
    query = update.callback_query
    query.answer()
    update.message = query.message
    server = str(query.data).split("|")[1]
    run_list = get_conference_running(SERVERS[server])
    keyboard = [
        [
            InlineKeyboardButton(
                STRINGS("back"), callback_data="service_select_button|{}".format(server)
            )
        ]
    ]
    if run_list is None:
        update.message.edit_text(
            STRINGS("error_oauth2").format(server),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML",
        )
    elif run_list == "ConnectionError":
        query.message.edit_text(
            STRINGS("connection_error").format(server),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML",
        )
    elif run_list:
        keyboard_stop = [[]]
        j = 0
        k = 0
        h = STRINGS("run_conf").format(server)
        for i in run_list:
            h += STRINGS("description_conf").format(
                i["named_id"],
                i["participant_count"],
                i["topic"],
                i["owner"],
                i["duration"],
                SERVERS[server]["ip"],
                i["conf_id"],
            )
            if k == 2:
                j += 1
                keyboard_stop.append([])
                k = 0
            keyboard_stop[j].append(
                InlineKeyboardButton(
                    "{}".format(i["named_id"]),
                    callback_data="stop_conference_button|{}|1|{}".format(
                        server, i["named_id"]
                    ),
                )
            )
            k += 1
        h += STRINGS("stop_conf")
        keyboard_stop.append(
            [
                InlineKeyboardButton(
                    STRINGS("back"),
                    callback_data="service_select_button|{}".format(server),
                )
            ]
        )
        update.message.edit_text(
            h,
            reply_markup=InlineKeyboardMarkup(keyboard_stop),
            parse_mode="HTML",
            disable_web_page_preview=True,
        )
    else:
        h = STRINGS("no_run_conf").format(server)
        update.message.edit_text(
            h, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML"
        )