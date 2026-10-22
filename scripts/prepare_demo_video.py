"""Download the licensed Wikimedia Commons Ogg file and convert for local Android judge playback.

Run manually: python scripts/prepare_demo_video.py
Requires ffmpeg. No package data, usernames, or provider credentials are used.
"""
from pathlib import Path
import shutil
import subprocess
import urllib.request

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"web"/"demo-media"
SOURCE="https://commons.wikimedia.org/wiki/Special:Redirect/file/Porch_Pirates.ogv"
LIMIT=85*1024*1024

def main():
    if not shutil.which("ffmpeg"):
        raise SystemExit("ffmpeg unavailable. Install via apt install ffmpeg (Ubuntu) or pkg install ffmpeg (Termux).")
    OUT.mkdir(exist_ok=True)
    ogv=OUT/"porch-pirates-cc-by-3.0.ogv"
    mp4=OUT/"porch-pirates-cc-by-3.0.mp4"
    if not ogv.exists():
        req=urllib.request.Request(SOURCE,headers={"User-Agent":"PackagePI-hackathon-licensed-video-demo/1.0"})
        with urllib.request.urlopen(req,timeout=45) as src, ogv.open("wb") as dest:
            count=0
            while True:
                chunk=src.read(65536)
                if not chunk:break
                count+=len(chunk)
                if count>LIMIT:
                    ogv.unlink(missing_ok=True)
                    raise SystemExit("Download exceeded size limit")
                dest.write(chunk)
    if not mp4.exists():
        subprocess.run(["ffmpeg","-nostdin","-y","-i",str(ogv),"-c:v","libx264",
                        "-pix_fmt","yuv420p","-preset","veryfast","-crf","28",
                        "-c:a","aac","-movflags","+faststart",str(mp4)],check=True)
    print("Local illustrative video prepared:",mp4)
    print("Credit: Porch Pirates, nayrproductions, CC BY 3.0 — https://commons.wikimedia.org/wiki/File:Porch_Pirates.ogv")

if __name__=="__main__":main()
