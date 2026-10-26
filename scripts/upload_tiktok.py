"""
Upload video vers TikTok via tiktok-uploader (session cookie).
"""
import argparse
import os
import sys
import json
import tempfile

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

    # Écrire les cookies dans un fichier JSON temporaire
    cookies = [
        {"name": "sessionid", "value": session_id, "domain": ".tiktok.com", "path": "/"}
    ]
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(cookies, f)
        cookies_path = f.name

    caption = f"{title} {description}"[:2200]
    result = upload_video(
        video_path,
        description=caption,
        cookies=cookies_path,
    )
    os.unlink(cookies_path)
    print(f"TikTok publie : {result}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--description", default="")
    args = parser.parse_args()
    upload(args.video, args.title, args.description)
