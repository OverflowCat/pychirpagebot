import requests
import re

def getMiddleText(_str:str, ini:str, end:str) -> str:
  return (_str.split(ini))[1].split(end)[0]
def dm(article_url:str) -> str:
  apiurl = "https://archives.duty-machine.now.sh/api/submit"
  form = {"url": article_url}
  res = requests.post(url=apiurl, data=form)
  issueID = re.findall(r'data-url="/duty-machine/duty-machine/issues/[0-9]+/show_partial', res.text)[0] #str
  issueID = getMiddleText(issueID, r'data-url="/duty-machine/duty-machine/issues/', r'/show_partial')
  print(article_url + "\n Issue " + issueID)
  issueURL = r"https://github.com/duty-machine/duty-machine/issues/" + issueID
  return issueURL