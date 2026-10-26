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

    # D'abord introspect ChannelsInput pour connaitre les champs requis
    r = requests.post(BUFFER_GRAPHQL, headers=headers, json={"query": '{ __type(name: "ChannelsInput") { inputFields { name type { name kind ofType { name kind } } } } }'})
    print("ChannelsInput schema:", json.dumps(r.json(), indent=2))

    # Essai avec input vide
    query = """
    {
      channels(input: {}) {
        id
        name
        service
        serviceId
      }
    }
    """
    resp = requests.post(BUFFER_GRAPHQL, headers=headers, json={"query": query})
    print("\nChannels:", json.dumps(resp.json(), indent=2))
