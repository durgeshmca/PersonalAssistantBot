from sqlmodel import Field, SQLModel,Column,TIMESTAMP,text
import uuid
import datetime
from sqlalchemy.dialects.postgresql import JSONB

class Chat_History(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    session_id : uuid.UUID = Field(index=True)
    message:  dict = Field(sa_type=JSONB, nullable=False)
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

