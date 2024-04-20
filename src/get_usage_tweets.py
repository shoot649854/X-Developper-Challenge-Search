import requests
import os
import json
from dotenv import load_dotenv
load_dotenv()

bearer_token = os.environ.get("BEARER_TOKEN")

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UsageTweetsPython"
    return r


def connect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def get_usage_tweets():
    url = "https://api.twitter.com/2/usage/tweets"
    json_response = connect_to_endpoint(url)
    return json.dumps(json_response, indent=4, sort_keys=True)


if __name__ == "__main__":
    get_usage_tweets()
