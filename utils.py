import sys
import config
import json
from tweepy import OAuthHandler
from tweepy import API
from textblob import TextBlob

def get_api():
    """ Twitter API """

    auth = OAuthHandler(config.consumer_key, 
                        config.consumer_secret)

    auth.set_access_token(config.access_token,
                        config.access_secret)

    api = API(auth)

    return api, auth


def get_tweets(api, keyword):
    """ Get tweets """

    tweets = api.search(keyword)

    # https://gist.github.com/dev-techmoe/ef676cdd03ac47ac503e856282077bf2
    tweets = [tweet._json for tweet in tweets]

    return tweets


def get_geo_tweets(filename):
    """ Get tweets with coordinates """

    with open(filename) as f:
        geo_data = {
            "type": "FeatureCollection",
            "features": []
        }
        for line in f:
            tweet = json.loads(line)
            if tweet['coordinates']:
                geo_json_feature = {
                    "type": "Feature",
                    "geometry": tweet['coordinates'],
                    "properties": {
                        "text": tweet['text'],
                        "created_at": tweet['created_at']
                    }
                }
                geo_data['features'].append(geo_json_feature)

    return geo_data


if __name__ == '__main__':

    # Check number of arguments
    if len(sys.argv) < 1:
        print('Error: No argument given')
        print('Usage: $ python utils.py <keyword>')
        sys.exit(1)
    # Get argument
    arg = sys.argv[1]
    # Get API
    api, auth = get_api()
    # Get tweets
    tweets = get_tweets(api, arg)
    # Print tweets
    for tweet in tweets:
        # Tweet's Text
        print('Tweet: {}'.format(tweet['text']))
        # Sentiment Analysis on Tweet
        analysis = TextBlob(tweet['text'])
        print('Polarity: {}'.format(analysis.polarity))
        print('Subjectivity: {}'.format(analysis.subjectivity))
        print()
