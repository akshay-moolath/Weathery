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

r = redis.from_url(REDIS_URL, decode_responses=True)


router = APIRouter()

@router.get("/weather/{location}")
def get_details(location: str):

    key = f"weather:{location.lower()}" #making key-value system
    
    cached = r.get(key)
    
    if cached:
        obj = json.loads(cached)
        if isinstance(obj, str):
            obj = json.loads(obj)
        extracted_info = obj
        return {"city":location,"info": extracted_info, "source": "cache"}

    api_url = URL+ location +"?key="+API_KEY
    response = requests.get(api_url)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=f"Weather API error: {response.text}")
    res = response.json()
    desired_info = {}
    desired_info["latitude"] = res.get("latitude")
    desired_info["longitude"] = res.get("longitude")
    desired_info["timezone"] = res.get("timezone")
    desired_info["currentConditions"] = res.get("currentConditions", {})
    json_data = json.dumps(desired_info)
    r.set(key,json_data,CACHE_TTL)
    return {"city":location ,"info":desired_info, "source": "api"}

