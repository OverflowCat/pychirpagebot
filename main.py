import telegram
import graph
import re
import os
import duty
from datetime import datetime
print("App started")
from dotenv import load_dotenv
load_dotenv()

import requests
def log(_path, _user, _type, _query):
    r = requests.post(
        os.environ["CHSHDB"],
        json={
            "data": {
                "path": _path,
                "user": _user,
                "type": _type,
                "query": _query,
                "time": int(datetime.utcnow().timestamp())
            }
        })
    return r.json()

cmdre = re.compile(r'^\/[a-z]+(@[a-zA-Z0-9_]+bot)? ?')


def cutcmd(msg_txt):
    return re.sub(cmdre, "", msg_txt)

myfllwings = []

bot = telegram.Bot(token=os.environ["chirpage"])
from telegram.ext import Updater
updater = Updater(os.environ["chirpage"], use_context=True)
dispatcher = updater.dispatcher
import logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
from telegram.ext.dispatcher import run_async


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=
        "Please send a Twitter user's screen name (like `@twitter`) to me then I will fetch the account's latest tweets and archive them as a Telegraph.",
        parse_mode=telegram.ParseMode.MARKDOWN)


@run_async
def arc_favs(update, ctx):
    text = update.message.text
    text = cutcmd(text)
    graf = graph.fetchFavs(text)
    log(graf, text, 'favs', text + ':favs')
    ctx.bot.send_message(
        chat_id=update.effective_chat.id,
        text="*" + text + "*\n" + graf["url"],
        parse_mode=telegram.ParseMode.MARKDOWN)
    print(graf)


@run_async
def arc_user(update, ctx):
    text = update.message.text
    text = cutcmd(text)
    graf = graph.fetchUser(text)
    log(graf, text, 'user', text + ':timeline')
    ctx.bot.send_message(
        chat_id=update.effective_chat.id,
        text="*" + text + "*\n" + graf["url"],
        parse_mode=telegram.ParseMode.MARKDOWN)
    print(graf)


@run_async
def dutymachine(update, ctx):
    text = update.message.text
    text = cutcmd(text)
    resp = duty.dm(text)
    log('DUTY', text, 'duty', resp)
    ctx.bot.send_message(
        chat_id=update.effective_chat.id,
        text="`" + text + "`\n" + resp,
        parse_mode=telegram.ParseMode.MARKDOWN)


@run_async
def ping(update, ctx):
    ctx.bot.send_message(chat_id=update.effective_chat.id, text="Pong!")


@run_async
def userduty(update, ctx):
    text = update.message.text
    text = cutcmd(text)
    graf = graph.fetchUser(text)
    resp = duty.dm(graf)
    log(graf, text, 'userduty', resp)
    ctx.bot.send_message(
        chat_id=update.effective_chat.id,
        text="`" + text + "`\n" + resp,
        parse_mode=telegram.ParseMode.MARKDOWN)

@run_async
def followings(update, ctx):
  text = update.message.text
  text = cutcmd(text)
  fllwings = []
  tweepy = graph.getTweepy()
  api = graph.getApi()
  try:
    for user in tweepy.Cursor(api.friends, screen_name="2Lmwx", count=4999).items():
      print(user.screen_name)
      fllwings.append(user.screen_name)
  except:
    pass
  else:
    pass
  global myfllwings
  myfllwings = fllwings
  resu = graph.p(" ".join(myfllwings), "My Followings")
  print(resu)
  ctx.bot.send_message(chat_id=update.effective_chat.id,
        text=resu["url"])
  
from telegram.ext import MessageHandler, CommandHandler, Filters
start_handler = CommandHandler('start', start)
favs_handler = CommandHandler('favs', arc_favs)
user_handler = CommandHandler('user', arc_user)
duty_handler = CommandHandler('duty', dutymachine)
userduty_handler = CommandHandler('userduty', userduty)
followings_handler = CommandHandler("followings", followings)
ping_handler = CommandHandler('ping', ping)
message_handler = MessageHandler(Filters.all, arc_user)
dispatcher.add_handler(start_handler)
# dispatcher.add_handler(message_handler)
dispatcher.add_handler(favs_handler)
dispatcher.add_handler(user_handler)
dispatcher.add_handler(duty_handler)
dispatcher.add_handler(followings_handler)
dispatcher.add_handler(ping_handler)
dispatcher.add_handler(userduty_handler)
# 拉清单
updater.start_polling()