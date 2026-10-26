"""
Upload video vers TikTok via Buffer API.
Buffer publie directement sur TikTok sans navigateur ni revue d'app.
"""
import argparse
import os
import sys
import requests

BUFFER_API_URL = "https://api.bufferapp.com/1"

def upload(video_path: str, title: str, description: str):
    api_key = os.environ.get("BUFFER_API_KEY")
    channel_id = os.environ.get("BUFFER_CHANNEL_ID")

    if not api_key or not channel_id:
        print("BUFFER_API_KEY ou BUFFER_CHANNEL_ID manquant")
        sys.exit(1)

    # Buffer v2 API - creer un post avec video URL
    caption = f"{title}\n\n{description}\n\n#CaliBodi #fitness #workout #squat"

    # Upload via Buffer API v2
    headers = {"Authorization": f"Bearer {api_key}"}

    # Lire la video et l'uploader
    with open(video_path, "rb") as f:
        upload_resp = requests.post(
            "https://api.bufferapp.com/1/media/upload.json",
            headers=headers,
            files={"file": (os.path.basename(video_path), f, "video/mp4")}
        )

    if upload_resp.status_code != 200:
        print(f"Erreur upload media Buffer : {upload_resp.text}")
        sys.exit(1)

    media_id = upload_resp.json().get("id")
    if not media_id:
        print(f"Pas d'ID media dans la reponse Buffer : {upload_resp.text}")
        sys.exit(1)

    # Creer le post
    post_resp = requests.post(
        "https://api.bufferapp.com/1/updates/create.json",
        headers=headers,
        data={
            "profile_ids[]": channel_id,
            "text": caption[:2200],
            "media[video_id]": media_id,
            "now": "true",
        }
    )

    result = post_resp.json()
    if post_resp.status_code == 200:
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
