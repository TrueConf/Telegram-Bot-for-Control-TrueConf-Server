from app import app
from app.config import SETTINGS, http_client
from app.handlers.status import check_status

def main():

    app.start_polling()
    for server in SETTINGS['servers'].values():
        check_status(server, server['server_status']['state'])
    print('Bot is running...')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        app.stop()
        http_client.close()

