import datetime
from typing import Annotated as Annttd

import jwt
import pwdlib
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel

auth_router = APIRouter(prefix="/auth", tags=["auth"])

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Pass = secret
fake_users_db = {
    "jp2": {
        "username": "jp2",
        "full_name": "John Duo",
        "email": "johnduo@example.com",
        "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$wagCPXjifgvUFBzq4hqe3w$CYaIb8sB+wtD+Vu/P4uod1+Qof8h+1g7bbDlBID48Rc",  # noqa: E501
        "disabled": False,
    }
}


class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


password_hash = pwdlib.PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

app = FastAPI()

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

USERNAME_PASS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},
)


async def get_current_user(token: Annttd[str, Depends(oauth2_scheme)]) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except InvalidTokenError as exc_info:
        raise CREDENTIALS_EXCEPTION from exc_info
    if (username := payload.get("sub", None)) is None:
        raise CREDENTIALS_EXCEPTION from None
    user = fake_users_db.get(username)
    if user is None or user["disabled"]:
        raise CREDENTIALS_EXCEPTION from None
    if user["disabled"]:
        raise HTTPException(status_code=400, detail="Inactive user")
    return User.model_validate(user)


@auth_router.post("/token")
async def login_for_access_token(
    form_data: Annttd[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = fake_users_db.get(form_data.username, None)
    if not user:
        raise USERNAME_PASS_EXCEPTION
    if not password_hash.verify(form_data.password, user["hashed_password"]):
        raise USERNAME_PASS_EXCEPTION
    now = datetime.datetime.now(datetime.UTC)
    expire = now + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data = {"sub": user["username"], "exp": expire}
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return Token(access_token=encoded_jwt, token_type="bearer")


@auth_router.get("/users/me/", response_model=User)
async def read_users_me(user: Annttd[User, Depends(get_current_user)]) -> User:
    return user


@auth_router.get("/users/me/items/")
async def read_own_items(user: Annttd[User, Depends(get_current_user)]):
    return [{"item_id": "Foo", "owner": user.username}]
