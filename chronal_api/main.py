from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from chronal_api.settings import CORSSettings, UvicornSettings, get_app_settings
from chronal_api.users.router import router as users_router

app_settings = get_app_settings()

app = FastAPI(
    title=app_settings.TITLE,
    version=app_settings.VERSION,
    debug=app_settings.DEBUG,
    docs_url=None if app_settings.ENVIRONMENT.is_production else "/docs",
    redoc_url=None if app_settings.ENVIRONMENT.is_production else "/redoc",
)

app.add_middleware(CORSMiddleware, **CORSSettings().model_dump())
app.include_router(users_router, prefix="/users")


@app.get("/")
async def index() -> dict[str, str]:
    return {"msg": "ok"}


def run():
    import uvicorn

    uvicorn.run("chronal_api.main:app", **UvicornSettings().model_dump())


if __name__ == "__main__":
    run()
