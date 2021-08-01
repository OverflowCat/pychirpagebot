import os
from pathlib import Path
import subprocess
from typing import Optional, List
Path("temp/_rubbish").mkdir(parents=True, exist_ok=True)
# TODO: auto remove splits

def split(path: str, size: Optional[int] = None) -> List[str]:
    splits = 0
    if size == None:
        size = os.path.getsize(path) / 1024.0 / 1000.0
    if size < 5:
        return [path]
    else:
        splits = size // 5 + 1

    #makedir
    filename = path
    if "/" in filename:
        filename = path.split("/")[-1]
    foldername = filename.split(".")[0]
    Path("temp/" + foldername).mkdir(parents=True, exist_ok=True)
    fformat = "." + path.split(".")[-1]

    duration = getDuration(path) / splits
    #ffmpeg
    print(subprocess.run("pwd"))
    result = os.system(
        f'ffmpeg -i "{path}" -c copy -f segment -segment_time {str(duration)} "temp/{foldername}/output%d{fformat}"')
    #result = subprocess.run(["ffmpeg", "-i", path, "-c copy -f segment", "-segment_time",    str(duration), f"temp/{foldername}/output%d{fformat}"],    stdout=subprocess.PIPE,    stderr=subprocess.STDOUT)
    print(result)
    return [f"temp/{foldername}/{x}" for x in os.listdir("temp/" + foldername)]


def getDuration(path: str) -> float:
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", path],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    return float(result.stdout)  # MB

# print(split('temp/YpwmNFwuCWoqtLE_.mp4'))