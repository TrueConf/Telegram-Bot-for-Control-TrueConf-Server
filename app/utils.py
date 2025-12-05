import httpx
import tomlkit
from telegram import Update

from .config import TG_USERS_ID, SETTINGS
from .localization import STRINGS


def save_settings(settings):
    with open("settings.toml", "w") as f:
        tomlkit.dump(settings, f)


def auth_user(update: Update):
    if update.message.from_user.id in TG_USERS_ID:
        return True
    if update.effective_user.id in TG_USERS_ID:
        return True
    update.message.reply_text(STRINGS("access_denied"))
    return False


def ssl_certificate(server):
    if server["ssl_certificate"]:
        return True
    elif not server["ssl_certificate"]:
        return False
    else:
        return server["ssl_certificate"]


def get_access_token(server):
    try:

        url = f"https://{server['ip']}/oauth2/v1/token"

        data = {
            "grant_type": "client_credentials",
            "client_id": server["client_id"],
            "client_secret": server["client_secret"],
        }

        with httpx.Client(verify=False) as client:
            response = client.post(url=url, data=data)
        if response.status_code != 200:
            raise httpx.HTTPError
        server["access_token"] = response.json()["access_token"]
        SETTINGS["servers"][server["ip"]]["access_token"] = server["access_token"]
        save_settings(SETTINGS)
        return True
    except httpx.HTTPError:
        if response.json()["reason"] == "InvalidCredentials":
            return False
