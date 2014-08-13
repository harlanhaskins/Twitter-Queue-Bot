#!/usr/bin/env python

from flask import Flask, Response
from flask import request, make_response, request, current_app
from flask.json import jsonify
from functools import update_wrapper
from datetime import timedelta
import argparse
from dbapi import Tweet

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
        h['Access-Control-Allow-Methods'] = request.headers['Access-Control' + \
                                                            '-Request-Method']
        # Allow for 10 seconds
        h['Access-Control-Max-Age'] = "10"

        # We also keep current headers
        if headers is not None:
            h['Access-Control-Allow-Headers'] = headers

        return resp


@app.route("/add", methods=["POST", "OPTIONS"])
def add():
    if request.method == "OPTIONS":
        return options_response()
    arguments = request.args
    tweet = arguments.get("tweet", "")
    index = arguments.get("index", "")
    if not tweet:
        return Response("Give me content, ya dingus.", status=412)

    if not index:
        response = Tweet.add(tweet)
    else:
        response = Tweet.insert_at_index(tweet, int(index))

    if not response:
        return database_error_response()

    tweet_dict = response.json_object()
    return jsonify(tweet=tweet_dict)


@app.route("/next", methods=["GET"])
def next_tweet():
    tweet = Tweet.top()
    if not tweet:
        return Response("No tweets.", 200)
    return jsonify(tweet=tweet.json_object())


@app.route("/count", methods=["GET"])
def count():
    return jsonify(count=Tweet.count())


@app.route("/all", methods=["GET"])
def all_tweets():
    return jsonify(tweets=Tweet.all_dicts())


@app.route("/remove", methods=["DELETE", "OPTIONS"])
def remove():
    arguments = request.args
    id = arguments.get("id", "")
    if not id:
        return Response("You must provide an id, otherwise I don't know what"
                        " to delete, ya dingus.", 412)
    response = Tweet.remove_with_id(id)
    if not response:
        return database_error_response()
    tweet_dict = response.json_object()
    return jsonify(tweet=tweet_dict)


@app.route("/move", methods=["POST"])
def move():
    arguments = request.args
    from_index = arguments.get("from", "")
    to_index = arguments.get("to", "")
    if not from_index:
        from_index = (Tweet.count() - 1)

    if not to_index:
        to_index = 0

    from_index = int(from_index)
    to_index = int(to_index)

    response = Tweet.move(from_index, to_index)
    if not response:
        return database_error_response()

    tweet_dict = response.json_object()
    return jsonify(tweet=tweet_dict)


@app.after_request
def set_allow_origin(resp):
    """ Set origin for GET, POST, PUT, DELETE requests """

    h = resp.headers

    # Allow crossdomain for other HTTP Verbs
    if request.method != 'OPTIONS' and 'Origin' in request.headers:
        h['Access-Control-Allow-Origin'] = request.headers['Origin']

    return resp


def database_error_response():
    return Response("The database is giving some issues with that query.", 500)


def options_response():
    return Response("Yeah there's some options here, bro.", 200)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test",
                        help="Runs the server in test mode and updates the"
                             " testUsers database.",
                        action="store_true")

    args = parser.parse_args()

    app.run(host="san.csh.rit.edu", port=4200, debug=args.test)
