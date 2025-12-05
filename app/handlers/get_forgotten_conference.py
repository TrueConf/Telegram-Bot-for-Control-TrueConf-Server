import urllib
import datetime
import httpx
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from ..config import SERVERS
from ..localization import STRINGS
from ..utils import ssl_certificate, get_access_token

def get_participants_list(server, session_id):
    try:

        url = f"https://{server["ip"]}/api/v3.3/conference-sessions/{session_id}/participants?access_token={server["access_token"]}"
        with httpx.Client(verify=ssl_certificate(server), timeout=5) as client:
            response = client.get(url)
        response.raise_for_status()
        count = response.json()["count"]
        participants = response.json()["participants"]
        if len(participants) == 1 and participants[0]["role"] == 2:
            return True, count
        else:
            for i in participants:
                if i["role"] == 2:
                    return False, count
        return True, count
    except httpx.HTTPError:
        return False, 0


def get_forgotten_conference(server):
    try:
        url = f"https://{server["ip"]}/api/v3.3/logs/calls?access_token={server["access_token"]}&sort_field=end_time&sort_order=1&page_size=500"
        with httpx.Client(verify=ssl_certificate(server), timeout=5) as client:
            response = client.get(url)
        response.raise_for_status()  # проверка статуса ответа
        forgotten_list = []
        for i in response.json()["list"]:
            if i["end_time"] is None and i["class"] > 1 and i["duration"] / 3600 >= 1:
                flag, participant_count = get_participants_list(
                    server, urllib.request.pathname2url(i["conference_id"])
                )
                if flag:
                    forgotten_list.append(
                        {
                            "conf_id": urllib.request.pathname2url(i["conference_id"]),
                            "named_id": i["named_conf_id"],
                            "participant_count": participant_count,
                            "topic": i["topic"],
                            "owner": i["owner"],
                            "duration": str(datetime.timedelta(seconds=i["duration"])),
                        }
                    )
        return forgotten_list
    except httpx.HTTPError:
        if 'response' in locals():
            if response.status_code == 403:
                if response.json()["error"]["errors"][0]["reason"] == "accessTokenInvalid":
                    if get_access_token(server):
                        return get_forgotten_conference(server)
                    else:
                        return None
            elif response.status_code == 404:
                return "ConnectionError"
    except httpx.ConnectTimeout:
        return "ConnectionError"


def get_result_forgotten(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    update.message = query.message
    server = str(query.data).split("|")[1]

    keyboard_back = [
        [
            InlineKeyboardButton(
                STRINGS("back"), callback_data="service_select_button|{}".format(server)
            )
        ]
    ]
    forgotten_list = get_forgotten_conference(SERVERS[server])
    if forgotten_list is None:
        update.message.edit_text(
            STRINGS("error_oauth2").format(server),
            reply_markup=InlineKeyboardMarkup(keyboard_back),
            parse_mode="HTML",
        )
    elif forgotten_list == "ConnectionError":
        query.message.edit_text(
            STRINGS("connection_error").format(server),
            reply_markup=InlineKeyboardMarkup(keyboard_back),
            parse_mode="HTML",
        )
    elif forgotten_list:
        keyboard_stop = [[]]
        j = 0
        k = 0
        h = STRINGS("found_forgotten_conf").format(server)
        for i in forgotten_list:
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
                    callback_data="stop_conference_button|{}|0|{}".format(
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
        update.message.edit_text(
            STRINGS("no_forgotten_conf").format(server),
            reply_markup=InlineKeyboardMarkup(keyboard_back),
            parse_mode="HTML",
        )
