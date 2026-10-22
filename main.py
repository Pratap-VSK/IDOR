import subprocess
import sys
import os

def start_lab():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    
    print("[*] Initializing Database...")
    subprocess.run([sys.executable, os.path.join(base_dir, "backend", "database.py")])
    
    print("[*] Starting Patched API Server on port 8001...")
    api_process = subprocess.Popen([sys.executable, "-m", "uvicorn", "backend.vulnerable_api:app", "--host", "127.0.0.1", "--port", "8001"])
    
    print("[*] API is running. Press Ctrl+C here to stop the server properly.")
    
    try:
        api_process.wait()
    except KeyboardInterrupt:
        print("\n[*] Shutting down server gracefully...")
        api_process.terminate()

if __name__ == "__main__":
    start_lab()