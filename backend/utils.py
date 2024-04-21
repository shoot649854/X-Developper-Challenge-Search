from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity
import json

def similarity_scorer(tokenized_text1, tokenized_text2):
    model = Word2Vec([tokenized_text1, tokenized_text2], min_count=1, vector_size=100)
    tweet_embeddings = [model.wv[word] for word in tokenized_text1]
    context_string_embeddings = [model.wv[word] for word in tokenized_text2]
    similarity_score = cosine_similarity([sum(tweet_embeddings)], [sum(context_string_embeddings)])
    return similarity_score[0][0]