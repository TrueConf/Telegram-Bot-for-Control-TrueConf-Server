from telegram.ext import Updater
from .config import TG_API_TOKEN

from telegram.ext import CommandHandler, CallbackQueryHandler
from .handlers import (
start_command,
get_conference_button,
stop_conference_button,
get_result_forgotten,
online_users_button,
check_status_button,
service_select_button,
server_status,
one_check_status,
server_select_button,
stop_conference
)

app = Updater(TG_API_TOKEN, use_context=True)

dispatcher = app.dispatcher

dispatcher.add_handler(CommandHandler("start", start_command))
dispatcher.add_handler(CallbackQueryHandler(
    service_select_button, pattern='^service_select_button'))
dispatcher.add_handler(CallbackQueryHandler(
    get_conference_button, pattern='^get_conference_button'))
dispatcher.add_handler(CallbackQueryHandler(
    server_status, pattern='^server_status'))
dispatcher.add_handler(CallbackQueryHandler(
    one_check_status, pattern='^one_check_status'))
dispatcher.add_handler(CallbackQueryHandler(
    server_select_button, pattern='^server_select_button'))
dispatcher.add_handler(CallbackQueryHandler(
    check_status_button, pattern='^check_status_button'))
dispatcher.add_handler(CallbackQueryHandler(
    online_users_button, pattern='^online_users_button'))
dispatcher.add_handler(CallbackQueryHandler(
    get_result_forgotten, pattern='^get_result_forgotten'))
dispatcher.add_handler(CallbackQueryHandler(
    stop_conference_button, pattern='^stop_conference_button'))
dispatcher.add_handler(CallbackQueryHandler(
    stop_conference, pattern='^stop_conference'))




