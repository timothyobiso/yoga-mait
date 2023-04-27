from flask import Flask, render_template, request
from utils import get_pose

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template("home.html")


@app.route("/results", methods=["POST"])
def results():
    query_text = request.form["query"]
    # res = perform search function
    return render_template("results.html",
                           q=query_text,
                           page=1)
                           #results=res


@app.route('/pose/<name>')
def pose(name):
    return render_template("pose.html",
                           pose=get_pose(name))


if __name__ == '__main__':
    app.run()
