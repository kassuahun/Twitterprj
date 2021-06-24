import datetime
import logging
import os
import tweepy
import time
import sys
from datetime import datetime
from limits import limits
import logging
import atexit

logger = logging.getLogger()


def increment(arg):
    return arg + 1

def get_influencer_ID(api, account_names):
    userIDlist = []
    for acc_name in account_names:
        try:
            user = api.get_user(acc_name)
            userIDlist.append(str(user.id))
        except Exception as e:
            print(e.reason)
            continue
    return userIDlist  


def write_to_file(file_name, tweet):
    logger.info(f"Writing a tweet to {file_name}")
    f = open(file_name, "a")
    f.write(f"{datetime.now()} {tweet}")
    f.write('\n')
    f.close()

def write_to_followerfile(file_name, name):
    logger.info(f"Writing a tweet to {file_name}")
    f = open(file_name, "a")
    f.write(name)
    f.write('\n')
    f.close()

def read_from_file(file_name):
    logger.info(f"Reading from {file_name}")
    file = open(file_name, encoding="utf-8")
    f = file.readlines()
    file.close()
    return f


def get_tweet_text(tweet):
    logger.info('Get the tweet text')
    if ': ' in tweet:
        tweet = tweet.split(': ', 1)[1]
    return tweet

def unfollow(api):
    SCREEN_NAME = 'Ethio_Norwagian'
    f_name_read = os.path.dirname(os.path.realpath(__file__)) + os.sep + 'newfollowings.txt'
    friendhunted = utils.read_from_file(f_name_read)
    friendhunted_id =[]
    followers = api.followers_ids(SCREEN_NAME)
    friends = api.friends_ids(SCREEN_NAME)
    notfollowing = [x for x in friends if x not in followers] 

    for friend in friendhunted:
        try:
            friendhunted_id.append(api.get_user(screen_name = friend.rstrip("\n")))
        except tweepy.TweepError as e:
            pass
    
    notfollowing = [x for x in friendhunted_id if x not in followers]
    count = 1
    for f in notfollowing:
        #api.destroy_friendship(f)
        name = api.get_user(f).screen_name
        logger.info('Unfollow ', api.get_user(f).screen_name)
        count += 1
        if count%10 ==0:
            sleep(60*60)
    print ("dfsdfsdg ")

# tweet = "RT @NeaminZeleke: Egypt snubbing the African Union and insisting on involving the EU &amp;
# USA in talks with #Ethiopia about the #GERD is as su…"
def tweet_exists(file_name, tweet):
    logger.info('Checking if tweet already handled')
    with open(file_name) as f:
        if get_tweet_text(tweet)[:70] in f.read():
            logger.info("Tweet already exists")
            return True
    return False

def is_Invalid_tweet(tweet, latest_tweet_id, me_id, file_name):
    logger.info('Checking if tweet is valid ')
    if tweet_exists(file_name, tweet.text) or\
            tweet.user.id == me_id or\
            tweet.in_reply_to_status_id is not None or\
            "quoted_status" in str(tweet) or\
            "AbiyToICC" in str(tweet) or\
            "IrobMassacre" in str(tweet) or\
            "#tembienMassacre #dengelatMassacre #KunamaStarvation " in str(tweet) or\
            "TigrayGenocide" in str(tweet) or\
            "TigrayCantWait" in str(tweet) or\
            "WarOnTigray" in str(tweet) or\
            "StandWithTigray" in str(tweet) or\
            "AbiyToICC" in str(tweet) or\
            tweet.id < latest_tweet_id:
            #tweet.retweeted:
        logger.info('The tweet is not valid')
        return True
    logger.info('The tweet is valid')
    return False


def is_retweeted_tweet(tweet):
    logger.info("Check if tweet is a retweet")
    if 'retweeted_status' in str(tweet):
        logger.info('This is a retweet tweet')
        return True
    logger.info('This is not a retweet tweet')
    return False

def exit_handler(lst, fname):
    logger.info('exit_handler: The application is ending: writing the remaining list!')
    with open(fname, 'w') as filetowrite:
        for itm in lst:
            filetowrite.write(itm)