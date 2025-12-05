import httpx
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from ..config import SERVERS
from ..localization import STRINGS
from ..utils import ssl_certificate
from .get_forgotten_conference import get_result_forgotten
from .get_conference import get_conference_button

def stop_conference_button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    update.message = query.message
    data = query.data.split("|")
    server = data[1]
    conf_id = data[3]
    keyboard = [
        [
            InlineKeyboardButton(
                STRINGS("confirm_stop"),
                callback_data="stop_conference|{}|{}|{}".format(
                    server, data[2], conf_id
                ),
            )
        ],
        [
            InlineKeyboardButton(
                STRINGS("back"), callback_data="get_conference_button|{}".format(server)
            )
        ],
    ]
    update.message.edit_text(
        STRINGS("confirm_stop_message").format(conf_id),
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="HTML",
    )


def stop_conference(update: Update, context: CallbackContext):
    q = update.callback_query.data.split("|")
    server = SERVERS[q[1]]
    conf_id = q[3]
    flag = q[2]
    response = ""
    try:
        url = f"https://{server["ip"]}/api/v3.3/conferences/{conf_id}/stop?access_token={server["access_token"]}"
        with httpx.Client(verify=ssl_certificate(server)) as client:
            response = client.post(url)
        response.raise_for_status()
        if flag == "0":
            get_result_forgotten(update, context)
            return None
        else:
            get_conference_button(update, context)
            return None
    except httpx.HTTPStatusError:
        if 'response' in locals():
            if response.json()["reason"] == "InvalidCredentials":
                return False
            elif response.status_code == 404:
                return False
        return None
    except httpx.ConnectTimeout:
        return False
