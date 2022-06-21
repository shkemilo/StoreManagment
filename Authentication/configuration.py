import os
from datetime import timedelta

databaseUrl = os.environ["DATABASE_URL"]


class Configuration ():
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:root@{databaseUrl}/authentication"
    JWT_SECRET_KEY = "SIBIRSKI_PLAVAC"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
