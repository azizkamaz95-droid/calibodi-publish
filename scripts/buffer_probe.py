"""Diagnostic Buffer (lecture seule) : champs lies aux miniatures / couvertures dans le schema."""
import json
import os
import sys
import requests

GRAPHQL = "https://api.buffer.com/graphql"
key = os.environ.get("BUFFER_API_KEY")
if not key:
    print("BUFFER_API_KEY manquant"); sys.exit(1)
H = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}


def gql(q):
    r = requests.post(GRAPHQL, headers=H, json={"query": q}, timeout=30)
    return r.json()


d = gql("query { __schema { types { name kind } } }")
names = [t["name"] for t in d["data"]["__schema"]["types"] if t["kind"] == "INPUT_OBJECT"]
focus = [n for n in names if any(k in n.lower() for k in ("asset", "video", "thumb", "cover", "tiktok", "instagram", "facebook", "metadata"))]
print("types d'entree concernes:", focus)
for n in focus:
    t = (gql('query { __type(name: "%s") { inputFields { name type { name kind ofType { name kind ofType { name kind } } } } } }' % n).get("data") or {}).get("__type")
    if not t:
        continue
    print(f"\n== {n}")
    for f in t["inputFields"] or []:
        ty = f["type"]; s = ty.get("name") or ty.get("kind"); o = ty.get("ofType")
        while o:
            s += f"({o.get('name') or o.get('kind')})"; o = o.get("ofType")
        print("  ", f["name"], ":", s)
