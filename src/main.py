# External
from fastapi import FastAPI

# Project
from app.routers import ROUTERS


app = FastAPI()

for router in ROUTERS:
    app.include_router(router)


if __name__ == "__main__":
    # External
    import uvicorn

    app.debug = True
    uvicorn.run("main:app", port=8000, reload=True)
