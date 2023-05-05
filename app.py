from flask import Flask, render_template, request
from flask_caching import Cache
from utils import get_pose, string_to_list
from elasticsearch_dsl.connections import connections
from gpt_yoga_interface import query_to_prompt, ask_chat_gpt
from es_search import SearchIndex
from query_classifier import get_model, get_classifier_df, classify

app = Flask(__name__)
app.jinja_env.filters['zip'] = zip

cache = Cache(config={'CACHE_TYPE': "SimpleCache"})
cache.init_app(app)

MODEL = get_model()
DF = get_classifier_df()

@app.route('/')
def hello_world():  # put application's code here
    return render_template("home.html")


@app.route("/results", methods=["POST"])
def results():
    connections.create_connection(hosts=["localhost"], timeout=100, alias="default")
    query_text = request.form["query"]
    # print(query_text)
    cls = classify(MODEL.encode(query_text), DF)
    print("CLASSIFIED AS:", cls)
    if cls != "name":
        res = []
        gpt_results = string_to_list(ask_chat_gpt(query_to_prompt(query_text)))
        for r in gpt_results:
            response, fail = SearchIndex.search_index(r, cls)
            for p in response[:5]:
                if p not in res:
                    res.append(p)
    else:

        res, fail = SearchIndex.search_index(query_text, cls)
    # gpt_results = string_to_list(ask_chat_gpt(query_to_prompt(query_text)))
    # print(res)

    cache.set("q", query_text)
    return render_template("results.html",
                           q=query_text,
<<<<<<< HEAD
                           page=1, results=res, fail=fail, cls=cls)
=======
                           page=1, results=res[0])
>>>>>>> 27aea857e7713ca03d6832f93c5369606c861d41


@app.route('/pose/<name>')
def pose(name):
    image_url = "/static/images/"+name+".png"
    q = cache.get("q")
    filler = "" if q is None else q
    return render_template("pose.html",
                           pose=get_pose(name),
                           anchor=name, image=image_url, q=filler) # image=image_urls[is_image(image_urls)]


if __name__ == '__main__':
    app.run(debug=True, use_debugger=True, use_reloader=True)
