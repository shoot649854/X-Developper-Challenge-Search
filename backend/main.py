import requests
import os
import json
from dotenv import load_dotenv
load_dotenv()

from Twitter.recent_search import recent_search
from Twitter.process_queries import analyze
from Twitter.rank_tweets import rank_tweets

DATA_DIR = os.path.join(os.getcwd(), "data")
# subqueries = [
#     "NBA Playoffs 2024",
#     "NBA Playoffs Bracket 2024"
# ]

# data = {"queries": []}

# for item in subqueries:
#     query = "#{0} -is:retweet".format(item)
#     search_result = recent_search(query, 10)
#     formatted_result = json.dumps(json.loads(search_result), indent=4)
#     data["queries"].append({"query": query, "results": formatted_result})

# directory = os.path.join(DATA_DIR, "recent_search_queries.json")
# with open(directory, "w") as json_file:
#     json.dump(data, json_file, indent=4)

def get_results(query):
    res = analyze(query)
    description = res["description"]
    subqueries = res["subqueries"]
    data = {"queries": []}
    for item in subqueries:
        query = "#{0} -is:retweet".format(item)
        search_result = recent_search(query, 10)
        search_result = search_result.replace("\n", "")
        formatted_result = json.dumps(search_result, indent=4)
        data["queries"].append({"query": query, "results": formatted_result})
    sorted_tweets = rank_tweets(data["queries"], description)
    return (res, data)

if __name__ == "__main__":
    res, data = get_results("NBA Playoffs 2024")
    directory = os.path.join(DATA_DIR, "output.json")
    with open(directory, "w") as json_file:
        json.dump(data, json_file, indent=4)
