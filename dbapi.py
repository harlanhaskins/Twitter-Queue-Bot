from peewee import * 
import json
db = SqliteDatabase('tweets.db', threadlocals=True)

class Tweet(Model):
    content = CharField()

    def __str__(self):
        return json.dumps({"content":self.content, "id":self.id})

    class Meta():
        database = db

def addTweet(content="", shouldIncludeTag=False):
    if not content:
        return
    if shouldIncludeTag:
        content += " #420Puns"
    return Tweet.create(content=content)

def allTweetSelectQuery():
    return Tweet.select().order_by(Tweet.id)

def allTweets():
    return [tweet for tweet in allTweetSelectQuery()]

def allTweetDicts():
    return [vars(tweet)["_data"] for tweet in allTweetSelectQuery()]

def numberOfTweets():
    return Tweet.select().count()

def topTweet():
    tweets = (Tweet
            .select()
            .order_by(Tweet.id)
            .limit(1))
    if not tweets:
        return None
    return tweets.first()

def popFirstTweet():
    tweet = topTweet()
    if not tweet:
        print("Tweet doesn't exist.")
        return None

    numberDeleted = tweet.delete_instance()

    if numberDeleted < 1:
        print("Tweet not deleted.")
        return None

    return tweet

Tweet.create_table(True)
