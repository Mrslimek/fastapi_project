from fastapi import FastAPI
from api.routes import router


app = FastAPI(
    title="Todo API on FastAPI",
    description="Простой RESTful API для управления задачами",
    version="1.0.0",
)

app.include_router(router)
