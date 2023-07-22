from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from fastapi.param_functions import Body
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from pymongo import MongoClient, errors
from pydantic import BaseModel, validator
from typing import List, Dict, Union
from datetime import datetime
from geopy.geocoders import Nominatim
import hashlib

app = FastAPI()

mongo_host = 'localhost'
mongo_port = 27017

# Connect to MongoDB
client = MongoClient(host=mongo_host, port=mongo_port, serverSelectionTimeoutMS=5000)
db = client["stop_and_search_reports"]
public_report_collection = db["reports"]

class LocationInput(BaseModel):
    latitude: str
    longitude: str
    address: str
    country: str

class PoliceBadgeInfo(BaseModel):
    badge_number: str
    officer: str

class VictimReports(BaseModel):
    report_type: str                        # "victim"
    date: Union[str, datetime]              # "get_date" | datetime
    location: Union[str, LocationInput]     # "get_location" | LocationInput
    victims_involved: str                   # 1 | 2 | 3 ... 10+
    reason: str                             # drugs | weapon | stolen property | something to commit a crime | suspect serious violence | carrying a weapon or have used one | in specific location/area
    visible_police: str                     # 1-2 | 3-4 | 5-6 | 6+
    type_of_search: str                     # moderate | aggressive
    police_badge: List[PoliceBadgeInfo]     # PoliceBadgeInfo
    outcome: str                            # unknown | ongoing | resolved | no further action
    age: str                                # prefer not to say | below 15 | 15-17 | 18-24 | 25-30 | 31-35 | 35+
    sex: str                                # prefer not to say | male | female | non-binary | trans
    race: str                               # prefer not to say | black | white | arab | south asain | east asain
    notes: str                              # (optional)
    supporting_evidence: List[UploadFile]   # (optional)
    email: str                              # (optional) - hashed for security
 

class WitnessReports(BaseModel):
    report_type: str                        # "witness"
    relation: str                           # known | unknown
    date: Union[str, datetime]              # get_date | datetime
    location: Union[str, LocationInput]     # get_location | LocationInput
    victims_involved: str                   # 1 | 2 | 3 ... 10+
    reason: str                             # drugs | weapon | stolen property | something to commit a crime | suspect serious violence | carrying a weapon or have used one | in specific location/area
    visible_police: str                     # 1-2 | 3-4 | 5-6 | 6+
    type_of_search: str                     # moderate | aggressive
    police_badge: List[PoliceBadgeInfo]     # PoliceBadgeInfo
    outcome: str                            # unknown | ongoing | resolved | no further action
    victim_description: str                 # yes | no
    age: str                                # I don't know | below 15 | 15-17 | 18-24 | 25-30 | 31-35 | 35+
    sex: str                                # I don't know | male | female 
    race: str                               # I don't know | black | white | arab | south asain | east asain
    notes: str                              # (optional)
    supporting_evidence: List[UploadFile]   # (optional)
    email: str                              # (optional) - hashed for security

class PartialWitnessReport(BaseModel):
    location: Union[str, LocationInput]
    victims_involved: str 
    visible_police: str
    type_of_search: str
    police_badge: List[PoliceBadgeInfo]
    notes: str
    supporting_evidence: List[UploadFile]
    
def get_user_location(request: Request) -> LocationInput:
    """get user's location via their IP address"""
    ip = request.client.host
    geolocator = Nominatim(user_agent="location_tracker")
    location = geolocator.geocode(ip)
    if location is None:
        return None
    return LocationInput(
        latitude=str(location.latitude),
        longitude=str(location.longitude),
        address=location.address,
        country=location.raw["address"].get("country", ""),
    )

@app.get("/")
async def hello_world():
    post = "hello world"
    if post:
        return post
    else:
        raise HTTPException(status_code=404, detail="Post not found")
    
# Create a union type of WitnessReports and VictimReports
VictimOrWitnessReport = Union[WitnessReports, VictimReports]


@app.post("/create-report")
async def create_report(report: VictimOrWitnessReport, request: Request, supporting_evidence: List[UploadFile] = File(...)):
    report_data = jsonable_encoder(report)
    if report_data["email"]:
        hashed_email = hashlib.sha256(report_data["email"].encode()).hexdigest()
        report_data["email"] = hashed_email
    if isinstance(report, WitnessReports):
        if report_data["date"] == "get_date":
            report_data["date"] = datetime.now()
        if report_data["location"] == "get_location":
            location_data = get_user_location(request)
            if location_data is not None:
                report_data["location"] = LocationInput(**location_data)
            else:
                raise HTTPException(status_code=500, detail="Failed to get user location")
        supporting_evidence_urls = []
        for file in supporting_evidence:
            file_content = await file.read()
            file_path = f"supporting_evidence/{file.filename}"
            with open(file_path, "wb") as f:
                f.write(file_content)
            supporting_evidence_urls.append(file_path)
        report_data["supporting_evidence"] = supporting_evidence_urls
        result = public_report_collection.insert_one(report_data)
        collection_type = "witnesses"
    elif isinstance(report, VictimReports):
        if report_data["date"] == "get_date":
            report_data["date"] = datetime.now()
        if report_data["location"] == "get_location":
            location_data = get_user_location(request)
            if location_data is not None:
                report_data["location"] = LocationInput(**location_data)
            else:
                raise HTTPException(status_code=500, detail="Failed to get user location")
        supporting_evidence_urls = []
        for file in supporting_evidence:
            file_content = await file.read()
            file_path = f"supporting_evidence/{file.filename}"
            with open(file_path, "wb") as f:
                f.write(file_content)
            supporting_evidence_urls.append(file_path)
        report_data["supporting_evidence"] = supporting_evidence_urls
        result = public_report_collection.insert_one(report_data)
        collection_type = "victims"
    else:
        raise HTTPException(status_code=400, detail="Invalid report type")

    return {
        "message": f"Report created successfully in {collection_type}",
        "report_id": str(result.inserted_id),
    }


@app.get("/witness-reports", response_model=List[PartialWitnessReport])
async def get_partial_witness_reports():
    partial_witness_report = public_report_collection.find({}, {
        "date": 1,
        "location": 1,
        "victims_involved": 1,
        "visible_police": 1,
        "type_of_search": 1,
        "police_badge": 1,
        "notes": 1,
        "supporting_evidence": 1
    })
    return list(partial_witness_report)

@app.get("/witness-reports/{report_id}", response_model=WitnessReports)
async def get_full_witness_report(report_id: str):
    full_witness_report = public_report_collection.find_one({
        "_id": ObjectId(report_id)
    })
    if full_witness_report:
        return full_witness_report
    else:
        raise HTTPException(status_code=404, detail="Report not found")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
    
    
"""reports
- report type: witness or victim
- relation to victim: known to victim or unknown to victim (if witness)

- date: select date or incident just happended

- location: get current location or enter location

- victims involved: 1, 2, 3, - 10+

- reason for search: (reasonable grounds) illegal drugs, a weapon, stolen property, something that can be used to commit a crime (without reasonable grounds) serious violence can take place, carrying a weapon or used one, in a specific location or area
- visible police: 1-2, 3-4, 5-6, 6+
- type of search: moderate, aggressive
- police badge: 
- outcome: ongoing, resolved, no further action, unknown

- victim description: yes or no (if witness)
- age: I don't know, below 15, 15-17, 18-24, 25-30, 31-35, 35+, prefer not to say
- sex: male, female, non-binary, trans, prefer not to say
- race: I don't know, black, white, south asain, east asian, arab, prefer not to say

- notes & comments: text optional

- supporting evidence: pics, vids, PNC document (optional)

- email: (optional) (hashed for security)
"""
