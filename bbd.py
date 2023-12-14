from subprocess import run, CalledProcessError
import time
from pathlib import Path
from shutil import rmtree
from result import Ok, Err
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

escape = lambda x: f'"{x}"'


class BBDownloader:
    def __init__(self, video: str) -> None:
        self.video = video
        self.timestamp = None
        self.temp_dir = None
        self.fname = None

    def __enter__(self):
        print(f"[bold blue]Start downloading {self.video}...[/bold blue]")
        self.timestamp = str(time.time_ns())
        self.temp_dir = Path("temp/bb" + self.timestamp)
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        cmd = f"""{" ".join(["BBDown", self.video, "--encoding-priority", "hevc", "--dfn-priority", "720P", "--work-dir", escape(self.temp_dir), "--file-pattern", escape(file_pattern)])}"""
        print("bbdown cmd: [cyan]" + cmd + "[/cyan]")
        try:
            res = run(
                cmd,
                capture_output=True,
                shell=True,
            )
        except CalledProcessError as e:
            print("Command failed with exit code", e.returncode)
            return Err(e.returncode)
        if res.returncode != 0:
            return Err(res.returncode)

        files = [f for f in Path(self.temp_dir).iterdir() if f.is_file()]
        if not (files and files[0].suffix == ".mp4"):
            return Err(files)
        self.fname = files[0]
        resolution_cmd = f"""{" ".join(["ffprobe", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "default=nw=1:nk=1", escape(self.fname)])}"""
        print("resolution_cmd:", "[cyan]" + resolution_cmd + "[/cyan]")
        try:
            resolution_res = run(
                resolution_cmd,
                capture_output=True,
                shell=True,
            )
        except CalledProcessError as e:
            print("Probe CalledProcessError", e)
            return Err(e.returncode)
        if resolution_res.returncode != 0:
            print("Probe Bad Return Code")
            return Err(resolution_res.returncode)

        resolutions = resolution_res.stdout.decode().split("\n")
        print("Probe Okay,", resolutions)
        return Ok(
            {
                "path": self.fname,
                "resolutions": {"width": resolutions[0], "height": resolutions[1]},
            }
        )

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.temp_dir and self.temp_dir.is_dir():
            rmtree(self.temp_dir)
        if self.fname and self.fname.is_file():
            self.fname.unlink()
