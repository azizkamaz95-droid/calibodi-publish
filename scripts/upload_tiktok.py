"""
Upload video vers TikTok via tiktok-uploader (session cookie).
Usage: python upload_tiktok.py --video path/to/video.mp4 --title "titre" --description "desc"
"""
import argparse
import os
import sys

def upload(video_path: str, title: str, description: str):
    try:
        from tiktok_uploader.upload import upload_video
    except ImportError:
        print("tiktok-uploader non installe.")
        sys.exit(1)

    session_id = os.environ.get("TIKTOK_SESSION_ID")
    if not session_id:
        print("TIKTOK_SESSION_ID manquant")
        sys.exit(1)

    caption = f"{title} {description}"[:2200]
    result = upload_video(
        video_path,
        description=caption,
        cookies=[{"name": "sessionid", "value": session_id, "domain": ".tiktok.com", "path": "/"}],
    )
    print(f"TikTok publie : {result}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--description", default="")
    args = parser.parse_args()
    upload(args.video, args.title, args.description)
