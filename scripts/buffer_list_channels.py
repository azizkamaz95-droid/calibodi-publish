"""
Introspect PostInputMetaData pour trouver les champs Instagram type.
"""
import os
import requests

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
            type_str = t.get('name') or t.get('kind', '')
            if t.get('ofType'):
                inner = t['ofType']
                type_str = f"{type_str}({inner.get('name') or inner.get('kind', '')})"
            print(f"  {f['name']}: {type_str}")
        return fields

    # Introspect PostInputMetaData to find Instagram type field
    meta_fields = introspect_type("PostInputMetaData")
    for f in meta_fields:
        name = f['name']
        if 'instagram' in name.lower() or 'type' in name.lower() or 'reel' in name.lower():
            print(f">>> FOUND in PostInputMetaData: {name}")

    # Also check InstagramPostMetaData if it exists
    ig_fields = introspect_type("InstagramPostMetaData")
    for f in ig_fields:
        print(f">>> InstagramPostMetaData field: {f['name']}")

    # Check InstagramMetaData
    ig2_fields = introspect_type("InstagramMetaData")
    for f in ig2_fields:
        print(f">>> InstagramMetaData field: {f['name']}")
