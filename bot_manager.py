# -*- coding: utf-8 -*-
import sqlite3
import tweepy
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
con = sqlite3.connect('tweet_ids.sqlite3', check_same_thread=False)
cur = con.cursor()

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

updater = Updater("TOKEN")

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi\nYou can send your opinion or hashtags that might be helpful\nThere is no command, just type and press send.\nPlease be advised, under any circumstances we will not reveal any hashtags or identity of our users.')


def get_last_tweet(user):
    tweet = api.user_timeline(id = user, count = 1)[0]
    return tweet.text
def send_to_me():
    api.send_direct_message("","hello master")

def trends(bot, update):
    update.message.reply_text("Fetching trends...")
    #trends = api.user_timeline(screen_name="trenditter", count=1)
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    #stuff = api.user_timeline(screen_name='trenditter', count=1, include_rts=True)
    send_to_me()
    update.message.reply_text(get_last_tweet(""))

def echo(bot, update):
    try:
        text = update.message.text
        #text = str(text)
        #text = str(text).encode('utf-8')
        updater.bot.send_message(chat_id="",text="#OP\nMessage From @"+update.message.from_user.username+"("+str(update.message.chat.id)+"):"+"\n"+text)
        print("sateg 1")
        update.message.reply_text("Thank you\n Your message has been sent to admin")
    except Exception as e:
        updater.bot.send_message(chat_id="", text="#Error:\n"+str(e))
        print(e)
def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    #dp.add_handler(CommandHandler("trends", trends))
    dp.add_handler(MessageHandler(Filters.text, echo))
    # on noncommand i.e message - echo the message on Telegram
    #dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
#    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
