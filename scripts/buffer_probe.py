"""Diagnostic Buffer (lecture seule) : valeurs possibles pour programmer un post a une heure precise."""
import os
import sys
import requests

GRAPHQL = "https://api.buffer.com/graphql"
key = os.environ.get("BUFFER_API_KEY")
if not key:
    print("BUFFER_API_KEY manquant"); sys.exit(1)
H = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}


def gql(q):
    return requests.post(GRAPHQL, headers=H, json={"query": q}, timeout=30).json()


for n in ("ShareMode", "SchedulingType", "DateTime"):
    d = gql('query { __type(name: "%s") { kind description enumValues { name description } } }' % n)
    t = (d.get("data") or {}).get("__type")
    print(f"\n== {n}:", t and t.get("kind"), (t or {}).get("description"))
    for e in (t or {}).get("enumValues") or []:
        print("   valeur:", e["name"], "-", e.get("description"))
d = gql('query { __type(name: "CreatePostInput") { inputFields { name description } } }')
for f in ((d.get("data") or {}).get("__type") or {}).get("inputFields") or []:
    print("  ", f["name"], "-", f.get("description"))
