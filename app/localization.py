import os
import i18n
from app.config import SETTINGS

i18n.load_path.append(os.path.join(os.getcwd(), "app", "locales"))
i18n.set("locale",SETTINGS["locale"])
i18n.set("filename_format", "{locale}.{format}")
i18n.set("skip_locale_root_data", True)
STRINGS = i18n.t