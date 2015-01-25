#!/usr/bin/env python

from flask import Flask, Response, request
from flask.json import jsonify
from flask_cors import CORS
from functools import update_wrapper
from datetime import timedelta
import HTMLParser
import argparse
from dbapi import Tweet

app = Flask(__name__)
cors = CORS(app)
h = HTMLParser.HTMLParser()

base_url = "/api"

def body_from_request(request):
    if request.method == "GET" or request.method == "DELETE":
        body = request.args
    else:
        body = request.get_json(force=True, silent=True)
        if body is None:
            body = request.form
    return body

@app.before_request
def parse_body():
    request.body = body_from_request(request)

@app.route(base_url + "/tweets/next", methods=["GET"])
def next_tweet():
    tweet = Tweet.top()
    if not tweet:
        return Response("No tweets.", 200)
    return jsonify(tweet=tweet.json_object())


@app.route(base_url + "/tweets", methods=["GET", "POST"])
def all_tweets():
    if request.method == "GET":
        return jsonify(tweets=Tweet.all_dicts())
    elif request.method == "POST":
        tweet = request.body.get("tweet", "")
        index = request.body.get("index", "")
        if not tweet:
            return Response("Give me content, ya dingus.", status=412)

        if not index:
            response = Tweet.add(h.unescape(tweet))
        else:
            if not index.isdigit():
                return Response("Index must be a number.", status=412)
            response = Tweet.insert_at_index(tweet, int(index))

        if not response:
            return database_error_response()

        tweet_dict = response.json_object()
        return jsonify(tweet=tweet_dict)


@app.route(base_url + "/tweets/count", methods=["GET"])
def tweet_count():
    return jsonify(count=Tweet.count())


@app.route(base_url + "/tweets/<int:id>", methods=["GET", "DELETE"])
def tweet_with_id(id):
    tweet = Tweet.for_id(id)
    if request.method == "GET":
        return jsonify(tweet=tweet.json_object())
    elif request.method == "DELETE":
        response = Tweet.remove_with_id(id)
        if not response:
            return database_error_response()
        tweet_dict = response.json_object()
        return jsonify(tweet=tweet_dict)


@app.route(base_url + "/tweets/move", methods=["POST"])
def move():
    from_index = request.body.get("from", "")
    to_index = request.body.get("to", "")
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


def database_error_response():
    return Response("The database is giving some issues with that query.", 500)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test",
                        help="Runs the server in test mode and updates the"
                             " testUsers database.",
                        action="store_true")

    args = parser.parse_args()

    app.run(host='localhost', port=4200, debug=args.test)
