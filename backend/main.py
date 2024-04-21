import requests
import os
import json
from dotenv import load_dotenv
load_dotenv()

from Twitter.recent_search import recent_search
from Twitter.process_queries import analyze
from Twitter.rank_tweets import rank_tweets

DATA_DIR = os.path.join(os.getcwd(), "data")


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
    return (res, data)
