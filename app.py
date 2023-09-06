import uvicorn
from fastapi import FastAPI

from config import settings
from models import init_models
from utils import include_routes

app = FastAPI()


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
