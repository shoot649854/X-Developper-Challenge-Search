from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity
import json

tweets = ["WHO’S WHO DOWN THERE IN THE EAST COAST Two MVP candidates in Embiid and Brunson going at it, and Spida vs Paolo B. banner this 2024 Playoff preview ft. the Eastern Conference. For more NBA stories, check out http://nba.onesports.ph #EveryonesGame"]

context_string = "Well, well, well, look at you, jumping straight into the heart of the matter! You've got that playoff fever, don't you? I'm not surprised, considering the NBA playoffs are the zenith of basketball entertainment. As of now, the first round of the 2024 NBA Playoffs is underway, with the first games kicking off on April 20, 2024. Some of the notable matchups include the Cleveland Cavaliers vs. the Orlando Magic, the Oklahoma City Thunder vs. the New Orleans Pelicans, and the Denver Nuggets vs. the Los Angeles Lakers. For those who are particularly interested in the drama unfolding between the Los Angeles Clippers and the Dallas Mavericks, Game 1 was scheduled for April 21, 2024, at 3:30 p.m. If you're looking for a comprehensive overview of the schedule and results, the 2024 NBA Playoffs Bracket on ESPN provides a detailed breakdown. The first round began on April 20, and the playoffs are set to continue with games happening almost daily until a champion is crowned. This year's playoffs promise to be a thrilling ride, with several exciting matchups and potential upsets in the making. So grab your popcorn, don your favorite team's jersey, and get ready for some of the best basketball you'll see all year."

def rank_tweets(tweets: list, context_string: str):

    ranked_tweets = []
    tokenized_context_string = context_string.split()

    for tweet in tweets:
        tokenized_tweet = tweet["text"].split()

        model = Word2Vec([tokenized_tweet, tokenized_context_string], min_count=1, vector_size=100)

        tweet_embeddings = [model.wv[word] for word in tokenized_tweet]
        context_string_embeddings = [model.wv[word] for word in tokenized_context_string]
        
        similarity_score = cosine_similarity([sum(tweet_embeddings)], [sum(context_string_embeddings)])
        ranked_tweets.append((similarity_score[0][0], tweet))
        # return sorted(ranked_tweets, key=lambda x: x[0], reverse=True)
        # print("Similarity score between the two texts:", similarity_score[0][0])
        return sorted(ranked_tweets, key=lambda x: x[0], reverse=True)


def process_rank_tweets(queries):
    tweets_text = []
    combined_tweets = []
    for query in queries:
        parsed_query_results = json.loads(query["results"])
        if "data" in parsed_query_results:        
            tweets = parsed_query_results["data"]
            for tweet in tweets:
                combined_tweets.append(tweet)
                tweets_text.append(tweet["text"])

    return rank_tweets(combined_tweets, context_string)

