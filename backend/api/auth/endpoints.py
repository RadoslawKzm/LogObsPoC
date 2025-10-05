import datetime
from typing import Annotated as Annttd

import jwt
import pwdlib
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from backend import exceptions
from backend.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    SECRET_KEY,
    Token,
    fake_users_db,
)

auth_router = APIRouter(prefix="/auth", tags=["auth"])


password_hash = pwdlib.PasswordHash.recommended()


@auth_router.post("/token")
async def login_for_access_token(
    form_data: Annttd[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = fake_users_db.get(form_data.username, None)
    if not user:
        raise exceptions.auth.UnauthorizedError
    if not password_hash.verify(form_data.password, user["hashed_password"]):
        raise exceptions.auth.UnauthorizedError
    now = datetime.datetime.now(datetime.UTC)
    expire = now + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data = {"sub": user["username"], "exp": expire}
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return Token(access_token=encoded_jwt, token_type="bearer")


# @auth_router.get("/users/me/")
# async def read_users_me(user: Annttd[User, Depends(get_current_user)]):
#     return user
#
#
# @auth_router.get("/users/me/items/")
# async def read_own_items(user: Annttd[User, Depends(get_current_user)]):
#     return [{"item_id": "Foo", "owner": user.username}]
