import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))

ADMINS = os.getenv("ADMIN_ID").split(",")

PAYME_TOKEN = str(os.getenv("PAYME_TOKEN"))

PG_USER = str(os.getenv("PGUSER"))
PG_PASS = str(os.getenv("PGPASSWORD"))
DATABASE = str(os.getenv("DATABASE"))
PGHOST = str(os.getenv("PGHOST"))


POSTGRES_URI = f"postgresql://{PG_USER}:{PG_PASS}@{PGHOST}/{DATABASE}"

I18N_DOMAIN = "bot"
BASE_DIR = Path(__file__).parent.parent
LOCALES_DIR = BASE_DIR / 'locales'


LANGUAGES = {
    "🇷🇺 Русский": "ru",
    "🇺🇿 Ўзбек тили": "uz",
}
