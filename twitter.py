import sys

arg = sys.argv[1]

import json

data = json.load(open('twitter-api-keys.json'))

from tweepy import OAuthHandler
from tweepy import API

auth = OAuthHandler(data['consumer_key'], 
                    data['consumer_secret'])

auth.set_access_token(data['access_token'],
                      data['access_token_secret'])

api = API(auth)

tweets = api.search(arg)

from textblob import TextBlob

for tweet in tweets:
    # Tweet's Text
    print('Tweet: {}'.format(tweet.text))
    # Sentiment Analysis on Tweet
    analysis = TextBlob(tweet.text)
    print('Polarity: {}'.format(analysis.polarity))
    print('Subjectivity: {}'.format(analysis.subjectivity))
    print()
