# k_y_tsa_sem5_project_env save with this directory name
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)



# twitter authentication
consumer_key = 'wPB1Rsclt7YtKcPKFjWdbyeRN'
consumer_secret = 'tsm67CihfQ65FMNqGNVkYmODLf4JlKW0LptnnzsRKtYmqZzoAd'
access_token = '1096098583214993408-s3Mz8xPp8FMKDS3LVGrjTPYusx996V'
access_token_secret = '8goJjN6EbMDr2kagUcq4cv0f6gBd2fF1hSjtynyXqDhJJ'

try:
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
except:
    print("Error: Authentication Failed")

##############################


# all req functions
def make_text_clean(tweet):

    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())


def get_tweet_sentiment(tweet):

    analysis = TextBlob(make_text_clean(tweet))
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'


def get_tweets(query, count):
    tweets = []

    try:
        fetched_tweets = api.search(q = query, count = count)
        for tweet in fetched_tweets:
            parsed_tweet = {}
            parsed_tweet['text'] = tweet.text
            parsed_tweet['sentiment'] = get_tweet_sentiment(tweet.text)

            if tweet.retweet_count > 0:
                if parsed_tweet not in tweets:
                    tweets.append(parsed_tweet)
            else:
                tweets.append(parsed_tweet)
        return tweets

    except tweepy.TweepError as e:
        print("Error : " + str(e))





@app.route('/', methods=['GET'])  # route to display the first page
@cross_origin()
def homepage():

    return render_template('index.html')


@app.route('/analysis', methods=['GET', 'POST'])
@cross_origin()
def index():

    if request.method == 'POST':

        try:
            tweet_string = request.form['content']
            tweet_count = request.form['count']

            tweets = get_tweets(query=tweet_string, count=tweet_count)
            # tweets is a dictonary

            p_tweets = [tweet['text'] for tweet in tweets if tweet['sentiment'] == 'positive']
            n_tweets = [tweet['text'] for tweet in tweets if tweet['sentiment'] == 'negative']
            neutral_tweets = [tweet['text'] for tweet in tweets if tweet['sentiment'] == 'neutral']

            percent_p_t = 100 * len(p_tweets) / len(tweets)
            percent_n_t = 100 * len(n_tweets) / len(tweets)
            percent_neutral_t = 100 * len(neutral_tweets) / len(tweets)

            print(percent_n_t)
            print(percent_p_t)
            print(percent_neutral_t)
            print(p_tweets)
            print('-'*30)
            print(n_tweets)
            print('-'*30)
            print(neutral_tweets)
            #print("Positive tweets percentage: {} %".format(100 * len(p_tweets) / len(tweets)))
            #all_tweet_data = api.search(q=tweet_string, count=tweet_count)

            #tweet_text = [i.text for i in all_tweet_data]

            #clean_tweets = list(map(make_text_clean, tweet_text))

            if len(p_tweets) < 5:
                pass
            else:
                p_tweets = p_tweets[:5]

            if len(n_tweets) < 5:
                pass
            else:
                n_tweets = n_tweets[:5]

            if len(neutral_tweets) < 5:
                pass
            else:
                neutral_tweets = neutral_tweets[:5]


            return render_template('results.html', tweet_string=tweet_string,
                                   p_neu = percent_neutral_t, p_n = percent_n_t, p_p = percent_p_t,
                                   p_tweets=p_tweets, n_tweets=n_tweets, neutral_tweets=neutral_tweets)

        except:
            pass



if __name__ == '__main__':
    app.run(debug=True)