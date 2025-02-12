from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from services.database import db
from beanie import init_beanie
from routes.recipe import Recipe
from contextlib import asynccontextmanager
from routes import recipe, autocomplete
from fastapi.templating import Jinja2Templates
from pathlib import Path
from models.autocomplete import AutoComplete

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_beanie(database=db, document_models=[Recipe, AutoComplete])
    yield
app = FastAPI(lifespan=lifespan)

app.include_router(recipe.router, prefix="/recipes", tags=["Recipes"])

app.include_router(autocomplete.router)

# Jinja2 템플릿 설정
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})