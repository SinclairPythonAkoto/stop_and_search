# frontend
from flask import Flask, render_template, request, redirect, url_for
import requests
import datetime

app = Flask(__name__)
backend_url = "http://localhost:8000"

class Post:
    def __init__(self, title, content, date):
        self.title = title
        self.content = content
        self.date = date

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        use_current_time = request.form.get("use_current_time")  # Check if checkbox is selected
        date = request.form["date"] if not use_current_time else datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
        post = Post(title=title, content=content, date=date)
        response = requests.post(f"{backend_url}/posts/", json=post.__dict__)
        return redirect(url_for("index"))
    else:
        response = requests.get(f"{backend_url}/posts/")
        posts_data = response.json()
        posts = [Post(**post) for post in posts_data]
        return render_template("index.html", posts=posts[::-1])


if __name__ == "__main__":
    app.run(debug=True)
    
    
"""
main page - dashboard/homepage
victim report page
witness report page
know my rights
map --> map partial witness/victim reports (follium)

"""