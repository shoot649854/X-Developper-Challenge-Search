from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity
import json
import statistics
from rank_tweets import similarity_scorer

def similarity_aggregate(tweets: list, context_string: str):
    tokenized_context_string = context_string.split()
    similarity_lst = []

    for tweet in tweets:
        tokenized_tweet = tweet["text"].split()
        similarity_lst.append(similarity_scorer(tokenized_tweet, tokenized_context_string))
    
    return statistics.mean(similarity_lst)

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
        'query': query,
        'tweet.fields': 'author_id,created_at,text',
        'max_results': str(max_results)
    }
    query_params.update(kwargs)
    json_response = connect_to_endpoint(search_url, query_params)
    print(json_response)
    return json.dumps(json_response, indent=4, sort_keys=True)

recent_search("playoffs")
