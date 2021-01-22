import re

url_patt = re.compile(r'(https?:\/\/)(mobile\.)?twitter\.com\/@?[a-zA-Z0-9_]+\/status\/[0-9]+(\/(s\?=[0-9]+)?)?', flags=re.IGNORECASE)
def is_status(url):
  return url_patt.match(url)
  
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
    if "http://" + domain in url or "https://" + domain in url:
    # Duty Machine requires protocol name
      return True
  return False

def escape(markdown_v2_text):
  escaped = markdown_v2_text
  for char in ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']:
    escaped = escaped.replace(char, "\\" + char)
  return escaped