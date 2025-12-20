import os
import sys
import subprocess
import time
import shutil

def run_command(command, description):
    """Helper to run shell commands and handle errors."""
    print(f"\n[STEP] {description}...")
    try:
        # shell=True is required for Windows commands
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f" Warning: Command failed or service already running.")
        print(f"   Details: {e.stderr.strip()}")
        return False

def check_venv():
    """Checks if the Virtual Environment is active."""
    # If sys.prefix (current env) is same as base_prefix (system python), we aren't in venv
    if sys.prefix == sys.base_prefix:
        print("\n CRITICAL ERROR: Virtual Environment is NOT active.")
        print("   Please run: venv\\Scripts\\activate")
        print("   Then run this script again.")
        sys.exit(1)
    print(" Virtual Environment is active.")

def manage_docker():
    """Checks and starts the Docker container."""
    # Check if container is running
    check_cmd = "docker ps --filter \"name=taxi-db\" --format \"{{.Status}}\""
    result = subprocess.run(check_cmd, shell=True, capture_output=True, text=True)
    
    if "Up" in result.stdout:
        print("Docker Database (taxi-db) is already running.")
    else:
        print("waking up Docker Database...")
        run_command("docker start taxi-db", "Starting 'taxi-db' container")
        time.sleep(2) # Give it a moment to initialize

def check_ollama():
    """Checks if Ollama is responsive."""
    # We check if 'ollama' command exists and can list models
    if not shutil.which("ollama"):
        print("Error: Ollama is not installed or not in PATH.")
        return

    print("Checking AI Engine (Ollama)...")
    try:
        # Try to list models to see if server is up
        subprocess.run("ollama list", shell=True, check=True, capture_output=True)
        print("Ollama is running.")
    except subprocess.CalledProcessError:
        print("Ollama seems to be stopped.")
        print("   Attempting to start Ollama (check your system tray if this hangs)...")
        # Trying to launch the app (Windows specific)
        subprocess.Popen("ollama app", shell=True)
        time.sleep(3)

def main_menu():
    print("\n" + "="*40)
    print("LOGISTICS PLATFORM LAUNCHER")
    print("="*40)
    print("1. Run API Backend (FastAPI + Swagger)")
    print("2. Run AI Agent (Phi-3 / Qwen)")
    print("0. Exit")
    
    choice = input("\n Select an option (0-2): ")
    
    if choice == "1":
        print("\n Launching API... (Press Ctrl+C to stop)")
        print("   Swagger UI will be at: http://127.0.0.1:8000/docs")
        subprocess.run("python -m uvicorn main:app --reload", shell=True)
        
    elif choice == "2":
        print("\n Launching AI Agent... (Type 'exit' to quit agent)")
        subprocess.run("python agent.py", shell=True)
        
    elif choice == "0":
        print(" Exiting.")
        sys.exit(0)
    else:
        print("Invalid choice.")
        main_menu()

if __name__ == "__main__":
    # 1. Check Venv
    check_venv()
    
    # 2. Wake up Infrastructure
    manage_docker()
    check_ollama()
    
    # 3. Show Menu
    main_menu()