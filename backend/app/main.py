from typing import Annotated
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from app.db import create_db_and_tables, SessionDep, User, UserCreate, UserPublic

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def hash_password(password: str) -> str:
    return f"hashed{password}"


@app.get("/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/users/", response_model=UserPublic)
def create_user(user: UserCreate, session: SessionDep):
    data = dict(hashed_password=hash_password(user.password))
    db_user = User.model_validate(user, update=data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
