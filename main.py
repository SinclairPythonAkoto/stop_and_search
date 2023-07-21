from fastapi import FastAPI, HTTPException
from fastapi.param_functions import Body
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from pymongo import MongoClient, errors
from pydantic import BaseModel
from typing import List, Dict, Union

app = FastAPI()

mongo_host = 'localhost'
mongo_port = 27017

# Connect to MongoDB
client = MongoClient(host=mongo_host, port=mongo_port, serverSelectionTimeoutMS=5000)
db = client["stop_and_search_reports"]
victim_collection = db["victims"]
witness_collection = db["witnesses"]

class VictimReports(BaseModel):
    date: str
    location: Dict
    age: str
    sex: str
    race: str
    reason: str
    visible_police: str
    police_badge: List[Dict]
    search_type: str
    outcome: str
    notes: str
    supporting_evidence: List[Dict]
    email: str

class WitnessReports(BaseModel):
    date: str
    location: Dict
    age: str
    sex: str
    race: str
    victims: str
    visible_police: str
    relation_to_victim: str
    search_type: str
    notes: str
    supporting_evidence: List[Dict]
    email: str

class PartialWitnessReport(BaseModel):
    date: str
    location: Dict
    victims: str
    visible_police: str
    search_type: str
    notes: str
    supporting_evidence: List[Dict]
    



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
async def create_report(report: VictimOrWitnessReport):
    report_data = jsonable_encoder(report)
    if isinstance(report, WitnessReports):
        result = witness_collection.insert_one(report_data)
        collection_name = "witnesses"
    elif isinstance(report, VictimReports):
        result = victim_collection.insert_one(report_data)
        collection_name = "victims"
    else:
        raise HTTPException(status_code=400, detail="Invalid report type")

    return {
        "message": f"Report created successfully in {collection_name}",
        "report_id": str(result.inserted_id)
    }

@app.get("/witness-reports", response_model=List[PartialWitnessReport])
async def get_partial_witness_reports():
    partial_witness_report = witness_collection.find({}, {
        "date": 1,
        "location": 1,
        "victims": 1,
        "visible_police": 1,
        "search_type": 1,
        "notes": 1,
        "supporting_evidence": 1
    })
    return list(partial_witness_report)

@app.get("/witness-reports/{report_id}", response_model=WitnessReports)
async def get_full_witness_report(report_id: str):
    full_witness_report = witness_collection.find_one({
        "_id": ObjectId(report_id)
    })
    if full_witness_report:
        return full_witness_report
    else:
        raise HTTPException(status_code=404, detail="Report not found")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
    
    
"""witness reports
- date: timestamp (auto) (create your own time feature)
- location: longitute & latitude (auto) (create your own date feature)
- age: below 15, 15-17, 18-24, 25-30, 31-35, 35+
- sex: male, female, non-binary, trans
- race: black, white, south asain, east asian, arab
- victims involved: 1, 2, 3, - 10+
- visible police: 1-2, 3-4, 5-6, 6+
- relation to victim: known to victim, unknown to victim
- type of search: moderate, aggressive
- notes & comments: large text (optional)
- supporting evidence: pics, vids, PNC document (optional)
- email: (optional) (hashed for security)
"""

"""victim reports
- date: timestamp (auto) (create your own time feature)
- location: longitute & latitude (auto) (create your own date feature)
- age: below 15, 15-17, 18-24, 25-30, 31-35, 35+
- sex: male, female, non-binary, trans
- race: black, white, south asain, east asian, arab
- reason for search: (reasonable grounds) illegal drugs, a weapon, stolen property, something that can be used to commit a crime (without reasonable grounds) serious violence can take place, carrying a weapon or used one, in a specific location or area
- visible police: 1-2, 3-4, 5-6, 6+
- police badge: 
- outcome: ongoing, resolved, no further action
- type of search: moderate, aggressive
- notes & comments: large text (optional)
- supporting evidence: pics, vids, PNC document (optional)
- email: (optional) (hashed for security)
"""