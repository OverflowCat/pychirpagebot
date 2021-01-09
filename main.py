from dotenv import load_dotenv
load_dotenv()  # graph.py requires env

import telegram
import graph
import re
import os
import duty
import reg
import db
import json
from telegram.ext.defaults import Defaults
from telegram import ParseMode
from datetime import datetime
print("App started")

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
	seps = msg_txt.split(" ")
	seps.pop(0)
	return ' '.join(seps)
	#return re.sub(cmdre, "", msg_txt)


myfllwings = []

defaults = Defaults(parse_mode=ParseMode.HTML, run_async=True)
bot = telegram.Bot(token=os.environ["chirpage"], defaults=defaults)
from telegram.ext import Updater
updater = Updater(os.environ["chirpage"], use_context=True)
dispatcher = updater.dispatcher

import logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
from telegram.ext.dispatcher import run_async


@run_async
def start(update, context):
	context.bot.send_message(
	    chat_id=update.effective_chat.id,
	    text=
	    "Please send me the link of any tweet directly or using the /user command plus the Twitter user's screen name (like `/user elonmusk`) to me then I will fetch the account's latest tweets and archive them as a Telegraph.\nYou can also forward voice messages to me to get the file sizes of them.",
	    parse_mode=telegram.ParseMode.MARKDOWN)


@run_async
def arc_favs(update, ctx):
	text = update.message.text
	text = cutcmd(text)
	sended_msg = ctx.bot.send_message(
	    chat_id=update.effective_chat.id,
	    text="Now fetching @" + text +
	    "'s favorite tweets…\n<i>This process may take several minutes, as we support archiving videos now.</i>",
	    parse_mode=telegram.ParseMode.HTML)
	log(graf, "favs", text, "2Lmwx" + ':favs')
	sended_msg.edit_text(
	    text="*" + text + "*\n" + graf["url"],
	    parse_mode=telegram.ParseMode.MARKDOWN)
	print(graf)


@telegram.ext.dispatcher.run_async
def arc_user(update, ctx):
	text = update.message.text
	text = cutcmd(text)
	if text == "":
		text = "elonmusk"
	splited = text.split(" as ")
	title = ""
	if splited != [text]:
		title = splited[1]
	sended_msg = ctx.bot.send_message(
	    chat_id=update.effective_chat.id,
	    text=
	    f"Now fetching user @{text}'s tweets…\n<i>This process may take several minutes, as we support archiving videos now.</i>",
	    parse_mode=telegram.ParseMode.HTML)
	graf = graph.fetchUser(text, title=title)
	log(graf, text, 'user', text + ':timeline')
	sended_msg.edit_text(
	    text="<b>" + text + "</b>\n" + graf["url"],
	    parse_mode=telegram.ParseMode.HTML)
	print(graf)

def arc_timeline(update, ctx):
	sended_msg = ctx.bot.send_message(
	    chat_id=update.effective_chat.id,text="Now fetching timeline tweets…",
	    parse_mode=telegram.ParseMode.MARKDOWN)
	graf = graph.fetchTimeline()
	log(graf, "tl", 'timeline', "2Lmwx" + ':favs')
	sended_msg.edit_text(
	    text="*" + " Timeline tweets" + "*\n" + graf["url"],
	    parse_mode=telegram.ParseMode.MARKDOWN)


def search_tweets(update, ctx):
	text = update.message.text
	text = cutcmd(text)
	graf = graph.search(text, title=text)
	log(graf, text, 'search', text + ':search')
	ctx.bot.send_message(
	    chat_id=update.effective_chat.id,
	    text="*" + text + "*\n" + graf["url"],
	    parse_mode=telegram.ParseMode.MARKDOWN)


def single_tweet(update, ctx):
	text = update.message.text
	text = cutcmd(text)


def favs_users(update, ctx):
	pass


@run_async
def dutymachine(update, ctx):
	text = update.message.text
	text = cutcmd(text)
	if len(text) <= 6:
		resp = "Unsupported link."
	else:
		resp = duty.dm(text)
		log('DUTY', text, 'duty', resp)
	ctx.bot.send_message(
	    chat_id=update.effective_chat.id,
	    text="`" + text + "`\n" + resp,
	    parse_mode=telegram.ParseMode.MARKDOWN)


@run_async
def ping(update, ctx):
	ctx.bot.send_message(chat_id=update.effective_chat.id, text="Pong!")


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


