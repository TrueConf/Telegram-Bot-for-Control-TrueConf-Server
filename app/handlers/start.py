from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from ..config import SERVERS
from ..localization import STRINGS

from app.utils import auth_user

def ssb_keyboard_generator(data):
    keyboard = [[]]
    i = 0
    k = 0
    for server in data.keys():
        if k == 2:
            i += 1
            keyboard.append([])
            k = 0
        keyboard[i].append(InlineKeyboardButton(
            server, callback_data='service_select_button|{}'.format(server)))
        k += 1
    return keyboard

def start_command(update: Update, context: CallbackContext) -> None:
    if not auth_user(update):
        return
    update.message.reply_text(
        STRINGS("select_server"),
        reply_markup=InlineKeyboardMarkup(ssb_keyboard_generator(SERVERS)),
    )


def server_select_button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.message.edit_text(STRINGS('select_server'),
                            reply_markup=InlineKeyboardMarkup(ssb_keyboard_generator(SERVERS)))

def service_select_button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    server = str(query.data).split('|')[1]
    keyboard = [
        [
            InlineKeyboardButton(
                STRINGS("server_status"),
                callback_data="server_status|{}".format(server),
            )
        ],
        [
            InlineKeyboardButton(
                STRINGS("show_run_conf"),
                callback_data="get_conference_button|{}".format(server),
            )
        ],
        [
            InlineKeyboardButton(
                STRINGS("online_user_count"),
                callback_data="online_users_button|{}".format(server),
            )
        ],
        [
            InlineKeyboardButton(
                STRINGS("find_forgotten_conf"),
                callback_data="get_result_forgotten|{}".format(server),
            )
        ],
        [
            InlineKeyboardButton(
                STRINGS("back"), callback_data="server_select_button|{}".format(server)
            )
        ],
    ]
    if query.answer() == "active_calls_button":
        query.message.reply_text(
            STRINGS("server_selected").format(server),
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
    elif query.answer() == "server_status" or "server_select_button":
        query.message.edit_text(
            STRINGS("server_selected").format(server),
            reply_markup=InlineKeyboardMarkup(keyboard),
        )