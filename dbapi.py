from peewee import * 
db = SqliteDatabase('tweets.db', threadlocals=True)

class Tweet(Model):
    content = CharField()

    class Meta():
        database = db

def addTweet(content="", shouldIncludeTag=False):
    if not content:
        return
    if shouldIncludeTag:
        content += " #420Puns"
    return Tweet.create(content=content)

def allTweets():
    return [tweet for tweet in Tweet.select().order_by(Tweet.id)]

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
        return None
    tweetQuery = (Tweet
                .delete()
                .where(Tweet.id == tweet.id))
    tweetQuery.execute()
    return tweet

Tweet.create_table(True)
