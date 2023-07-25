# frontend
from flask import Flask, render_template, request, redirect, url_for
import requests
import datetime

app = Flask(__name__)
backend_url = "http://localhost:8000"

# create clss to mimmick db models
class Post:
    def __init__(self, title, content, date):
        self.title = title
        self.content = content
        self.date = date

# home / dashboard
@app.route("/")
def home():
    return render_template("home.html")

# victim report page
@app.route("/victim", methods=["GET", "POST"])
def victim_report_page():
    report_type: str = "victim"
    if request.method == "GET":
        return render_template("victim_report.html")
    else:
        current_date: str = request.form.get("use_current_time")
        # if current date is not selected
        if not current_date:
            date: str = str(request.form.get("date"))
        else:
            date: str = str(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M"))
        current_location: str = request.form.get("use_current_location")
        # if current location is not selected
        if not current_location:
            
            street: str = request.form.get("streetname")
            town_city: str = request.form.get("town_city")
            postcode: str = request.form.get("postcode")
            if street and not postcode:
                # Street is provided, but postcode is missing
                # Handle the condition here
                pass

            if street and not town_city:
                # Street is provided, but town_city is missing
                # Handle the condition here
                pass

            if postcode and not town_city:
                # Postcode is provided, but town_city is missing
                # Handle the condition here
                pass
        victims_involved: str
        number_of_victims: str
        reason: str
        reason_for_stop: str
        visible_police: str
        type_of_search: str
        police_officer_badge: str
        officer_name: str
        police_station: str
        final_outcome: str
        victim_age: str
        victim_sex: str
        victim_race: str
        victim_notes: str
        photos = request.files.getlist('photos')
        films = request.files.getlist('films')
        for photo in photos:
            # Process each photo file as needed
            # Example: Save to a folder or store in a database
            pass

        for film in films:
            # Process each film file as needed
            # Example: Save to a folder or store in a database
            pass
        victim_email: str
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


# class Post:
#     def __init__(self, title, content, date):
#         self.title = title
#         self.content = content
#         self.date = date
# 
# @app.route("/", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         title = request.form["title"]
#         content = request.form["content"]
#         use_current_time = request.form.get("use_current_time")  # Check if checkbox is selected
#         date = request.form["date"] if not use_current_time else datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
#         post = Post(title=title, content=content, date=date)
#         response = requests.post(f"{backend_url}/posts/", json=post.__dict__)
#         return redirect(url_for("index"))
#     else:
#         response = requests.get(f"{backend_url}/posts/")
#         posts_data = response.json()
#         posts = [Post(**post) for post in posts_data]
#         return render_template("home.html", posts=posts[::-1])


if __name__ == "__main__":
    app.run(debug=True)
    
    
"""
victim report page
witness report page
know my rights
map --> map partial witness/victim reports (follium)

# get media files
photos = request.files.getlist('photos')
films = request.files.getlist('films')

"""