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
        return CORSResponse("Give me content, ya dingus.", status=412)

    response = dbapi.addTweet(tweet)
    if not response:
        return databaseErrorResponse()

    tweetDict = dbapi.dictionaryForTweet(response)
    return jsonify(tweet=tweetDict)

@app.route("/next", methods=["GET"])
def next():
    tweet = dbapi.topTweet()
    if not tweet:
        return CORSResponse("No tweets.", 200)
    return jsonify(tweet=dbapi.dictionaryForTweet(tweet))

@app.route("/count", methods=["GET"])
def count():
    return jsonify(count=dbapi.numberOfTweets())

@app.route("/all", methods=["GET"])
def all():
    return jsonify(tweets=dbapi.allTweetDicts())

@app.route("/remove", methods=["DELETE"])
def remove():
    arguments = request.args
    id = arguments.get("id", "")
    if not id:
        return CORSResponse("You must provide an id, otherwise I don't know what to delete, ya dingus.", 412)
    response = dbapi.removeTweetWithID(id)
    if not response:
        return databaseErrorResponse()
    return CORSResponse("Removed tweet.", 200)

def databaseErrorResponse():
    return CORSResponse("The database is giving some issues with that query.", 500)

def CORSResponse(message, status):
    response = Response(message, status)
    response.headers['Access-Control-Allow-Origin'] = "*"
    return response

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test",
                        help="Runs the server in test mode and updates the testUsers database.",
                        action="store_true")

    args = parser.parse_args()

    app.run(host="localhost", debug=args.test)
