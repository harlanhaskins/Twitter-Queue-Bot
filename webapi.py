#!/usr/bin/env python

from flask import Flask, Response
from flask import request, make_response, request, current_app
from flask.json import jsonify
from functools import update_wrapper
from datetime import timedelta
import argparse
import dbapi

app = Flask(__name__)

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

@app.route("/add", methods=["POST"])
@crossdomain(origin='*')
def add():
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
@crossdomain(origin='*')
def next():
    tweet = dbapi.topTweet()
    if not tweet:
        return Response("No tweets.", 200)
    return jsonify(tweet=dbapi.dictionaryForTweet(tweet))

@app.route("/count", methods=["GET"])
@crossdomain(origin='*')
def count():
    return jsonify(count=dbapi.numberOfTweets())

@app.route("/all", methods=["GET"])
@crossdomain(origin='*')
def all():
    return jsonify(tweets=dbapi.allTweetDicts())

@app.route("/remove", methods=["DELETE"])
@crossdomain(origin='*')
def remove():
    arguments = request.args
    id = arguments.get("id", "")
    if not id:
        return Response("You must provide an id, otherwise I don't know what to delete, ya dingus.", 412)
    response = dbapi.removeTweetWithID(id)
    if not response:
        return databaseErrorResponse()
    return Response("Removed tweet.", 200)

def databaseErrorResponse():
    return Response("The database is giving some issues with that query.", 500)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test",
                        help="Runs the server in test mode and updates the testUsers database.",
                        action="store_true")

    args = parser.parse_args()

    app.run(host="localhost", debug=args.test)
