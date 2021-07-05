#!/usr/bin/env python
# bots/followfollowers.py

import tweepy
import logging
from config import create_api_List
import os
import time
import utils

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

api_list= create_api_List()

def followback(api_list):
    for api in api_list:
        follow_followers(api)



def follow_followers(api):
    logger.info("Retrieving and following followers")
    for follower in tweepy.Cursor(api.followers).items():
        if not follower.following:
            logger.info(f"Following {follower.name}")
            follower.follow()

def unfollow(api):
    SCREEN_NAME = api.me().screen_name
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
    uname = api.me().screen_name
    
    for f in notfollowing:
        #api.destroy_friendship(f)
        #name = api.get_user(f).screen_name
        #logger.info('Unfollow ', api.get_user(f).screen_name)
        count += 1
        # if count%10 ==0:
        #     #sleep(60*60)
    print("dfsdfsdg ")


def main():
    api = create_api()
    # while True:
    #     follow_followers(api)
    #     logger.info("Waiting...")
    #     time.sleep(60)
    unfollow(api)

if __name__ == "__main__":
    main()