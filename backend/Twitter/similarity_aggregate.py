from gensim.models import Word2Vec
import statistics
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
from analyze import get_subqueries, get_description
from openai import OpenAI

load_dotenv()

openai_client = OpenAI(
    organization="org-1EDbnzjdGhFGeAAiDIyKSyc6",
)
def generate_embeddings(query):
    response = openai_client.embeddings.create(
        input=query,
        model="text-embedding-ada-002"
        )
    return response.data[0].embedding
AI_results = [
    {
        "author_id": "110852856",
        "created_at": "2024-04-21T19:01:41.000Z",
        "edit_history_tweet_ids": [
            "1782122553320124441"
        ],
        "id": "1782122553320124441",
        "name": "Fred Smith",
        "profile_image_url": "https://pbs.twimg.com/profile_images/1892625509/47-32_normal.jpg",
        "text": "F1 looooooves pulling the points scoring threshold down and hates expanding the grid. It\u2019s going to be like the NBA with 20 postseason teams from 30 franchises. https://t.co/rA6qQrC0ng",
        "username": "FredSmith914"
    },
    {
        "author_id": "28695500",
        "created_at": "2024-04-21T19:00:51.000Z",
        "edit_history_tweet_ids": [
            "1782122342614761489"
        ],
        "id": "1782122342614761489",
        "name": "DJ",
        "profile_image_url": "https://pbs.twimg.com/profile_images/1718128441831170048/_xgdTgOe_normal.jpg",
        "text": "My favorite sports teams\n\nCollege: BYU\nNFL: @Broncos \nMLB: I guess Rockies \nNBA: @nuggets \nWNBA: don\u2019t know\nNHL: @Avalanche \nSoccer: uhhh Rapids? lol \nGolf: Tiger Tiger Woods y\u2019all https://t.co/RthhEjFkfH",
        "username": "Donye_G"
    },
    {
        "author_id": "4822618528",
        "created_at": "2024-04-21T19:00:23.000Z",
        "edit_history_tweet_ids": [
            "1782122226373869810"
        ],
        "id": "1782122226373869810",
        "name": "Mr. Feeny",
        "profile_image_url": "https://pbs.twimg.com/profile_images/1093421580309458944/b13qiU25_normal.jpg",
        "text": ". @NBAOfficial @NBA needs to start calling Bam for these EXTREMELY OBVIOUS illegal screens.\n\nIt\u2019s been happening for years. It\u2019s absolutely ridiculous. Even play by play teams talk about it.\n\nDo your damn job.",
        "username": "coachfeeny"
    },
    {
        "author_id": "37732316",
        "created_at": "2024-04-21T19:00:01.000Z",
        "edit_history_tweet_ids": [
            "1782122134988620249"
        ],
        "id": "1782122134988620249",
        "name": "TYLER COSTON | SAVI Coaching",
        "profile_image_url": "https://pbs.twimg.com/profile_images/1510010809786638339/wdiLyCBz_normal.jpg",
        "text": "It was his first NBA game where he shot free throws underhand.\n\nWilt was a terrible free throw shooter, sub 50%. But he was so dominant that teams would throw multiple bodies at him because the only way to stop him was to foul him. Wilt was the original hack-a-shaq.",
        "username": "tylercoston"
    },
    {
        "author_id": "1357553542383476737",
        "created_at": "2024-04-21T18:58:42.000Z",
        "edit_history_tweet_ids": [
            "1782121802178683322"
        ],
        "id": "1782121802178683322",
        "name": "Drew",
        "profile_image_url": "https://pbs.twimg.com/profile_images/1755361195836526592/WsR2CsH3_normal.jpg",
        "text": "In the NBA Playoffs, teams that win should be able to carry the (+)margin they won by to the next game. \n\nWould keep blow outs interesting",
        "username": "_Drew_2_U"
    },
    {
        "author_id": "29063026",
        "created_at": "2024-04-21T18:58:21.000Z",
        "edit_history_tweet_ids": [
            "1782121715553665048"
        ],
        "id": "1782121715553665048",
        "media": [
            {
                "media_key": "16_1782121706917707776",
                "type": "animated_gif"
            }
        ],
        "name": "Jon Alba",
        "profile_image_url": "https://pbs.twimg.com/profile_images/1733354310715498496/LvGK5Tzo_normal.jpg",
        "text": "I am LIVE at 3 p.m. ET with @john_tortorelli discussing our sleeper #NBAPlayoffs teams on the @livetakesports app!\n\nDownload it now and join the conversation! #NBA https://t.co/xejm1AemR5",
        "username": "JonAlba"
    },
    {
        "author_id": "1716678228172046336",
        "created_at": "2024-04-21T18:57:38.000Z",
        "edit_history_tweet_ids": [
            "1782121534099783891"
        ],
        "id": "1782121534099783891",
        "name": "MUNYPICKS DISCORD",
        "profile_image_url": "https://pbs.twimg.com/profile_images/1777157876735246336/lE0QU0R2_normal.jpg",
        "text": "RT @munypicks: MLB MUST bet play \u26be\ufe0f\n\nDarius Vines O 1.5 Walks \n\n\u2022 projected for 2.6 walks \n\u2022 rangers are one of the best at drawing the wal\u2026",
        "username": "munysdiscord"
    },
    {
        "author_id": "27716677",
        "created_at": "2024-04-21T18:57:27.000Z",
        "edit_history_tweet_ids": [
            "1782121488302383602"
        ],
        "id": "1782121488302383602",
        "name": "G.King",
        "profile_image_url": "https://pbs.twimg.com/profile_images/1288147575111946240/FmFUO6JF_normal.jpg",
        "text": "Denver vs Boston in the NBa Finals\u2026. This year\u2026 I don\u2019t see nobody beating those teams",
        "username": "gkingcomic"
    },
    {
        "author_id": "1634776929420165121",
        "created_at": "2024-04-21T18:57:20.000Z",
        "edit_history_tweet_ids": [
            "1782121458639982635"
        ],
        "id": "1782121458639982635",
        "media": [
            {
                "media_key": "3_1782121454143762433",
                "type": "photo",
                "url": "https://pbs.twimg.com/media/GLteBTzXcAE4chW.jpg"
            }
        ],
        "name": "MUNYPICKS \ud83d\udcb2",
        "profile_image_url": "https://pbs.twimg.com/profile_images/1634776990325567488/4IAcDyi9_normal.jpg",
        "text": "MLB MUST bet play \u26be\ufe0f\n\nDarius Vines O 1.5 Walks \n\n\u2022 projected for 2.6 walks \n\u2022 rangers are one of the best at drawing the walk \n\u2022 vines continues to struggle vs goo teams \n\n-142 on DraftKings \n\ngar ALL FREE slips and plays \u2935\ufe0f\nhttps://t.co/eILA50idrk\n\n#mlb #nba #prizepicks\u2026 https://t.co/EjB7Lpwvmg https://t.co/Kp1LOr5Wck",
        "username": "munypicks"
    },
    {
        "author_id": "768887301149569024",
        "created_at": "2024-04-21T18:54:57.000Z",
        "edit_history_tweet_ids": [
            "1782120856828682433"
        ],
        "id": "1782120856828682433",
        "name": "Jerel McNeal",
        "profile_image_url": "https://pbs.twimg.com/profile_images/1699240943856050176/XAmBEO9D_normal.jpg",
        "text": "\ud83c\udfaf this where I got the idea that year \ud83e\udd23\ud83e\udd23 I remember watching old NBA playoff series and teams would all go bald Knicks did it one year when they were good. Solidarity! \ud83d\ude02\ud83d\ude02\ud83e\udd85\ud83e\udee1 https://t.co/In5UwELSyM",
        "username": "jerel_mcneal"
    }
]


