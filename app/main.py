from fastapi import FastAPI
from fastapi.responses import FileResponse
from app.routers.weather import router



app = FastAPI(title="Weather API with Redis")

app.include_router(router)

@app.get("/")# connecting static pages to url/endpoint
def home():
    return FileResponse("static/weather.html")




