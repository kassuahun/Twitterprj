import tweepy
import time
import sys
from datetime import datetime
from config import  create_api, create_api_List, create_api_test
from limits import limits
import random
import os
import utils
import logging
import atexit

api = create_api()
  
# the ID of the user
id = 1168167671151628290
  
# fetching the user
user = api.get_user(id)

print("USER NAME = ", user.screen_name)
keywords=["Consulate", "consulate", "Embassy", "embassy", "Ambassador"]
potential_deplomats = []
ids=[]


def filewriter(fname, deplomats):
    print("writing deplomats ---------")
    f_name = os.path.dirname(os.path.realpath(__file__)) + os.sep + fname
    with open(fname, 'w') as filetowrite:
        for deplomat in deplomats:
            filetowrite.write(deplomat)
    

for page in tweepy.Cursor(api.followers_ids, screen_name="AbiyAhmedAli").pages():
    ids.extend(page)
    for id in page:
        try:
            user = api.get_user(id)
            if "Ethiopia" in user.description:
                for key in keywords:
                    if key in user.description:
                        potential_deplomats.append(id)
                        potential_deplomats.append([user.screen_name, user.description])
                        print("Deplomat added ", user.screen_name, user.description)
        except tweepy.TweepError as e:
            print(e.reason)
            continue
    time.sleep(60)

print(len(ids)) 

atexit.register(utils.exit_handler,potential_deplomats,"deplomats.txt")


