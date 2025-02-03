from fastapi import FastAPI
from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, create_engine, SQLModel
from sqlalchemy.engine import URL
from pydantic_settings import BaseSettings 

#DATABASE_URL = "postgresql://postgres:postgres@localhost/fastapi_transaction"
DATABASE_URL = URL.create(
    drivername = "postgresql",
    username = "postgres",
    password = "postgres",
    host = "localhost",
    database = "fastapi_transaction",
    port = 5432
)

engine = create_engine(DATABASE_URL)

def create_all_tables(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session,Depends(get_session)]
