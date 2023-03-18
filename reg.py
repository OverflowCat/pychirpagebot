import re

import string
import random

url_patt = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

bili_url_patt = re.compile(r'https?://(?:www\.)?(?:bilibili\.com|b23\.(?:tv|wtf))/\S+')

whole_bili_url_patt = re.compile(r'^https?://(?:www\.)?(?:bilibili\.com|b23\.(?:tv|wtf))/\S+$')

status_url_patt = re.compile(
    r"(https?:\/\/)(mobile\.)?([vf]x)?twitter\.com\/@?[a-zA-Z0-9_]+\/status\/[0-9]+(\/(s\?=[0-9]+)?)?",
    flags=re.IGNORECASE,
)


def is_bili(url: str) -> bool:
    return bool(whole_bili_url_patt.match(url))

def get_bili(url: str):
    res = bili_url_patt.search(url)
    return res.group() if res else None

def is_status(url: str):
    return status_url_patt.match(url)


profile_url_patt = re.compile(
    r"(https?:\/\/)(mobile\.)?([vf]x)?twitter\.com\/@?[a-zA-Z0-9_]+\/?", flags=re.IGNORECASE
)


def is_user_profile_page(url):
    return profile_url_patt.match(url)


duties = [
    "matters.news/",
    "telegra.ph/",
    "graph.org/",
    "zhihu.com/",
    "rfa.fi/",
    "chinadigitaltimes.net/",
    "mp.weixin.qq.com/",
    "archive.",
    "web.archive.org/",
    "douban.com/",
    "weibo.com/",
    "weibo.cn/",
]


# Refer to https://github.com/duty-machine/duty-machine-action/tree/master/websites


def is_duty(url):
    for domain in duties:
        if domain in url:
            if "http" in url.lower():
                # Duty Machine requires protocol name
                return True
    return False


annies = [
    "bilibili.com",
    "youtube.com",
    "douyin.com",
    "twitter.com",
    "vimeo.com",
    "youku.com",
]


def is_vid(url):
    for domain in annies:
        if domain in url:
            return True
    return False


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


def is_list(url):
    return url.startswith("https://twitter.com/i/lists/")


twitter_username_re = re.compile(r"^[a-zA-Z0-9_]{1,15}$")


def is_valid_twitter_username(s: str):
    """Your username cannot be longer than 15 characters. Your name can be longer (50 characters) or shorter than 4
    characters, but usernames are kept shorter for the sake of ease. A username can only contain alphanumeric
    characters (letters A-Z, numbers 0-9) with the exception of underscores, as noted above."""
    return twitter_username_re.match(s)


def is_valid_as_twitter_username(s: str):
    if " as " in s:
        username = s.split(" as ")[0]
        return is_valid_twitter_username(username)
    return False


def cutcmd(msg_txt):  # cmdre = re.compile(r'^\/[a-z]+(@[a-zA-Z0-9_]+bot)? ?')
    seps = msg_txt.split(" ")
    seps.pop(0)
    return " ".join(seps).strip()
