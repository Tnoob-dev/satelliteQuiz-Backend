from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.utils.sqlite_db_reqs import create_QuizDB, get_Quiz
from src.utils.postgre_db_reqs import create_PeopleDB, get_People, insert_people, updatePoints
from src.utils.logger import Logger

log = Logger()

async def lifespan(app: FastAPI):
    try:
        create_QuizDB()
        create_PeopleDB()
        log.info("dbs created")
        yield
    finally:
        log.info("app closed")
    

app = FastAPI(
    version="1.0.0",
    title="satelliteQuiz-Backend",
    lifespan=lifespan
)
# Solo para desarrollo
origins = ["*"]
# origins = ["https://satellite-quiz.vercel.app/", "localhost", "127.0.0.1"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def hello():
    return JSONResponse({"Hello": "World!"}, status_code=status.HTTP_200_OK)

@app.get("/questions")
async def questions():
    try:
        results = get_Quiz()
        return results
    except Exception as e:
        log.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(f"Error -> {e}"))

@app.get("/get_people")
async def get_all_people():
    try:
        result = get_People()
        return JSONResponse({"result": result}, status_code=status.HTTP_200_OK)
    except Exception as e:
        log.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(f"Error -> {e}"))
    
@app.post("/add_people/{name}")
async def add_people(name: str):
    try:
        msg = insert_people(name)
        return JSONResponse({"message": msg}, status_code=status.HTTP_201_CREATED)
    except Exception as e:
        log.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(f"Error -> {e}"))

@app.put("/update_points")
async def update_points(name: str, points: int):
    try:
        msg = updatePoints(name, points)
        return JSONResponse({"message": msg}, status_code=status.HTTP_200_OK)
    except Exception as e:
        log.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(f"Error -> {e}"))