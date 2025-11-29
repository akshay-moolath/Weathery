from fastapi import FastAPI
from app.routers.weather import router as weather_router


app = FastAPI(title="Weather API with Redis")

app.include_router(weather_router, prefix="/weather", tags=["weather"])



