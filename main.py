from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from src.utils.db_reqs import create_QuizDB, get_Quiz
from src.utils.logger import Logger

log = Logger()

async def lifespan(app: FastAPI):
    try:
        create_QuizDB()
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def hello():
    return JSONResponse({"Hello": "World!"})

@app.get("/questions")
async def questions():
    results = get_Quiz()
    return results