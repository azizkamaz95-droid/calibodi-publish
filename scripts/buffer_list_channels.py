"""
Introspect CreatePostInput pour trouver les champs Instagram.
"""
import os
import requests
import json

BUFFER_GRAPHQL = "https://api.buffer.com/graphql"

if __name__ == "__main__":
    api_key = os.environ.get("BUFFER_API_KEY")
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    # Introspect CreatePostInput
    query = '{ __type(name: "CreatePostInput") { inputFields { name type { name kind ofType { name kind } } } } }'
    r = requests.post(BUFFER_GRAPHQL, headers=headers, json={"query": query})
    fields = r.json().get("data", {}).get("__type", {}).get("inputFields", [])
    print("CreatePostInput fields:")
    for f in fields:
        t = f['type']
        type_name = t.get('name') or t.get('kind')
        if t.get('ofType'):
            type_name = f"{type_name}({t['ofType'].get('name')})"
        print(f"  {f['name']}: {type_name}")
