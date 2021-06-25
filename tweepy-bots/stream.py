import tweepy
import logging
import time
import datetime
from config import create_api_List
import os
import utils
from timeit import default_timer as timer
from limits import limits
import random
import multiprocessing as mp

f_name_following = os.path.dirname(os.path.realpath(__file__)) + os.sep + 'newfollowings.txt'
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
my_limits = limits()
followList= []
# == OAuth Authentication ==
api_List = create_api_List()
api=api_List[0]


class MyStreamListener(tweepy.StreamListener):

    def __init__(self, api, nr_tweets=0, latest_tweet_id=1407144449940021250,
                 file_name=os.path.dirname(os.path.realpath(__file__)) + os.sep + "streamed_tweets.txt",
                 follow_counter=0
                 ):
        self.api = api
        self.me = api.me()
        self.nr_tweets = nr_tweets
        self.latest_tweet_id = latest_tweet_id
        self.file_name = file_name
        self.follow_counter = follow_counter
        self.start_time = timer()
        self.last_tweet_time = timer()

        self.wait_minutes = 15

        logger.info(os.path.dirname(os.path.realpath(__file__)))

    def set_tweet_id(self, tweet_id):
        self.latest_tweet_id = tweet_id

    def reset_limit_counters(self):
        elapsed_time = timer() - self.start_time # Elapse time in seconds
        if elapsed_time > 86400:  # 86400 seconds = 24 hrs
            logger.info("Resetting limit counters.")
            self.follow_counter = 0

    def follow_limit_reached(self):
        elapsed_time = timer() - self.start_time # Elapse time in seconds
        logger.info(f"Total users followed = {self.follow_counter}")
        if  elapsed_time < 72000 and self.follow_counter > 300:  # 72000 seconds = 20 hrs
            return True
        return False

    def on_status(self, tweet):
        if utils.is_Invalid_tweet(tweet, self.latest_tweet_id, self.me.id, self.file_name):
            return
        try:    
            #Limit
            if my_limits.tweetlimit():

                tweet.retweet()
                self.last_tweet_time = datetime.datetime.now()
                logger.info(f"Tweet Retweeted by {api.get_user(self.me.id).screen_name}")
                for i in range(1,len(api_List)):
                    api_List[i].retweet(tweet.id)
                    logger.info(f"Tweet Retweeted by {api.get_user(api_List[i].me().id).screen_name}")
                my_limits.update_today_tweet()
                tweet_number = utils.increment(self.nr_tweets)
                logger.info(tweet.id)
                utils.write_to_file(self.file_name, tweet.text)
                self.wait_minutes = random.randint(6,10)
                logger.info(
                    f"{datetime.datetime.now()}  Tweet \n {tweet_number}: "
                    f"{tweet.text}")
            elif my_limits.likelimit():
                logger.info("Tweet liked")
                tweet.favorite()
                my_limits.update_today_like()

            if  my_limits.followlimit() :
                if (not tweet.user.following) and tweet.user.followers_count < 500:
                    logger.info(f'Follow user {tweet.user.name.encode("utf-8")}')
                    tweet.user.follow()
                    for i in range(1,len(api_List)):
                        frendship= api_List[i].lookup_friendships(user_ids = [tweet.user.id])
                        isfr = frendship[0].is_following
                        if (not isfr) and (tweet.user.followers_count < 150):
                            api_List[i].create_friendship(tweet.user.id)
                    utils.write_to_followerfile(f_name_following,tweet.user.screen_name)
                    logger.info(f'Write on newfollowings file user {tweet.user.name.encode("utf-8")}')
                    my_limits.update_today_follow()
                    logger.info(f'Update Follow limit ')

                if utils.is_retweeted_tweet(tweet) and (not tweet.retweeted_status.user.following) and tweet.retweeted_status.user.followers_count < 150:
                    tweet.retweeted_status.user.follow()
                    logger.info(f'Followed user {tweet.retweeted_status.user.name.encode("utf-8")}')
                    
                    for i in range(1,len(api_List)):
                        frendship= api_List[i].lookup_friendships(user_ids = [tweet.user.id])
                        isfr = frendship[0].is_following
                        if (not isfr) and tweet.retweeted_status.user.id < 150:
                            api_List[i].create_friendship(tweet.retweeted_status.user.id)
                    
                    utils.write_to_followerfile(f_name_following,tweet.retweeted_status.user.screen_name)
                    logger.info(f'Write on newfollowings file user {tweet.user.name.encode("utf-8")}')
                    self.follow_counter = self.follow_counter + 1
                    my_limits.update_today_follow()
                    logger.info(f'Update Follow limit ')

            self.reset_limit_counters()
            self.set_tweet_id(tweet.id)
            
            timediff = int((datetime.datetime.now() - self.last_tweet_time).total_seconds()/60)
            logger.info(f"Time since last tweet = {timediff}")

            logger.info(f"Waiting for {self.wait_minutes-timediff} minutes ...")
            if timediff < self.wait_minutes:
                time.sleep((self.wait_minutes * 60) - timediff)
        except tweepy.TweepError as e:
            logger.error(e.reason)
        except UnicodeEncodeError as e:
            logger.error(e.reason)
            pass
        except ConnectionResetError:
            logger.error("Error detected")
            pass

    def on_error(self, status):
        logger.info(f"Error detected {status}")

def main(t_keyword, f_keyword):
    myStreamListener = MyStreamListener(api)
    myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
    myStream.filter(track=t_keyword, follow=f_keyword, languages=["en", "am"], is_async=False)
    
if __name__ == "__main__":
    string_pattern_to_track = ["EthiopianLivesMatter", "ItsMyDam", "ItsOurDam", "FillTheDam", "EthiopiaPrevails", "StandWithEthiopia",
                               "EthioEritreaPrevail", "SupportEthiopia", "UNSCsupportEthiopia", "UnityForEthiopia", "GleanEthiopia", "GetEthiopianFactsRight",
                               "TplfLies", "FakeAxumMassacre", "DeliverTheAid", "TPLFisaTerroristGroup",
                               "TPLFisTheCause", "TPLFCrimes", "TPLFcrimes", "MaiKadraMassacre", "AxumFiction",
                               "TPLF_Junta", "DisarmTPLF", "StopScapegoatingEritrea",
                               "RisingEthiopia", "TPLFisDEAD", "EthiopiaPrevails", "EritreaPrevails"] # EthiopianLivesMatter AbiyMustLead

    followList = ['neaminzeleke','gleanethiopian','dejene_2011','unityforethio','ETHinSweden','kassahungedlu',
                'BisratLKabeta','sofanit_t','BilleneSeyoum','AbiyAhmedAli','BlenDiriba','LanderMiddle',
                'KelikoSmart',"Alaroosi871","jeffpropulsion","engineerdagi","NicolaADeMarco","mfaethiopia",
                "NEBEthiopia","Betty_Moges", "_HenokTeferra", "EthioAmbUK", "ALEMAYEHUTEGENU", "seleshi_b_a", 
                "fitsumaregaa","NafyadWakjira", "BekeleWoyecha", "AlMariam1", "GetachewDejene4"]

    followers_to_track = utils.get_influencer_ID(api,followList)
    main(string_pattern_to_track, followers_to_track)