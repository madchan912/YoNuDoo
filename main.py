from fastapi import FastAPI
from services.database import db
from beanie import init_beanie
from routes.recipe import Recipe
from contextlib import asynccontextmanager
from routes import recipe

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_beanie(database=db, document_models=[Recipe])
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(recipe.router, prefix="/recipes", tags=["Recipes"])

@app.get("/")
async def root():
    return {"message": "YoNuDoo 프로젝트 시작!"}
