from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity
import json
import statistics
from backend.Twitter.rank_tweets import similarity_scorer

def similarity_aggregate(tweets: list, context_string: str):
    tokenized_context_string = context_string.split()
    similarity_lst = []

    for tweet in tweets:
        tokenized_tweet = tweet["text"].split()
        similarity_lst.append(similarity_scorer(tokenized_tweet, tokenized_context_string))
    
    return statistics.mean(similarity_lst)

