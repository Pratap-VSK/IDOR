# 🏥 IDOR Vulnerability Lab & Automated Scanner

A complete, pure-Python cybersecurity laboratory designed to demonstrate the mechanics of Insecure Direct Object Reference (IDOR) vulnerabilities, automated exploitation, and secure remediation. Built for educational purposes and penetration testing practice.

## 🚀 Project Overview

This project consists of a two-part architecture:
1. **The Vulnerable Target:** A mock healthcare API built with FastAPI that issues session tokens but fails to implement proper object-level access controls.
2. **The Attacker Tool:** An automated Python exploitation script that brute-forces user IDs to extract highly sensitive PII and medical records belonging to other users.

## 🛠️ Tech Stack

* **Backend API:** Python, FastAPI, Uvicorn
* **Database:** SQLite (Built-in)
* **Automation/Exploitation:** Python `requests` library

## 📁 Architecture

```text
IDOR-System/
├── backend/
│   ├── database.py         # Initializes SQLite DB with mock users & sensitive records
│   ├── vulnerable_api.py   # The FastAPI server containing the IDOR flaw
├── attacker/
│   ├── idor_scanner.py     # Automated script to exploit the IDOR vulnerability
├── main.py                 # Multi-process launcher for the lab environment
└── requirements.txt        # Project dependencies

```
⚙️ Installation & Setup
Clone this repository to your local machine.

Ensure Python 3.8+ is installed.

Install the required dependencies:

```
pip install -r requirements.txt
```
🎯 How to Run the Lab
1. Start the Target API:
Run the launcher script to initialize the database and start the API server on localhost:8001.

```
python main.py
```

2. Launch the Automated Attack:
Open a new terminal window and execute the attacker script. The script will log in as a low-privileged user (john) and iterate through object IDs to steal unauthorized data.
```
Bash
python attacker/idor_scanner.py
```
🔓 The Vulnerability (The Attack)
In the original vulnerable state, the API endpoint /api/records/{user_id} verified that an authorization token was present, but it failed to verify ownership.
```
Python
# VULNERABLE CODE SNIPPET
@app.get("/api/records/{user_id}")
def get_record(user_id: int, authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Not logged in")
    
    # ❌ Flaw: The server fetches the record strictly based on the URL parameter 
    # without checking if the requested user_id belongs to the provided token.
    cursor.execute("SELECT * FROM medical_records WHERE user_id = ?", (user_id,))
Because of this missing access control check, the attacker script successfully extracted Admin and Alice's sensitive medical records just by changing the user_id integer in the API request.
```
🛡️ The Remediation (The Patch)
To secure the endpoint, a strict Access Control Check was implemented. The server now decrypts the session token, identifies the true owner of the request, and explicitly blocks access if the requested object ID does not match the token owner's actual ID (unless they are an admin).
```
Python
# SECURE PATCH SNIPPET
# 1. Identify the user from the token
username = authorization.replace("_session", "") 

# 2. Look up the logged-in user's actual database ID
cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
logged_in_user = cursor.fetchone()
actual_user_id = logged_in_user[0]

# 3. Block access if the requested ID doesn't match their actual ID
if actual_user_id != user_id and username != 'admin':
    raise HTTPException(status_code=403, detail="Forbidden: You can only access your own records")
After applying this patch, the attacker script receives a 403 Forbidden response for any unauthorized enumeration attempts.
```
⚠️ Disclaimer
This project is strictly for educational and portfolio purposes. Do not use these scripts against systems you do not own or have explicit permission to test.

<FollowUp label="Agla project?" query="Aapka IDS aur IDOR lab dono successfully complete ho chuke hain. Kya hum ab kisi naye vulnerability lab par kaam shuru karein, jaise Command Injection ya Cross-Site Request Forgery (CSRF)?"/>
