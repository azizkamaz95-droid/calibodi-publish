"""
Upload video vers TikTok via Buffer API v1.
Buffer publie directement sur TikTok via une URL video publique.
"""
import argparse
import os
import sys
import requests

def upload(video_path: str, title: str, description: str):
    api_key = os.environ.get("BUFFER_API_KEY")
    channel_id = os.environ.get("BUFFER_CHANNEL_ID")
    video_url = os.environ.get("VIDEO_PUBLIC_URL")

    if not api_key or not channel_id:
        print("BUFFER_API_KEY ou BUFFER_CHANNEL_ID manquant")
        sys.exit(1)

    if not video_url:
        # Construire l'URL depuis le nom du fichier
        video_name = os.path.basename(video_path)
        video_url = f"https://raw.githubusercontent.com/azizkamaz95-droid/calibodi-publish/main/videos/{video_name}"

    caption = f"{title}\n\n{description}\n\n#CaliBodi #fitness #workout #squat"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "profile_ids": [channel_id],
        "text": caption[:2200],
        "media": {
            "video": video_url,
        },
        "now": True,
    }

    resp = requests.post(
        "https://api.buffer.com/v1/updates/create",
        headers=headers,
        json=payload,
    )

    result = resp.json()
    if resp.status_code == 200 or "updates" in result:
        print(f"TikTok Buffer publie : {result}")
    else:
        print(f"Erreur Buffer : {result}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--description", default="")
    args = parser.parse_args()
    upload(args.video, args.title, args.description)
