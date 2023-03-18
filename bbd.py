from subprocess import run
import time
from pathlib import Path
from result import Ok, Err, Result
from rich import print

tok = "𖩏"

file_pattern = ["<aid>", "<videoTitle>", "<aid>", "<cid>", "<fps>", "<ownerMid>"]
"""
<videoTitle>: 视频主标题
<pageNumber>: 视频分P序号
<pageNumberWithZero>: 视频分P序号(前缀补零)
<pageTitle>: 视频分P标题
<aid>: 视频aid
<cid>: 视频cid
<dfn>: 视频清晰度
<res>: 视频分辨率
<fps>: 视频帧率
<videoCodecs>: 视频编码
<videoBandwidth>: 视频码率
<audioCodecs>: 音频编码
<audioBandwidth>: 音频码率
<ownerName>: 上传者名称
<ownerMid>: 上传者mid
"""
file_pattern = tok.join(file_pattern)
print(file_pattern)

escape = lambda x: f'"{x}"'


def download(video):
    print(f"[bold blue]Start downloading {video}...[/bold blue]")
    timestamp = str(time.time_ns())
    temp_dir = Path("temp/bb" + timestamp)
    temp_dir.mkdir(parents=True, exist_ok=True)
    cmd = f"""{" ".join(["BBDown", video, "--encoding-priority", "hevc", "--work-dir", escape(temp_dir), "--file-pattern", escape(file_pattern)])}"""
    print("[cyan]" + cmd + "[/cyan]")
    timestamp = None
    res = run(
        cmd,
        capture_output=True,
        shell=True,
    )
    if res.returncode != 0:
        return Err(res.returncode)

    files = [f for f in Path(temp_dir).iterdir() if f.is_file()]
    if not (files and files[0].suffix == ".mp4"):
        return Err(files)
    fname = files[0]

    print(fname)
    # run(" ".join(["rm", "-r", temp_dir]), capture_output=True, shell=True)
    return Ok(fname)
