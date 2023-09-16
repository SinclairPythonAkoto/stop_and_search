# backend
from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from pydantic import BaseModel
from pymongo import MongoClient, errors
from typing import List, Dict, Union
from datetime import datetime
from geopy.geocoders import Nominatim
import hashlib
import base64
import io
import uvicorn

app = FastAPI()

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["stop_search"]
report_collection = db["reports"]

class Post(BaseModel):
    title: str
    content: str
    date: str = None # Date will be empty string format

class LocationInput(BaseModel):
    latitude: str
    longitude: str
    address: str
    country: str = "UK"

class PoliceInfo(BaseModel):
    badge_number: str
    officer: str
    station: str

class VictimReports(BaseModel):
    report_type: str  # "victim"
    report_date: str  # "current_date" | 
    location: Union[str, LocationInput]  # "get_location" | LocationInput
    victims_involved: str  # 1 | 2 | 3 ... 10+
    reason: str  # I don't know | drugs | weapon | stolen property | something to commit a crime | suspect serious violence | carrying a weapon or have used one | in specific location/area
    visible_police: str  # 1-2 | 3-4 | 5-6 | 6+
    type_of_search: str  # moderate | aggressive
    police_info: List[str] = None # PoliceInfo
    outcome: str  # unknown | ongoing | resolved | no further action
    age: str = None # prefer not to say | below 15 | 15-17 | 18-24 | 25-30 | 31-35 | 35+
    sex: str = None  # prefer not to say | male | female | non-binary | trans
    race: str = None # prefer not to say | black | white | arab | south asain | east asain
    notes: str = None  # (optional)
    report_media: List[str] = None  # list of filenames (optional)
    email: str = None  # (optional) - hashed for security


@app.post("/victim/")
def create_victim_report(victim_report: VictimReports):
    print(victim_report)
    # convert data into Pydantic model for BE
    victim_data = victim_report
    print(victim_data)
    decoded_images = [base64.b64decode(encoded) for encoded in victim_data["report_media"]]
    # save list of img uploads to DB
    victim_data["report_media"] = decoded_images
    # save victim report to DB
    inserted_id = report_collection.insert_one(victim_data).inserted_id
    # return data with new ID
    return {**victim_data, "_id": str(inserted_id)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)