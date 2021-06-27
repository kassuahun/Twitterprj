# bots/config.py
import tweepy
import logging
import sys
from   os import environ
import os
import utils
import csv
import keys

logger = logging.getLogger()


def create_api():
    Home = environ['HOME']
    CONSUMER_KEY = environ['CONSUMER_KEY']
    CONSUMER_SECRET = environ['CONSUMER_SECRET']
    ACCESS_KEY = environ['ACCESS_KEY']
    ACCESS_SECRET = environ['ACCESS_SECRET']
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True,
        wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api

def create_api_lical( consumer_name,
                consumer_key, 
                consumer_secret, 
                access_token,
                access_token_secret ):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True,
        wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info(f"API created for {consumer_name}" )
    return api

def create_api_test():
    auth = tweepy.OAuthHandler(keys.consumer_key, keys.consumer_secret)
    auth.set_access_token(keys.access_token, keys.access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True,
        wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
        return None
    logger.info("API created")
    return api

def create_api_List():
    f_name_read = os.path.dirname(os.path.realpath(__file__)) + os.sep + 'API_Keys.csv'
    with open(f_name_read) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 1
        api_list = []
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                pass
            else:
                consumer_name= row[0]
                consumer_key = row[1]
                consumer_secret = row[2]
                access_token = row[3]
                access_token_secret = row[4]
                line_count += 1
                newapi = create_api_lical( consumer_name,
                    consumer_key, 
                    consumer_secret, 
                    access_token,
                    access_token_secret )
                if newapi != None:
                    api_list.append(newapi)
                    print(f'Processed {line_count} lines.')

    return api_list

# def create_api_List(key_list):
    
#         for key in key_list:
#             if line_count == 0:
#                 line_count += 1
#                 pass
#             else:
#                 consumer_name= row[0]
#                 consumer_key = row[1]
#                 consumer_secret = row[2]
#                 access_token = row[3]
#                 access_token_secret = row[4]
#                 line_count += 1
#                 newapi = create_api( consumer_name,
#                     consumer_key, 
#                     consumer_secret, 
#                     access_token,
#                     access_token_secret )
#                 if newapi != None:
#                     api_list.append(newapi)
#                     print(f'Processed {line_count} lines.')

#     return api_list





# api_list = create_api_List()
# lst = ["Alaroosi871","jeffpropulsion","engineerdagi","NicolaADeMarco","mfaethiopia","NEBEthiopia","Betty_Moges"]
# print(utils.get_influencer_ID(api_list[0], lst))
# # api = create_api()