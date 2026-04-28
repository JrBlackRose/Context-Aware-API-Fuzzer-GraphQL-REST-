# fuzzer_cli.py
import argparse
from fuzzer.parsers import APIParser
from fuzzer.payloads import PayloadGenerator

def main():
    parser = argparse.ArgumentParser(description="Context-Aware API Fuzzer for REST & GraphQL")
    parser.add_argument("-t", "--target", required=True, help="Target API URL")
    parser.add_argument("-m", "--mode", choices=["rest", "graphql"], required=True, help="API Type")
    parser.add_argument("--schema", help="Path to OpenAPI JSON schema (for REST mode)")
    parser.add_argument("--auth", help="Authorization Bearer token")
    
    args = parser.parse_args()

    print(f"[*] Initializing fuzzer against {args.target}...")

    if args.mode == "rest":
        if not args.schema:
            print("[!] REST mode requires an OpenAPI schema file (--schema).")
            return
            
        parser_instance = APIParser(args.target)
        endpoints = parser_instance.parse_openapi(args.schema)
        print(f"[*] Parsed {len(endpoints)} actionable REST endpoints.")
        
        # Example Output for Mass Assignment
        print("[*] Generating Mass Assignment Payloads for testing...")
        base_user_data = {"username": "test_user", "email": "test@test.com"}
        malicious_payloads = PayloadGenerator.mass_assignment_payloads(base_user_data)
        
        for p in malicious_payloads:
            print(f"    -> [Simulated Attack] Sending: {p}")
            # In your actual fuzzer, you would use requests.post() here

    elif args.mode == "graphql":
        print("[*] Attempting to fetch GraphQL Introspection Schema...")
        parser_instance = APIParser(args.target)
        schema = parser_instance.fetch_graphql_introspection()
        
        if schema:
            print("[*] Introspection successful. Schema mapped.")
        else:
            print("[-] Introspection failed or is disabled.")

        print("[*] Generating deeply nested DoS query...")
        dos_query = PayloadGenerator.graphql_dos_query(target_node="users", nested_relation="posts", depth=15)
        print(f"    -> [Simulated Attack] Payload: \n{dos_query}")

if __name__ == "__main__":
    main()
