import tweepy
import time
import sys
from datetime import datetime
from config import create_api_List
from limits import limits
import random
import os
import utils
import logging
import atexit

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# create a text file with each line containing a sentence you want to tweet
#To run the bot do the following from command line:
#python tweetlinesfromfile.py

# == OAuth Authentication ==
# api = create_api()
# api = create_api_list()

apilist = create_api_List()

f_name_read = os.path.dirname(os.path.realpath(__file__)) + os.sep + 'campaign_tweets.txt'
f_name_write = os.path.dirname(os.path.realpath(__file__)) + os.sep + 'streamed_tweets.txt'
my_Limits = limits()
tweet_no = 0
f = utils.read_from_file(f_name_read)
interval = 15
internal_interval = 0.5
tweet_bunch = 10
i = 1
toremove =[]

def tweet_forall(txt):
    for api in apilist:
        try:
            api.update_status(txt)
            print(api.me().screen_name, "tweeted [", txt, "]")
        except tweepy.TweepError as e:
            logger.error(e.reason)
            if e.api_code == 187 : # 'Status is a duplicate. '
                toremove.append(line)
                continue
            elif e.api_code == 261:
                apilist.remove(api)
                continue
            elif e.api_code == 186: #[{'code': 186, 'message': 'Tweet needs to be a bit shorter.'}]
                toremove.append(line)
                continue
            
        except UnicodeEncodeError as e:
            logger.error(e.reason)
            toremove.append(line)
            continue
        except ConnectionResetError:
            logger.error("Error detected")
            pass


for line in f:
    if my_Limits.tweetlimit():
        if utils.tweet_exists(f_name_write, line):
            continue
        
        logger.info(f"Tweeting: {line}")
        tweet_forall(line)
        toremove.append(line)
        my_Limits.update_today_tweet()
        logger.info(f"Writing tweet {utils.increment(tweet_no)} to file")
        tweet_no = tweet_no + 1
        utils.write_to_file(f_name_write, line)
        if i == tweet_bunch:
            interval = random.randint(20,30)
            now = datetime.now()
            logger.info(f" waiting for {interval} minutes ... Staring from {now.hour}:{now.minute}:{now.second}")
            time.sleep(interval*60)
            i = 1
        else:
            internal_interval = random.randint(35,120)
            logger.info(f" waiting for {internal_interval} seconds ...")
            time.sleep(internal_interval)
        i += 1
        
    else: 
        logger.info("The dayly limit reached")
        break
print("The list is Done" )

atexit.register(utils.exit_handler,[t for t in f if(t not in toremove)],f_name_read)
