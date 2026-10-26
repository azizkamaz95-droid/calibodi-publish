"""
Verifie le statut des derniers posts Instagram dans Buffer.
"""
import os
import requests
import json

BUFFER_GRAPHQL = "https://api.buffer.com/graphql"
INSTAGRAM_CHANNEL_ID = "6adfb6842f1f5ed648deb265"

if __name__ == "__main__":
    api_key = os.environ.get("BUFFER_API_KEY")
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    # Lister les posts recents du channel Instagram
    query = """
    query {
      posts(input: { channelIds: [\"6adfb6842f1f5ed648deb265\"], limit: 5 }) {
        edges {
          node {
            id
            status
            text
            dueAt
            sentAt
            ... on SentPost { sentAt }
            ... on FailedPost { failure { code message } }
          }
        }
      }
    }
    """
    r = requests.post(BUFFER_GRAPHQL, headers=headers, json={"query": query})
    print(f"HTTP: {r.status_code}")
    data = r.json()
    if "errors" in data:
        print(f"Erreurs GraphQL: {json.dumps(data['errors'], indent=2)}")
    else:
        print(json.dumps(data, indent=2))
