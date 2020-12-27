import gspread
import json

gc = gspread.service_account('.gstoken.json')
imgsh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1-R1mFwvI5lxmL4ogJZ64esEQcHZ12sXj1o_KCyoK3rg/edit?usp=drivesdk")

rawtweets = gc.open_by_url("https://docs.google.com/spreadsheets/d/1qk1-nWxFh5o8Z-3bnx6t_99tGtbuIsKdG67B_nzsakA/edit?usp=sharing")

msgspread = gc.open_by_url("https://docs.google.com/spreadsheets/d/1b90DbQNGfXdl9CFAbwYF6kogGi0D2bXelH3xo4VPnqI/edit?usp=drivesdk")

#print(sh.sheet1.get('A1'))
ws = imgsh.sheet1
#ws.append_row(['u','t', 'h', 's'])
tws = rawtweets.sheet1

mws = msgspread.sheet1

def logimg(url, telegraphfileurl, imgid, src, fmt, size):
  ws.append_row([url, telegraphfileurl, imgid, src, fmt, size])
  
def logtweet(tid, json_content, uid):
  if type(json_content) != type("{str}"):
    json_content = json.dumps(json_content)
  row_data = [tid, json_content, uid]
  print(row_data)
  tws.append_row(row_data)

def logtweets(tweets):
  print(tweets)
  try:
    tws.append_rows([[t["id_str"], json.dumps(t), t["user"]["id"]] for t in tweets])
  except:
    print("Google Sheets quota_limit")
    
def logmsgs(msg):
  try:
    mws.append_row(msg)
  except:
    print("Google Sheets quota_limit")