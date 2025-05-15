from fastapi import FastAPI
from fastapi.responses import JSONResponse


app = FastAPI(
    version="1.0.0",
    title="satelliteQuiz-Backend"
)

@app.get("/")
async def hello():
    return JSONResponse({"Hello": "World!"})