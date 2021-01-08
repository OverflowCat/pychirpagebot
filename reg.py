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
  "chinadigitaltimes.net/"
  ]

def is_duty(url):
  for domain in duties:
    if domain in url:
      return True
  return False