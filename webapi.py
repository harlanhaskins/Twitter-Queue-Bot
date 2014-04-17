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

@app.before_request
def option_autoreply():
    """ Always reply 200 on OPTIONS request """

    if request.method == 'OPTIONS':
        resp = app.make_default_options_response()

        headers = None
        if 'ACCESS_CONTROL_REQUEST_HEADERS' in request.headers:
            headers = request.headers['ACCESS_CONTROL_REQUEST_HEADERS']

        h = resp.headers

        # Allow the origin which made the XHR
        h['Access-Control-Allow-Origin'] = request.headers['Origin']
        # Allow the actual method
        h['Access-Control-Allow-Methods'] = request.headers['Access-Control-Request-Method']
        # Allow for 10 seconds
        h['Access-Control-Max-Age'] = "10"

        # We also keep current headers
        if headers is not None:
            h['Access-Control-Allow-Headers'] = headers

        return resp

@app.route("/add", methods=["POST", "OPTIONS"])
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
def next():
    tweet = dbapi.topTweet()
    if not tweet:
        return Response("No tweets.", 200)
    return jsonify(tweet=dbapi.dictionaryForTweet(tweet))

@app.route("/count", methods=["GET"])
def count():
    return jsonify(count=dbapi.numberOfTweets())

@app.route("/all", methods=["GET"])
def all():
    return jsonify(tweets=dbapi.allTweetDicts())

@app.route("/remove", methods=["DELETE", "OPTIONS"])
def remove():
    arguments = request.args
    id = arguments.get("id", "")
    if not id:
        return Response("You must provide an id, otherwise I don't know what to delete, ya dingus.", 412)
    response = dbapi.removeTweetWithID(id)
    if not response:
        return databaseErrorResponse()
    tweetDict = dbapi.dictionaryForTweet(response)
    return jsonify(tweet=tweetDict)

@app.after_request
def set_allow_origin(resp):
    """ Set origin for GET, POST, PUT, DELETE requests """

    h = resp.headers

    # Allow crossdomain for other HTTP Verbs
    if request.method != 'OPTIONS' and 'Origin' in request.headers:
        h['Access-Control-Allow-Origin'] = request.headers['Origin']

    return resp

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
