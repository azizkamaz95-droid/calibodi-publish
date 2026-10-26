"""
File d'attente : cherche la publication planifiee la plus ancienne dont l'heure est passee.

Chaque publication est un dossier  queue/<nom>/  contenant une video .mp4 et un metadata.json :
  {"title": "...", "description": "...", "networks": ["youtube","tiktok","instagram","facebook"],
   "publish_at": "2026-10-27T17:00:00Z"}      <- heure UTC (18h a Paris en hiver = 17h UTC, en ete = 16h UTC)

Affiche  dir=<dossier>  si une publication est due (sinon rien), pour GitHub Actions ($GITHUB_OUTPUT).
Les dossiers dont l'heure n'est pas arrivee, ou sans .mp4, ou au metadata invalide, sont ignores et signales sur stderr.
"""
import glob
import json
import os
import sys
from datetime import datetime, timezone

now = datetime.now(timezone.utc)
due = []
for meta in sorted(glob.glob("queue/*/metadata.json")):
    d = os.path.dirname(meta)
    try:
        m = json.load(open(meta, encoding="utf-8"))
        at = datetime.fromisoformat(m["publish_at"].replace("Z", "+00:00"))
        if at.tzinfo is None:
            raise ValueError("publish_at sans fuseau : ajouter Z (UTC)")
        if not m.get("title") or not m.get("description"):
            raise ValueError("title ou description manquant")
    except Exception as e:
        print(f"ignore {d} : {e}", file=sys.stderr)
        continue
    if not glob.glob(os.path.join(d, "*.mp4")):
        print(f"ignore {d} : aucun .mp4", file=sys.stderr)
        continue
    if at <= now:
        due.append((at, d))
    else:
        print(f"en attente {d} : {at.isoformat()} (dans {(at - now)})", file=sys.stderr)
if due:
    due.sort()
    print(f"dir={due[0][1]}")
else:
    print("rien a publier", file=sys.stderr)
