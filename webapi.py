#!/usr/bin/env python

from flask import Flask, Response
from flask import request
from flask.json import jsonify
import argparse
import dbapi

app = Flask(__name__)

@app.route("/add", methods=["POST"])
def add():
    arguments = request.args
    tweet = arguments.get("tweet", "")
    if not (tweet):
        return Response("Give me content, ya dingus.", status=412)

    response = dbapi.addTweet(tweet)
    if not response:
        return Response("We had some trouble adding it to the database.", 500)

    return Response("Added to the queue.", 200)

@app.route("/next", methods=["GET"])
def top():
    tweet = dbapi.topTweet()
    if not tweet:
        return Response("No tweets.", 200)
    return jsonify(content=tweet.content)

@app.route("/count", methods=["GET"])
def count():
    return jsonify(count=dbapi.numberOfTweets())

@app.route("/all", methods=["GET"])
def all():
    return jsonify(tweets=dbapi.allTweetDicts())

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test",
                        help="Runs the server in test mode and updates the testUsers database.",
                        action="store_true")

    args = parser.parse_args()

    app.run(host="localhost", debug=args.test)
