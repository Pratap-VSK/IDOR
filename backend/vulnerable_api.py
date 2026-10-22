from fastapi import FastAPI, HTTPException, Header
import sqlite3
import os

app = FastAPI(title="Vulnerable Hospital API")
DB_PATH = os.path.join(os.path.dirname(__file__), 'hospital.db')

@app.get("/api/login")
def login(username: str):
    return {"token": f"{username}_session"}

@app.get("/api/records/{user_id}")
def get_record(user_id: int, authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Not logged in")
        
    # --- THE PATCH: Identify the User & Verify Ownership ---
    # 1. Extract the username from our mock token (e.g., "john_session" -> "john")
    username = authorization.replace("_session", "") 
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 2. Look up the logged-in user's actual database ID
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    logged_in_user = cursor.fetchone()
    
    if not logged_in_user:
        conn.close()
        raise HTTPException(status_code=401, detail="Invalid token")
        
    actual_user_id = logged_in_user[0]
    
    # 3. THE CORE FIX: Block access if the requested ID doesn't match their actual ID
    # (We also allow the 'admin' user to bypass this rule)
    if actual_user_id != user_id and username != 'admin':
        conn.close()
        raise HTTPException(status_code=403, detail="Forbidden: You can only access your own records")
    # ------------------------------------------------------
    
    # If the check passes, fetch and return the record
    cursor.execute("SELECT * FROM medical_records WHERE user_id = ?", (user_id,))
    record = cursor.fetchone()
    conn.close()
    
    if record:
        return {"user_id": record[1], "disease": record[2], "bill": record[3]}
    return {"error": "Record not found"}