tweets_lst = [
        {
            "text": "RT @BradeyKing: Gru and a minion reporting for the NBA playoffs 😆 https://t.co/XIWdhtPmRJ",
            "id": "1782120248155771153",
            "edit_history_tweet_ids": [
                "1782120248155771153"
            ],
            "created_at": "2024-04-21T18:52:32.000Z",
            "author_id": "1129454867863359488"
        },
        {
            "text": "🔴NBA Streams➡️@nbastardayy\n\nWatch NBA | Playoffs | Game 1 Tournament Live Streaming Online Free \n\n🔴Go Live➡️@nbastardayy  [Try for Free]\n\nMiami Heat vs Boston Celtics live\nCeltics vs Heat\nNBA | Playoffs | Game 1\nNBA Streams\n#CelticsvsHeat\n#NBAPlayoffsGame https://t.co/EiqG43wHNQ",
            "id": "1782120242719723577",
            "edit_history_tweet_ids": [
                "1782120242719723577"
            ],
            "created_at": "2024-04-21T18:52:30.000Z",
            "author_id": "1782024159637204992"
        },
        {
            "text": "Ok il y’a les 3 points qui tombent mais on parle de la defense des @celtics moins de 70 pts encaissés sur 3QT c’est vraiment #DifferentHere #NBA #Playoffs",
            "id": "1782120238089220246",
            "edit_history_tweet_ids": [
                "1782120238089220246"
            ],
            "created_at": "2024-04-21T18:52:29.000Z",
            "author_id": "606503267"
        },
        {
            "text": "RT @barstoolsports: It’s 2014 and you’re getting ready to watch the NBA Playoffs https://t.co/UidgarvhCy",
            "id": "1782120213716025783",
            "edit_history_tweet_ids": [
                "1782120213716025783"
            ],
            "created_at": "2024-04-21T18:52:23.000Z",
            "author_id": "3988834719"
        },
        {
            "text": "🔴NBA Streams➡️@nbastardayy\n\nWatch NBA | Playoffs | Game 1 Tournament Live Streaming Online Free \n\n🔴Go Live➡️@nbastardayy  [Try for Free]\n\nMiami Heat vs Boston Celtics live\nCeltics vs Heat\nNBA | Playoffs | Game 1\nNBA Streams\n#CelticsvsHeat\n#NBAPlayoffsGame https://t.co/em4MYp2p8u",
            "id": "1782120189842084094",
            "edit_history_tweet_ids": [
                "1782120189842084094"
            ],
            "created_at": "2024-04-21T18:52:18.000Z",
            "author_id": "1782024159637204992"
        },
        {
            "text": ".@google, you should make bracket design on homepage for playoffs (@nba, @nfl, @mlb, @wnba).",
            "id": "1782120172586729743",
            "edit_history_tweet_ids": [
                "1782120172586729743"
            ],
            "created_at": "2024-04-21T18:52:13.000Z",
            "author_id": "1014472378330607616"
        },
        {
            "text": "@NYCDaFuture_ @HaterReport_ You nba fans be so flip floppy I swear. He been playing good. As soon as he had one bad game, yall talk shit… he just won the the game against the pelicans in the playoffs in. Now he has a bad game and he needs to be traded? Yall mfs be on dick crazy. I’m not even a LA fan",
            "id": "1782120163547976160",
            "edit_history_tweet_ids": [
                "1782120163547976160"
            ],
            "created_at": "2024-04-21T18:52:11.000Z",
            "author_id": "1285023999328755714"
        },
        {
            "text": "RT @KevinGarnett5KG: NBA Playoffs… Rap Playoffs… fight night… Happy 4/20 too 💯 💨",
            "id": "1782120155323023395",
            "edit_history_tweet_ids": [
                "1782120155323023395"
            ],
            "created_at": "2024-04-21T18:52:09.000Z",
            "author_id": "1215452785841491971"
        },
        {
            "text": "🔴NBA Streams➡️@nbastardayy\n\nWatch NBA | Playoffs | Game 1 Tournament Live Streaming Online Free \n\n🔴Go Live➡️@nbastardayy  [Try for Free]\n\nMiami Heat vs Boston Celtics live\nCeltics vs Heat\nNBA | Playoffs | Game 1\nNBA Streams\n#CelticsvsHeat\n#NBAPlayoffsGame https://t.co/r6MQU1Kxw1",
            "id": "1782120153502593521",
            "edit_history_tweet_ids": [
                "1782120153502593521"
            ],
            "created_at": "2024-04-21T18:52:09.000Z",
            "author_id": "1782024159637204992"
        },
        {
            "text": "RT @scotteTheKing: Tune in for Fantasy Baseball, NBA Playoffs and NFL Draft talk on @SiriusXMFantasy from 3 to 5 pm ET - it's @RotoBaller R…",
            "id": "1782120137367425100",
            "edit_history_tweet_ids": [
                "1782120137367425100"
            ],
            "created_at": "2024-04-21T18:52:05.000Z",
            "author_id": "344981016"
        }
    ]
context_st = "Today, April 20, 2024, marks the height of basketball excitement as the NBA Playoffs reach their climax. The Eastern and Western Conference Semifinals are underway, with several intense matchups gracing the hardwood. The Boston Celtics and Milwaukee Bucks face off in the East, while the Golden State Warriors and Denver Nuggets duel in the West. Stay tuned for thrilling games, upsets, and the race to secure a spot in the Conference Finals. Don't miss a moment of the action!"
def similarity_aggregate(tweets: list, context_string: str):
    tokenized_context_string = context_string.split()
    similarity_lst = []

    for tweet in tweets:
        tokenized_tweet = tweet["text"].split()
        similarity_lst.append(similarity_scorer(tokenized_tweet, tokenized_context_string))
    
    return statistics.mean(similarity_lst)

def similarity_scorer(tokenized_text1, tokenized_text2):
    embeddings1 = generate_embeddings(' '.join(tokenized_text1))
    embeddings2 = generate_embeddings(' '.join(tokenized_text2))
    similarity_score = cosine_similarity([embeddings1], [embeddings2])
    return similarity_score[0][0]

print("Original Query: ", similarity_aggregate(tweets_lst, context_st))
print("AI Query Score: ", similarity_aggregate(AI_results, context_st))

