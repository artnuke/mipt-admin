from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import mongodb
from pydantic import BaseModel
import logging
import uvicorn
from logging.config import dictConfig
import logging


logger = logging.getLogger("mycoolapp")

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class user(BaseModel):
    username: str
    gender: str
    age: int
    city: str
    bio: str | None = None
    activate: bool


@app.get("/")
async def read_root():
    logging.error
    ("main")
    return {"Hello": "World"}


@app.get("/main", response_class=HTMLResponse)
async def main_page(request: Request, response_class=HTMLResponse):

    return templates.TemplateResponse("main_page.html", {"request": request, "id": id})


@app.get("/chats", response_class=HTMLResponse)
async def main_page(request: Request, response_class=HTMLResponse):
    return templates.TemplateResponse("chats_page.html", {"request": request, "id": id})


@app.get("/groups", response_class=HTMLResponse)
async def main_page(request: Request, response_class=HTMLResponse):
    data = {"name": "Kirill"}
    return templates.TemplateResponse("groups_page.html", {"request": request, "some": data})


@app.get("/users", response_class=HTMLResponse)
async def main_page(request: Request, response_class=HTMLResponse):
    data = mongodb.list_users()
    return templates.TemplateResponse("users_page.html", {"request": request, "data": data})


# add user
@app.post("/add_user")
async def main_page(request: Request):
    request_data = await request.json()
    response = mongodb.add_user(request_data)
    return {
        "status": "ok",
        "response": response
    }


@app.get("/get_users")
async def main_page():
    response = mongodb.list_users()
    return {
        "status": "ok",
        "response": response
    }


@app.post("/create_group")
async def create_group(request: Request):
    request_data = await request.json()
    response = mongodb.create_collection(request_data.get("groupname"))
    return {
        "status": "ok",
        "response": request_data
    }


@app.get("/get_groups")
async def create_group():
    response = mongodb.list_collections()
    return {
        "status": "ok",
        "response": response
    }
