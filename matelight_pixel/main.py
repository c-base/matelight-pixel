import asyncio
import traceback
import sys
import json
from contextlib import asynccontextmanager
# sfrom starlette.config import Config
from fastapi import Depends, FastAPI, Request, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from starlette.middleware.sessions import SessionMiddleware
# from fastapi.security import OAuth2AuthorizationCodeBearer
from starlette.responses import HTMLResponse, RedirectResponse

from . import matelight

class Settings(BaseSettings):
    matelight_host: str
    matelight_port: int
    framerate: float

    # File '.env' will be read
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
templates = StaticFiles(directory="build")
templates = Jinja2Templates(directory="build")


class Pixel(BaseModel):
    r: int = 0
    g: int = 0
    b: int = 0
    a: int = 0

    def __init__(self, r=128, g=0, b=0, a=255, **kwargs):
        super().__init__(**kwargs)
        self.r = r
        self.g = g
        self.b = b
        self.a = a

class Coordinates(BaseModel):
    x: int = 0
    y: int = 0

ROWS = 16
COLS = 40 
PIXEL_WALL = []
for i in range(ROWS):   # create 640 empty pixels with R, G, B = 0
    row = []
    for j in range(COLS):
        row.append(Pixel())
    PIXEL_WALL.append(row)

# TODO: Pixel wall should be persistet to disk so we don't loose the image on every reboots

def set_pixel(x, y, pixel):
    PIXEL_WALL[y][x] = pixel

set_pixel(19, 7, Pixel(255,255,255))
set_pixel(20, 7, Pixel(255,255,255))
set_pixel(19, 8, Pixel(255,255,255))
set_pixel(20, 8, Pixel(255,255,255))

class MateLightRunner:
    def __init__(self):
        self.started = False

    async def matelight_loop(self):
        global PIXEL_WALL
        try:
            message = matelight.prepare_message(PIXEL_WALL)
            matelight.send_array(message, settings.matelight_host, settings.matelight_port)
            await asyncio.sleep(1.0 / settings.framerate)
        except Exception as error:
            traceback.print_exc(file=sys.stdout)
            await asyncio.sleep(1.0 / settings.framerate)

    async def run_main(self):
        self.started = True
        while self.started is True:
            await asyncio.sleep(0.1)
            await self.matelight_loop()

    async def stop(self):
        self.started = False
        message = matelight.blank_screen()
        matelight.send_array(message, settings.matelight_host, settings.matelight_port)


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
app.add_middleware(SessionMiddleware, secret_key="secret_key")
@app.middleware("http")
async def some_middleware(request: Request, call_next):
    response = await call_next(request)
    session = request.cookies.get('session')
    print(session)
    # if session:
    #     response.set_cookie(key='session', value=request.cookies.get('session'), httponly=True)
    return response

@app.post("/pixel/")
async def pixel(request: Request, coordinates: Coordinates, pixel: Pixel):
    if(request.session):
        lastPixelSet = request.session["lastPixelSet"]
        print(lastPixelSet)
        print(time.time() - lastPixelSet < 300)
        if (lastPixelSet and time.time() - lastPixelSet < 300) :
            return 'Wait 5 mins...'
        request.session["lastPixelSet"] = time.time()
        set_pixel(coordinates.x, coordinates.y, pixel)
        return 'OK'
    return 'Get a session'  # TODO: Here call captcha, which will set the session.

@app.get("/framebuffer/")
async def framebuffer(request: Request):
    return PIXEL_WALL

# TODO: Delete this, should happen on first attempt to set a pixel.
@app.get("/getToken/")
async def getToken(request: Request):
    request.session["lastPixelSet"] = 1
    print(request.cookies.get('session'))
    return 'OK'

# Static files
app.mount("/", StaticFiles(directory="build", html=True), name="static")
