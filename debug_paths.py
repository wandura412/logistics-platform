import sys
import os

print(f"Python Executable: {sys.executable}")
print(f"Current Working Dir: {os.getcwd()}")

print("\nAttempting to import langchain...")
try:
    import langchain
    print(f"LangChain found at: {langchain.__file__}")
except ImportError as e:
    print(f"LangChain Import Failed: {e}")

print("\nAttempting to import langchain.chains...")
try:
    import langchain.chains
    print("langchain.chains imported successfully!")
except ImportError as e:
    print(f"langchain.chains Failed: {e}")
    print("   (This usually means 'langchain' package is missing, even if 'langchain-community' is there)")

print("\nChecking for shadowing...")
if os.path.exists("langchain.py"):
    print("CRITICAL WARNING: You have a file named 'langchain.py'. Rename it!")
else:
    print("No shadowing file found.")