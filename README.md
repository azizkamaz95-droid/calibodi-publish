# CaliBodi — Publication automatique vidéos

Publie automatiquement une vidéo sur **TikTok + YouTube Shorts + Instagram Reels + Facebook Reels** en un seul push GitHub.

---

## 🚀 Publier une vidéo (usage quotidien)

1. Ajoute ta vidéo : `videos/mavideo.mp4`

2. Crée `videos/metadata.json` :
```json
{
  "title": "Squat parfait — CaliBodi 💪",
  "description": "Apprends le squat parfait avec Calix, ton coach IA.\n\n📲 Télécharge CaliBodi gratuitement :\nhttps://calibodi.com\n\n#CaliBodi #fitness #workout #coach"
}
```

3. Push :
```bash
git add videos/
git commit -m "Nouvelle vidéo : squat"
git push
```

4. ✅ GitHub Actions publie sur les 4 plateformes automatiquement.

---

## ⚙️ Configuration initiale (une seule fois)

### Secrets GitHub à ajouter
**Settings → Secrets and variables → Actions → New repository secret**

| Secret | Plateforme | Comment l'obtenir |
|--------|-----------|-------------------|
| `TIKTOK_SESSION_ID` | TikTok | Cookie `sessionid` → voir ci-dessous |
| `YOUTUBE_TOKEN_JSON` | YouTube | Token OAuth → voir ci-dessous |
| `INSTAGRAM_SESSION_JSON` | Instagram | Session JSON → voir ci-dessous |
| `FACEBOOK_PAGE_TOKEN` | Facebook | Token page → voir ci-dessous |
| `FACEBOOK_PAGE_ID` | Facebook | ID de ta page Facebook |

---

### 🎵 TikTok — obtenir `sessionid`
1. Connecte-toi sur [tiktok.com](https://tiktok.com) dans Chrome
2. F12 → **Application** → **Cookies** → `https://www.tiktok.com`
3. Copie la valeur de `sessionid`

---

### 📺 YouTube — obtenir le token OAuth
1. Va sur [Google Cloud Console](https://console.cloud.google.com)
2. Crée un projet → Active **YouTube Data API v3**
3. Crée des identifiants OAuth 2.0 (type : application bureau)
4. Télécharge le JSON → lance `python scripts/youtube_auth.py`
5. Copie le contenu du fichier `token.json` généré

---

### 📸 Instagram — obtenir la session
1. Connecte-toi sur [instagram.com](https://instagram.com) dans Chrome
2. F12 → **Application** → **Cookies** → `https://www.instagram.com`
3. Copie `sessionid` et `csrftoken`
4. Formate en JSON :
```json
{"sessionid": "xxx", "csrftoken": "yyy"}
```

---

### 👍 Facebook — obtenir le token de page
1. Va sur [developers.facebook.com](https://developers.facebook.com)
2. Crée une app → ajoute le produit **Pages API**
3. Génère un **Page Access Token** pour ta page CaliBodi
4. Récupère l'**ID de ta page** (visible dans les paramètres de la page)
