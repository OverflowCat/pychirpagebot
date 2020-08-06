import json
import re
import os
import tweepy
import requests
import string
import random
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

def save_imgs(imgurls):
  graphPicUrls = []
  for pic in imgurls:
    filename = 'temp.jpg'
    request = requests.get(pic.replace("http://", "https://")+"?format=jpg&name=orig", stream=True)
    if request.status_code == 200:
      with open(filename, 'wb') as image:
        for chunk in request:
          image.write(chunk)
      graphPicUrls.append(upload_image(filename))
  return graphPicUrls

def save_img(imgurl):
  res = save_imgs([imgurl])
  if len(res) == 1:
    return res[0]
  else:
    return "err"

def fetchFavs(user, title=""):
  if user == "ofc":
    user = "u7x09"
  if title == "":
    title = "F" + id_generator(3)
  print("Fetching @" + user + "'s favorites")
  tweets = tweepy.Cursor(api.favorites, screen_name=user, tweet_mode="extended").items(63)
  ooo = dealWithTweets(tweets, username=True)
  graf = graph.post(title=title, author='Twitter', text="".join(ooo))
  return graf

def fetchUser(user, title=""):
  if user == "ofc":
    user = "u7x09"
  if title == "":
    title = user
  print("Fetching @" + user)
  tweets = tweepy.Cursor(api.user_timeline, screen_name=user, tweet_mode="extended").items(60)
  ooo = dealWithTweets(tweets, username=False)
  graf = graph.post(title="Twitter User @"+title+" Tweets Archive", author='Twitter', text=" "+"".join(ooo))
  return graf

def old_fetchFavs(user):
  if user == "ofc":
    user = "u7x09"
  tweets = tweepy.Cursor(api.favorites, screen_name=user).items(60)
  output = []
  for t in tweets:
    htm = []
    twurl = "https://twitter.com/" + t.user.screen_name + "/status/" + t.id_str
    htm.append('<h3># <a href="' + twurl + '">' + t.id_str + "</h3>")
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
    htm.append("<p>" + t.text + "</p>")
    if 'media' in t.entities:
      imgurls = []
      for media in t.extended_entities['media']:
        imgurls.append(" " + media['media_url'])
      graphimgurls = save_imgs(imgurls)
      graphimgshtml = ['<img src="' + ele + '">' for ele in graphimgurls]
      htm.append("".join(graphimgshtml))
    date_time = t.created_at
    date_time = date_time.strftime("%Y/%m/%d, %H:%M:%S")
    htm.append("<p><i>" + date_time + "</i> · " + t.source + "</p>")
    output.append("".join(htm))
  graf = graph.post(title=user, author='Twitter', text="".join(output))
  return graf

def old_fetchUser(user="realDonaldTrump"):
  tweets = tweepy.Cursor(api.user_timeline, screen_name=user, tweet_mode="extended").items(80)
  output = []
  for t in tweets:
    htm = []
    twurl = "https://twitter.com/" + t.user.screen_name + "/status/" + t.id_str
    htm.append('<h4># <a href="' + twurl + '">' + t.id_str + "</h4>")
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
    htm.append("<p>" + t.full_text + "</p>") # full!!!!!
    date_time = t.created_at.strftime("%Y/%m/%d, %H:%M:%S")
    htm.append("<p><i>" + date_time + "</i> · " + t.source + "</p>")
    output.append(" ".join(htm))

  graf = graph.post(title=user, author='Twitter', text="\n".join(output))
  return graf

def dealWithTweets(tweets, **pa):
  output = []
  counter = 0
  bioInfo = ["", ""]
  for t in tweets:
    counter += 1
    if counter == 1:
      if not pa["username"]: # 使用了 /user 故不需要每条推都显示作者用户名，因为都是一样的
        bioInfo.append(userBio(t.user))
    
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
    htm.append("<p>" + t.full_text + "</p>") # full!!!!!

    # Image(s)
    if 'media' in t.entities:
      imgurls = []	
      for media in t.extended_entities['media']:	
        imgurls.append(" " + media['media_url'])	
      graphimgurls = save_imgs(imgurls)	
      graphimgshtml = ['<img src="' + ele + '">' for ele in graphimgurls]	
      htm.append("".join(graphimgshtml))

    date_time = t.created_at.strftime("%Y/%m/%d, %H:%M:%S")
    htm.append("<p><i>" + date_time + "</i> · " + t.source + "</p>")
    output.append("".join(htm))
  ooo = "".join(output)
  ooo = "".join(bioInfo) + ooo
  print(ooo)
  ooo = ooo.replace('\n', '<br>')
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
  htm.append("<h3>" + u.name + "</h3><code>@" + u.screen_name + "</code><br>ID: <code>_" + u.id_str + "</code>")
  if u.protected:
    htm.append(" 🔓")
  if u.verified:
    htm.append(" ✔️")

  if hasattr(u, "profile_banner_url"):
    print("Banner URL: " + u.profile_banner_url)
    saved = save_img(u.profile_banner_url)
    if saved != "err":
      htm.append('<img src="' + saved + ">")

  htm.append("<aside>" + u.description + "</aside>")
  if False:#hasattr(u, "url"):
    print("has attr! ")
    print(u.url)
    url = u.url
    htm.append('🔗 <a href="' + url + '">' + url + '</a>')
  if not u.default_profile_image:
    print("Avatar: " + u.profile_image_url_https)
    htm.append('<img src="' + u.profile_image_url_https + '">')
    # saved = save_img(u.profile_image_url_https.replace('_normal', "_original"))
    # htm.append('<img src="' + saved + '">')
  ooo.append("".join(htm))
  ooo = "".join(ooo)
  print(ooo)
  return ooo