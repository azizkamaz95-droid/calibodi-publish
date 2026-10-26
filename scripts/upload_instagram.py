"""
Upload Reels vers Instagram via instagrapi + Cloudflare Workers proxy.
Le proxy contourne le blocage des IPs Azure de GitHub Actions.
"""
import argparse
import os
import sys
import json

PROXY_URL = "https://instagram-proxy.azizkamaz951.workers.dev"

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

    # Proxy Cloudflare Workers pour contourner le blocage Meta sur IPs Azure
    cl.set_proxy(PROXY_URL)

    cl.set_settings({
        "cookies": {
            "sessionid": session_data.get("sessionid", ""),
            "csrftoken": session_data.get("csrftoken", ""),
        }
    })

    try:
        cl.get_timeline_feed()
    except Exception as e:
        print(f"Erreur connexion Instagram : {e}")
        sys.exit(1)

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
