#!/usr/bin/env python
from __future__ import print_function
from dbapi import Tweet
import json
import twitter
import argparse


def tweet(twit):
    tweet_to_tweet = Tweet.top()
    if not tweet_to_tweet:
        return
    return (twit.statuses.update(status=tweet_to_tweet.content),
            tweet_to_tweet)


def url_with_endpoint(end_point):
    return base_url() + end_point


def base_url():
    return "https://api.twitter.com/1.1/"


def oauth_credentials():
    with open("credentials.json") as credentialsFile:
        return json.loads(credentialsFile.readline())


def authenticate():
    credentials = oauth_credentials()
    consumer_key = credentials["consumer_key"]
    consumer_secret = credentials["consumer_secret"]
    access_key = credentials["access_key"]
    access_secret = credentials["access_secret"]

    auth = twitter.OAuth(access_key, access_secret,
                         consumer_key, consumer_secret)
    return twitter.Twitter(auth=auth)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test",
                        help="Don't tweet and print to standard out.",
                        action="store_true")
    args = parser.parse_args()
    if Tweet.count() == 0:
        print("No tweets found.")
        exit(0)
    if args.test:
        print(Tweet.top().content)
        exit(0)
    twitter_client = authenticate()
    response, tweeted = tweet(twitter_client)
    if response:
        Tweet.pop()
        print("Tweeted: \"", tweeted.content, "\"", sep="")
    else:
        print("Could not send tweet.")
