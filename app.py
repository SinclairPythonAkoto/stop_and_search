# frontend
import json
from flask import Flask, render_template, request, redirect, url_for
import requests
import datetime
from typing import Union, Dict, List
# from PIL import Image
import base64
import io
import os
from os.path import join, dirname, realpath
import uuid
import base64 # needed to send binary file as serialised JSON obj


UPLOADS_PATH = join(dirname(realpath(__file__)), 'static/uploads')


app = Flask(__name__)
backend_url = "http://localhost:8000"


app.config['UPLOADS_PATH'] = UPLOADS_PATH


# create class to convert data to json
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        return super().default(o)

    
# create clss to mimmick db models
class Post:
    def __init__(self, title, content, date):
        self.title = title
        self.content = content
        self.date = date

# class VictimLocation:
#     def __init__(self, street: str, town_city: str, postcode: str):
#         self.street = street
#         self.town_city = town_city
#         self.postcode = postcode

class VictimLocation:
    def __init__(self, latitude: str, longitude: str, address: str, country: str):
        self.latitude = latitude
        self.longitude = longitude
        self.address = address
        self.country = country

class Victims:
    def __init__(self, report_type: str, date: str, location: Union[str, VictimLocation], victims_involved: str, reason: str, visible_police: str, type_of_search: str, police_info: List[str], outcome: str, age: str, sex: str, race: str, notes: str, report_media: List[str], email: str):
        self.report_type = report_type
        self.date = date
        self.location = location
        self.victims_involved = victims_involved
        self.reason = reason
        self.visible_police = visible_police
        self.type_of_search = type_of_search
        self.police_info = police_info
        self.outcome = outcome
        self.age = age
        self.sex = sex
        self.race = race
        self.notes = notes
        self.report_media = report_media
        self.email = email


class PoliceInfo:
    def __init__(self, badge: str, officer: str, station: str):
        self.badge = badge
        self.officer = officer
        self.station = station

def valid_location_options(current_location: str, street: str, town_city: str, postcode: str) -> bool:
    if current_location and (street or town_city or postcode):
        return False
    if current_location and not (street or town_city or postcode):
        return True

# home / dashboard
@app.route("/")
def home():
    return render_template("home.html")

