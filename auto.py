import schedule

import time
import threading

def daily(fun):
  print("Daily job started!")
  fun()

def hourly(fun):
  print("I'm working hourly!")
  fun()

def minly(fun):
  print("I'm working minly!")
  fun()

def add(fun, secs):
  schedule.every(secs).seconds.do(fun)
#schedule.every(1).hours.do(hourly)
#schedule.every(86400).seconds.do(daily)

while True:
  schedule.run_pending()
  time.sleep(1)