"""
Upload Reels vers Instagram via instagrapi (cookies session).
Usage: python upload_instagram.py --video path/to/video.mp4 --title "titre" --description "desc"
"""
import argparse
import os
import sys

def upload(video_path: str, title: str, description: str):
    try:
        from instagrapi import Client
    except ImportError:
        print("❌ instagrapi non installé. Lance: pip install instagrapi")
        sys.exit(1)

    session_json = os.environ.get("INSTAGRAM_SESSION_JSON")
    if not session_json:
        print("❌ INSTAGRAM_SESSION_JSON manquant")
        sys.exit(1)

    cl = Client()
    cl.load_settings_json(session_json)

    caption = f"{title}\n\n{description}\n\n#CaliBodi #fitness #workout #coach #sport"
    media = cl.clip_upload(video_path, caption=caption)
    print(f"✅ Instagram Reel publié : {media.pk}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--description", default="")
    args = parser.parse_args()
    upload(args.video, args.title, args.description)