# victim report page
@app.route("/victim/", methods=["GET", "POST"])
def victim_report_page():
    report_type: str = "victim"
    report_date: str
    report_location: Union[str, VictimLocation] = None
    report_police_info: PoliceInfo = None
    report_age: str = None
    report_sex: str = None
    report_race: str = None
    report_notes: str = None
    report_media = None
    report_email: str = None
    
    if request.method == "GET":
        return render_template("victim_report.html")
    else:
        # get all elements from form
        current_date: str = request.form.get("use_current_time")
        date: str = str(request.form.get("date"))
        current_location: str = request.form.get("use_current_location")
        street: str = request.form.get("streetname")
        town_city: str = request.form.get("town_city")
        postcode: str = request.form.get("postcode")
        victims_involved: str = request.form.get("victims_involved")
        reason_for_stop: str = request.form.get("reason")
        visible_police: str = request.form.get("visible_police")
        type_of_search: str = request.form.get("type_of_search")
        police_badge: str = request.form.get("police_officer_badge")
        officer_name: str = request.form.get("officer_name")
        police_station: str = request.form.get("police_station")
        final_outcome: str = request.form.get("outcome")
        victim_age: str = request.form.get("victim_age")
        victim_sex: str = request.form.get("victim_sex")
        victim_race: str = request.form.get("victim_race")
        victim_notes: str = request.form.get("victim_notes")
        photos = request.files['pic_file']
        films = request.files.getlist('video_file')
        victim_email: str = request.form.get("victim_email")
        
        if current_date:
            report_date = current_date
        # if current date is not selected
        if current_date == None:
            report_date = date
        if current_date == None and date == "":
            date_error: str = "Please select a date above."
            return render_template("victim_report.html", date_error=date_error)
        if current_date and date:
            date_error_2: str = "Please tick the box to choose today's date, or enter your own date and time above."
            return render_template("victim_report.html", date_error_2=date_error_2)
        
        # if current location selected
        if current_location:
            report_location = report_location  # True
            # now do logic to get current address from IP address
            
        # if current location and user location entered
        if valid_location_options(report_location, street, town_city, postcode) == False:
            location_error: str = "Please tick the box to get your current location, or enter your location above."
            return render_template("victim_report.html", location_error=location_error)
        
        # save this into location clss object if not current_location
        if street and not postcode:
            report_location = VictimLocation(
                street=street,
                town_city=town_city,
                postcode=postcode
            )

        if street and not town_city:
            report_location = VictimLocation(
                street=street,
                town_city=town_city,
                postcode=postcode
            )

        if postcode and not town_city:
            report_location = VictimLocation(
                street=street,
                town_city=town_city,
                postcode=postcode
            )
        
        # save media files
        binary_images = []
        if 'pic_file' in request.files:
            photos = request.files.getlist('pic_file')
            
            for i, photo in enumerate(photos):
                if photo.filename:
                    # Read the binary data from the uploaded image
                    binary_data = photo.read()
                    binary_images.append(binary_data)
        
        # encode binary image data
        encoded_images = [base64.b64encode(image).decode('utf-8') for image in binary_images]


        if victim_email:
            # hash the email
            pass
        
        message = "report sent!"
        
        # store FE data in class 
        victim_report = Victims
        victim_report.report_type = str(report_type)
        victim_report.date = str(report_date)
        victim_report.location = str(report_location)
        victim_report.victims_involved = str(victims_involved)
        victim_report.reason = str(reason_for_stop)
        victim_report.visible_police = str()
        victim_report.visible_police = str(visible_police)
        victim_report.type_of_search = str(type_of_search)
        victim_report.police_info = [str(report_police_info)]
        victim_report.outcome = str(final_outcome)
        victim_report.age = str(victim_age)
        victim_report.sex = str(victim_sex)
        victim_report.race = str(victim_race)
        victim_report.notes = str(victim_notes)
        victim_report.report_media = [str(encoded_images)]
        victim_report.email = victim_email
        
    
        # create vicitim report dict object
        # needs to be in the same json format as in backend 
        victim_data = {
            "report_type": victim_report.report_type,
            "report_date": victim_report.date,
            "location": {
                "get_location": victim_report.location,
                # "street": str(report_location.street) if isinstance(report_location, VictimLocation) else None,
                # "town_city": str(report_location.town_city) if isinstance(report_location, VictimLocation) else None,
                # "postcode": str(report_location.postcode) if isinstance(report_location, VictimLocation) else None
            },
            "victims_involved": victim_report.victims_involved,
            "reason": victim_report.reason,
            "visible_police": victim_report.visible_police,
            "type_of_search": victim_report.type_of_search,
            "police_info": victim_report.police_info, # police info obbject 
            "outcome": victim_report.outcome,
            "age": victim_report.age,
            "sex": victim_report.sex,
            "race": victim_report.race,
            "notes": victim_report.notes,
            "report_media": victim_report.report_media, # list of img filenames to the BE
            "email": victim_report.email
        }
        print(victim_data)
        # print(victim_data["report_date"], victim_data["location"], victim_data["report_media"])
        # Serialize the data using the custom JSON encoder
        # json_payload = json.dumps(victim_report_data, cls=CustomJSONEncoder)
        response = requests.post(f"{backend_url}/victim-report/", json=victim_data)

        return render_template("victim_report.html")

# witness report page
@app.route("/witness", methods=["GET", "POST"])
def witness_report_page():
    return render_template("witness_report.html")

# know my rights page
@app.route("/my-rights", methods=["GET", "POST"])
def my_rights_page():
    return render_template("my_rights.html")

# view report via map page
@app.route("/map", methods=["GET", "POST"])
def report_map():
    return render_template("map.html")


if __name__ == "__main__":
    app.run(debug=True)

