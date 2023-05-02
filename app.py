from flask import Flask, render_template, request
from utils import get_pose, string_to_list, get_poses
from elasticsearch_dsl.connections import connections
from gpt_yoga_interface import query_to_prompt, ask_chat_gpt
from es_search import SearchIndex

app = Flask(__name__)
app.jinja_env.filters['zip'] = zip


@app.route('/')
def hello_world():  # put application's code here
    return render_template("home.html")


@app.route("/results", methods=["POST"])
def results():
    connections.create_connection(hosts=["localhost"], timeout=100, alias="default")
    query_text = request.form["query"]
    print(query_text)
    res = string_to_list(ask_chat_gpt(query_to_prompt(query_text)))
    # print(res)
    res = SearchIndex.search_index(res[0], "name", embed=False)
    for r in res:
        print(r)
        for field in r:
            print(field)

    return render_template("results.html",
                           q=query_text,
                           page=1, results=res)


@app.route('/pose/<name>')
def pose(name):
    image_url = "/static/images/"+name+".png"
    return render_template("pose.html",
                           pose=get_pose(name),
                           anchor=name, image=image_url) # image=image_urls[is_image(image_urls)]


if __name__ == '__main__':
    app.run(debug=True, use_debugger=True, use_reloader=True)
