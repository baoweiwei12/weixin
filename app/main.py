from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles
from app.core.log import logging
from app.core.config import CONFIG
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, user, weixin
from app.core.scheduler import scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(
    title=CONFIG.APP.NAME,
    description=CONFIG.APP.DESCRIPTION,
    version=CONFIG.APP.VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(user.router, prefix="/api")
app.include_router(weixin.router, prefix="")

app.mount(
    "/weixin/attched-file", StaticFiles(directory="./attched-file"), name="attched-file"
)
