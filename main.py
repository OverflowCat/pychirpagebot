from telegram.ext import MessageHandler, CommandHandler, Filters
from telegram.ext.dispatcher import run_async
import logging
from telegram.ext import Updater
import requests
from datetime import datetime
from telegram import ParseMode
from telegram.ext.defaults import Defaults
import math
import publish
import json
import db
import reg
import duty
import os
import re
import telegram
from dotenv import load_dotenv
load_dotenv()  # graph.py requires env
import graph

print("App started")


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
updater = Updater(os.environ["chirpage"], use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


def start(update, context):
	context.bot.send_message(
	    chat_id=update.effective_chat.id,
	    text="""Please send me the link of any tweet directly, or using the /user command plus the Twitter user's screen name (like `/user elonmusk`) to me then I will fetch the account's latest tweets and archive them as a Telegraph.
		You can also forward voice messages to me to get the file sizes of them.
		Duty Machine service is temporarily down due to GitHub's term of service.""",
	    parse_mode=telegram.ParseMode.MARKDOWN)


def arc_favs(update, ctx):
	text = update.message.text
	text = cutcmd(text).lower()
	_t = text.lower()
	if _t == "" or _t == "ofc" or _t == "i":
		if update.effective_chat.id == (1000 * (2061 + math.pow(2, 16)) + 97) * 6:
			text = "2LMWX"
		else:
			update.message.reply_markdown("Please specify a username.")
			return
			# text = "elonmusk"
	elif _t == "2lmwx":
		if update.effective_chat.id != (1000 * (2061 + math.pow(2, 16)) + 97) * 6:
			return
	_t = None

	sended_msg = ctx.bot.send_message(
	    chat_id=update.effective_chat.id,
	    text="Now fetching @" + text +
	    "'s favorite tweets…\n<i>This process may take several minutes, as we support archiving videos now.</i>",
	    parse_mode=telegram.ParseMode.HTML)
	graf = graph.fetchFavs(text)
	# log(graf, "favs", text, "2Lmwx" + ':favs')
	sended_msg.edit_text(
	    text="*" + text + "*\n" + graf["url"],
	    parse_mode=telegram.ParseMode.MARKDOWN)
	print(graf)

# @telegram.ext.dispatcher.run_async


def arc_user(update, ctx):
	text = cutcmd(update.message.text)
	if text == "":
		update.message.reply_markdown("Please specify a username.")
		return
	else:
		if "twitter.com" not in text:
			if re.match("^[0-9a-zA-Z_]+$", text):
				# This is a valid username!
				pass
			elif re.match("^[0-9a-zA-Z_ ]$", text):
				# This is a valid "as" username!
				pass
			else:
				update.message.reply_markdown(
					'The username you provided is not valid. A valid one consists of only alphanumeric letters and "_"s.')
		else:
			ctx.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text='Please input a valid twitter username rather than a link, which contains alphanumeric letters and "_"s only.')
		return
		text = text.split('/')[-1]
	splited = text.split(" as ")
	title = ""
	as_what = ""
	if splited != [text]:
		title = splited[1]
		as_what = " as " + title
	sended_msg = ctx.bot.send_message(
	    chat_id=update.effective_chat.id,
	    text=f"Now fetching user @{text}'s tweets{as_what}…\n<i>This process may take several minutes, as we support archiving large videos now.</i>",
	    parse_mode=telegram.ParseMode.HTML)
	graf = graph.fetchUser(text, title=title)
	log(graf, text, 'user', text + ':timeline')
	sended_msg.edit_text(
	    text="<b>" + text + "</b>\n" + graf["url"],
	    parse_mode=telegram.ParseMode.HTML)
	print(graf)


