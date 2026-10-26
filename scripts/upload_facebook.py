"""\nUpload video vers Facebook Page via Graph API.\nUtilise un token de page longue duree (60 jours).\n"""
import argparse
import os
import sys
import requests

def get_long_lived_page_token(page_token: str, page_id: str, app_id: str, app_secret: str) -> str:
    """Echange un token court contre un token longue duree (60 jours)."""
    res = requests.get(
        "https://graph.facebook.com/oauth/access_token",
        params={
            "grant_type": "fb_exchange_token",
            "client_id": app_id,
            "client_secret": app_secret,
            "fb_exchange_token": page_token,
        }
    ).json()
    long_user_token = res.get("access_token")
    if not long_user_token:
        return page_token

    res2 = requests.get(
        f"https://graph.facebook.com/v19.0/{page_id}",
        params={"fields": "access_token", "access_token": long_user_token}
    ).json()
    return res2.get("access_token", page_token)

def upload(video_path: str, title: str, description: str):
    page_token = os.environ.get("FACEBOOK_PAGE_TOKEN")
    page_id = os.environ.get("FACEBOOK_PAGE_ID")
    app_id = os.environ.get("FACEBOOK_APP_ID")
    app_secret = os.environ.get("FACEBOOK_APP_SECRET")

    if not page_token or not page_id:
        print("FACEBOOK_PAGE_TOKEN ou FACEBOOK_PAGE_ID manquant")
        sys.exit(1)

    if app_id and app_secret:
        page_token = get_long_lived_page_token(page_token, page_id, app_id, app_secret)

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
