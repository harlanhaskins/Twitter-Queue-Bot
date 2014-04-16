#!/usr/bin/env python

from flask import Flask, Response
from flask import request, make_response, request, current_app
from flask.json import jsonify
from functools import update_wrapper
from datetime import timedelta
from flask_cors import *
import argparse
import dbapi

app = Flask(__name__)

@app.route("/add", methods=["POST", "OPTIONS"])
@cross_origin(headers=["Content-Type"])
def add():
    if request.method == "OPTIONS":
        return optionsResponse()
    arguments = request.args
    tweet = arguments.get("tweet", "")
    if not (tweet):
        return Response("Give me content, ya dingus.", status=412)

    response = dbapi.addTweet(tweet)
    if not response:
        return databaseErrorResponse()

    tweetDict = dbapi.dictionaryForTweet(response)
    return jsonify(tweet=tweetDict)

@app.route("/next", methods=["GET"])
@cross_origin(headers=["Content-Type"])
def next():
    tweet = dbapi.topTweet()
    if not tweet:
        return Response("No tweets.", 200)
    return jsonify(tweet=dbapi.dictionaryForTweet(tweet))

@app.route("/count", methods=["GET"])
@cross_origin(headers=["Content-Type"])
def count():
    return jsonify(count=dbapi.numberOfTweets())

@app.route("/all", methods=["GET"])
@cross_origin(headers=["Content-Type"])
def all():
    return jsonify(tweets=dbapi.allTweetDicts())

@app.route("/remove", methods=["DELETE", "OPTIONS"])
@cross_origin(headers=["Content-Type"])
def remove():
    if request.method == "OPTIONS":
        return optionsResponse()
    arguments = request.args
    id = arguments.get("id", "")
    if not id:
        return Response("You must provide an id, otherwise I don't know what to delete, ya dingus.", 412)
    response = dbapi.removeTweetWithID(id)
    if not response:
        return databaseErrorResponse()
    tweetDict = dbapi.dictionaryForTweet(response)
    return jsonify(tweet=tweetDict)

def databaseErrorResponse():
    return Response("The database is giving some issues with that query.", 500)

def optionsResponse():
    return Response("Yeah there's some options here, bro.", 200)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test",
                        help="Runs the server in test mode and updates the testUsers database.",
                        action="store_true")

    args = parser.parse_args()

    app.run(host="localhost", port=4200, debug=args.test)
