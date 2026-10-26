"""
Publie une video sur Instagram (Reel) via Buffer GraphQL API.
"""
import argparse
import os
import sys
import requests

BUFFER_GRAPHQL = "https://api.buffer.com/graphql"
INSTAGRAM_CHANNEL_ID = "6adfb6842f1f5ed648deb265"

def upload(video_path: str, title: str, description: str):
    api_key = os.environ.get("BUFFER_API_KEY")
    if not api_key:
        print("BUFFER_API_KEY manquant")
        sys.exit(1)
    video_name = os.path.basename(video_path)
    video_url = f"https://raw.githubusercontent.com/azizkamaz95-droid/calibodi-publish/main/videos/{video_name}"
    caption = f"{title}\n\n{description}\n\n#CaliBodi #fitness #workout #squat"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    mutation = """
    mutation CreatePost($input: CreatePostInput!) {
      createPost(input: $input) {
        ... on PostActionSuccess { post { id status } }
        ... on MutationError { message }
      }
    }
    """
    variables = {
        "input": {
            "channelId": INSTAGRAM_CHANNEL_ID,
            "text": caption[:2200],
            "mode": "shareNow",
            "schedulingType": "automatic",
            "needsApproval": False,
            "instagramPostType": "reel",
            "assets": [{"video": {"url": video_url}}],
        }
    }
    resp = requests.post(BUFFER_GRAPHQL, headers=headers, json={"query": mutation, "variables": variables})
    print(f"HTTP status: {resp.status_code}")
    if resp.status_code != 200:
        print(f"Erreur HTTP: {resp.text}")
        sys.exit(1)
    result = resp.json()
    if "errors" in result:
        print(f"Erreur GraphQL: {result['errors']}")
        sys.exit(1)
    data = result.get("data", {}).get("createPost", {})
    post = data.get("post")
    if post:
        print(f"Instagram publie via Buffer : id={post.get('id')} status={post.get('status')}")
    else:
        print(f"Resultat inattendu: {data}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--description", default="")
    args = parser.parse_args()
    upload(args.video, args.title, args.description)
