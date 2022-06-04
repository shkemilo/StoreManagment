from datetime import timedelta
import os

databaseUrl = os.environ["DATABASE_URL"]


class Configuration ():
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:root@{databaseUrl}/authentication"
    JWT_SECRET_KEY = "SIBIRSKI_PLAVAC"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
