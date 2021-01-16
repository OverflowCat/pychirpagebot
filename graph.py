import re
import os
import tweepy
import requests
import string
import random
import db
import pagination
import json
import select
from tweets import *

current_tweet = ""
use_png = False

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))
from datetime import datetime
from html_telegraph_poster import TelegraphPoster
from html_telegraph_poster.upload_images import upload_image
graphacc = os.environ["G1"]
graph = TelegraphPoster(access_token=graphacc)
T1 = os.environ["T1"]
T2 = os.environ["T2"]
T3 = os.environ["T3"]
T4 = os.environ["T4"]
auth = tweepy.OAuthHandler(T1, T2)
auth.set_access_token(T3, T4)
api = tweepy.API(auth)
temp_dir = 'temp'
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

def getTweepy():
  return tweepy

def getApi():
  return api

def save_img(url):
  print("Saving " + url)
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
  filename = temp_dir + "/" + filename
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
  try:
    graphfileurl = upload_image(filename)
  except:
    print(f"Upload {filename} failed.")
    return ""
  else:
    return graphfileurl

def save_imgs(imgurls):
  print("Saving " + ", ".join(imgurls))
  return [save_img(x) for x in imgurls]

def old_save_imgs(imgurls):
  print("Saving " + ", ".join(imgurls))
  graphPicUrls = []
  
  for pic in imgurls:
    global fformat
    find_hash = re.findall(r"\/[a-zA-Z0-9_-]+\.jpe?g$", pic)
    filename = 'temp_' + id_generator(5) + '.jpg'
    if "video.twimg" in pic:
      filename = 'temp_' + id_generator(5) + '.mp4'
      fformat = 'mp4'
      filename = pic.split('/')[-1].split("?")[0]
    if pic.endswith('.png'):
      filename = pic.split(r"/")[-1]
      fformat = "png"
    if find_hash != []:
      if use_png:
        pic = pic.replace(".jpg",".png", 1)
        fformat = "png"
      else:
        fformat = "jpg"
      # +"?format=jpg&name=orig"
      filename = find_hash[0].replace(r'/', "").replace(".jpg",".png", 1)
    print(r'/' + filename)
    filename = temp_dir + "/" + filename
    if os.path.exists(filename):
      print("Duplicate " + pic)
    request = requests.get(pic.replace(r"http://", r"https://"), stream=True)
    if request.status_code == 200:
      with open(filename, 'wb') as image:
        for chunk in request:
          image.write(chunk)
    graphfileurl = upload_image(filename)
    graphPicUrls.append(graphfileurl)
    #os.remove(filename)
    fsize = os.path.getsize(filename)
    db.logimg(pic, graphfileurl, "CALCULATED_HASH", "UNKNOWN", fformat, fsize)
  return graphPicUrls
  # return "https://telegra.ph/file/256c7e4f9da49eef2f129.jpg"

def old_save_img(imgurl):
  res = save_imgs([imgurl])
  if len(res) == 1:
    return res[0]
  else:
    return "err"

tco_rgx = re.compile(r"(https:\/\/t\.co)/([a-zA-Z0-9]{10})")
def tco(texto):
  return re.sub(tco_rgx,
  r'<a href="\1/\2">\2</a>', texto)

def get_user_link(user, html=False, id_str=False):
  link = r"https://twitter.com/" + user.screen_name
  if html:
    user_html = f'<a hr ef="{link}">@{user.screen_name}</a>'
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

def fetchFavs(user="elonmusk", title=''):
  if user == "i":
    user = "2Lmwx"
  if title == "":
    title = user + "-favs-" + id_generator(2)
  print("Fetching @" + user + "'s favorites")
  tweets = tweepy.Cursor(api.favorites, screen_name=user, tweet_mode="extended").items(63)
  ooo = dealWithTweets(tweets, username=True)
  graf = graph.post(title=title, author='Twitter', text="".join(ooo))
  return graf

def fetchUser(user="elonmusk", title=""):
  if user == "ofc":
    user = "2Lmwx"
  if title == "":
    title = "@" + user
  print("Fetching @" + user)
  tweets = tweepy.Cursor(api.user_timeline, screen_name=user, tweet_mode="extended").items(60)
  ooo = dealWithTweets(tweets, username=False)
  graf = graph.post(title=title, author='Twitter', text=" "+"".join(ooo))
  return graf

