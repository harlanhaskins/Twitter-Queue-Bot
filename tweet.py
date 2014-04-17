#!/usr/bin/env python
import dbapi
import json
import twitter

def tweet(twit):
    tweetToTweet = dbapi.topTweet()
    if not tweetToTweet:
        return
    return (twit.statuses.update(status=tweetToTweet.content),
            tweetToTweet)

def urlWithEndpoint(endpoint):
    return baseURL + endPoint

def baseURL():
    return "https://api.twitter.com/1.1/"

def oAuthCredentials():
    with open("credentials.json") as credentialsFile:
        return json.loads(credentialsFile.readline())

def authenticate():
    credentials        = oAuthCredentials()
    consumerKey        = credentials["consumer_key"]
    consumerSecret     = credentials["consumer_secret"]
    accessKey          = credentials["access_key"]
    accessSecret       = credentials["access_secret"]

    auth = twitter.OAuth(accessKey, accessSecret, consumerKey, consumerSecret)
    return twitter.Twitter(auth=auth)

if __name__ == "__main__":
    twit = authenticate()
    response, tweeted = tweet(twit)
    if response:
        dbapi.popFirstTweet()
        print("Tweeted: \"" + tweeted.content + "\"")
    else:
        print("Could not send tweet. Will try again tomorrow.")
