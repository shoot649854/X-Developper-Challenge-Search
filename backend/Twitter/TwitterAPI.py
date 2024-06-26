import requests
import os
import json
from typing import Dict, Any
from dotenv import load_dotenv
load_dotenv()

# Twitter API search URL
bearer_token = os.environ.get("BEARER_TOKEN")
search_url = "https://api.twitter.com/2/tweets/search/recent"

class TwitterAPI:
    def __init__(self):
        self.bearer_token = os.environ.get("BEARER_TOKEN")
        self.search_url = "https://api.twitter.com/2/tweets/search/recent"
        self.usage_url = "https://api.twitter.com/2/usage/tweets"

    def bearer_oauth(self, r: requests.Request) -> requests.Request:
        """
        Method required by bearer token authentication.
        """
        r.headers["Authorization"] = f"Bearer {self.bearer_token}"
        r.headers["User-Agent"] = "v2RecentSearchPython"
        return r

    def connect_to_endpoint(self, url: str, params: Dict[str, str]) -> Dict[str, Any]:
        """
        Connect to Twitter API endpoint
        """
        response = requests.get(url, auth=self.bearer_oauth, params=params)
        print(response.status_code)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        return response.json()

    def recent_search(self, query: str, max_results: int = 25) -> str:
        """
        Search for recent tweets based on a query and maximum number of results.
        """
        query_params = {
            'query': query,
            'tweet.fields': 'author_id,created_at,text',
            'max_results': str(max_results),
            'user.fields': 'name,username,profile_image_url',
            'media.fields': 'url',
            'expansions': 'attachments.media_keys,author_id'
        }
        json_response = self.connect_to_endpoint(self.search_url, query_params)
        return json.dumps(json_response, indent=4, sort_keys=True)

    def get_usage_tweets(self):
        json_response = self.connect_to_endpoint(self.usage_url)
        return json.dumps(json_response, indent=4, sort_keys=True)
    
    
# # Example Usage
# if __name__ == "__main__":
#     twitter_api = TwitterAPI()
#     keyword = "NBAPlayoffs"
#     query = "#{0} -is:retweet".format(keyword)
#     # print(twitter_api.recent_search(query, 10))
#     twitter_api.get_usage_tweets()