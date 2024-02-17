import logging
from typing import Annotated
from fastapi import FastAPI, Response, Cookie
from keycloak import KeycloakOpenID
from starlette.responses import RedirectResponse

from settings import settings

logger = logging.getLogger(__name__)
app = FastAPI()

keycloak_openid = KeycloakOpenID(
    server_url=settings.KEYCLOAK_URL,
    realm_name=settings.REALM,
    client_id=settings.CLIENT_ID,
    client_secret_key=settings.CLIENT_SECRET_KEY
)

options = {"verify_signature": False, "verify_aud": False, "verify_exp": False}


def decode_token(token: str):
    KEYCLOAK_PUBLIC_KEY = "-----BEGIN PUBLIC KEY-----\n" + keycloak_openid.public_key() + "\n-----END PUBLIC KEY-----"
    try:
        token_info = keycloak_openid.decode_token(token, key=KEYCLOAK_PUBLIC_KEY, options=options)
    except Exception as e:
        logger.error(e)
        token_info = None
    return token_info


@app.get("/auth/check")
def check_auth(access_token: Annotated[str, Cookie()] = ""):
    if access_token:
        token_info = decode_token(access_token)
        redirect = token_info is None
    else:
        redirect = True
    url = keycloak_openid.auth_url(scope="openid+profile", redirect_uri=settings.REDIRECT_URL)
    return {
        "url": url,
        "redirect": redirect
    }


@app.get("/auth/logout")
def logout(refresh_token: Annotated[str | None, Cookie()] = None):
    keycloak_openid.logout(refresh_token)
    response = RedirectResponse("/")
    response.set_cookie(key="access_token", value="")
    response.set_cookie(key="refresh_token", value="")
    return response


@app.get("/auth/callback")
def auth_callback(code: str = "", ):
    access_token = keycloak_openid.token(
        grant_type='authorization_code',
        code=code,
        redirect_uri=settings.REDIRECT_URL)
    response = RedirectResponse("/")
    response.set_cookie(key="access_token", value=access_token["access_token"])
    response.set_cookie(key="refresh_token", value=access_token["refresh_token"])
    return response


@app.get("/api/group_1")
def read_root():
    return {"message": "Hello group 1 member"}


@app.get("/api/group_2")
def read_root():
    return {"message": "Hello group 2 member"}


@app.get("/api/group_3")
def read_root():
    return {"message": "Hello group 3 member"}
