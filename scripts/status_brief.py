"""Statut concis des publications (lecture seule) : peu de lignes, pour limiter ce qui revient dans la conversation.

Affiche, par reseau Buffer, les 2 derniers posts (statut, heure d'envoi, debut du texte, erreur eventuelle),
puis les 3 dernieres executions de publish.yml avec l'adresse YouTube quand elle existe."""
import os
import re
import sys
import requests

GRAPHQL = "https://api.buffer.com/graphql"
key = os.environ.get("BUFFER_API_KEY")
if not key:
    print("BUFFER_API_KEY manquant"); sys.exit(1)
H = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
CHANNELS = {"facebook": "6aeb4096e29c69a1715d9234", "instagram": "6adfb6842f1f5ed648deb265", "tiktok": "6adf90d62f1f5ed648dc301e"}


def gql(q, v=None):
    return requests.post(GRAPHQL, headers=H, json={"query": q, "variables": v or {}}, timeout=30).json()


org = gql("query { account { organizations { id } } }")["data"]["account"]["organizations"][0]["id"]
Q = ("query($o: OrganizationId!, $c: [ChannelId!]) { posts(input: { organizationId: $o, filter: { channelIds: $c } }, first: 2) "
     "{ edges { node { id status text sentAt dueAt error { message } } } } }")
print("== BUFFER ==")
for name, cid in CHANNELS.items():
    r = gql(Q, {"o": org, "c": [cid]})
    for e in (((r.get("data") or {}).get("posts") or {}).get("edges") or []):
        n = e["node"]
        err = (n.get("error") or {}).get("message")
        print("%-9s %-8s %s | %s%s" % (name, n["status"], (n.get("sentAt") or n.get("dueAt") or "")[:16], (n.get("text") or "")[:38].replace("\n", " "), (" | ERREUR: " + err[:80]) if err else ""))
    if r.get("errors"):
        print(name, "erreur GraphQL:", str(r["errors"])[:120])

tok, repo = os.environ.get("GITHUB_TOKEN"), os.environ.get("GITHUB_REPOSITORY")
if tok and repo:
    GH = {"Authorization": "Bearer " + tok, "Accept": "application/vnd.github+json"}
    print("== PUBLISH.YML (3 dernieres executions) ==")
    runs = requests.get(f"https://api.github.com/repos/{repo}/actions/workflows/publish.yml/runs?per_page=3", headers=GH, timeout=30).json().get("workflow_runs", [])
    for run in runs:
        yt = ""
        jobs = requests.get(run["jobs_url"], headers=GH, timeout=30).json().get("jobs", [])
        for j in jobs:
            log = requests.get(f"https://api.github.com/repos/{repo}/actions/jobs/{j['id']}/logs", headers=GH, timeout=60)
            m = re.search(r"YouTube publie : (\S+)", log.text if log.ok else "")
            if m:
                yt = " | YouTube : " + m.group(1)
        print("#%s %s %s | %s%s" % (run["run_number"], run["status"] if run["status"] != "completed" else run["conclusion"], run["created_at"][:16], run["head_commit"]["message"][:55].replace("\n", " "), yt))
