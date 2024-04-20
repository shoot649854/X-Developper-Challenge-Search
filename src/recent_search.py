import requests
import os
import json
from dotenv import load_dotenv
load_dotenv()

# Twitter API search URL
bearer_token = os.environ.get("BEARER_TOKEN")
search_url = "https://api.twitter.com/2/tweets/search/recent"

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def connect_to_endpoint(url, params):
    """
    Connect to Twitter API endpoint
    """
    response = requests.get(url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def recent_search(query, max_results=10):
    """
    Search for recent tweets based on a query and maximum number of results.
    """
    query_params = {
        'query': query,
        'tweet.fields': 'author_id,created_at,text',
        'max_results': str(max_results)
    }
    json_response = connect_to_endpoint(search_url, query_params)
    return json.dumps(json_response, indent=4, sort_keys=True)

# if __name__ == "__main__":
#     query = "#NBAPlayoffs -is:retweet"
#     print(recent_search(query, 10))