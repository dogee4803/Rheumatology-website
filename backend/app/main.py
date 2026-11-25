from app.api import screening
from fastapi import FastAPI

app = FastAPI(
    title="Rheuma Screening API",
    description="API для сайта раннего выявления ревматологических заболеваний",
    version="0.1.0",
)

# Подключаем роутер скрининга
app.include_router(screening.router, prefix="/api")

@app.get("/")
def read_root():
    return {"status": "ok", "message": "API is running"}