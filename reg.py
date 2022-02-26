import re

import string
import random

status_url_patt = re.compile(r'(https?:\/\/)(mobile\.)?twitter\.com\/@?[a-zA-Z0-9_]+\/status\/[0-9]+(\/(s\?=[0-9]+)?)?', flags=re.IGNORECASE)
def is_status(url):
  return status_url_patt.match(url)

profile_url_patt = re.compile(r'(https?:\/\/)(mobile\.)?twitter\.com\/@?[a-zA-Z0-9_]+\/?', flags=re.IGNORECASE)
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
  "weibo.com/", "weibo.cn/"
  ]
# Refer to https://github.com/duty-machine/duty-machine-action/tree/master/websites

def is_duty(url):
  for domain in duties:
    if domain in url:
      if "http" in url.lower():
    # Duty Machine requires protocol name
        return True
  return False

def escape(markdown_v2_text):
  escaped = markdown_v2_text
  for char in ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']:
    escaped = escaped.replace(char, "\\" + char)
  return escaped

annies = ["bilibili.com", "youtube.com", "douyin.com", "twitter.com", "vimeo.com", "youku.com"]
def is_vid(url):
  for domain in annies:
    if domain in url:
      return True
  return False

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))

def is_list(url):
  return url.startswith("https://twitter.com/i/lists/")