import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from jwt.exceptions import InvalidTokenError
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestFormStrict
from sqlmodel import Session, select

from fastapi.middleware.cors import CORSMiddleware
from app.db import (
    SessionDep,
    User,
    UserCreate,
    UserPublic,
    create_db_and_tables,
    hash_password,
    verify_password,
)

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
HASH_ALGORITHM = os.getenv("HASH_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINS = os.getenv("ACCESS_TOKEN_EXPIRE_MINS") or 10

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

origins = [
    "http://localhost",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def main():
    return {"message": "Hello World"}


def authenticate_user(session: Session, username: str, password: str):
    try:
        user = session.exec(select(User).where(User.username == username)).one()
        if verify_password(password, user.hashed_password):
            return user
    except:  # noqa: E722
        return False


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: SessionDep,
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[HASH_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = session.exec(select(User).where(User.username == username)).one()
    if user is None:
        raise credentials_exception
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=HASH_ALGORITHM)
    return encoded_jwt


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestFormStrict, Depends()],
    session: SessionDep,
):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINS)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return dict(access_token=access_token, token_type="bearer")


@app.post("/signup", response_model=UserPublic)
def create_user(user: UserCreate, session: SessionDep):
    data = dict(hashed_password=hash_password(user.password))
    db_user = User.model_validate(user, update=data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@app.get("/users/me", response_model=UserPublic)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
