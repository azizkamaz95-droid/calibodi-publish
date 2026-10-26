"""
Introspect CreatePostInput pour trouver les champs Instagram type.
"""
import os
import requests
import json

BUFFER_GRAPHQL = "https://api.buffer.com/graphql"

if __name__ == "__main__":
    api_key = os.environ.get("BUFFER_API_KEY")
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    def introspect_type(type_name):
        query = '{  __type(name: "' + type_name + '") { inputFields { name type { name kind ofType { name kind ofType { name kind } } } } } }'
        r = requests.post(BUFFER_GRAPHQL, headers=headers, json={"query": query})
        fields = r.json().get("data", {}).get("__type", {}).get("inputFields", [])
        print(f"\n{type_name} fields:")
        for f in fields:
            t = f['type']
            type_name2 = t.get('name') or t.get('kind', '')
            if t.get('ofType'):
                inner = t['ofType']
                type_name2 = f"{type_name2}({inner.get('name') or inner.get('kind', '')})"
            print(f"  {f['name']}: {type_name2}")
        return fields

    fields = introspect_type("CreatePostInput")
    # Look for instagram-related fields
    for f in fields:
        name = f['name']
        if 'instagram' in name.lower() or 'type' in name.lower():
            print(f">>> FOUND: {name}")
