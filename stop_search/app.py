# frontend
from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)
backend_url = "http://localhost:8000"

class Post:
    def __init__(self, title, content):
        self.title = title
        self.content = content

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # get info form form file
        title = request.form["title"]
        content = request.form["content"]
        # create form data into request clss object
        post = Post(title=title, content=content)
        # send the request clss object to backend
        response = requests.post(f"{backend_url}/posts/", json=post.__dict__)
        # send user back to FE
        return redirect(url_for("index"))
    else:
        # get request from backend
        response = requests.get(f"{backend_url}/posts/")
        # turn the response into json object
        posts_data = response.json()
        # unpack data into list comprehension
        posts = [Post(**post) for post in posts_data]
        # pass list comp to frontend for display
        return render_template("index.html", posts=posts)

if __name__ == "__main__":
    app.run(debug=True)