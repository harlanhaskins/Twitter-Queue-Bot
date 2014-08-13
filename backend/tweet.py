#!/usr/bin/env python
from __future__ import print_function
import dbapi
import json
import twitter
import argparse

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
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test",
                        help="Don't tweet and print to standard out.",
                        action="store_true")
    args = parser.parse_args()
    if args.test:
        print(dbapi.topTweet())
        exit(0)
    twit = authenticate()
    response, tweeted = tweet(twit)
    if response:
        dbapi.popFirstTweet()
        print("Tweeted: \"", tweeted.content, "\"", sep="")
    else:
        print("Could not send tweet. Will try again tomorrow.")
