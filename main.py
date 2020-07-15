import telegram
import graph
import re
cmdre = re.compile(r'\/[a-z]+(@[a-zA-Z0-9_]+bot)? ?')
def cutcmd(msg_txt):
  return re.sub(cmdre, "", msg_txt)
with open("token.txt") as f:
  _token = f.readlines()[0]
bot = telegram.Bot(token=_token)
from telegram.ext import Updater
updater = Updater(token=_token, use_context=True)
dispatcher = updater.dispatcher
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
def start(update, context):
  context.bot.send_message(chat_id=update.effective_chat.id, text="Please send a Twitter user's screen name (like `@twitter`) to me then I will fetch the account's latest tweets and archive them as a Telegraph.", parse_mode=telegram.ParseMode.MARKDOWN)
def arc_favs(update, ctx):
  text = update.message.text
  text = cutcmd(text)
  graf = graph.fetchFavs(text)
  ctx.bot.send_message(chat_id=update.effective_chat.id, text="*"+text+"*\n" + graf["url"], parse_mode=telegram.ParseMode.MARKDOWN) 
  print(graf)
def arc_user(update, ctx):
  text = update.message.text
  ctx.bot.send_message(chat_id=update.effective_chat.id, text="Ao!", parse_mode=telegram.ParseMode.MARKDOWN) 
from telegram.ext import MessageHandler, CommandHandler, Filters
start_handler = CommandHandler('start', start)
favs_handler = CommandHandler('favs', arc_favs)
message_handler = MessageHandler(Filters.all, arc_user)
dispatcher.add_handler(start_handler)
#dispatcher.add_handler(message_handler)
dispatcher.add_handler(favs_handler)
updater.start_polling()