def arc_timeline(update, ctx):
	sended_msg = ctx.bot.send_message(
	    chat_id=update.effective_chat.id, text="Now fetching timeline tweets…",
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


def dutymachine(update, ctx):
	update.message.reply_markdown(
		"Sorry, duty machine service is temporarily down. If you want to archive tweets, please send Twitter link without any command.")

	"""
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
	"""


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


def textilegraph(update, ctx):
  graf = publish.txtile(cutcmd(update.message.text))
  update.message.reply_markdown("`" + reg.escape(graf) + "`")


def followings(update, ctx):
	text = cutcmd(update.message.text)
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


def voice_listener(update, ctx):
	voi = update.message.voice
	ctx.bot.send_message(
	    chat_id=update.effective_chat.id,
	    text=f"*Voice data*\n\nVoice file ID: `{voi.file_id}`\nUnique ID: `{voi.file_unique_id}`\nDuration: {voi.duration} sec(s)\nFile type: `{voi.mime_type}`\nFile size: {round(voi.file_size/1024,2)}KB",
	    parse_mode=telegram.ParseMode.MARKDOWN)


def photo_uploader(update, ctx):
	msg = update.message
	file = bot.getFile(update.message.photo[-1].file_id)
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
		    parse_mode='Markdown')
	else:
		file = bot.getFile(update.message.document.file_id)
		graphfile = graph.save_img(file.file_path)
		msg.reply_text(text=str(format(sizmb, '.2f')) + 'MB\n' + graphfile)


def plain_msg(update, ctx):
	text = update.message.text
	print(text)
	if reg.is_status(text):
		regf = re.findall(r'com\/@?[a-zA-Z0-9_]+\/status', text)[0]
		spl = regf.split(r'/')
		user = spl[1]
		if user.startswith("@"):
			user = user[1:]
		print('User in link: ' + user)
		sended_msg = update.message.reply_text(text=f"""Found user in link: @{user}
This process will be finished in several minutes, for we have supported archiving large videos. Please wait patiently.""",
                                             quote=True)
		graf = graph.fetchUser(user, title=user)
		log(graf, user, 'user', text + ':timeline')
		sended_msg.edit_text(
		    text="Got user from link: " + user + "\n" + graf["url"],
                 			parse_mode=telegram.ParseMode.HTML
                )
		print(graf)
	elif reg.is_user_profile_page(text):
		arc_user(update, ctx)
	elif reg.is_duty(text):
		dutymachine(update, ctx)
		"""
		resp = duty.dm(text)
		log('DUTY', text, 'duty', resp)
		ctx.bot.send_message(
		    chat_id=update.effective_chat.id,
		    text="`" + text + "`\n" + resp,
		    parse_mode=telegram.ParseMode.MARKDOWN)
		"""


start_handler = CommandHandler('start', start, run_async=True)
favs_handler = CommandHandler(['favs', 'fav'], arc_favs, run_async=True)
user_handler = CommandHandler(['user', 'twitter'], arc_user, run_async=True)
timeline_handler = CommandHandler(
	["tl", "timeline"], arc_timeline, run_async=True)
# command: Union[str, List[str], Tuple[str, ...]]
search_handler = CommandHandler('search', search_tweets, run_async=True)
duty_handler = CommandHandler(
	['duty', 'dm', "dutymachine"], dutymachine, run_async=True)
userduty_handler = CommandHandler('userduty', userduty, run_async=True)
followings_handler = CommandHandler("followings", followings, run_async=True)
ping_handler = CommandHandler('ping', ping)
textile_handler = CommandHandler('textile', textilegraph)
message_handler = MessageHandler(Filters.text & (
	~Filters.command), plain_msg, run_async=True)
file_handler = MessageHandler(
    Filters.document.image & Filters.chat_type.private, file_keeper, run_async=True)
voice_handler = MessageHandler(Filters.voice & Filters.chat_type.private,
                               voice_listener, run_async=True)
photo_handler = MessageHandler(Filters.photo & Filters.chat_type.private,
                               photo_uploader, run_async=True)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(message_handler)
dispatcher.add_handler(favs_handler)
dispatcher.add_handler(user_handler)
dispatcher.add_handler(timeline_handler)
# dispatcher.add_handler(search_handler)
dispatcher.add_handler(duty_handler)
dispatcher.add_handler(followings_handler)
dispatcher.add_handler(ping_handler)
dispatcher.add_handler(textile_handler)
dispatcher.add_handler(userduty_handler)
dispatcher.add_handler(voice_handler)
dispatcher.add_handler(photo_handler)
dispatcher.add_handler(file_handler)

# 拉清单
updater.start_polling()
