import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+mysqlconnector://{os.environ['MYSQL_ADDON_USER']}"
        f":{quote_plus(os.environ['MYSQL_ADDON_PASSWORD'])}"
        f"@{os.environ['MYSQL_ADDON_HOST']}:{os.environ['MYSQL_ADDON_PORT']}"
        f"/{os.environ['MYSQL_ADDON_DB']}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 2,
        "max_overflow": 0,
        "pool_recycle": 280,
        "pool_pre_ping": True,
    }

    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "static", "uploads")
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB; si se pasa, Flask responde error 413

    SESSION_COOKIE_SECURE = os.environ.get("PRODUCCION") == "1"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"