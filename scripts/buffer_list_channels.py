"""
Liste les channels connectes dans Buffer pour recuperer les IDs.
"""
import os
import requests
import json

BUFFER_GRAPHQL = "https://api.buffer.com/graphql"

if __name__ == "__main__":
    api_key = os.environ.get("BUFFER_API_KEY")
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    query = """
    {
      channels {
        id
        name
        service
        serviceType
        serviceId
      }
    }
    """
    resp = requests.post(BUFFER_GRAPHQL, headers=headers, json={"query": query})
    print(json.dumps(resp.json(), indent=2))
