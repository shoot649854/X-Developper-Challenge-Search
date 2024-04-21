from flask import Flask, request
from flask_cors import CORS  # Import CORS
from sklearn.metrics.pairwise import cosine_similarity
from utils import similarity_scorer
import statistics
import json
from Twitter.recent_search import recent_search
from Twitter.process_queries import analyze
from Twitter.rank_tweets import rank_tweets



async def get_results(query):
    res = analyze(query)
    description = res["description"]
    subqueries = res["subqueries"]
    data = {"queries": []}
    for item in subqueries:
        query = item
        search_result = recent_search(query, 10)
        formatted_result = json.dumps(json.loads(search_result), indent=4)
        data["queries"].append({"query": query, "results": formatted_result})
    with open("recent_search_queries.json", 'w') as file:
        json.dump(data["queries"], file, indent=4, sort_keys=True)
    sorted_tweets = await rank_tweets(data["queries"], description)
    return json.dumps([res, sorted_tweets], default=float)

app = Flask(__name__)
CORS(app)  # Enable CORS for the Flask app

# Define routes
@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/search', methods=['POST'])
async def search():
    query = request.json['query']
    res = await get_results(query)
    return res

if __name__=='__main__':
    app.run(port=4000)
