import easyocr
import pillow
initialisiert = False
reader = False
def init():
  global reader
  reader = easyocr.Reader(['ch_sim','en']) # need to run only once to load model into memory

def tell(file):
  global initialisiert, reader
  if not initialisiert:
    init()
  else:
    result = reader.readtext(file)
    return result