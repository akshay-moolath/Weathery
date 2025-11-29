from fastapi import FastAPI
from fastapi.responses import FileResponse
from app.routers.weather import router as weather_router
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(title="Weather API with Redis")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(weather_router, prefix="/weather", tags=["weather"])

@app.get("/")# connecting static pages to url/endpoint
def home():
    return FileResponse("static/weather.html")




