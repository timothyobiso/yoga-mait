# Main Flask File
# Developed by Timothy Obiso

# Import Statements
from flask import Flask, render_template, request
from flask_caching import Cache
from utils import get_pose, string_to_list
from elasticsearch_dsl.connections import connections
from gpt_yoga_interface import query_to_prompt, ask_chat_gpt
from es_search import SearchIndex
from query_classifier import get_model, get_classifier_df, classify

# App Setup
app = Flask(__name__)
app.jinja_env.filters['zip'] = zip #allows use of zip on flask templates

# Cache Setup
cache = Cache(config={'CACHE_TYPE': "SimpleCache"})
cache.init_app(app)

# Query Classifier Setup
MODEL = get_model()
DF = get_classifier_df()

# Home/Search Page
@app.route('/')
def hello_world():
    return render_template("home.html")

# 404 Error Page
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")

# Results Page
@app.route("/results", methods=["POST"])
def results():
    # Connect to Elasticsearch Database
    connections.create_connection(hosts=["localhost"], timeout=100, alias="default")
    # Get Query from page
    query_text = request.form["query"]

    # Fix for " pose"
    if query_text[len(query_text)-5:] == " pose":
        query_text = query_text[:len(query_text)-5]

    # Classify Query (name, benefits, description)
    cls = classify(MODEL.encode(query_text), DF)

    # Uncomment to see classification
    # print("CLASSIFIED AS:", cls)

    # Classified as "benefits" or "description"
    if cls != "name":
        res = []
        # send to GPT with prompt engineering wrapper
        # Turn GPT String into list
        gpt_results = string_to_list(ask_chat_gpt(query_to_prompt(query_text)))

        # Iterate through GPT responses
        for r in gpt_results:
            # Use Elasticsearch to get poses
            response, fail = SearchIndex.search_index(r, cls)

            # Top 5 poses for each GPT result
            for p in response[:5]:
                if p not in res:
                    res.append(p)

    # Classified as "name"
    else:
        # res = results, fail = True if name keyword search failed, False otherwise
        res, fail = SearchIndex.search_index(query_text, cls)

    # Uncomment to print results to be shown on results page
    # print(res)

    # Update cache
    cache.set("q", query_text)

    #
    return render_template("results.html", q=query_text, results=res, fail=fail, cls=cls)


# Pose Page
@app.route('/pose/<name>')
def pose(name):
    # Get Picture of Pose
    image_url = "/static/images/"+name+".png"

    # Get Query From Cache to persist to user
    q = cache.get("q")
    filler = "" if q is None else q
    return render_template("pose.html",
                           pose=get_pose(name),
                           anchor=name, image=image_url, q=filler)


if __name__ == '__main__':
    app.run()
