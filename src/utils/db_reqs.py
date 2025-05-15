from sqlmodel import SQLModel, Column, JSON, Field, create_engine, select, Session
from typing import List, Dict, Any
import os, json

class Questions(SQLModel, table = True):
    id: int = Field(default=None, primary_key=True)
    question: str = Field(default=None)
    answers: List[Dict[str, str]] = Field(default=None, sa_column=Column(JSON))
    correct_answer: int = Field(default=None)
    description: str = Field(default=None)
    difficult: str = Field(default=None)
    points: int = Field(default=None)

quiz_sqlite_path = "src/core/quiz.db"
json_path = "src/core/quiz.json"
quiz_dbsqlite = f"sqlite:///{quiz_sqlite_path}"
quiz_sqlite_engine = create_engine(quiz_dbsqlite)

def create_QuizDB() -> None:
    # Chequeamos que la DB exista, en caso de que no exista, la creamos y le metemos todas las preguntas dentro
    if not os.path.exists(quiz_sqlite_path):
        Questions.metadata.create_all(quiz_sqlite_engine)
        
        if os.path.exists(json_path):
            with open(json_path, "r", encoding="utf-8") as file:
                data = json.load(file)    
                
                with Session(quiz_sqlite_engine) as session:
                    for questions in data:
                        session.add(Questions(question=questions["question"],
                                            answers=questions["answers"],
                                            correct_answer=questions["correct_answer"],
                                            description=questions["description"],
                                            difficult=questions["difficult"],
                                            points=questions["points"]
                                            ))
                        session.commit()
        else:
            raise Exception("No existe el archivo quiz.json")
        
def get_Quiz() -> List[Dict[str, Any]]:
    questions = []
    with Session(quiz_sqlite_engine) as session:
        counter = 1
        
        while counter <= 20:
            
            statement = select(Questions).where(Questions.id == counter)
            result = session.exec(statement)
            
            for res in result:
                questions.append({
                    "id": res.id,
                    "question": res.question,
                    "answers": res.answers,
                    "correct_answer": res.correct_answer,
                    "description": res.description,
                    "difficult": res.difficult,
                    "points": res.points
                })
            
            counter += 1
        
    return questions

class People(SQLModel, table = True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(default=None)
    points: int = Field(default=0)
    
people_sqlite_path = "src/core/people.db"
people_db = f"sqlite:///{people_sqlite_path}"
people_sqlite_engine = create_engine(people_db)

def create_PeopleDB() -> None:
    if not os.path.exists(people_sqlite_path):
        People.metadata.create_all(people_sqlite_engine)