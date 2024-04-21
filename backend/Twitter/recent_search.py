import requests
import os
import json
from dotenv import load_dotenv
load_dotenv()

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
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def recent_search(query, max_results=10, **kwargs):
    """
    Search for recent tweets based on a query and maximum number of results.
    """
    query_params = {
        'query': f'{query} -is:retweet',
        'tweet.fields': 'author_id,created_at,text',
        'max_results': str(max_results),
        'user.fields': 'name,username,profile_image_url',
        'media.fields': 'url',
        'expansions': 'attachments.media_keys,author_id'
    }
    query_params.update(kwargs)
    try:
        json_response = connect_to_endpoint(search_url, query_params)
    except:
        print("Error: Unable to connect to Twitter API.", search_url, query_params)
        return "{}"
    with open("recent_search_queries.json", 'w') as file:
        file.write(json.dumps(json_response, indent=4, sort_keys=True))
    file.close()
    return json.dumps(json_response, indent=4, sort_keys=True)
