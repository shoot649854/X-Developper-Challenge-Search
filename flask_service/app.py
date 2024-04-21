from flask import Flask
from sklearn.metrics.pairwise import cosine_similarity
from utils import similarity_scorer
import statistics

app = Flask(__name__)

# Define routes
@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/twitter_query_search')
def twitter_query_search():
    return 'Success'

@app.route('/get_subqueries_context_string')
def get_subqueries_context_string():
    return 'Success'

@app.route('/twitter_subquery_search')
def twitter_subquery_search():
    return 'Success'

@app.route('/rank_tweets')
def rank_tweets(tweets: list, context_string: str):
    ranked_tweets = []
    tokenized_context_string = context_string.split()

    for tweet in tweets:
        tokenized_tweet = tweet["text"].split()
        ranked_tweets.append((similarity_scorer(tokenized_tweet, tokenized_context_string), tweet))
    
    return sorted(ranked_tweets, key=lambda x: x[0], reverse=True)

@app.route('/original_similarity_aggregate')
def similarity_aggregate(tweets: list, context_string: str):
    tokenized_context_string = context_string.split()
    similarity_lst = []
    for tweet in tweets:
        tokenized_tweet = tweet["text"].split()
        similarity_lst.append(similarity_scorer(tokenized_tweet, tokenized_context_string))
    
    return statistics.mean(similarity_lst)


if __name__ == '__main__':
    app.run(debug=True)
