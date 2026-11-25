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


# ---------------------------------------------------------------------------------------------------------------------------
# 2026-11-22 : pourquoi Instagram refuse toutes les videos depuis le 18 novembre ? (lecture seule, ne publie rien)
# Affiche les derniers posts Instagram en erreur avec le message d'erreur renvoye par Buffer / Instagram, et l'etat du canal.
# ---------------------------------------------------------------------------------------------------------------------------
import json

INSTAGRAM_CHANNEL_ID = "6adfb6842f1f5ed648deb265"


def tname(t):
    while t and not t.get("name") and t.get("ofType"):
        t = t["ofType"]
    return (t or {}).get("name"), (t or {}).get("kind")


def fields_of(type_name):
    d = gql('query { __type(name: "%s") { kind fields { name type { name kind ofType { name kind ofType { name kind ofType { name kind } } } } } possibleTypes { name } } }' % type_name)
    t = (d.get("data") or {}).get("__type") or {}
    return t


print("\n\n===== INSTAGRAM : diagnostic des posts en erreur =====")
orgs = gql("query { account { organizations { id } } }")
org = (((orgs.get("data") or {}).get("account") or {}).get("organizations") or [{}])[0].get("id")
print("organisation:", org)
post_t = fields_of("Post")
print("type Post:", post_t.get("kind"), "possibleTypes:", [p["name"] for p in post_t.get("possibleTypes") or []])
post_fields = {f["name"]: tname(f["type"]) for f in post_t.get("fields") or []}
print("champs de Post:", json.dumps(post_fields))
# champs utiles : tout ce qui ressemble a une erreur / un echec
sel = ["id", "status", "text", "dueAt", "createdAt"]
for n, (tn, kind) in post_fields.items():
    low = n.lower()
    if any(k in low for k in ("error", "fail", "reason", "problem")):
        if kind in ("SCALAR", "ENUM"):
            sel.append(n)
        else:
            sub = fields_of(tn)
            subs = [s["name"] for s in sub.get("fields") or [] if tname(s["type"])[1] in ("SCALAR", "ENUM")]
            if subs:
                sel.append("%s { %s }" % (n, " ".join(subs)))
sel = [s for s in sel if s.split()[0] in post_fields or s in ("id", "status", "text")]
print("champs demandes:", sel)
q = ("query($o: OrganizationId!, $c: [ChannelId!]) { posts(input: { organizationId: $o, filter: { channelIds: $c } }, first: 6) "
     "{ edges { node { %s } } } }" % " ".join(sel))
res = gql(q.replace("$c: [ChannelId!]", "$c: [ChannelId!]")) if False else requests.post(GRAPHQL, headers=H, json={"query": q, "variables": {"o": org, "c": [INSTAGRAM_CHANNEL_ID]}}, timeout=30).json()
print(json.dumps(res, ensure_ascii=False, indent=1)[:6000])
# etat du canal (connexion, erreurs, besoin de reconnexion)
ch_t = fields_of("Channel")
ch_fields = {f["name"]: tname(f["type"]) for f in ch_t.get("fields") or []}
print("\nchamps de Channel:", json.dumps(ch_fields))
csel = [n for n, (tn, kind) in ch_fields.items() if kind in ("SCALAR", "ENUM")]
cq = 'query($o: OrganizationId!) { channels(input: { organizationId: $o }) { %s } }' % " ".join(csel[:30])
cres = requests.post(GRAPHQL, headers=H, json={"query": cq, "variables": {"o": org}}, timeout=30).json()
print(json.dumps(cres, ensure_ascii=False, indent=1)[:5000])

# --- TikTok : statut des derniers posts (lecture seule) ---
TIKTOK_CHANNEL_ID = "6adf90d62f1f5ed648dc301e"
print("\n\n===== TIKTOK : derniers posts =====")
q2 = ("query($o: OrganizationId!, $c: [ChannelId!]) { posts(input: { organizationId: $o, filter: { channelIds: $c } }, first: 4) "
      "{ edges { node { id status text dueAt sentAt error { message rawError } } } } }")
r2 = requests.post(GRAPHQL, headers=H, json={"query": q2, "variables": {"o": org, "c": [TIKTOK_CHANNEL_ID]}}, timeout=30).json()
for e in (((r2.get("data") or {}).get("posts") or {}).get("edges") or []):
    n = e["node"]
    print("TIKTOK", n["id"], "statut=%s" % n["status"], "dueAt=%s" % n.get("dueAt"), "sentAt=%s" % n.get("sentAt"), "|", (n.get("text") or "")[:40].replace("\n", " "), "| erreur:", (n.get("error") or {}).get("message"))
if r2.get("errors"):
    print("erreurs GraphQL:", r2["errors"])
