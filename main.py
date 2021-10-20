# -*- coding: utf-8 -*-
import sqlite3
import time
import tweepy
import datetime
import random
from telegram.ext import Updater
from telegram import ParseMode

con = sqlite3.connect('tweet_ids.sqlite3')
cur = con.cursor()

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)



def check_uniqe(id):
    cur.execute("select Count(*) from tweets where id='{0}'".format(id))
    ch = cur.fetchone()[0]
    if ch == 0:
        cur.execute("insert into tweets values ({0})".format(id))
        con.commit()
        return True
    if ch !=0:
        print("tweet exists")
        return False ## damn

updater = Updater("TOKEN")

date = "2018-1-1"

q = "#batman OR #superman OR #catwoman -filter:retweets"

while True:
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    try:
        for tweet in tweepy.Cursor(api.search, q=q,
                                   count=400,
                                   lang="fa OR en",
                                   since=date,
                                   tweet_mode='extended', ).items():
            if check_uniqe(tweet.id_str):
                user = ">> [{0}](https://twitter.com/{0}) <<".format(tweet.user.screen_name)
                if len(tweet.full_text)>71:
                    updater.bot.send_message(chat_id="@twitterdataminer", text=(tweet.full_text).encode('utf-8')+("\n" + user +"\n_"+str(tweet.created_at)+"_")+("\n"+"@twitterdataminer"),
                                                 parse_mode=ParseMode.MARKDOWN)
                else:
                     updater.bot.send_message(chat_id="", text="#short tweet: " + tweet.id_str+"\n"+str(datetime.datetime.time(datetime.datetime.now())))
            else:
                 updater.bot.send_message(chat_id="", text="#repeated tweet id: " + tweet.id_str+"\n"+str(datetime.datetime.time(datetime.datetime.now())))
            tm = random.randint(1, 1200)
            print(tm)
            time.sleep(tm)

    except Exception as e:
        updater.bot.send_message(chat_id="your chat id", text="#Error:\n"+str(e), parse_mode=ParseMode.MARKDOWN)
        print(e)
        pass
