from fastapi import APIRouter
import json
import os
from dotenv import load_dotenv
import requests

load_dotenv()
API_KEY = os.getenv("API_KEY")
URL = os.getenv("URL")


router = APIRouter()

@router.get("/{city_name}")
def get_details(location: str):
    api_url = URL+ location +"?key="+API_KEY
    response = requests.get(api_url)
    data_dict = response.json()
    latitude= data_dict['latitude']
    return latitude

