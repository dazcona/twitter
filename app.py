#!/usr/bin/python

from flask import Flask, render_template, jsonify, request
from flask_bootstrap import Bootstrap
import os
import json
from bson.objectid import ObjectId
from bson.json_util import dumps
import config
from utils import get_api, get_tweets, get_geo_tweets

# APP
app = Flask(__name__)
Bootstrap(app)

# Get API
api, auth = get_api()

# Static path
static_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "static"))

@app.route('/')
def index():
    """ Show Menu """

    values = ['Select one']
    data_values = [ filename.split('.json')[0] for filename in os.listdir('data/') if filename.endswith('.json') ]
    values.extend(data_values)

    return render_template('index.html', values = values)


# Calculate email offsets for fetchig lists of emails from MongoDB
def get_navigation_offsets(offset, increment = config.N_PER_PAGE):

    return {
        'Previous': { 'offset': max(offset - increment, 0) }, # Don't go below 0
        'Next': { 'offset': offset + increment },
    }

@app.route('/tweets/<keyword>')
@app.route('/tweets/<keyword>/')
@app.route('/tweets/<keyword>/<int:offset>')
def tweets(keyword, offset = 0):
    """ Show tweets in a tabulated format """

    tweets = []
    filename = os.path.join('data', keyword + '.json')
    if os.path.isfile(filename):
        with open(filename) as f:
            # Get all
            data = [ json.loads(line) for line in f.readlines() ]
            # Slice tweets
            tweets = data[offset : offset + config.N_PER_PAGE]

    return render_template('tweets.html',
                           tweets = tweets,
                           nav_offsets = get_navigation_offsets(offset),
                           nav_path = "/tweets/{}/".format(keyword))


@app.route('/map/<keyword>')
@app.route('/map/<keyword>/')
def map(keyword):
    """ Show MAP """

    return render_template('map.html', keyword = keyword)


@app.route('/data/<keyword>')
@app.route('/data/<keyword>/')
def get_geo_data(keyword):
    """ Get MAP's data """

    filename = 'data/{}.json'.format(keyword)
    geo_data = dumps(get_geo_tweets(filename))

    return geo_data


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')