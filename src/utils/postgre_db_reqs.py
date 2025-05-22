from sqlmodel import SQLModel, Field, create_engine, select, Session
import os, dotenv
from fastapi import status
from fastapi.exceptions import HTTPException

dotenv.load_dotenv("./src/core/.env")

class People(SQLModel, table = True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(default=None, index=True)
    points: int = Field(default=0)
    
DB_URL: str = os.getenv("PEOPLE_DB")
people_postgre_engine = create_engine(DB_URL)

def create_PeopleDB() -> None:
    for table in SQLModel.metadata.tables.values():
        if table.name != "questions":
            if not people_postgre_engine.dialect.has_table(people_postgre_engine.connect(), table.name):
                table.create(people_postgre_engine)
        
def insert_people(name: str) -> str:
    with Session(people_postgre_engine) as session:
        statement = select(People).where(People.name == name)
        person = session.exec(statement).first()
        
        if person:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str("Already exists a user with that name"))
        else:
            try:
                session.add(People(name=name))
                session.commit()
                
                return "User added"
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(f"Error -> {e}"))

def get_People():
    people = []
    
    with Session(people_postgre_engine) as session:
        statement = select(People)
        results = session.exec(statement).all()
        for person in results:
            people.append(person.model_dump())

    return people

def updatePoints(name: str, points: int) -> str:
    with Session(people_postgre_engine) as session:
        statement = select(People).where(People.name == name)
        person = session.exec(statement).first()
        
        if not person:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(f"Error -> {e}"))
        else:
            try:                
                if person.points == 100:
                    return {"User already have maximum points"}
                elif person.points < 100 and person.points > 0:
                    
                    person.points += points
                        
                    if person.points >= 100:
                        person.points = 100
                        
                    session.add(person)
                    session.commit()
                    
                    session.refresh(person)
                    
                    return "Points added"
            except Exception as e:
                session.rollback()
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(f"Error -> {e}"))
                