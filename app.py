from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse

from config import settings
from models import init_models
from utils import include_routes

app = FastAPI()

build_path = Path(__file__).parent / 'client' / 'dist' 
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


@app.get('/{file}')
async def catch_dir(req: Request, file: str):
    if not Path(build_path / file).exists():
        file = 'index.html'
    return FileResponse(build_path / file)


@app.route('/{full_path:path}')
async def catch_all(req: Request):
    return FileResponse(build_path / 'index.html')


@app.on_event('startup')
async def startup_event():
    await init_models()
    include_routes(app)

if __name__ == '__main__':
    uvicorn.run(
        'app:app',
        host=settings.SRV_HOST,
        port=settings.SRV_PORT,
        log_level='debug',
        access_log=True,
    )
