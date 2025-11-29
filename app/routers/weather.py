from fastapi import APIRouter,HTTPException
import json
import os
from dotenv import load_dotenv
import requests
import redis

load_dotenv()
API_KEY = os.getenv("API_KEY")
URL = os.getenv("URL")
REDIS_URL = os.getenv("REDIS_URL")
CACHE_TTL = int(os.getenv("CACHE_TTL_SECONDS")) 

r = redis.from_url(REDIS_URL)


router = APIRouter()

@router.get("/{city_name}")
def get_details(location: str):

    key = f"weather:{location.lower()}" #making key-value system

    # 1) Check cache
    cached = r.get(key)
    
    ''' cached is stored as a string,which means if 
    we are storing a number ,it will convert to string.we need to convert it back'''
    if cached:
        try:
            lat_val = float(cached)
        except ValueError:
            lat_val = cached
        return {"city": location, "latitude": lat_val, "source": "cache"}

    api_url = URL+ location +"?key="+API_KEY
    response = requests.get(api_url)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=f"Weather API error: {response.text}")
    data_dict = response.json()
    desired_info =['address','latitude','longitude','timezone','currentConditions']
    extracted_info = {}
    for x in desired_info:
        extracted_info[x]=data_dict[x]
    json_data = json.dumps(extracted_info)
    r.set(key, json_data, CACHE_TTL)
    return {"city": location, 'info':extracted_info, "source": "api"}

