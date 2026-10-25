"""
Upload vidéo vers TikTok via autotok (cookies session).
Usage: python upload_tiktok.py --video path/to/video.mp4 --title "titre" --description "desc"
"""
import argparse
import os
import sys

def upload(video_path: str, title: str, description: str):
    try:
        from autotok import TikTokUploader
    except ImportError:
        print("❌ autotok non installé. Lance: pip install autotok")
        sys.exit(1)

    session_id = os.environ.get("TIKTOK_SESSION_ID")
    if not session_id:
        print("❌ TIKTOK_SESSION_ID manquant dans les variables d'environnement")
        sys.exit(1)

    uploader = TikTokUploader(session_id=session_id)
    caption = f"{title}\n\n{description}"
    result = uploader.upload(video_path, caption=caption)
    print(f"✅ TikTok publié : {result}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--description", default="")
    args = parser.parse_args()
    upload(args.video, args.title, args.description)
