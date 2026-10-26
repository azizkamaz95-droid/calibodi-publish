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

    # Introspect Query root pour voir les champs disponibles
    r = requests.post(BUFFER_GRAPHQL, headers=headers, json={"query": '{ __type(name: "Query") { fields { name type { name kind } } } }'})
    fields = r.json().get("data", {}).get("__type", {}).get("fields", [])
    print("Query fields disponibles:")
    for f in fields:
        print(f"  {f['name']}: {f['type']['name'] or f['type']['kind']}")
