import re
import os
import time
import storage
import tweepy
import requests
import db
import pagination
import json
import select
import ffm
from typing import Optional, Dict, List, Tuple, Union
from tweets import *
from cachetools import cached, TTLCache

current_tweet = ""
use_png = False

### debug ###
# ltw: last fetched tweets

from reg import id_generator
from datetime import datetime
from html_telegraph_poster import TelegraphPoster
from html_telegraph_poster.upload_images import upload_image
graphacc = os.environ["G1"]
graph = TelegraphPoster(access_token=graphacc)
auth = tweepy.OAuthHandler(os.environ["T1"], os.environ["T2"])
auth.set_access_token(os.environ["T3"], os.environ["T4"])
api = tweepy.API(auth)

def getTweepy():
  return tweepy

def getApi():
  return api

def get_tweetid_range(tweets) -> Tuple[int, int]:
  since_id = max_id = None
  for tweet in tweets:
    if since_id is None or tweet.id < since_id:
      since_id = tweet.id
    if max_id is None or tweet.id > max_id:
      max_id = tweet.id
  return since_id, max_id

@cached(cache=TTLCache(maxsize=8192, ttl=432000))
def save_img(url: str, save2disk : Optional[bool] = False) -> str:
  raw_url = url
  res = db.lookup_pic(raw_url)
  if res != "":
    print(f"Reusing {res} for {raw_url}…")
    return res
  # print("Saving " + url)
  global fformat
  find_hash = re.findall(r"\/[a-zA-Z0-9_-]+\.jpe?g$", url)
  filename = 'temp_' + id_generator(5) + '.jpg'
  if "video.twimg" in url:
    filename = 'temp_' + id_generator(5) + '.mp4'
    fformat = 'mp4'
    filename = url.split('/')[-1].split("?")[0]
  if url.endswith('.png'):
    filename = url.split(r"/")[-1]
    fformat = "png"
  if find_hash != []:
    global use_png
    if use_png:
      url = url.replace(".jpg",".png", 1)
      fformat = "png"
    else:
      fformat = "jpg"
    # +"?format=jpg&name=orig"
    filename = find_hash[0].replace(r'/', "").replace(".jpg",".png", 1)
  print(r'/' + filename)
  _filename = filename
  filename = storage.TEMP_DIR + "/" + filename
  if os.path.exists(filename):
    print("Duplicate " + url)
  request = requests.get(url.replace(r"http://", r"https://"), stream=True)
  if request.status_code == 200:
    with open(filename, 'wb') as image:
      for chunk in request:
        image.write(chunk)
  else:
    print(f"Download {url} failed.")
    return ""
  if save2disk:
    return filename # actually path
  try:
    graphfileurl = upload_image(filename)
  except:
    print(f"Upload {filename} failed.")
    return ""
  else:
    storage.mv(filename, "/pan/pychirpagebot/saved/" + _filename, True)
    db.associate_pic(raw_url, graphfileurl)
    return graphfileurl

def save_imgs(imgurls: List[str]) -> List[str]:
  print("Saving " + ", ".join(imgurls))
  return [save_img(x) for x in imgurls]

def save_vid(url, removeFailed=False):
  return [upload(x) for x in ffm.split(save_img(url, True)) if not removeFailed or x != ""]
  # 当 not 和 and 及 or 在一起运算时，优先级为 not > and > or，即 t and f or not t == t and f or f == f or f == f

def upload(path: str) -> str:
  try:
    print("现正在上传 " + path)
    graphfileurl = upload_image(path)
  except:
    print(f"Upload {path} failed.")
    return ""
  else:
    return graphfileurl

# DEPRECATED OLD CODE HAS BEEN REMOVED

tco_rgx = re.compile(r"(https:\/\/t\.co)/([a-zA-Z0-9]{10})")
def tco(texto):
  return re.sub(tco_rgx,
  r'<a href="\1/\2">\2</a>', texto)

def get_user_link(user, html=False, id_str=False):
  link = r"https://twitter.com/" + user.screen_name
  if html:
    user_html = f'<a href="{link}">@{user.screen_name}</a>'
    if id_str:
      return user_html + ' <code>_' + user.id_str + r"</code>"
    return user_html
  return link

# collect
user_collect=[]

def fetch_tweets(tweets):
  graphs = []
  for tweet in tweets:
    graphs.append("")

def fetch_tweet(tweet, title=''):
  # get username
  if title == '':
    title = "tweet"

@cached(cache=TTLCache(maxsize=500, ttl=1800))
def fetchFavs(user: str = "elonmusk", title: str = ''):
  if user == "i":
    user = "twitter"
  if title == "":
    title = user + "-favs-" + id_generator(4)
  print("Fetching @" + user + "'s favorites")
  tweets = api.get_favorites(screen_name=user, count=60)
  #tweets = tweepy.Cursor(api.favorites, screen_name=user, tweet_mode="extended").items(60)
  ooo = dealWithTweets(tweets, username=True)
  graf = graph.post(title=title, author='Twitter Likes', text="".join(ooo))
  since_id, max_id = get_tweetid_range(tweets)
  print("========= since id is", since_id, "/ max id is",  max_id)
  graf["since_id"] = since_id
  graf["max_id"] = max_id
  return graf