def fetchTimeline(user=""):
  tweets = api.home_timeline(tweet_mode="extended")
  ooo = dealWithTweets(tweets, username=True)
  graf = graph.post(title="Neko_Timeline", author="Twitter", text=" "+''.join(ooo))
  return graf

def search(query, title='text'):
  print('Searching "' + query + '"')
  search_results = api.search(q=query, count=65, tweet_mode='extended')
  output = dealWithTweets(search_results, username=True)
  graf = graph.post(title=title, author='Twitter Search', text="".join(output))  
  return graf

def dealWithTweets(tweets, **pa):
  output = []
  counter = 0
  bioInfo = ["", ""]

  print(tweets)
  for t in tweets:
    # db.logtweet(t.id ,t._json, t.user.id)
    counter += 1
    if counter == 1:
      if not pa["username"]: # 使用了 /user 故不需要每条推都显示作者用户名，因为都是一样的
        bioInfo.append(userBio(t.user))
      else:
        # 不是用户 bio 页，故需要收集用户
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
        in_reply_to_status_id_str_attr = getattr(t, 'in_reply_to_status_id_str') #被屏蔽这里就是 NoneType
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
      
    #deal with text
    status_text  = t.full_text #extended_mode
    if status_text.startswith("RT @") & status_text.endswith("…"):
      # This may be a retweet with over 140 chars
      if hasattr(t, 'retweeted_status'):
        rt = t.retweeted_status
        status_text = f"RT {get_user_link(rt.user, True, True)}: " + rt.full_text
    htm.append("<p>" + tco(status_text) + r"</p>")

    # Image(s)
    if 'media' in t.entities:
      imgurls = []	
      for media in t.extended_entities['media']:	
        imgurls.append(" " + media['media_url'])	
      graphimgurls = save_imgs(imgurls)	
      graphimgshtml = ['<img src="' + ele + '">' for ele in graphimgurls]	
      htm.append("".join(graphimgshtml))
    #print(t.entities)
    
    global current_tweet
    current_tweet = t._json
    if hasattr(t, "extended_entities"):
      e = t.extended_entities
      # print(json.dumps(e, sort_keys=True, indent=2, separators=(',', ': ')))
      v = e["media"][0]
      if v["type"] == "video":
        variants = v["video_info"]["variants"]
        for vari in variants:
          print(vari)
        variants = [variant for variant in variants if variant["content_type"] == "video/mp4"]
        sorted_variants = sorted(variants, key=lambda va : -va["bitrate"])
        print(json.dumps(sorted_variants, indent=2))
        vid_url = save_img(sorted_variants[0]["url"])
        print("vid_url: " + vid_url)
        htm.append(f'<figure><video src="{vid_url}" preload="auto" controls="controls"></video><figcaption>Video</figcaption></figure>')
        #(f'<video src="{vid_url}">')
   
    date_time = t.created_at.strftime("%Y/%m/%d, %H:%M:%S")
    htm.append("<p><i>" + date_time + "</i> · " + t.source + "</p>")
    output.append("".join(htm))
  ooo = "".join(output)
  ooo = "".join(bioInfo) + ooo
  #print(ooo)
  ooo = ooo.replace('\n', '<br>')
  db.logtweets([t._json for t in tweets])
  # 放在 for t in tweets:... 前就不行
  return ooo

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

def userBio(userobj):
  ooo = []
  u = userobj
  htm = []
  htm.append("<h3>" + u.name + "</h3><code>@" + u.screen_name + "</code><p>ID: <code>_" + u.id_str + "</code></p>")
  if u.protected:
    htm.append(" 🔒")
  if u.verified:
    htm.append(" ✔️")

  if False: # hasattr(u, "profile_banner_url"):
    print("Banner URL: " + u.profile_banner_url)
    saved = save_img(u.profile_banner_url)
    if saved != "err":
      htm.append('<img src="' + saved + ">")
    else:
      print("Saving Banner ERR")

  htm.append("<aside>" + u.description + "</aside>")
  if False:#hasattr(u, "url"):
    print("has attr! ")
    print(u.url)
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
  
def p(text, title="Logs"):
  return graph.post(title=title, author='Chirpage', text=text)