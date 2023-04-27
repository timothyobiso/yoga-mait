from flask import Flask, render_template, request
from utils import get_pose, is_image

app = Flask(__name__)
app.jinja_env.filters['zip'] = zip


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

    image_urls = ["https://pocketyoga.com/assets/images/full/" + name + ".png", "https://pocketyoga.com/assets/images/full/" + name + "_R.png"]
    return render_template("pose.html",
                           pose=get_pose(name),
                           anchor=name, image=image_urls[is_image(image_urls)])


if __name__ == '__main__':
    app.run(debug=True, use_debugger=True, use_reloader=True)
