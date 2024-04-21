from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity
import json

def similarity_scorer(tokenized_text1, tokenized_text2):
    model = Word2Vec([tokenized_text1, tokenized_text2], min_count=1, vector_size=100)
    tweet_embeddings = [model.wv[word] for word in tokenized_text1]
    context_string_embeddings = [model.wv[word] for word in tokenized_text2]
    similarity_score = cosine_similarity([sum(tweet_embeddings)], [sum(context_string_embeddings)])
    return similarity_score[0][0]

def rank_tweets(queries: list, context_string: str):
    ranked_tweets = []
    tokenized_context_string = context_string.split()

    for q in queries:
        try:
            tweets = eval(q['results'])['data']
            for tweet in tweets:
                tokenized_tweet = tweet["text"].split()
                ranked_tweets.append((similarity_scorer(tokenized_tweet, tokenized_context_string), tweet))
        except:
            continue
    
    return sorted(ranked_tweets, key=lambda x: x[0], reverse=True)

