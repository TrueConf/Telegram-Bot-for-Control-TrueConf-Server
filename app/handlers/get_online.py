import httpx
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CallbackQueryHandler
from ..config import SERVERS
from ..localization import STRINGS
from ..utils import ssl_certificate, get_access_token

def get_online_users(server):
    online_count = 0
    page_id = 0
    next_page_id = 0
    try:
        while next_page_id != -1:
            url = f"https://{server["ip"]}/api/v3.3/users?access_token={server["access_token"]}&page_id={page_id}"
            with httpx.Client(verify=ssl_certificate(server), timeout=5) as client:
                response = client.get(url)
            response.raise_for_status()  # проверка статуса ответа
            for i in response.json()["users"]:
                if i["status"] in (1, 2, 5):
                    online_count += 1
            next_page_id = response.json()["next_page_id"]
            page_id += 1
        return online_count
    except httpx.HTTPError:
        if 'response' in locals():
            if response.status_code == 403:
                if response.json()["error"]["errors"][0]["reason"] == "accessTokenInvalid":
                    if get_access_token(server):
                        return get_online_users(server)
                    else:
                        return None
            elif response.status_code == 404:
                return "ConnectionError"
    except httpx.ConnectTimeout:
        return "ConnectionError"


def online_users_button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    update.message = query.message
    server = str(query.data).split("|")[1]
    online_list = get_online_users(SERVERS[server])
    keyboard = [
        [
            InlineKeyboardButton(
                STRINGS("back"), callback_data="service_select_button|{}".format(server)
            )
        ]
    ]

    if online_list:
        query.message.edit_text(
            STRINGS("online_user").format(server, online_list),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML",
        )
    elif online_list is None:
        query.message.edit_text(
            STRINGS("error_oauth2").format(server),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML",
        )
    elif online_list == "ConnectionError":
        query.message.edit_text(
            STRINGS("connection_error").format(server),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML",
        )
    else:
        query.message.edit_text(
            STRINGS("no_online_user").format(server),
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="HTML",
        )
