from fastapi import FastAPI, HTTPException

from src.Auth_service.models import User
from src.Auth_service.services import get_password_hash, verify_password, create_access_token

app = FastAPI()


db = []

@app.post("/register/")
async def register(username: str, password: str):
    hashed_password = get_password_hash(password)
    new_user = User(username=username, hashed_password=hashed_password, role='user')
    db.append(new_user)
    return {"msg": "User created"}

@app.post("/login/")
async def login(username: str, password: str):
    for user in db:
        if user.username == username:
            break
    else:
        user = None

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": user.username, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app)