# fuzzer/parsers.py
import requests
import json

class APIParser:
    def __init__(self, target_url):
        self.target_url = target_url

    def parse_openapi(self, schema_path):
        """
        Basic OpenAPI 3.0 parser to extract POST/PUT endpoints and their expected schemas.
        *Note for GitHub: You will want to expand this or use a library like `prance` to handle $refs*
        """
        try:
            with open(schema_path, 'r') as file:
                schema = json.load(file)
        except Exception as e:
            return f"Error loading schema: {e}"

        endpoints = []
        paths = schema.get('paths', {})
        
        for path, methods in paths.items():
            for method, details in methods.items():
                if method.lower() in ['post', 'put', 'patch']:
                    endpoints.append({
                        "path": path,
                        "method": method.upper(),
                        # In a full version, extract properties from the requestBody schema here
                        "requires_auth": "security" in details
                    })
        return endpoints

    def fetch_graphql_introspection(self):
        """
        Fetches the schema of a GraphQL endpoint to map out queries and mutations.
        """
        query = """
        query IntrospectionQuery {
            __schema {
                queryType { name }
                mutationType { name }
                types {
                    name
                    fields { name type { name kind } }
                }
            }
        }
        """
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.post(self.target_url, json={'query': query}, headers=headers)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch introspection: {e}")
            return None
