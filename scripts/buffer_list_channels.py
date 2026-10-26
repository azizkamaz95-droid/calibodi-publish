"""
Liste les channels connectes dans Buffer pour recuperer les IDs.
"""
import os
import requests
import json

BUFFER_GRAPHQL = "https://api.buffer.com/graphql"
ORG_ID = "6adf9041be0f746ddf0f5707"

if __name__ == "__main__":
    api_key = os.environ.get("BUFFER_API_KEY")
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    query = """
    query {
      channels(input: { organizationId: "%s" }) {
        id
        name
        service
        serviceId
      }
    }
    """ % ORG_ID
    r = requests.post(BUFFER_GRAPHQL, headers=headers, json={"query": query})
    print("Channels response:")
    print(json.dumps(r.json(), indent=2))
