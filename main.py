from telegram import Update
from telegram.ext import (
    MessageHandler,
    CommandHandler,
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    filters,
)
from telegram.helpers import escape_markdown
import logging
import requests
from datetime import datetime
from telegram.constants import ParseMode
import math
import publish
import reg
from reg import cutcmd
from context import ProgressContext, FakeProgressContext
import duty
import os
import sys
import re

args = sys.argv[1:]  # 从第二个参数开始获取所有命令行参数
bot_id = args[0]
from dotenv import load_dotenv

load_dotenv()  # graph.py requires env
from ffm import is_ffmpeg_installed
import storage
import graph
import sys
from termcolor import cprint
from rich import print
from result import Ok, Err
import bbd
import ai
import poeai
from messages import msg_manager

logger = logging.getLogger(__name__)

logger.info("Starting up...")
is_ffmpeg_installed() or cprint(
    "`ffmpeg` is not installed. Video archiving will not work.",
    "red",
    attrs=["bold"],
    file=sys.stderr,
)


def log(_path, _user, _type, _query):
    r = requests.post(
        os.environ["CHSHDB"],
        json={
            "data": {
                "path": _path,
                "user": _user,
                "type": _type,
                "query": _query,
                "time": int(datetime.utcnow().timestamp()),
            }
        },
    )
    return r.json()


def parse_int_or_str(s: str) -> int | str:
    try:
        return int(s)
    except ValueError:
        return s


ADMIN_ID = int(os.environ["CHIRPAGE_BOT_ADMIN_ID"])

myfllwings = []

