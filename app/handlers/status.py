import httpx
import threading
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup, TelegramError
from telegram.ext import CallbackContext, CallbackQueryHandler
from ..config import SERVERS, SETTINGS, TG_API_TOKEN, TG_USERS_ID, STATUS
from ..localization import STRINGS
from ..utils import save_settings, ssl_certificate

def one_check_status(server):
    try:
        url = f"http://{server}:4307/vsstatus"
        with httpx.Client(timeout=5) as client:
            response = client.get(url)
        response.raise_for_status()
        return STRINGS("one_status_on")
    except (httpx.ConnectTimeout, httpx.ConnectError):
        return STRINGS("one_status_off")


def check_status(server, state):
    if state:
        bot = Bot(TG_API_TOKEN)
        global STATUS
        status_th = threading.Timer(
            server["server_status"]["timeout"], check_status, args=[server, state]
        )
        try:
            url = f"http://{server["ip"]}:4307/vsstatus"
            with httpx.Client(timeout=5) as client:
                response = client.get(url)
            response.raise_for_status()
            if server["ip"] not in STATUS.keys():
                STATUS[server["ip"]] = 1
                status_th.start()
            elif STATUS[server["ip"]] == 0:
                STATUS[server["ip"]] = 1
                for _id in TG_USERS_ID:
                    try:
                        bot.send_message(
                            chat_id=_id,
                            text=STRINGS("status_on").format(server["ip"]),
                            parse_mode="html",
                        )
                    except TelegramError:
                        continue
                status_th.start()
            else:
                status_th.start()
        except (
            httpx.ConnectError,
            httpx.ConnectTimeout,
        ):
            if server["ip"] not in STATUS.keys():
                STATUS[server["ip"]] = 0
                status_th.start()
            elif STATUS[server["ip"]] == 1:
                STATUS[server["ip"]] = 0
                for _id in TG_USERS_ID:
                    try:
                        bot.send_message(
                            chat_id=_id,
                            text=STRINGS("status_off").format(server["ip"]),
                            parse_mode="html",
                        )
                    except TelegramError:
                        continue
                status_th.start()
            else:
                status_th.start()


def check_status_button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    update.message = query.message
    server = SERVERS[str(query.data).split("|")[1]]
    if not server["server_status"]["state"]:
        server["server_status"]["state"] = True

        check_status(server, 1)
    else:
        server["server_status"]["state"] = False
        check_status(server, 0)
    SETTINGS["servers"][str(query.data).split("|")[1]] = server
    save_settings(SETTINGS)
    server_status(update, context, server)


def server_status(update: Update, context: CallbackContext, server=None) -> None:
    query = update.callback_query
    query.answer()
    server = str(query.data).split("|")[1]
    if SERVERS[server]["server_status"]["state"]:
        keyboard = [
            [
                InlineKeyboardButton(
                    STRINGS("stop_check_status"),
                    callback_data="check_status_button|{}".format(server),
                )
            ],
            [
                InlineKeyboardButton(
                    STRINGS("back"),
                    callback_data="service_select_button|{}".format(server),
                )
            ],
        ]
        query.message.edit_text(
            STRINGS("started_check_status").format(
                server,
                one_check_status(server),
                SERVERS[server]["server_status"]["timeout"],
            ),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML",
        )
    else:
        keyboard = [
            [
                InlineKeyboardButton(
                    STRINGS("start_check_status"),
                    callback_data="check_status_button|{}".format(server),
                )
            ],
            [
                InlineKeyboardButton(
                    STRINGS("back"),
                    callback_data="service_select_button|{}".format(server),
                )
            ],
        ]
        query.message.edit_text(
            STRINGS("stoped_check_status").format(server, one_check_status(server)),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML",
        )