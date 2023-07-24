# backend
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from typing import List

app = FastAPI()

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["stop_search"]
report_collection = db["reports"]

class Post(BaseModel):
    title: str
    content: str
    date: str = None # Date will be empty string format

@app.post("/posts/", response_model=Post)
def create_post(post: Post):
    post_data = post.dict()
    post_id = report_collection.insert_one(post_data).inserted_id
    return {**post_data, "_id": str(post_id)}

@app.get("/posts/", response_model=List[Post])
def get_posts():
    posts_data = report_collection.find()
    return [Post(**post) for post in posts_data]



"""
class LocationInput(BaseModel):
    latitude: str
    longitude: str
    address: str
    country: str


class PoliceBadgeInfo(BaseModel):
    badge_number: str
    officer: str


class VictimReports(BaseModel):
    report_type: str  # "victim"
    date: Union[str, datetime]  # "get_date" | datetime
    location: Union[str, LocationInput]  # "get_location" | LocationInput
    victims_involved: str  # 1 | 2 | 3 ... 10+
    reason: str  # I don't know | drugs | weapon | stolen property | something to commit a crime | suspect serious violence | carrying a weapon or have used one | in specific location/area
    visible_police: str  # 1-2 | 3-4 | 5-6 | 6+
    type_of_search: str  # moderate | aggressive
    police_badge: List[PoliceBadgeInfo]  # PoliceBadgeInfo
    outcome: str  # unknown | ongoing | resolved | no further action
    age: str  # prefer not to say | below 15 | 15-17 | 18-24 | 25-30 | 31-35 | 35+
    sex: str  # prefer not to say | male | female | non-binary | trans
    race: str  # prefer not to say | black | white | arab | south asain | east asain
    notes: str  # (optional)
    supporting_evidence: List[UploadFile]  # (optional)
    email: str  # (optional) - hashed for security


class WitnessReports(BaseModel):
    report_type: str  # "witness"
    relation: str  # known | unknown
    date: Union[str, datetime]  # get_date | datetime
    location: Union[str, LocationInput]  # get_location | LocationInput
    victims_involved: str  # 1 | 2 | 3 ... 10+
    reason: str  # I don't know | drugs | weapon | stolen property | something to commit a crime | suspect serious violence | carrying a weapon or have used one | in specific location/area
    visible_police: str  # 1-2 | 3-4 | 5-6 | 6+
    type_of_search: str  # moderate | aggressive
    police_badge: List[PoliceBadgeInfo]  # PoliceBadgeInfo
    outcome: str  # unknown | ongoing | resolved | no further action
    victim_description: str  # yes | no
    age: str  # I don't know | below 15 | 15-17 | 18-24 | 25-30 | 31-35 | 35+
    sex: str  # I don't know | male | female
    race: str  # I don't know | black | white | arab | south asain | east asain
    notes: str  # (optional)
    supporting_evidence: List[UploadFile]  # (optional)
    email: str  # (optional) - hashed for security


class PartialWitnessReport(BaseModel):
    location: Union[str, LocationInput]
    victims_involved: str
    visible_police: str
    type_of_search: str
    police_badge: List[PoliceBadgeInfo]
    notes: str
    supporting_evidence: List[UploadFile]

"""