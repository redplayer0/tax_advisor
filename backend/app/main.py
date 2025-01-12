from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestFormStrict
from sqlmodel import select, Session
from app.db import (
    create_db_and_tables,
    SessionDep,
    User,
    UserCreate,
    UserPublic,
    hash_password,
    verify_password,
)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def authenticate_user(session: Session, username: str, password: str):
    try:
        user = session.exec(select(User).where(User.username == username)).one()
        if verify_password(password, user.hashed_password):
            return user
    except:  # noqa: E722
        return False


def decode_token(token: str, session: Session):
    return token


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: SessionDep,
):
    user = decode_token(token, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


# async def get_current_active_user(
#     current_user: Annotated[User, Depends(get_current_user)],
# ):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


@app.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestFormStrict, Depends()],
    session: SessionDep,
):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return dict(access_token=user.username, token_type="bearer")


@app.post("/users/", response_model=UserPublic)
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
