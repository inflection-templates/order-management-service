from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):

    # App
    ENV: str = "development"
    BASE_URL: str = "http://localhost:12345"
    USER_ACCESS_TOKEN_SECRET="secret"
    CIPHER_SALT="salt"

    #Database
    DB_USER_NAME: str = "dbuser"
    DB_USER_PASSWORD: str = "dbpassword"
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_NAME: str = "order_management"
    DB_POOL_SIZE: int = 10
    DB_POOL_RECYCLE: int = 1800
    DB_POOL_TIMEOUT: int = 30
    DB_DIALECT: str = "mysql"
    DB_DRIVER: str = "pymysql"
    DB_CONNECTION_STRING: str = f"{DB_DIALECT}+{DB_DRIVER}://{DB_USER_NAME}:{DB_USER_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
