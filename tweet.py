#!/usr/bin/env python
import requests
import dbapi
import json
import webbrowser
import twitter

def tweet(twit):
    tweet = dbapi.topTweet()
    if not tweet:
        return
    return twit.statuses.update(status=tweet.content)

def urlWithEndpoint(endpoint):
    return baseURL + endPoint

def baseURL():
    return "https://api.twitter.com/1.1/"

def oAuthCredentials():
    with open("credentials.txt") as credentialsFile:
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
    response = tweet(twit)
    if response:
        dbapi.popFirstTweet()
