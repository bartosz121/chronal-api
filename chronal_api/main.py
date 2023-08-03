from fastapi import FastAPI

from chronal_api.settings import UvicornSettings, get_app_settings

app_settings = get_app_settings()

app = FastAPI(
    title=app_settings.TITLE,
    version=app_settings.VERSION,
    debug=app_settings.DEBUG,
    docs_url=None if app_settings.ENVIRONMENT.is_production else "/docs",
    redoc_url=None if app_settings.ENVIRONMENT.is_production else "/redoc",
)



@app.get("/")
async def index() -> dict[str, str]:
    return {"msg": "ok"}


def run():
    import uvicorn

    uvicorn.run("chronal_api.main:app", **UvicornSettings().model_dump())


if __name__ == "__main__":
    run()
