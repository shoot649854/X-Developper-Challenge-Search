import requests
import os
import json
from dotenv import load_dotenv
load_dotenv()

from Twitter.recent_search import recent_search
from Ranking.rank_tweets import process_rank_tweets
DATA_DIR = os.path.join(os.getcwd(), "data")

# Subqueries 
subqueries = [
    "NBA Playoffs 2024",
    "NBA Playoffs Bracket 2024"
]

# Get recent_search
data = {"queries": []}
for item in subqueries:
    query = "#{0} -is:retweet".format(item)
    search_result = recent_search(query, 10)
    formatted_result = json.dumps(json.loads(search_result), indent=4)
    data["queries"].append({"query": query, "results": formatted_result})

# process_rank_tweets
queries = data["queries"]
process_rank_tweets(queries=queries)