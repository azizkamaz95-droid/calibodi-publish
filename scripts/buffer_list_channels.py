"""
Introspect InstagramPostMetadataInput pour trouver le champ type.
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
        data = r.json()
        if not data or not data.get("data") or not data["data"].get("__type"):
            print(f"{type_name}: type inconnu ou null")
            return []
        fields = data["data"]["__type"].get("inputFields", [])
        print(f"\n{type_name} fields:")
        for f in fields:
            t = f['type']
            type_str = t.get('name') or t.get('kind', '')
            if t.get('ofType'):
                inner = t['ofType']
                type_str = f"{type_str}({inner.get('name') or inner.get('kind', '')})"
            print(f"  {f['name']}: {type_str}")
        return fields

    # Introspect InstagramPostMetadataInput
    ig_fields = introspect_type("InstagramPostMetadataInput")
    for f in ig_fields:
        print(f">>> field: {f['name']}")
        # Check enum values for type fields
        t = f['type']
        type_name = t.get('name') or (t.get('ofType') or {}).get('name')
        if type_name:
            enum_q = '{  __type(name: "' + type_name + '") { enumValues { name } } }'
            r2 = requests.post(BUFFER_GRAPHQL, headers=headers, json={"query": enum_q})
            d2 = r2.json()
            enum_vals = (d2.get("data") or {}).get("__type") or {}
            if enum_vals.get("enumValues"):
                print(f"    enum values: {[e['name'] for e in enum_vals['enumValues']]}")
