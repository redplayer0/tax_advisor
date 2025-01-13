from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    username: str = Field(index=True, unique=True, nullable=False)


class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    hashed_password: str = Field(nullable=False)


class UserPublic(UserBase):
    username: str


class UserCreate(UserBase):
    password: str


class AdviceBase(SQLModel):
    monthly_income: int = Field(nullable=False, gt=0)
    monthly_expenses: int = Field(nullable=False, gt=0)
    is_married: bool = Field(default=False)
    children_count: int = Field(default=0, ge=0)
    prompt: str | None


class Advice(AdviceBase, table=True):
    id: int = Field(default=None, primary_key=True)
    model_response: str
    user_id: int = Field(foreign_key="user.id")


class AdvicePublic(AdviceBase):
    monthly_income: int
    monthly_expenses: int
    is_married: bool
    children_count: int
    prompt: str | None
    model_response: str
