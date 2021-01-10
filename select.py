def video(variants, bitrate):
  for x in dict(sorted(variants.items(), key=lambda item: item[1])):
    size = x["bitrate"] * bitrate / 8 / 1024.0 #KB
    if size >= 1024*5:
      continue
    else return x
  return False