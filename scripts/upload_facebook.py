"""
Upload vidéo vers Facebook Page via Graph API.
"""
import argparse
import os
import sys
import requests

def upload(video_path: str, title: str, description: str):
    page_token = os.environ.get("FACEBOOK_PAGE_TOKEN")
    page_id = os.environ.get("FACEBOOK_PAGE_ID")

    if not page_token or not page_id:
        print("FACEBOOK_PAGE_TOKEN ou FACEBOOK_PAGE_ID manquant")
        sys.exit(1)

    # Upload direct de la vidéo sur la page
    url = f"https://graph.facebook.com/v19.0/{page_id}/videos"

    with open(video_path, "rb") as f:
        response = requests.post(
            url,
            data={
                "access_token": page_token,
                "title": title,
                "description": description,
                "published": "true",
            },
            files={"source": f},
        )

    result = response.json()
    if "id" in result:
        print(f"Facebook video publiee : id={result['id']}")
    else:
        print(f"Erreur Facebook : {result}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--description", default="")
    args = parser.parse_args()
    upload(args.video, args.title, args.description)
