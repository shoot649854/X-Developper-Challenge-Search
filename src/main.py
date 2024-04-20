import requests
import os
import json
from dotenv import load_dotenv
load_dotenv()

from Twitter.recent_search import recent_search
DATA_DIR = os.path.join(os.getcwd(), "data")
subqueries = [
    "NBA Playoffs 2024",
    "NBA Playoffs Bracket 2024"
]

data = {"queries": []}

for item in subqueries:
    query = "#{0} -is:retweet".format(item)
    search_result = recent_search(query, 10)
    formatted_result = json.dumps(json.loads(search_result), indent=4)
    data["queries"].append({"query": query, "results": formatted_result})

directory = os.path.join(DATA_DIR, "recent_search_queries.json")
with open(directory, "w") as json_file:
    json.dump(data, json_file, indent=4)