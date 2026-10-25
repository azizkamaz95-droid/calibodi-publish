"""
Upload vidéo vers YouTube Shorts via l'API gratuite (OAuth token JSON).
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
        from google.auth.transport.requests import Request
    except ImportError:
        print("google-api-python-client non installe.")
        sys.exit(1)

    token_json = os.environ.get("YOUTUBE_TOKEN_JSON")
    if not token_json:
        print("YOUTUBE_TOKEN_JSON manquant")
        sys.exit(1)

    # Nettoyer le token JSON (enlever espaces/newlines parasites)
    token_json = token_json.strip()

    try:
        token_data = json.loads(token_json)
    except json.JSONDecodeError as e:
        print(f"Token JSON invalide: {e}")
        sys.exit(1)

    creds = Credentials(
        token=token_data.get("token"),
        refresh_token=token_data.get("refresh_token"),
        token_uri=token_data.get("token_uri", "https://oauth2.googleapis.com/token"),
        client_id=token_data.get("client_id"),
        client_secret=token_data.get("client_secret"),
        scopes=token_data.get("scopes", ["https://www.googleapis.com/auth/youtube.upload"]),
    )

    # Rafraîchir le token si expiré
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())

    youtube = build("youtube", "v3", credentials=creds)

    body = {
        "snippet": {
            "title": title[:100],
            "description": description,
            "tags": ["CaliBodi", "fitness", "workout", "coach", "Shorts"],
            "categoryId": "17",
        },
        "status": {"privacyStatus": "public"},
    }

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype="video/mp4")
    request = youtube.videos().insert(part=",".join(body.keys()), body=body, media_body=media)
    response = request.execute()
    print(f"YouTube publie : https://youtube.com/watch?v={response['id']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--description", default="")
    args = parser.parse_args()
    upload(args.video, args.title, args.description)
