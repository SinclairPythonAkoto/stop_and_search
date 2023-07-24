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
        title = request.form["title"]
        content = request.form["content"]
        post = Post(title=title, content=content)
        response = requests.post(f"{backend_url}/posts/", json=post.__dict__)
        return redirect(url_for("index"))
    else:
        response = requests.get(f"{backend_url}/posts/")
        posts_data = response.json()
        posts = [Post(**post) for post in posts_data]
        return render_template("index.html", posts=posts)

if __name__ == "__main__":
    app.run(debug=True)