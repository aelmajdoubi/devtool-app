from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles

from app.routes import code_routes
from app.routes import tool_routes

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="super-secret-key")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(code_routes.router)
app.include_router(tool_routes.router)
