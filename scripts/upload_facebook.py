"""
Upload Reel vers Facebook via Graph API (token page).
Usage: python upload_facebook.py --video path/to/video.mp4 --title "titre" --description "desc"
"""
import argparse
import os
import sys
import requests

def upload(video_path: str, title: str, description: str):
    page_token = os.environ.get("FACEBOOK_PAGE_TOKEN")
    page_id = os.environ.get("FACEBOOK_PAGE_ID")

    if not page_token or not page_id:
        print("❌ FACEBOOK_PAGE_TOKEN ou FACEBOOK_PAGE_ID manquant")
        sys.exit(1)

    # Étape 1 : initialiser l'upload
    init_res = requests.post(
        f"https://graph.facebook.com/v19.0/{page_id}/video_reels",
        data={"upload_phase": "start", "access_token": page_token}
    ).json()

    video_id = init_res.get("video_id")
    upload_url = init_res.get("upload_url")
    if not video_id or not upload_url:
        print(f"❌ Erreur init Facebook : {init_res}")
        sys.exit(1)

    # Étape 2 : upload binaire
    with open(video_path, "rb") as f:
        upload_res = requests.post(
            upload_url,
            headers={
                "Authorization": f"OAuth {page_token}",
                "offset": "0",
                "file_size": str(os.path.getsize(video_path)),
            },
            data=f
        )
    if upload_res.status_code != 200:
        print(f"❌ Erreur upload Facebook : {upload_res.text}")
        sys.exit(1)

    # Étape 3 : publier
    pub_res = requests.post(
        f"https://graph.facebook.com/v19.0/{page_id}/video_reels",
        data={
            "upload_phase": "finish",
            "access_token": page_token,
            "video_id": video_id,
            "title": title,
            "description": description,
            "published": "true",
        }
    ).json()

    if pub_res.get("success"):
        print(f"✅ Facebook Reel publié : video_id={video_id}")
    else:
        print(f"❌ Erreur publication Facebook : {pub_res}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--description", default="")
    args = parser.parse_args()
    upload(args.video, args.title, args.description)
