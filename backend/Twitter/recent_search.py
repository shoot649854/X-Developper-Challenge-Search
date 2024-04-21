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

def clean_data(api_data):
    cleaned_data = []
    for tweet in api_data["data"]:
        cleaned_tweet = {
            "edit_history_tweet_ids": tweet["edit_history_tweet_ids"],
            "text": tweet["text"],
            "author_id": tweet["author_id"],
            "created_at": tweet["created_at"],
            "id": tweet["id"]
        }
        # Extract user information
        user_id = tweet["author_id"]
        user_data = next((user for user in api_data["includes"]["users"] if user["id"] == user_id), None)
        if user_data:
            cleaned_tweet["username"] = user_data["username"]
            cleaned_tweet["profile_image_url"] = user_data["profile_image_url"]
            cleaned_tweet["name"] = user_data["name"]
        # Extract media information if present
        if "attachments" in tweet and "media_keys" in tweet["attachments"]:
            media_keys = tweet["attachments"]["media_keys"]
            media_data = [media for media in api_data["includes"]["media"] if media["media_key"] in media_keys]
            if media_data:
                cleaned_tweet["media"] = media_data
        cleaned_data.append(cleaned_tweet)
    return cleaned_data

def recent_search(query, max_results=10, **kwargs):
    """
    Search for recent tweets based on a query and maximum number of results.
    """
    query_params = {
        'query': query,
        'tweet.fields': 'author_id,created_at,text,attachments',
        'max_results': str(max_results),
        'user.fields': 'name,username,profile_image_url',
        'media.fields': 'url,media_key',
        'expansions': 'attachments.media_keys,author_id'
    }
    query_params.update(kwargs)
    try:
        json_response = connect_to_endpoint(search_url, query_params)
    except:
        print("Error: Unable to connect to Twitter API.", search_url, query_params)
        return "{}"
    cleaned_data = clean_data(json_response)
    return json.dumps(cleaned_data, indent=4, sort_keys=True)
