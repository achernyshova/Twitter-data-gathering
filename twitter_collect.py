import time
import json
import tweepy
from tweepy import OAuthHandler
from tweepy import API

import datetime as dt
import pandas as pd
import os
import csv

# Define the path
ROOT_DIR = '/home/ubuntu/twitter/'


# Variables that contains the user credentials to access Twitter API
ACCESS_TOKEN = '***'
ACCESS_SECRET = '***'
CONSUMER_KEY = '***'
CONSUMER_SECRET = '***'

# Setup tweepy to authenticate with Twitter credentials:
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

# Create the api to connect to twitter with your creadentials
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

#function accepts list of tweets ids and returns all tweets information as dictionary
def tweet_collection(tweet_id):
    json = api.get_status(tweet_id)._json
    tweet = {}
    tweet['id'] = json['id']
    tweet['created_at'] = json['created_at']
    tweet['text'] = json['text']
    #information about user
    tweet['user'] = json['user']
    tweet['user_id'] = json['user']['id']
    tweet['user_name'] = json['user']['name']
    tweet['user_location'] = json['user']['location']
    tweet['user_description'] = json['user']['description']
    tweet['user_followers'] = json['user']['followers_count']
    #tweet info
    tweet['retweet_count'] = json['retweet_count']
    tweet['favorite_count'] = json['favorite_count']
    tweet['lang'] = json['lang']
    tweet['is_quote_status'] = json['is_quote_status']
    #about location if user uses geotags
    if json['place']!=None:
        tweet['place'] = json['place']
        tweet['place_name'] = json['place']['full_name']
        tweet['place_country'] = json['place']['country_code']
        tweet['coordinates'] = json['place']['bounding_box']['coordinates'][0][0]
        tweet['coordinates_longitude'] = json['place']['bounding_box']['coordinates'][0][0][0]
        tweet['coordinates_latitude'] = json['place']['bounding_box']['coordinates'][0][0][1]
    else:
        tweet['place']= None
        tweet['place_name'] = None
        tweet['place_country'] = None
        tweet['coordinates'] = None
        tweet['coordinates_longitude'] = None
        tweet['coordinates_latitude'] = None
    return tweet

#function accepts list of key words as an argument and returns new tweets with geo location and returns all tweets information as list of dictionaries
def geo_tweets_collection(disaster_list):
    result = []
    for word in disaster_list:
        for tweet in tweepy.Cursor(api.search, q=word, lang='en').items(100):
            json = tweet._json
            if json['place']!=None:
                tweet = {}
                tweet['id'] = json['id']
                tweet['created_at'] = json['created_at']
                tweet['text'] = json['text']
                #information about user
                tweet['user'] = json['user']
                tweet['user_id'] = json['user']['id']
                tweet['user_name'] = json['user']['name']
                tweet['user_location'] = json['user']['location']
                tweet['user_description'] = json['user']['description']
                tweet['user_followers'] = json['user']['followers_count']
                #tweet info
                tweet['retweet_count'] = json['retweet_count']
                tweet['favorite_count'] = json['favorite_count']
                tweet['lang'] = json['lang']
                tweet['is_quote_status'] = json['is_quote_status']
                #about location if user uses geotags
                tweet['place'] = json['place']
                tweet['place_name'] = json['place']['full_name']
                tweet['place_country'] = json['place']['country_code']
                tweet['coordinates'] = json['place']['bounding_box']['coordinates'][0][0]
                tweet['coordinates_longitude'] = json['place']['bounding_box']['coordinates'][0][0][0]
                tweet['coordinates_latitude'] = json['place']['bounding_box']['coordinates'][0][0][1]
                result.append(tweet)
            else:
                continue
            time.sleep(3)
    return result

output = open(ROOT_DIR + 'tweets_results.csv','a+') #create and open final file with results
header = ",".join(list(tweet_collection(open(ROOT_DIR + 'tweet_ids.txt').readline()).keys())) #create a header
output.write(header + '\n') #add header there
with open(ROOT_DIR + 'tweet_ids.txt','r') as file: #loop through list of ids
    for tweet in file:
        try:
            tweet_dict = tweet_collection(tweet) #get data for selected tweet
            line = ",".join(["\"" + "".join(str(e).splitlines()).replace("\"", "") + "\"" for e in tweet_dict.values()])
            output.write(line + '\n') #write it down
        except Exception as e:
            f = open(ROOT_DIR + 'errors.txt','a+') #save errors to errors.txt
            f.write(str(time.ctime()) +':' + str(e) + tweet)
            f.close()
    time.sleep(1) #add 1 sec to delay request in order to follow API rules (up to 900 requests per 15 minutes)
output.close()
