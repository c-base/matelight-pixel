import asyncio
import json
from typing import Annotated
from datetime import datetime
from contextlib import asynccontextmanager
from starlette.config import Config
from fastapi import Depends, FastAPI, Request, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import BackgroundTasks
from pydantic_settings import BaseSettings, SettingsConfigDict
from starlette.middleware.sessions import SessionMiddleware
# from fastapi.security import OAuth2AuthorizationCodeBearer
from starlette.responses import HTMLResponse, RedirectResponse


class Settings(BaseSettings):
    matelight_host: str
    matelight_port: int

    # File '.env' will be read
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
templates = Jinja2Templates(directory="templates")


PIXEL_WALL = []


class MateLightRunner:
    def __init__(self):
        self.started = False

    async def matelight_loop(self):
        global PIXEL_WALL
        try:
            await asyncio.sleep(1.0)
        except Exception as error:
            await asyncio.sleep(2.0)

    async def run_main(self):
        self.started = True
        while self.started is True:
            await asyncio.sleep(0.1)
            await self.matelight_loop()
                    
    async def stop(self):
        self.started = False

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    runner = MateLightRunner()
    loop = asyncio.get_event_loop()
    loop.create_task(runner.run_main())
    yield
    # Clean up the ML models and release the resources
    runner.stop()

app = FastAPI(lifespan=lifespan)        

# Allow sessions    
app.add_middleware(SessionMiddleware, secret_key="secret-string")

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")


# Home page (index)
@app.get('/')
async def homepage(request: Request):
    user = request.session.get('user')
    context = {
        "request": request,
        "status": "it'    s",
        "user": user
    }
    return templates.TemplateResponse("index.html", context)
