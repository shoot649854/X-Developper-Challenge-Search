import requests
import os
import json
from dotenv import load_dotenv
load_dotenv()

from Twitter.recent_search import recent_search
from Twitter.process_queries import analyze
from Twitter.rank_tweets import rank_tweets, similarity_scorer

DATA_DIR = os.path.join(os.getcwd(), "data")

def get_results(query):
    res = analyze(query)
    description = res["description"]
    subqueries = res["subqueries"]
    data = {"queries": []}
    for item in subqueries:
        query =  item
        search_result = recent_search(query, 25)
        formatted_result = json.dumps(json.loads(search_result), indent=4)
        scoring = similarity_scorer(query, description)
        if(scoring > 0.85):
            data["queries"].append({"query": query, "results": formatted_result})
    sorted_tweets = rank_tweets(data["queries"], description)
    return (res, data)

# if __name__ == "__main__":
#     res, data = get_results("NBA Playoffs 2024")
#     directory = os.path.join(DATA_DIR, "output.json")
#     with open(directory, "w") as json_file:
#         json.dump(data, json_file, indent=4)
