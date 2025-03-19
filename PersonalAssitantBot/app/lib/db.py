from sqlmodel import Session,create_engine
from app.config import Config
from typing import Annotated
from fastapi import Depends

# connect_args = {"check_same_thread": False}
engine = create_engine(Config.PG_CONNECTION)
def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]