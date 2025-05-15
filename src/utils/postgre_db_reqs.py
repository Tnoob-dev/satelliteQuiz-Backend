from sqlmodel import SQLModel, Field, create_engine, select, Session
from typing import List, Dict, Any
import os, dotenv

dotenv.load_dotenv("./src/core/.env")

class People(SQLModel, table = True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(default=None)
    points: int = Field(default=0)
    
people_postgre_engine = create_engine(os.getenv("PEOPLE_DB"))

def create_PeopleDB() -> None:
    for table in SQLModel.metadata.tables.values():
        if table.name != "questions":
            table.create(people_postgre_engine)
        
# def insert_people() -> str:
#     pass