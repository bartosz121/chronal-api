import uvicorn
import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from chronal_api.core import debug, config


# api_config = config.get_config(local=True)
api_config = config.get_config()

app = FastAPI(
    title=api_config.TITLE,
    version=api_config.VERSION,
    root_path=api_config.ROOT_PATH,
    docs_url=api_config.DOCS_URL,
    redoc_url=api_config.REDOC_URL,
)

if api_config.IS_DEV:
    app.add_middleware(debug.TimerMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=api_config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(debug.RequestUUIDMiddleware)


@app.get("/")
def home():
    return {"msg": api_config.TITLE}


def run():
    uvicorn.run(
        "chronal_api.main:app",
        log_config=debug.LOGGING_CONFIG,
        reload=api_config.UVICORN_RELOAD,
        workers=api_config.UVICORN_WORKERS,
        host=api_config.UVICORN_HOST,
        port=api_config.UVICORN_PORT,
    )
