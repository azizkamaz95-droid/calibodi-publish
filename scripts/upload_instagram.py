"""
Upload Reels vers Instagram via instagrapi (session cookie).
Usage: python upload_instagram.py --video path/to/video.mp4 --title "titre" --description "desc"
"""
import argparse
import os
import sys
import json

def upload(video_path: str, title: str, description: str):
    try:
        from instagrapi import Client
    except ImportError:
        print("instagrapi non installe.")
        sys.exit(1)

    session_json = os.environ.get("INSTAGRAM_SESSION_JSON")
    if not session_json:
        print("INSTAGRAM_SESSION_JSON manquant")
        sys.exit(1)

    session_data = json.loads(session_json)
    cl = Client()

    # Connexion via sessionid + csrftoken
    cl.set_settings({
        "cookies": {
            "sessionid": session_data.get("sessionid", ""),
            "csrftoken": session_data.get("csrftoken", ""),
        }
    })
    cl.get_timeline_feed()  # Valide la session

    caption = f"{title}\n\n{description}\n\n#CaliBodi #fitness #workout #coach"
    media = cl.clip_upload(video_path, caption=caption)
    print(f"Instagram Reel publie : {media.pk}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--description", default="")
    args = parser.parse_args()
    upload(args.video, args.title, args.description)
