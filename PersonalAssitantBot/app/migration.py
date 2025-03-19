from sqlmodel import SQLModel, create_engine
import os
from dotenv import load_dotenv

from models import User
from models import Chat_History

load_dotenv()
PG_CONNECTION_URL = os.getenv("PG_CONNECTION")

engine = create_engine(PG_CONNECTION_URL)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine,checkfirst=True)


def main():
    create_db_and_tables()

if __name__ == "__main__":
    main()

