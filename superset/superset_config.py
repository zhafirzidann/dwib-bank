import os


SECRET_KEY = os.getenv(
    "SUPERSET_SECRET_KEY",
    "dwib-bank-superset-secret-key-for-local-development-2026",
)
WTF_CSRF_ENABLED = True
SQLALCHEMY_DATABASE_URI = "sqlite:////app/superset_home/superset.db"
