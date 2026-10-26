"""
Introspection du schema Buffer GraphQL pour trouver les valeurs correctes.
"""
import os
import requests
import json

BUFFER_GRAPHQL = "https://api.buffer.com/graphql"

def introspect(type_name):
    api_key = os.environ.get("BUFFER_API_KEY")
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    query = f'{{ __type(name: "{type_name}") {{ kind enumValues {{ name }} inputFields {{ name type {{ name kind ofType {{ name kind ofType {{ name kind }} }} }} }} }} }}'
    resp = requests.post(BUFFER_GRAPHQL, headers=headers, json={"query": query})
    print(f"\n=== {type_name} ===")
    print(json.dumps(resp.json(), indent=2))

if __name__ == "__main__":
    for t in ["AssetInput"]:
        introspect(t)
