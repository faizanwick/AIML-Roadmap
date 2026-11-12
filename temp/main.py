from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/css", StaticFiles(directory="css"), name="css")
app.mount("/js", StaticFiles(directory="js"), name="js")
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home(request : Request):
    return templates.TemplateResponse(request, name="index.html")

@app.get("/login")
def login(request : Request):
    return templates.TemplateResponse(request, name="login.html")

@app.get("/register")
def register(request : Request):
    return templates.TemplateResponse(request, name="register.html")

@app.get("/dashboard")
def dashboard(request : Request):
    return templates.TemplateResponse(request, name="dashboard.html")


app.include_router(api_router, prefix="/api/v1")