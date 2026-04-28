# 🎯 Context-Aware API Fuzzer (GraphQL & REST)

Traditional fuzzers (like `ffuf` or `dirb`) are "dumb"—they throw massive wordlists at a target without understanding the application's logic. Modern web applications running on complex APIs (like GraphQL and REST) require structured data, rendering traditional fuzzing highly ineffective.

This project is a **Context-Aware API Fuzzer** written in Python. Instead of blind fuzzing, it ingests API documentation (OpenAPI/Swagger schemas or GraphQL Introspection queries), maps the endpoints, and dynamically generates valid and malicious payloads based on expected data types to test for modern API logic flaws.

## ✨ Features

* **Context-Aware Parsing:** Automatically parses OpenAPI 3.0 schemas and fetches GraphQL Introspection queries to build a map of the target API.
* **Mass Assignment Testing:** Ingests valid JSON schemas and automatically injects privileged fields (e.g., `{"is_admin": true}`, `{"role": "admin"}`) to test for improper object mapping.
* **BOLA / IDOR Testing:** Automatically swaps valid resource IDs with attacker-controlled IDs across parsed endpoints to test for Broken Object Level Authorization.
* **GraphQL Denial of Service (DoS):** Dynamically constructs deeply nested, circular GraphQL queries (e.g., `User -> Posts -> Author -> Posts`) to test for resource exhaustion vulnerabilities.

## 📂 Project Structure

```text
Context-Aware-API-Fuzzer-GraphQL-REST-/
├── fuzzer/
│   ├── __init__.py
│   ├── parsers.py          # OpenAPI and GraphQL schema extraction logic
│   └── payloads.py         # Generators for Mass Assignment, BOLA, and DoS payloads
├── fuzzer_cli.py           # Main Command Line Interface
└── README.md
```
🚀 Installation
1. Clone the repository:
```bash
git clone [https://github.com/JrBlackRose/Context-Aware-API-Fuzzer-GraphQL-REST-.git](https://github.com/JrBlackRose/Context-Aware-API-Fuzzer-GraphQL-REST-.git)
cd Context-Aware-API-Fuzzer-GraphQL-REST-
```
2. install the required dependencies
```bash
pip install requests
```
(Note: For future updates involving complex schema parsing, openapi-core and aiohttp may be required).

💻 Usage
The tool is operated via the command line interface (fuzzer_cli.py).

Fuzzing a REST API
To fuzz a REST API, you must provide the target URL and a path to the OpenAPI/Swagger JSON schema file.
```bash
python fuzzer_cli.py -t [http://api.target.com/v1](http://api.target.com/v1) -m rest --schema swagger.json
```
Fuzzing a GraphQL API
To fuzz a GraphQL API, you simply need to provide the target endpoint. The tool will automatically attempt an Introspection query to map the schema.

```bash
python fuzzer_cli.py -t [http://target.com/graphql](http://target.com/graphql) -m graphql
```
🗺️ Roadmap & Future Enhancements
This is currently a Minimum Viable Product (MVP). Future updates will include:

 - [ ] Asynchronous Requests: Implementing asyncio and aiohttp for high-speed concurrent payload delivery.

 - [ ] Automated Dependency Handling: Generating valid Object IDs programmatically before testing endpoints that require them (e.g., POST /users/{id}/comments).

 - [ ] Reporting Engine: Outputting clean JSON and HTML reports detailing tested endpoints, sent payloads, and HTTP response codes.

⚠️ Disclaimer
This tool is designed for educational purposes and for use by security professionals, penetration testers, and developers on systems they own or have explicit, written permission to test. Do not use this tool on targets without authorization. The author is not responsible for any misuse or damage caused by this program.
```bash
### One final housekeeping tip:
To make sure your project is fully reproducible, I recommend adding a `requirements.txt` file to your GitHub repository. Since you are using the `requests` library in `parsers.py`, simply create a file named `requirements.txt` in the root folder (next to `fuzzer_cli.py`) and add this single line to it:

```text
requests
```
