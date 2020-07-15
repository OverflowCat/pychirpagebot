import json
import re
import tweepy
from datetime import datetime
from html_telegraph_poster import TelegraphPoster
from html_telegraph_poster.upload_images import upload_image
graph = TelegraphPoster(access_token='556b039106f6877d599578530b74768a2959e488c4419355944819d369af')
T1 = 'VwvCRQnzMY26nGQFVhTTZxAqM'
T2 = '2Q98qYh9lUL7FPqi0VNZo9ZrmdlZhQdkYvBrUHqIzvrwiPaneL'
T3 = '758295043337617408-OkKZJAu36S6yXb7iCwA3tfO1y60zfo1'
T4 = '4iJf8fMiIF9LkOlMpxbTa2zwrGxxH2CTQs3OW6Q7LwwBy'
auth = tweepy.OAuthHandler(T1, T2)
auth.set_access_token(T3, T4)
api = tweepy.API(auth)






def fetchFavs(user):
  if user == "ofc":
    user = "u7x09"
  # Cursor is the search method this search query will return 20 of the users latest favourites just like the php api you referenced
  favs = tweepy.Cursor(api.favorites, screen_name=user).items(60)
  urls = []
  txts = []
  output = []
  for t in favs:
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
        replurl = "https://twitter.com/" + t.in_reply_to_screen_name + "/status/" + t.in_reply_to_status_id_str
        repl = "<p><strong>↬</strong> <code>@" + t.in_reply_to_screen_name + '</code> · _<code>' + t.in_reply_to_user_id_str + '</code> : # <a href="' + replurl + '">' + t.in_reply_to_status_id_str + '</a>'
      print(repl)
      htm.append(repl)
    htm.append("<p>" + t.text + "</p>")
    date_time = t.created_at.strftime("%Y/%m/%d, %H:%M:%S")
    htm.append("<p><i>" + date_time + "</i> · " + t.source + "</p>")
    #if(t.media):
    #  htm.append(t.media.media_url_https)
    #htm.append('<iframe src="' + twurl + '"></iframe>')
    output.append(" ".join(htm))
  graf = graph.post(title=user, author='Twitter', text="\n".join(output))
  return graf





def fetchUser(user="realDonaldTrump"):
  usertimeline = tweepy.Cursor(api.user_timeline, screen_name=user, tweet_mode="extended").items(80)
  urls = []
  txts = []
  output = []
  userobj = ""
  for t in usertimeline:
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
      print(repl)
      htm.append(repl)
    htm.append("<p>" + t.full_text + "</p>") # full!!!!!
    date_time = t.created_at.strftime("%Y/%m/%d, %H:%M:%S")
    htm.append("<p><i>" + date_time + "</i> · " + t.source + "</p>")
    #if(t.media):
    #  htm.append(t.media.media_url_https)
    #htm.append('<iframe src="' + twurl + '"></iframe>')
    output.append(" ".join(htm))
    print(" ".join(htm))
  graf = graph.post(title=user, author='Twitter', text="\n".join(output))
  return graf