def followings(update, ctx):
	text = update.message.text
	text = cutcmd(text)
	fllwings = []
	tweepy = graph.getTweepy()
	api = graph.getApi()
	try:
		for user in tweepy.Cursor(
		    api.friends, screen_name="2Lmwx", count=4999).items():
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
	ctx.bot.send_message(chat_id=update.effective_chat.id, text=resu["url"])


@run_async
def voice_listener(update, ctx):
	#print(update)
	voi = update.message.voice
	ctx.bot.send_message(
	    chat_id=update.effective_chat.id,
	    text=
	    f"*Voice data*\n\nVoice file ID: `{voi.file_id}`\nUnique ID: `{voi.file_unique_id}`\nDuration: {voi.duration} sec(s)\nFile type: `{voi.mime_type}`\nFile size: {round(voi.file_size/1024,2)}KB",
	    parse_mode=telegram.ParseMode.MARKDOWN)


@run_async
def photo_uploader(update, ctx):
	#print(update)
	msg = update.message
	file = bot.getFile(update.message.photo[-1].file_id)
	#print(file)
	#reply = json.dumps(msg.photo, sort_keys=True, indent=4, separators=(',', ': '))
	graphfile = graph.save_img(file.file_path)

	bot.send_message(chat_id=update.effective_chat.id, text=graphfile)
	# DO NOT POST file.file_path TO OTHERS AS IT CONTAINS BOT_TOKEN!
	# According to the documentation, link may expire after 1 h.


def file_keeper(update, ctx):
	# print(update.message)
	msg = update.message
	siz = msg.document.file_size
	sizmb = siz / 1024.0**2
	print(sizmb)
	if sizmb >= 5:
		msg.reply_text(
		    r'_Your file exceeds the limit of *5MB*\._',
		    parse_mode='MarkdownV2')
	else:
		file = bot.getFile(update.message.document.file_id)
		graphfile = graph.save_img(file.file_path)
		msg.reply_text(text=str(format(sizmb, '.2f')) + 'MB\n' + graphfile)


@run_async
def plain_msg(update, ctx):
	text = update.message.text
	print(text)
	if reg.is_status(text):
		regf = re.findall(r'com\/@?[a-zA-Z0-9_]+\/status', text)[0]
		spl = regf.split(r'/')
		user = spl[1]
		print('User in link: ' + user)
		graf = graph.fetchUser(user, title=user)
		log(graf, user, 'user', text + ':timeline')
		#ctx.bot.send_message(
		update.message.reply_markdown(
		    quote=True,
		    text="*" + "Get user from link: " + user + "*\n" + graf["url"])
		print(graf)
	elif reg.is_duty(text):
		resp = duty.dm(text)
		log('DUTY', text, 'duty', resp)
		ctx.bot.send_message(
		    chat_id=update.effective_chat.id,
		    text="`" + text + "`\n" + resp,
		    parse_mode=telegram.ParseMode.MARKDOWN)


from telegram.ext import MessageHandler, CommandHandler, Filters
start_handler = CommandHandler('start', start)
favs_handler = CommandHandler('favs', arc_favs)
user_handler = CommandHandler('user', arc_user)
timeline_handler = CommandHandler("timeline", arc_timeline)
tl_handler = CommandHandler("tl", arc_timeline)
search_handler = CommandHandler('search', search_tweets)
duty_handler = CommandHandler('duty', dutymachine)
userduty_handler = CommandHandler('userduty', userduty)
followings_handler = CommandHandler("followings", followings)
ping_handler = CommandHandler('ping', ping)
message_handler = MessageHandler(Filters.text & (~Filters.command), plain_msg)
file_handler = MessageHandler(
    Filters.document.image & Filters.chat_type.private, file_keeper)
voice_handler = MessageHandler(Filters.voice & Filters.chat_type.private,
                               voice_listener)
photo_handler = MessageHandler(Filters.photo & Filters.chat_type.private,
                               photo_uploader)
print(Filters.chat_type.private)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(message_handler)
dispatcher.add_handler(favs_handler)
dispatcher.add_handler(user_handler)
dispatcher.add_handler(timeline_handler)
dispatcher.add_handler(tl_handler)
# dispatcher.add_handler(search_handler)
dispatcher.add_handler(duty_handler)
dispatcher.add_handler(followings_handler)
dispatcher.add_handler(ping_handler)
dispatcher.add_handler(userduty_handler)
dispatcher.add_handler(voice_handler)
dispatcher.add_handler(photo_handler)
dispatcher.add_handler(file_handler)

# 拉清单
updater.start_polling()
