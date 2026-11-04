"""Diagnostic Buffer (lecture seule) : canaux connectes + champs attendus pour un Reel Facebook."""
import json
import os
import sys
import requests

GRAPHQL = "https://api.buffer.com/graphql"
key = os.environ.get("BUFFER_API_KEY")
if not key:
    print("BUFFER_API_KEY manquant"); sys.exit(1)
H = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}


def gql(q, v=None):
    r = requests.post(GRAPHQL, headers=H, json={"query": q, "variables": v or {}}, timeout=30)
    try:
        return r.json()
    except Exception:
        return {"http": r.status_code, "text": r.text[:300]}


def show_type(name):
    d = gql('query { __type(name: "%s") { kind inputFields { name type { name kind ofType { name kind ofType { name kind } } } } enumValues { name } } }' % name)
    t = (d.get("data") or {}).get("__type")
    print(f"\n== {name}:", "inconnu" if not t else "")
    if t:
        for f in t.get("inputFields") or []:
            ty = f["type"]; s = ty.get("name") or ty.get("kind")
            o = ty.get("ofType")
            while o:
                s += f"({o.get('name') or o.get('kind')})"; o = o.get("ofType")
            print("  ", f["name"], ":", s)
        for e in t.get("enumValues") or []:
            print("   valeur:", e["name"])


orgs = (((gql("query { account { organizations { id } } }").get("data") or {}).get("account") or {}).get("organizations")) or []
print("organisations:", orgs)
for o in orgs:
    for q in ('query($o: OrganizationId!) { channels(input: { organizationId: $o }) { id name service } }',
              'query($o: OrganizationId!) { channels(input: { organizationId: $o }) { id name service type } }'):
        d = gql(q, {"o": o["id"]})
        if d.get("data"):
            print("canaux:", json.dumps(d["data"], ensure_ascii=False)); break
        print("tentative sans succes:", json.dumps(d.get("errors") or d, ensure_ascii=False)[:300])
for n in ("CreatePostInput", "PostMetadataInput", "FacebookPostMetadataInput", "FacebookPostType"):
    show_type(n)
