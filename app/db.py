from fastapi import FastAPI
from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, create_engine, SQLModel
from app.config import Config

engine = create_engine(Config.DATABASE_URL, echo = False)

def init_db(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    #print(f"--[>] Server is starting ...")
    yield
    #print(f"--[x] Server has been stopped")

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session,Depends(get_session)]