@cached(cache=TTLCache(maxsize=1000, ttl=3600))
def fetchUser(user: str = "elonmusk", title: str = ""):
  if user == "ofc":
    user = "elonmusk"
  if title == "":
    title = "@" + user
  print("Fetching @" + user)
  tweets = tweepy.Cursor(api.user_timeline, screen_name=user,
                         tweet_mode="extended").items(60)
  ooo = dealWithTweets(tweets, username=False)
  graf = graph.post(title=title, author='Twitter', text=" "+"".join(ooo))
  return graf

@cached(cache=TTLCache(maxsize=1000, ttl=3600))
def fetchList(list_id: str, title: str = ''):
  # tweets = tweepy.Cursor(api.list_timeline, list_id=1496265153821745158,
  #                       tweet_mode="extended").items(60)
  print(f"Fetching list {list_id}…")
  tweets = tweepy.Cursor(api.list_timeline, list_id=list_id, tweet_mode="extended").items(60)
  #tweepy.Client.get_list_tweets(list_id, max_results=60)
  print(tweets)
  ooo = dealWithTweets(tweets, username=True)
  graf = graph.post(title=list_id, author='Twitter', author_url=f"https://twitter.com/i/lists/{list_id}", text=" "+"".join(ooo))
  return graf

@cached(cache=TTLCache(maxsize=50, ttl=200))
def fetchTimeline(user: str = ""):
  tweets = api.home_timeline(tweet_mode="extended")
  ooo = dealWithTweets(tweets, username=True)
  graf = graph.post(title="Neko_Timeline", author="Twitter", text=" "+''.join(ooo))
  return graf

@cached(cache=TTLCache(maxsize=10, ttl=15))
def fetchMentions(user: str = "neko_modules"):
  tweets = api.mentions_timeline(tweet_mode="extended")
  ooo = dealWithTweets(tweets, username=True)
  # get time
  hh_mm = time.strftime("%H %M", time.localtime())
  graf = graph.post(title=f"neko mentions {hh_mm}", author="Twitter", text=" "+''.join(ooo))
  return graf

def search(query, title: str = 'text'):
  print('Searching "' + query + '"')
  search_results = api.search(q=query, count=65, tweet_mode='extended')
  output = dealWithTweets(search_results, username=True)
  graf = graph.post(title=title, author='Twitter Search', text="".join(output))  
  return graf

