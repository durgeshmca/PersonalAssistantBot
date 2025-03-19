from sqlmodel import Field, SQLModel,Column,TIMESTAMP,text,select,Session
import uuid
import datetime
from pydantic import BaseModel

# class UserRead(BaseModel):
#     id: int | None = None
#     user_uuid : uuid.UUID | None = Field(default_factory=uuid.uuid4, unique=True)
#     first_name: str | None = None
#     last_name: str | None = None
#     mobile: str  | None = None
#     email: str  | None = None


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_uuid : uuid.UUID | None = Field(default_factory=uuid.uuid4, unique=True)
    first_name: str = Field(index=True)
    last_name: str | None = None
    mobile: str = Field(index=True)
    email: str = Field(index=True)
    password: str 
    is_active: bool |None = Field(default=True)
    email_verified_at : datetime.datetime | None = Field(default=None)
    created_at : datetime.datetime | None = Field(sa_column=Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    ))
    updated_at : datetime.datetime | None = Field(sa_column=Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        server_onupdate=text("CURRENT_TIMESTAMP"),
    ))
    deleted_at : datetime.datetime | None = Field(default=None)


class UserBase(BaseModel):
    user_uuid : uuid.UUID | None = None
    first_name: str 
    last_name: str | None = None
    mobile: str 
    email: str 
    is_active: bool |None = True
    email_verified_at : datetime.datetime | None 
    created_at : datetime.datetime | None = None
    updated_at : datetime.datetime | None = None
    deleted_at : datetime.datetime | None = None

class UserInDB(UserBase):
    password: str

class UserCreate(BaseModel):
    first_name: str 
    last_name: str | None = None
    mobile: str 
    email: str 
    password: str
    

def get_user_by_username(session:Session,username:str):
    statement = select(User).where(User.email == username)
    user = session.exec(statement).first()
    return user


def create_user(session:Session,user : UserCreate):
    new_user = User(
        user_uuid=None,
        first_name=user.first_name,
        last_name=user.last_name,
        mobile=user.mobile,
        email=user.email,
        password=user.password
    )

    with  session:
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user