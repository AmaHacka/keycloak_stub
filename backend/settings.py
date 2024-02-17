import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    KEYCLOAK_URL: str = os.getenv("KEYCLOAK_URL")
    REALM: str = os.getenv("REALM")
    CLIENT_ID: str = os.getenv("CLIENT_ID")
    CLIENT_SECRET_KEY: str = os.getenv("CLIENT_SECRET_KEY")
    REDIRECT_URL: str = os.getenv("REDIRECT_URL")


settings = Settings()

