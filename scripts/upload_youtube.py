"""
Upload vidéo vers YouTube via l'API gratuite (OAuth).
Usage: python upload_youtube.py --video path/to/video.mp4 --title "titre" --description "desc"
"""
import argparse
import os
import sys
import json

def upload(video_path: str, title: str, description: str):
    try:
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
        from google.oauth2.credentials import Credentials
    except ImportError:
        print("❌ google-api-python-client non installé.")
        sys.exit(1)

    token_json = os.environ.get("YOUTUBE_TOKEN_JSON")
    if not token_json:
        print("❌ YOUTUBE_TOKEN_JSON manquant")
        sys.exit(1)

    creds = Credentials.from_authorized_user_info(json.loads(token_json))
    youtube = build("youtube", "v3", credentials=creds)

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": ["CaliBodi", "fitness", "workout", "coach"],
            "categoryId": "17",  # Sports
        },
        "status": {"privacyStatus": "public"},
    }

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(part=",".join(body.keys()), body=body, media_body=media)
    response = request.execute()
    print(f"✅ YouTube publié : https://youtube.com/watch?v={response['id']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--description", default="")
    args = parser.parse_args()
    upload(args.video, args.title, args.description)
