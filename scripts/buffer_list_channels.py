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

    # Recuperer l'organizationId via le currentUser
    r = requests.post(BUFFER_GRAPHQL, headers=headers, json={"query": "{ currentUser { id currentOrganization { id name } } }"})
    print("CurrentUser:", json.dumps(r.json(), indent=2))

    data = r.json().get("data", {})
    org_id = data.get("currentUser", {}).get("currentOrganization", {}).get("id")
    print(f"\nOrganization ID: {org_id}")

    if not org_id:
        print("Impossible de trouver l'organizationId")
        exit(1)

    # Lister les channels
    query = """
    query GetChannels($input: ChannelsInput!) {
      channels(input: $input) {
        id
        name
        service
        serviceId
      }
    }
    """
    resp = requests.post(BUFFER_GRAPHQL, headers=headers, json={"query": query, "variables": {"input": {"organizationId": org_id}}})
    print("\nChannels:", json.dumps(resp.json(), indent=2))
