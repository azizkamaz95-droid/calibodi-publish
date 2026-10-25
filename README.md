# CaliBodi — Publication automatique vidéos

Publie automatiquement une vidéo sur **TikTok + YouTube + Instagram** en une seule action.

## Comment publier une vidéo

1. Crée un fichier `videos/metadata.json` :
```json
{
  "title": "Ton titre ici",
  "description": "Ta description ici\n\nhttps://calibodi.com"
}
```

2. Ajoute ta vidéo : `videos/mavideo.mp4`

3. Push sur GitHub :
```bash
git add videos/
git commit -m "Nouvelle vidéo : titre"
git push
```

4. GitHub Actions publie automatiquement sur toutes les plateformes ✅

---

## Configuration initiale (une seule fois)

### GitHub Secrets à configurer
Vas dans **Settings → Secrets → Actions** de ce repo et ajoute :

| Secret | Description |
|--------|-------------|
| `TIKTOK_SESSION_ID` | Cookie `sessionid` de TikTok |
| `YOUTUBE_TOKEN_JSON` | Token OAuth YouTube (JSON) |
| `INSTAGRAM_SESSION_JSON` | Session Instagram (JSON) |

### Obtenir les cookies

**TikTok `sessionid` :**
1. Connecte-toi sur tiktok.com dans Chrome
2. F12 → Application → Cookies → tiktok.com
3. Copie la valeur de `sessionid`

**Instagram session :**
1. Connecte-toi sur instagram.com dans Chrome
2. F12 → Application → Cookies → instagram.com
3. Copie `sessionid` et `csrftoken`

**YouTube token :**
→ Voir guide dans `/docs/youtube-setup.md`
