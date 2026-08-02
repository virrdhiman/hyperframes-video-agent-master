import os
import sys
import requests
from dotenv import load_dotenv

sys.path.append(os.path.dirname(__file__))
from pexels import get_api_key, best_video_file, download_file, PEXELS_VIDEO_URL

def download_by_id(video_id, out_dest):
    api_key = get_api_key()
    url = f"https://api.pexels.com/videos/videos/{video_id}"
    resp = requests.get(url, headers={"Authorization": api_key}, timeout=15)
    resp.raise_for_status()
    video = resp.json()
    
    best = best_video_file(video)
    if not best:
        print("No video file found in response.")
        return
        
    download_url = best.get("link", "")
    print(f"Downloading {download_url} to {out_dest}")
    if download_file(download_url, out_dest, api_key):
        print("Success.")
    else:
        print("Failed.")

if __name__ == "__main__":
    download_by_id("4201554", "/Users/face/Movies/my-video/public/fortnite/pexels_new_phone.mp4")
