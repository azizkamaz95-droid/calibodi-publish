"""
Upload video vers TikTok via Buffer GraphQL API.
"""
import argparse
import os
import sys
import requests

BUFFER_GRAPHQL = "https://api.buffer.com/graphql"

def upload(video_path: str, title: str, description: str):
    api_key = os.environ.get("BUFFER_API_KEY")
    channel_id = os.environ.get("BUFFER_CHANNEL_ID")

    if not api_key or not channel_id:
        print("BUFFER_API_KEY ou BUFFER_CHANNEL_ID manquant")
        sys.exit(1)

    video_name = os.path.basename(video_path)
    video_url = f"https://raw.githubusercontent.com/azizkamaz95-droid/calibodi-publish/main/videos/{video_name}"
    caption = f"{title}\n\n{description}\n\n#CaliBodi #fitness #workout #squat"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    mutation = """
    mutation CreatePost($input: CreatePostInput!) {
      createPost(input: $input) {
        post {
          id
          status
        }
        userErrors {
          message
        }
      }
    }
    """

    variables = {
        "input": {
            "channelId": channel_id,
            "text": caption[:2200],
            "media": [
                {"url": video_url, "type": "video"}
            ],
            "timing": {"publishNow": True},
        }
    }

    resp = requests.post(
        BUFFER_GRAPHQL,
        headers=headers,
        json={"query": mutation, "variables": variables},
    )

    if resp.status_code != 200:
        print(f"Erreur HTTP Buffer : {resp.status_code} {resp.text}")
        sys.exit(1)

    result = resp.json()
    errors = result.get("data", {}).get("createPost", {}).get("userErrors", [])
    if errors:
        print(f"Erreur Buffer : {errors}")
        sys.exit(1)

    post = result.get("data", {}).get("createPost", {}).get("post", {})
    print(f"TikTok Buffer publie : id={post.get('id')} status={post.get('status')}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--description", default="")
    args = parser.parse_args()
    upload(args.video, args.title, args.description)