application = (
    ApplicationBuilder()
    .token(os.environ["CHIRPAGE" + bot_id])
    .concurrent_updates(4)
    .build()
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_html(
        """你好，我是 pychirpagebot，支持以下多种指令：

<code>/start，/help</code> - 显示本帮助消息
<code>/ping</code> - 测试机器人是否宕机
<code>/textile</code> - 将 Textile 标记文本转换成富文本的 Telegram 消息
<code>语音消息</code> - 获取其文件大小
/clear, /klar - 清除缓存
<b>- Twitter</b>
发送推文链接 - 抓取推文和媒体，以及该用户最近的 60 条推文
<code>/favs + 用户名</code> - 抓取 Twitter 用户最近的 60 条点赞
<code>/user + 用户名</code> - 抓取 Twitter 用户最近的 60 条推文
<code>/list + 列表编号</code> - 抓取 Twitter 主题列表
<code>/mentions</code> - 获取提及列表
/tl - 获取时间线
<b>- AI</b>
<code>/ai</code>, <code>/wen</code>, <code>/man</code>, <code>/ask</code> - 通过 OpenAI API 向 GPT 3.5 提问
<code>/net</code> - 联网搜索并通过 GPT 3.5 用英文解释
<code>/netzh</code> - 联网搜索并通过 GPT 3.5 用中文解释
<code>/poe</code>, <code>/gpt</code> - 通过 Poe 向 GPT 3.5 提问
<code>/sage</code> - 通过 Poe 向 Sage 提问，Sage 的回答更简明
<code>/claude</code>, <code>/cl</code> - 通过 Poe 向 Anthropic 的 Claude Instant 提问
<code>/ruiping</code>, <code>/rp</code> - 用中文锐评
<code>/criticize</code>, <code>/cr</code> - 用英文锐评
<code>/sum</code> - 生成聊天记录摘要
<b>- 哔哩哔哩</b>
<code>/bb</code> 或直接发送含有 <code>b23.*</code>，<code>bilibili.com</code> 链接的消息 - 下载哔哩哔哩视频（最高画质）

请注意，某些指令需要特定的权限和条件才能使用，例如管理员权限和私人聊天。
"""
    )


async def arc_favs(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    text = cutcmd(text).lower()
    _t = text.lower()
    if _t == "" or _t == "ofc" or _t == "i":
        if update.effective_chat.id == (1000 * (2061 + math.pow(2, 16)) + 97) * 6:
            text = "lazy_static"
        else:
            await update.message.reply_markdown("Please specify a username.")
            return
        # text = "elonmusk"
    elif _t == "lazy_static":
        if update.effective_chat.id != (1000 * (2061 + math.pow(2, 16)) + 97) * 6:
            return
    _t = None

    sent_msg = await update.message.reply_html(
        "Now fetching @"
        + text
        + "'s favorite tweets…\n<i>This process may take several minutes, as we support archiving videos now.</i>",
    )
    graf = await graph.fetch_favs(text)
    # log(graf, "favs", text, "lazy_static" + ':favs')
    await sent_msg.edit_text(
        text="*" + text + "*\n" + graf["url"], parse_mode=ParseMode.MARKDOWN
    )
    print(graf)


async def arc_user(update: Update, ctx, cmd=True):
    text = cutcmd(update.message.text) if cmd else update.message.text
    if text == "":
        await update.message.reply_markdown("Please specify a username.")
        return
    if "twitter.com" not in text:
        if reg.is_valid_twitter_username(text) or reg.is_valid_as_twitter_username(
            text
        ):
            pass
        else:
            await update.message.reply_markdown(
                'The username you provided is not valid. A valid one consists of only alphanumeric letters and "_"s.'
            )
            return
    else:
        await ctx.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Please input a valid twitter username rather than a link, which contains alphanumeric letters and "
            '"_"s only.',
        )
        return
    text = text.split("/")[-1]
    splited = text.split(" as ")
    title, as_what = "", ""
    if splited != [text]:
        title = splited[1]
        as_what = " as " + title
    sent_msg = await update.message.reply_html(
        f"Now fetching user @{text}'s tweets{as_what}…\n<i>This process may take several minutes, as we support archiving large videos now.</i>",
    )
    progress_context = (
        FakeProgressContext
        if update.effective_chat.type == "PRIVATE"
        else ProgressContext(sent_msg, update)
    )
    graf = await graph.fetch_user(text, title, progress_context)
    log(graf, text, "user", text + ":timeline")
    await sent_msg.edit_text(
        text="<b>" + text + "</b>\n" + graf["url"], parse_mode=ParseMode.HTML
    )
    print(graf)


async def arc_timeline(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    sent_msg = await update.message.reply_markdown(
        text="Now fetching timeline tweets…",
    )
    graf = await graph.fetch_timeline()
    log(graf, "tl", "timeline", "lazy_static" + ":favs")
    await sent_msg.edit_text(
        text="*" + " Timeline tweets" + "*\n" + graf["url"],
        parse_mode=ParseMode.MARKDOWN,
    )


list_reg = r"^(https?://)?([a-zA-Z.]+\.)?twitter\.com/i/lists/[0-9]+"


async def arc_list(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    list_id = "1496265153821745158"
    text = update.message.text
    if text.startswith("/"):
        text = cutcmd(text)
        # if text.isdigit():
        if text.isdigit():
            list_id = text
    else:
        res = list_reg.search(text)
        if res is None:
            await update.message.reply_markdown("Please specify a list ID.")
            return
        else:
            clean_link = res.group(0)
            print("clean_link:", clean_link)
            _list_id = clean_link.split("/")[-1].strip()
            if _list_id.length > 1:
                list_id = _list_id
            print("list_id:", list_id)
    sended_msg = await ctx.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Now fetching list {list_id}…\n<i>This process may take several minutes, as we support archiving large videos now.</i>",
        parse_mode=ParseMode.HTML,
    )
    graf = await graph.fetch_list(list_id)

    await sended_msg.edit_text(
        text="*" + " Archived tweets" + "*\n" + graf["url"],
        parse_mode=ParseMode.MARKDOWN,
    )


async def arc_mentions(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    sended_msg = await update.message.reply_html("Now fetching mentions…\n")
    graf = await graph.fetch_mentions()
    log(graf, "mentions", "mentions", "lazy_static" + ":favs")
    await sended_msg.edit_text(
        text="*Mentions tweets*\n" + graf["url"], parse_mode=ParseMode.MARKDOWN
    )


def search_tweets(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    text = cutcmd(text)
    graf = graph.search(text, title=text)
    log(graf, text, "search", text + ":search")
    ctx.bot.send_message(
        chat_id=update.effective_chat.id,
        text="*" + text + "*\n" + graf["url"],
        parse_mode=ParseMode.MARKDOWN,
    )


def single_tweet(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    text = cutcmd(text)
    # UNIMPLEMENTED


def favs_users(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    pass


async def dutymachine(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Sorry, duty machine service is temporarily down. If you want to archive tweets, please send Twitter link without any command."
    )
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
		parse_mode=ParseMode.MARKDOWN)
	"""


async def ping(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await ctx.bot.send_message(chat_id=update.effective_chat.id, text="Pong!")


async def userduty(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    text = cutcmd(text)
    graf = await graph.fetch_user(text)
    resp = duty.dm(graf)
    log(graf, text, "userduty", resp)
    await ctx.bot.send_message(
        chat_id=update.effective_chat.id,
        text="`" + text + "`\n" + resp,
        parse_mode=ParseMode.MARKDOWN,
    )


async def textile_graph(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    graf = publish.txtile(cutcmd(update.message.text))
    await update.message.reply_markdown("`" + escape_markdown(graf) + "`")


def followings(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    text = cutcmd(update.message.text)
    fllwings = []
    tweepy = graph.getTweepy()
    api = graph.getApi()
    try:
        for user in tweepy.Cursor(
            api.friends, screen_name="lazy_static", count=4999
        ).items():
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


async def voice_listener(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    voi = update.message.voice
    await ctx.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"*Voice data*\n\nVoice file ID: `{voi.file_id}`\nUnique ID: `{voi.file_unique_id}`\nDuration: {voi.duration} sec(s)\nFile type: `{voi.mime_type}`\nFile size: {round(voi.file_size / 1024, 2)}KB",
        parse_mode=ParseMode.MARKDOWN,
    )


async def photo_uploader(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    bot = ctx.bot
    file = bot.getFile(update.message.photo[-1].file_id)
    graph_file = graph.save_img(file.file_path)

    await bot.send_message(chat_id=update.effective_chat.id, text=graph_file)


# DO NOT POST file.file_path TO OTHERS AS IT CONTAINS BOT_TOKEN!
# According to the documentation, link may expire after 1 h.


async def file_keeper(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    # print(update.message)
    msg = update.message
    siz = msg.document.file_size
    siz_mb = siz / 1024.0**2
    print(f"File size is {siz_mb} MB")
    if siz_mb >= 5:
        await msg.reply_markdown_v2(r"_Your file exceeds the limit of *5MB*\._")
    else:
        file = ctx.bot.getFile(update.message.document.file_id)
        graph_file = graph.save_img(file.file_path)
        await msg.reply_text(text=str(format(siz_mb, ".2f")) + "MB\n" + graph_file)


async def bbdown(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text.startswith("/"):
        text = cutcmd(text)
    text = reg.get_bili(text)
    if text is None:
        return await update.message.reply_text("Failed to find bili url.")
    await update.message.reply_text("Downloading Bilibili video…")
    with bbd.BBDownloader(text) as res:
        match res:
            case Ok(f):
                path = f["path"]
                resolutions = f["resolutions"]
                await update.message.reply_video(
                    path, caption=f"Downloaded {path.name.replace(bbd.tok, ' | ')}.", width=resolutions["width"], height=resolutions["height"]
                )
            case Err(e):
                print(f"[bold red]ERROR Downloading video, error {e}...[/bold red]")
                await update.message.reply_html(
                    f"<b>Error</b>: Process ended with return code {e}. Maybe the link is a live steam."
                    if isinstance(e, int)
                    else f"<b>Error</b>: Video file expected to be found but failed. Please check logs."
                )


async def plain_msg(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not update.message or not (update.message.text or update.message.caption):
        print(update)
        return
    if update.message.text:
        if reg.get_bili(update.message.text):
            return await bbdown(update, ctx)
        if await ai.respond_to_ai(update, ctx):
            return
    text = update.message.text or update.message.caption
    if reg.is_status(text):
        regf = re.findall(r"com\/@?[a-zA-Z0-9_]+\/status", text)[0]
        spl = regf.split(r"/")
        user = spl[1]
        if user.startswith("@"):
            user = user[1:]
        print("User in link: " + user)
        sent_msg = await update.message.reply_text(
            text=f"""Found user in link: @{user}
This process will be finished in several minutes, for we have supported archiving large videos. Please wait patiently.""",
            quote=update.effective_chat.type == "PRIVATE",
        )
        graf = await graph.fetch_user(
            user,
            user,
            ProgressContext(sent_msg, update, tweet_id=int(reg.get_status_id(text))),
        )
        log(graf, user, "user", text + ":timeline")
        text = "Got user from link: " + user + "\n" + graf["url"]
        await sent_msg.edit_text(
            text=text
            if update.effective_chat.type == "PRIVATE"
            else sent_msg.text + "\n" + text,
            parse_mode=ParseMode.HTML,
        )
        print(graf)
    elif reg.is_list(text):
        await arc_list(update, ctx)
    elif reg.is_user_profile_page(text):
        await arc_user(update, ctx, cmd=False)
    elif reg.is_duty(text):
        dutymachine(update, ctx)
        """
        resp = duty.dm(text)
        log('DUTY', text, 'duty', resp)
        ctx.bot.send_message(
            chat_id=update.effective_chat.id,
            text="`" + text + "`\n" + resp,
            parse_mode=ParseMode.MARKDOWN)
        """
    elif update.effective_chat.type != "PRIVATE":
        msg_manager.add_message(
            group_id=update.effective_chat.id,
            msg_id=update.message.id,
            user_id=update.message.from_user.id,
            msg_text=text,
        )


# TODO: 错误处理


async def del_cache(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    pre = storage.get_disk_usage("./")
    storage.rm("./temp")
    storage.mkdir("./temp")
    await update.message.reply_text(
        "Alle klar!\n" + pre + "\n" + storage.get_disk_usage("./")
    )


def clear():  # ???
    storage.clear_temp()


async def summarize(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await ai.summarize_recent_chat_messages(update)

start_handler = CommandHandler(["start", 'help'], start, block=False)
clear_handler = CommandHandler("clear", clear)
favs_handler = CommandHandler(["favs", "fav"], arc_favs, block=False)
user_handler = CommandHandler(["user", "twitter"], arc_user, block=False)
mentions_handler = CommandHandler(
    ["mentions", "mention", "men"], arc_mentions, block=False
)
list_handler = CommandHandler(["list", "li"], arc_list, block=False)
timeline_handler = CommandHandler(["tl", "timeline"], arc_timeline, block=True)
# command: Union[str, List[str], Tuple[str, ...]]
search_handler = CommandHandler("search", search_tweets)
duty_handler = CommandHandler(["duty", "dm", "dutymachine"], dutymachine)
userduty_handler = CommandHandler("userduty", userduty)
followings_handler = CommandHandler("followings", followings)
ping_handler = CommandHandler("ping", ping, block=False)
textile_handler = CommandHandler("textile", textile_graph)
file_handler = MessageHandler(
    filters.Document.IMAGE & filters.ChatType.PRIVATE, file_keeper, block=False
)
voice_handler = MessageHandler(filters.VOICE & filters.ChatType.PRIVATE, voice_listener)
photo_handler = MessageHandler(filters.PHOTO & filters.ChatType.PRIVATE, photo_uploader)
bbdown_handler = CommandHandler(["bb", "bili", "b"], bbdown)
# video_handler = CommandHandler(["vid", "video"], download_video, # filters=(~ filters.Update.EDITED_MESSAGE),)
clear_handler = CommandHandler(["clear", "klar"], del_cache)
ai_handler = CommandHandler(
    ["wen", "man", "ask", "ai", "net", "netzh"], ai.ask_ai, block=False
)
sage_handler = CommandHandler(
    ["poe", "sage", "cl", "claude", "gpt"],
    poeai.ask_poe,
    filters.User(ADMIN_ID) | ~filters.ChatType.PRIVATE,
    block=True,
)
criticize_handler = CommandHandler(
    ["criticize", "cr", "ruiping", "rp"], poeai.criticize, block=True
)
summarize_handler = CommandHandler(
    "sum", summarize, ~filters.ChatType.PRIVATE, block=True
)
message_handler = MessageHandler(
    (filters.TEXT | filters.CAPTION | filters.FORWARDED) & (~filters.COMMAND), plain_msg
)

handlers = [
    start_handler,
    clear_handler,
    favs_handler,
    user_handler,
    mentions_handler,
    list_handler,
    timeline_handler,
    # search_handler,
    duty_handler,
    userduty_handler,
    followings_handler,
    ping_handler,
    textile_handler,
    message_handler,
    file_handler,
    voice_handler,
    photo_handler,
    bbdown_handler,
    # video_handler,
    clear_handler,
    ai_handler,
    summarize_handler,
    sage_handler,
    criticize_handler,
]

for handler in handlers:
    application.add_handler(handler)

# 拉清单
logger.info("Bot started.")
application.run_polling()
