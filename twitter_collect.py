import time
import json
import tweepy
from tweepy import OAuthHandler
from tweepy import API


import datetime as dt
import pandas as pd
import os
import csv

# Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN = '**'
ACCESS_SECRET = '**'
CONSUMER_KEY = '**'
CONSUMER_SECRET = '**'

# Setup tweepy to authenticate with Twitter credentials:
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

# Create the api to connect to twitter with your creadentials
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def tweet_collection(json):
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
    tweet['favorited'] = json['favorited']
    tweet['retweeted'] = json['retweeted']
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


fields = ['id','created_at','text','user','user_id','user_name','user_location','user_description','user_followers',
         'retweet_count','favorite_count','favorited','retweeted','lang','is_quote_status','place',
         'place_name','place_country','coordinates','coordinates_longitude','coordinates_latitude']


output = open('/home/ubuntu/twitter/tweets_results.csv','a+')  
header = ",".join(fields)
output.write(header + '\n')
with open('/home/ubuntu/twitter/tweet_ids.txt','r') as file:
    for tweet in file:
        try: 
            tweet_dict = tweet_collection(api.get_status(tweet)._json)
            line = ",".join(["\"" + "".join(str(e).splitlines()).replace("\"", "") + "\"" for e in tweet_dict.values()])
            output.write(line + '\n')
            time.sleep(1)
        except Exception as e:
            f = open('/home/ubuntu/twitter/errors.txt','a+')
            f.write(str(time.ctime()) +':' + str(e) + ' - ' + tweet)
            time.sleep(1)
            f.close()
output.close()