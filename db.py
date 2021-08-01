import os
import re
import json
import pymysql.cursors

def exe(operation):
# Connect to the database
  try:
    connection = pymysql.connect(host=os.environ['PYCMYSQLHOST'],
                              user=os.environ['PYCMYSQLUSER'],
                              password=os.environ['PYCMYSQLPWD'],
                              database='twimg',
                              cursorclass=pymysql.cursors.DictCursor)
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(operation)
        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()
  except:
    print("DB ERR!")

def get(operation, needcommit=False):
  return []
# Connect to the database
  try:
    connection = pymysql.connect(host=os.environ['PYCMYSQLHOST'],
                              user=os.environ['PYCMYSQLUSER'],
                              password=os.environ['PYCMYSQLPWD'],
                              database='twimg',
                              cursorclass=pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
      cursor.execute(operation)
    if needcommit:
      connection.commit()
  except:
    #print("GET DB ERR!")
    return []
  return cursor.fetchall()

def newformat(fmtname):
  exe(f"""CREATE TABLE `{fmtname}`(
       twitter varchar(18) primary key,
       telegraph char(21) not null,
       tweetid bigint(20),
       createtime TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);""")

def save_tweet(json_data):
  return True

def associate_pic(twimgurl, grafurl):
  find_hash = re.findall(r"\/[a-zA-Z0-9_-]+\.(jpe?g|png)$", twimgurl)
  if find_hash != []:
    twimgid = twimgurl.split(".")[-2].split("/")[-1]
  else:
    return False
  grafid = grafurl.split("/")[-1]
  # if "." in grafid:
  grafid = grafid.split(".")[0] # "aaa".split(".") == ["aaa"]
  print("DB: ", twimgid, grafid)
  _t = twimgurl.split(".")[-1]
  if "jpg" in _t or "jpeg" in _t:
    mediaformat = "jpg"
  elif "png" in _t:
    mediaformat = "png"
  exe(f"""INSERT INTO `{mediaformat}`
  (`twitter`, `telegraph`)
  VALUES
  ("{twimgid}", "{grafid}")""")
  return True

def lookup_pic(twimgurl):
  find_hash = re.findall(r"\/[a-zA-Z0-9_-]+\.(jpe?g|png)$", twimgurl)
  if find_hash != []:
    twimgid = twimgurl.split(".")[-2].split("/")[-1]
    fformat = twimgurl.split(".")[-1]
    if fformat == "jpeg":
      fformat = "jpg"
    res = get(f"SELECT * FROM `{fformat}` WHERE twitter = {twimgid}")
    if len(res) == 1:
      print(res)
      return "http://telegra.ph/file/" + res[0]["telegraph"]
  return ""

## DEPRECATED
def logimg(url, telegraphfileurl, imgid, src, mediaformat, size):
  find_hash = re.findall(r"\/[a-zA-Z0-9_-]+\.(jpe?g|png)$", url)
  if find_hash != []:
    twimgid = url.split(".")[-2].split("/")[-1]
  else:
    return False
  telegraphfileid = telegraphfileurl.split("/")[-1]
  print("DB: ", twimgid, telegraphfileid)
  if False:
    try:
      exe(f"""INSERT INTO `{mediaformat}`
  (`twitter`, `telegraph`)
  VALUES
  ("{twimgid}", "{telegraphfileid}")""")
    except:
      print('Got error')
      return False
  return True

def logtweet(tid, json_content, uid):
  return 

def logtweets(tweets):
  return

def logmsgs(msg):
  return