import jwt
from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from backend import exceptions

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


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


async def get_user(
    request: Request,
    _=Depends(oauth2_scheme),  # noqa: B008
) -> User:
    # middleware may have already decoded token
    if request.state.user is None:
        raise exceptions.auth.ForbiddenError
    return request.state.user


async def extract_jwt(token: str) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.exceptions.InvalidTokenError as exc_info:
        raise exceptions.auth.JwtDecodeError from exc_info
    if (username := payload.get("sub", None)) is None:
        raise exceptions.auth.JwtDecodeError from None
    user = fake_users_db.get(username)
    if user is None or user["disabled"]:
        raise exceptions.auth.ForbiddenError from None
    return User.model_validate(user)
