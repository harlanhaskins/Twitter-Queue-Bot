from peewee import * 
import json
db = SqliteDatabase('tweets.db', threadlocals=True)

class Tweet(Model):
    content = CharField()

    class Meta():
        database = db

def addTweet(content=""):
    if not content:
        return
    return Tweet.create(content=content)

def allTweetSelectQuery():
    return Tweet.select().order_by(Tweet.id)

def allTweets():
    return [tweet for tweet in allTweetSelectQuery()]

def allTweetDicts():
    return [dictionaryForTweet(tweet) for tweet in allTweetSelectQuery()]

def dictionaryForTweet(tweet):
    return vars(tweet)["_data"]

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
    removeTweet(tweet)
    return tweet

def removeTweet(tweet):
    numberDeleted = tweet.delete_instance()
    return numberDeleted

def removeTweetWithID(id):
    tweet = Tweet.select().where(Tweet.id == id).first()
    if not tweet:
        return None
    return removeTweet(tweet)

Tweet.create_table(True)
