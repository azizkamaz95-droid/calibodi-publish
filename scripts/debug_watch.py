"""
Diagnostic pendant l'attente avant nettoyage : toutes les 45 s pendant N minutes, affiche
 - l'etat de l'URL publique de la video (code HTTP, type, taille) : Buffer et Make la telechargent a cet endroit ;
 - les derniers posts Buffer (Instagram, TikTok) avec leur statut et, en cas d'echec, le code et le message d'erreur.
Ne modifie rien et ne publie rien. usage : debug_watch.py <nom_video> <minutes>
"""
import json
import os
import sys
import time

import requests

GRAPHQL = "https://api.buffer.com/graphql"
CHANNELS = {"instagram": "6adfb6842f1f5ed648deb265", "tiktok": os.environ.get("BUFFER_CHANNEL_ID", "")}
BASE = "https://raw.githubusercontent.com/azizkamaz95-droid/calibodi-publish/main/videos/"
QUERY = """
query($ids: [ChannelId!]) {
  posts(input: { channelIds: $ids, limit: 2 }) {
    edges { node { id status text ... on FailedPost { failure { code message } } } }
  }
}
"""


def check_url(name):
    try:
        r = requests.head(BASE + name, allow_redirects=True, timeout=20)
        print(f"  URL {name}: HTTP {r.status_code} · {r.headers.get('content-type')} · {r.headers.get('content-length')} octets")
    except Exception as e:
        print(f"  URL {name}: erreur {e}")


def check_buffer(label, cid):
    key = os.environ.get("BUFFER_API_KEY")
    if not key or not cid:
        print(f"  Buffer {label}: cle ou canal manquant")
        return
    r = requests.post(GRAPHQL, headers={"Authorization": f"Bearer {key}"}, json={"query": QUERY, "variables": {"ids": [cid]}}, timeout=30)
    d = r.json()
    if "errors" in d:
        print(f"  Buffer {label}: erreur GraphQL {json.dumps(d['errors'])[:400]}")
        return
    for e in d["data"]["posts"]["edges"]:
        n = e["node"]
        fail = n.get("failure")
        print(f"  Buffer {label}: post {n['id']} statut={n['status']}" + (f" ECHEC {fail}" if fail else ""))


if __name__ == "__main__":
    video, minutes = sys.argv[1], float(sys.argv[2])
    end = time.time() + minutes * 60
    while True:
        print(f"--- {time.strftime('%H:%M:%S')}")
        for name in (video, "instagram_reel.mp4"):
            check_url(name)
        for label, cid in CHANNELS.items():
            try:
                check_buffer(label, cid)
            except Exception as e:
                print(f"  Buffer {label}: erreur {e}")
        sys.stdout.flush()
        if time.time() >= end:
            break
        time.sleep(45)
