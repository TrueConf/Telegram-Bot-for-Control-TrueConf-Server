import tomlkit
import httpx

with open("settings.toml", "rb") as f:
    SETTINGS = tomlkit.load(f)

# SETTINGS = json.loads(os.environ['settings']) # for Replit
TG_API_TOKEN = SETTINGS['tg-api-token']
TG_USERS_ID = SETTINGS['tg-users-id']
SERVERS = SETTINGS['servers']
STATUS = {}

http_client = httpx.Client(timeout=5)