import requests
import re

def getMiddleText(_str, ini, end):
  return (_str.split(ini))[1].split(end)[0]
def dm(article_url):
  apiurl = "https://archives.duty-machine.now.sh/api/submit"
  form = {"url": article_url}
  res = requests.post(url=apiurl, data=form)
  #print(res.text)
  issueID = re.findall(r'data-url="/duty-machine/duty-machine/issues/[0-9]+/show_partial', res.text)[0] #str
  issueID = getMiddleText(issueID, r'data-url="/duty-machine/duty-machine/issues/', r'/show_partial')
  print(issueID)
  print(article_url + "\n Issue " + issueID)
  issueURL = r"https://github.com/duty-machine/duty-machine/issues/" + issueID
  return issueURL