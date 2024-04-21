import json
import asyncio
from sklearn.metrics.pairwise import cosine_similarity
from backend.Twitter.process_queries import generate_embeddings

async def similarity_scorer(tokenized_text1, tokenized_text2):
    embeddings1 = generate_embeddings(' '.join(tokenized_text1))
    embeddings2 = generate_embeddings(' '.join(tokenized_text2))
    similarity_score = cosine_similarity([embeddings1], [embeddings2])
    return similarity_score[0][0]

async def rank_tweet(tweet, tokenized_context_string):
    tokenized_tweet = tweet["text"].split()
    score = await similarity_scorer(tokenized_tweet, tokenized_context_string)
    if score >= 0.35:
        return (score, tweet)
    return None

async def rank_tweets(queries: list, context_string: str):
    ranked_tweets = []
    tokenized_context_string = context_string.split()
    tasks = []
    for q in queries:
        try:
            tweets = eval(q['results'])["data"]
            for tweet in tweets:
                tasks.append(rank_tweet(tweet, tokenized_context_string))
        except:
            continue
    
    results = await asyncio.gather(*tasks)
    for result in results:
        if result is not None:
            ranked_tweets.append(result)
    
    sorted_items = sorted(ranked_tweets, key=lambda x: x[0], reverse=True)
    ranked_tweets_dict = [{"score": score_tweet_pair[0], "tweet": score_tweet_pair[1]} for score_tweet_pair in sorted_items]
    return ranked_tweets_dict

