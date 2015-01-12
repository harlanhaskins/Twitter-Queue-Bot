#!/usr/bin/env python

from flask import Flask, Response
from flask import request, make_response, request, current_app
from flask.json import jsonify
from functools import update_wrapper
from datetime import timedelta
import HTMLParser
import argparse
from dbapi import Tweet

app = Flask(__name__)
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

    app.run(host='localhost', port=4200, debug=args.test)
