from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse

from config import settings
from models import init_models
from utils import include_routes

app = FastAPI()
include_routes(app)

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




@app.on_event('startup')
async def startup_event():
    await init_models()

if __name__ == '__main__':
    uvicorn.run(
        'app:app',
        host=settings.SRV_HOST,
        port=settings.SRV_PORT,
        log_level='debug',
        access_log=True,
    )
