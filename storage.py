import os
import shutil
import threading
from typing import Optional

_debug = True
TEMP_DIR = 'temp'


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