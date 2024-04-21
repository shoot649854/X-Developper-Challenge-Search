from flask import Flask, request
from sklearn.metrics.pairwise import cosine_similarity
from utils import similarity_scorer
import statistics
import json
from Twitter.recent_search import recent_search
from Twitter.process_queries import analyze
from Twitter.rank_tweets import rank_tweets


def get_results(query):
    res = analyze(query)
    description = res["description"]
    subqueries = res["subqueries"]
    data = {"queries": []}
    for item in subqueries:
        query = "#{0} -is:retweet".format(item)
        search_result = recent_search(query, 10)
        formatted_result = json.dumps(json.loads(search_result), indent=4)
        data["queries"].append({"query": query, "results": formatted_result})
    sorted_tweets = rank_tweets(data["queries"], description)
    return json.dumps([res, str(sorted_tweets)])

app = Flask(__name__)

# Define routes
@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/search', methods=['POST'])
def search():
    query = request.json['query']
    res = get_results(query)
    return res



if __name__=='__main__':
    app.run(port=4000)

