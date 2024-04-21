from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity
import json
from backend.Twitter.process_queries import generate_embeddings

def similarity_scorer(tokenized_text1, tokenized_text2):
    embeddings1 = generate_embeddings(' '.join(tokenized_text1))
    embeddings2 = generate_embeddings(' '.join(tokenized_text2))
    similarity_score = cosine_similarity([embeddings1], [embeddings2])
    return similarity_score[0][0]

def rank_tweets(queries: list, context_string: str):
    ranked_tweets = []
    tokenized_context_string = context_string.split()
    for q in queries:
        try:
            tweets = eval(q['results'])["data"]
            
            for tweet in tweets:
                tokenized_tweet = tweet["text"].split()
                score = similarity_scorer(tokenized_tweet, tokenized_context_string)
                if score < 0.35:
                    continue
                else:
                    ranked_tweets.append((score, tweet))
        except:
            continue
    
    sorted_items = sorted(ranked_tweets, key=lambda x: x[0], reverse=True)
    ranked_tweets_dict = [{"score": score_tweet_pair[0], "tweet": score_tweet_pair[1]} for score_tweet_pair in sorted_items]
    return ranked_tweets_dict

