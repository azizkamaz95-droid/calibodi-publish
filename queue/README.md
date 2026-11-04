# File d'attente

Un dossier par video : `queue/2026-10-27-nom/` avec la video `.mp4`, un `metadata.json` et, si on veut, une miniature `miniature.jpg` (1080x1920) envoyee avec la video a Buffer (Instagram, Facebook) :

```json
{
  "title": "Titre",
  "description": "Description (hashtags en fin de texte)",
  "networks": ["youtube", "tiktok", "instagram", "facebook"],
  "publish_at": "2026-10-27T17:00:00Z"
}
```

`publish_at` est en UTC : 18h a Paris = 17h UTC en hiver, 16h UTC en ete.
Toutes les 5 minutes, `scheduled.yml` deplace la video due dans `videos/` et lance `publish.yml`.
