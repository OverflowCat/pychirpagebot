import re

url_patt = re.compile(r'(https?:\/\/)(mobile\.)?twitter\.com\/@?[a-zA-Z0-9_]+\/status\/[0-9]+(\/(s\?=[0-9]+)?)?', flags=re.IGNORECASE)
def is_status(url):
  return url_patt.match(url)
  
