import jwt
from fastapi import FastAPI, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import NoReturn
from src.models import User, TokenData, AccessToken
from src.services import Salt, auth_service


user_db: dict[str, User] = {
    "john": User("john", Salt.hash_password("test-test")),
    "maks": User("maks", Salt.hash_password("lorem")),
}

oauth2_bearer = OAuth2PasswordBearer("/login/")
app = FastAPI()


def validate_auth_user(  # user service
    username: str = Form(), password: str = Form()
) -> User | NoReturn:
    invalid_data_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )
    user = user_db.get(username)
    if user is None:
        raise invalid_data_exc
    if not Salt.validate_password(password, user.password):
        raise invalid_data_exc
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User is banned"
        )

    return user


def get_current_user(  # user service
    credentials: AccessToken = Depends(oauth2_bearer),
) -> User:
    try:
        payload = auth_service.decode(token=credentials)
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="token invalid"
        )
    username = payload.get("sub")

    user = user_db.get(username)
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="token invalid"
    )


@app.post("/login/")
async def auth_user(user: User = Depends(validate_auth_user)) -> TokenData:
    access_token = auth_service.create_access_token(user)
    refresh_token = auth_service.create_refresh_token(user)
    return TokenData(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@app.post("/get_user/")
async def get_user_by_token(user: User = Depends(get_current_user)):
    return user


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