def dealWithTweets(tweets, **pa):
  global dwt
  dwt = tweets
  output = []
  counter = 0
  bioInfo = ["", ""]
  print(tweets)
  for t in tweets:
    db.save_tweet(t._json)
    # db.logtweet(t.id ,t._json, t.user.id)
    counter += 1
    if counter == 1:
      if not pa["username"]: # 使用了 /user 故不需要每条推都显示作者用户名，因为都是一样的
        bioInfo.append(userBio(t.user))
      else: # 不是用户 bio 页，故需要收集用户
        user_collect.append(t.user.screen_name)
    htm = []
    twurl = "https://twitter.com/" + t.user.screen_name + "/status/" + t.id_str
    htm.append('<h4># <a href="' + twurl + '">' + t.id_str + "</h4>")
    if pa['username']:
      htm.append("<p><b>" + t.user.name + "</b> (<code>@" + t.user.screen_name + "</code> · _<code>" + t.user.id_str + "</code>)</p>")
    # 判断是否是 reply
    replyattr = getattr(t, 'in_reply_to_screen_name', None)
    if replyattr is not None:
      if t.in_reply_to_screen_name == t.user.screen_name: #thread 我回复我自己
        replurl = "https://twitter.com/" + t.user.screen_name + "/status/" + t.in_reply_to_status_id_str
        repl = '<p><strong>↬</strong> # <a href="' + replurl + '">' + t.in_reply_to_status_id_str + "</a>"
      else:
        replurl = "https://twitter.com/" + t.in_reply_to_screen_name
        in_reply_to_status_id_str_attr = getattr(t, 'in_reply_to_status_id_str') # 被屏蔽这里就是 NoneType
        if in_reply_to_status_id_str_attr is not None:
          replurl = replurl + "/status/" + t.in_reply_to_status_id_str
          _in_reply_to_status_id_str =  t.in_reply_to_status_id_str #the text
        else:
          _in_reply_to_status_id_str = '@' + t.in_reply_to_screen_name #the text
        repl = "<p><strong>↬</strong> <code>@" + t.in_reply_to_screen_name 
        repl += '</code> · _<code>' + t.in_reply_to_user_id_str
        repl += '</code> : # <a href="' + replurl + '">'
        repl += _in_reply_to_status_id_str + '</a>'
      htm.append(repl)
      
    # deal with text
    status_text = ""
    if hasattr(t, "full_text"):
      status_text = t.full_text #extended_mode, old
    else:
      status_text = t.text # used by favs
    if status_text.startswith("RT @") & status_text.endswith("…"): # ?
      # This may be a retweet with over 140 chars
      if hasattr(t, 'retweeted_status'):
        rt = t.retweeted_status
        r_status_text = ""
        if hasattr(rt, "full_text"):
          r_status_text = rt.full_text
        else:
          r_status_text = rt.text
        status_text = f"RT {get_user_link(rt.user, True, True)}: " + r_status_text
    htm.append("<p>" + tco(status_text) + r"</p>")

    # Image(s)
    if 'media' in t.entities:
      imgurls = []	
      for media in t.extended_entities['media']:	
        imgurls.append(" " + media['media_url'])	
      graphimgurls = save_imgs(imgurls)	
      graphimgshtml = ['<img src="' + ele + '">' for ele in graphimgurls]	
      htm.append("".join(graphimgshtml))
    
    # Save videos
    global current_tweet
    current_tweet = t._json
    if hasattr(t, "extended_entities"):
      e = t.extended_entities
      v = e["media"][0]
      if v["type"] == "video":
        variants = v["video_info"]["variants"]
        variants = [variant for variant in variants if variant["content_type"] == "video/mp4"]
        sorted_variants = sorted(variants, key=lambda va : -va["bitrate"])
        # print(json.dumps(sorted_variants, indent=2)) # 不同清晰度的视频
        vid_urls = save_vid(sorted_variants[0]["url"]) # <- save_img(…)
        print(f"vid_rls: {', '.join(vid_urls)}")
        htm.append("".join([f'<figure><video src="{vid_url}" preload="auto" controls="controls"></video><figcaption>Video</figcaption></figure>' for vid_url in vid_urls]))
        # TODO: Move figure to its preview image
        #htm.append(f'<figure><video src="{vid_url}" preload="auto" controls="controls"></video><figcaption>Video</figcaption></figure>')
   
    date_time = t.created_at.strftime("%Y/%m/%d, %H:%M:%S")
    htm.append("<p><i>" + date_time + "</i> · " + t.source + "</p>")
    output.append("".join(htm))
  db.logtweets([t._json for t in tweets])
  # 放在 for t in tweets:... 前就不行
  return ("".join(bioInfo) + "".join(output)).replace('\n', '<br>')

def pagesTweets(tweets, **pa):
  counter = 0
  outputTweets = []
  graves = []
  for t in tweets:
    counter += 1
    if counter%60 == 0:
      # New page!
      graves.append(dealWithTweets(outputTweets, pa))
    else:
      outputTweets.append(t)
  return graves


def userBio(userobj) -> str:
  ooo = []
  u = userobj
  htm = []
  htm.append("<h3>" + u.name + "</h3><code>@" + u.screen_name + "</code><p>ID: <code>_" + u.id_str + "</code></p>")
  if u.protected:
    htm.append(" 🔒")
  if u.verified:
    htm.append(" ✔️")

  if hasattr(u, "profile_banner_url"):
    print("Banner URL: " + u.profile_banner_url)
    # Banner URL be like: https://pbs.twimg.com/profile_banners/{userid}/1234567890
    # TODO: change banner pic name
    saved = save_img(u.profile_banner_url)
    if saved != "err":
      htm.insert(0, f'<img src="{saved}">')
    else:
      print("Saving Banner ERR")
  htm.append("<aside>" + u.description + "</aside>")

  if False:#hasattr(u, "url"):
    print("has attr!", u.url)
    url = u.url
    htm.append('🔗 <a href="' + url + '">' + url + '</a>')
  if not u.default_profile_image:
    profilepic = u.profile_image_url_https.replace("_normal", "") # original
    # other sizes:
    # https://stackoverflow.com/questions/34761622/how-to-get-users-high-resolution-profile-picture-on-twitter
    print("Avatar: " + profilepic)
    htm.append('<img src="' + profilepic + '">')
    # saved = save_img(u.profile_image_url_https.replace('_normal', "_original"))
    # htm.append('<img src="' + saved + '">')
  htm.append(f'✏️ {str(u.statuses_count)}丨👥 {str(u.followers_count)}丨👁️ {str(u.friends_count)}丨♥️ {str(u.favourites_count)}<br>📆 {u.created_at}<hr>')
  ooo.append("".join(htm))
  ooo = "".join(ooo)
  print(ooo)
  return ooo


def p(text: str, title: str = "Logs"):
  return graph.post(title=title, author='Chirpage', text=text)
