from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def index() -> dict[str, str]:
    return {"msg": "ok"}


def run():
    import uvicorn

    uvicorn.run("chronal_api.main:app", host="127.0.0.1", port=8080, reload=True)


if __name__ == "__main__":
    run()
