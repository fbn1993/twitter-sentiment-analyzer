from secrets import Oauth_Secrets
import tweepy
from django.http import HttpResponse
from textblob import TextBlob
import pandas as pd
import warnings
import seaborn as sns
import re

def clean_text(txt):
    txt = re.sub(r'@[A-Za-z0-9]+', '', txt) #remove @mentions
    txt = re.sub(r'#', '', txt) # remove the # symbol
    txt = re.sub(r'RT[\s]', '', txt) #remove RT
    txt = re.sub(r'((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*', '', txt) #remove the urls
    return txt

def get_tweets(input_hashtag):
    secrets = Oauth_Secrets()       #secrets imported from secrets.py
    auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
    auth.set_access_token(secrets.access_token, secrets.access_token_secret)

    api = tweepy.API(auth)
    tweets = tweepy.Cursor(api.search,
                   q=input_hashtag,
                   lang="en",
                   since='2018-08-25').items(1000)         
    return tweets

def primary(input_hashtag):
    
    Tweets = get_tweets(input_hashtag)
    neg = 0.0
    pos = 0.0
    neg_count = 0
    neutral_count = 0
    pos_count = 0
    for tweet in Tweets:
        blob = TextBlob(clean_text(tweet.text))
        print(clean_text(tweet.text))
        if blob.sentiment.polarity < 0:         #Negative
            neg += blob.sentiment.polarity
            neg_count += 1
        elif blob.sentiment.polarity == 0:      #Neutral
            neutral_count += 1
        else:                                   #Positive
            pos += blob.sentiment.polarity
            pos_count += 1
    
    return [['Sentiment', 'no. of tweets'],['Positive',pos_count]
            ,['Neutral',neutral_count],['Negative',neg_count]]

def secondary(input_hashtag):
    warnings.filterwarnings("ignore")
    sns.set(font_scale=1.5)
    sns.set_style("whitegrid")         
    
    tweets = get_tweets(input_hashtag)
    cleaned_tweets = [clean_text(tweet.text) for tweet in tweets]
    
    # Create textblob objects of the tweets
    sentiment_objects = [TextBlob(tweet) for tweet in cleaned_tweets]
    sentiment_objects[0].polarity, sentiment_objects[0]

    # Create list of polarity values and tweet text
    sentiment_values = [[tweet.sentiment.polarity, str(tweet)] for tweet in sentiment_objects]

    # Create dataframe containing the polarity value and tweet text using pandas library
    sentiment_df = pd.DataFrame(sentiment_values, columns=["polarity", "tweet"])

    # Remove polarity values equal to zero
    sentiment_df = sentiment_df[sentiment_df.polarity != 0]
    return sentiment_df
    