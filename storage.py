import os
import shutil
import threading
from typing import Optional

_debug = True
TEMP_DIR = 'temp'

import math

def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

def to_percentage(f: float) -> str:
  return '{:.2f}'.format(f*100) + r'%'

def mv(src:str, dst:str, delay:Optional[bool]=False, sec:Optional[int]=6) -> bool:
  """
  if delay:
    if _debug:
      print("Now delaying " + src)
    mv_threading = threading.Timer(sec, mv, args=(src, dst, False))
    mv_threading.start()
  else:
    if _debug:
      print("Now moving " + src)
    shutil.copy(src, dst)
    os.remove(src)
    if _debug:
      print("Have moved " + src)
    return True
  """
  return True

def mkdir(path:str) -> bool:
  if not os.path.exists(path):
    os.makedirs(path)
    return True
  return False

mkdir(TEMP_DIR)

def rm(path:str) -> bool:
  # TODO
  shutil.rmtree(path, True)
  return True

def clear_temp() -> bool:
  rm(TEMP_DIR)
  mkdir(TEMP_DIR)
  return True


def get_disk_usage(path: str) -> str:
  stat = shutil.disk_usage(path)
  return(f"Used: {to_percentage(stat.used/stat.total)}\nFree: {convert_size(stat.free)}")
