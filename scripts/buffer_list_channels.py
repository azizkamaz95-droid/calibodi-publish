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

    # Introspect Account type pour trouver le champ org
    r = requests.post(BUFFER_GRAPHQL, headers=headers, json={"query": '{ __type(name: "Account") { fields { name type { name kind } } } }'})
    print("Account fields:")
    fields = r.json().get("data", {}).get("__type", {}).get("fields", [])
    for f in fields:
        print(f"  {f['name']}: {f['type']['name'] or f['type']['kind']}")

    # Query account
    r2 = requests.post(BUFFER_GRAPHQL, headers=headers, json={"query": "{ account { id email organizations { id name } } }"})
    print("\nAccount:", json.dumps(r2.json(), indent=2))
