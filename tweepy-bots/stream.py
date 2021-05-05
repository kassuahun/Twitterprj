import tweepy
import logging
import time
import datetime
from config import create_api_test
import os
import utils
from timeit import default_timer as timer
from limits import limits

f_name_following = os.path.dirname(os.path.realpath(__file__)) + os.sep + 'newfollowings.txt'
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
my_limits = limits()
followList= []
wait_minutes = 0
# == OAuth Authentication ==
api = create_api_test()


class MyStreamListener(tweepy.StreamListener):

    def __init__(self, api, nr_tweets=0, latest_tweet_id=1384927621063004164,
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
        self.wait_minutes = 0

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
                my_limits.update_today_tweet()
                logger.info("Tweet Retweeted")
                tweet_number = utils.increment(self.nr_tweets)
                logger.info(tweet.id)
                utils.write_to_file(self.file_name, tweet.text)
                self.wait_minutes = 7
                logger.info(
                    f"{datetime.datetime.now()} Tweet {tweet_number}: "
                    f"{tweet.text}")
            elif my_limits.likelimit():
                tweet.favorite()
                my_limits.update_today_like()
            
            if  my_limits.followlimit():
                if not tweet.user.following:
                    logger.info(f'Follow user {tweet.user.name.encode("utf-8")}')
                    tweet.user.follow()
                    utils.write_to_followerfile(f_name_following,tweet.user.screen_name)
                    my_limits.update_today_follow()
                if utils.is_retweeted_tweet(tweet):
                    logger.info(f'Follow user {tweet.retweeted_status.user.name.encode("utf-8")}')
                    if not tweet.retweeted_status.user.following:
                        tweet.retweeted_status.user.follow()
                        utils.write_to_followerfile(f_name_following,tweet.retweeted_status.user.screen_name)
                        self.follow_counter = self.follow_counter + 1
                        my_limits.update_today_follow()
            self.reset_limit_counters()
            self.set_tweet_id(tweet.id)
            
            
            logger.info(f" waiting for {self.wait_minutes} minutes ...")
            time.sleep(self.wait_minutes * 60)
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
    myStream.filter(track=t_keyword, languages=["en", "am"], is_async=False)


if __name__ == "__main__":
    string_pattern_to_track = ["AmharaGenocide", "EthiopianLivesMatter", "ItsMyDam", "ItsOurDam", "FillTheDam", "EthiopiaPrevails", "StandWithEthiopia",
                               "EthioEritreaPrevail", "SupportEthiopia", "UNSCsupportEthiopia", "UnityForEthiopia", "GleanEthiopia", "GetEthiopianFactsRight",
                               "TplfLies", "FakeAxumMassacre", "DeliverTheAid", "TPLFisaTerroristGroup",
                               "TPLFisTheCause", "TPLFCrimes", "TPLFcrimes", "MaiKadraMassacre", "AxumFiction",
                               "TPLF_Junta", "DisarmTPLF", "StopScapegoatingEritrea",
                               "RisingEthiopia", "TPLFisDEAD"] # EthiopianLivesMatter AbiyMustLead

    followers_to_track = ["4077439067",  # @neaminzeleke
                          "1357188308242169856",  # @gleanethiopian
                          "276370580",  # @dejene_2011
                          "1345123740603047936"  # @unityforethio
                          ]

    main(string_pattern_to_track, followers_to_track)
