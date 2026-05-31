import os
from pathlib import Path
from dotenv import load_dotenv

print("--- 🔍 STARTING DIAGNOSTIC CHECK ---")

# 1. Check where Python thinks it is running from
cwd = os.getcwd()
print(f"1. Current Working Directory: {cwd}")

# 2. Check if the file actually exists in this folder
env_file = Path(cwd) / ".env"
print(f"2. Looking for .env file at: {env_file}")
print(f"   Does it exist? {'✅ YES' if env_file.exists() else '❌ NO'}")

# 3. Try to load it explicitly
success = load_dotenv(dotenv_path=env_file)
print(f"3. Did python-dotenv successfully read the file? {'✅ YES' if success else '❌ NO'}")

# 4. Read the key
api_key = os.environ.get("GEMINI_API_KEY")

print("\n--- 📊 FINAL RESULT ---")
if api_key:
    print(f"🚀 Success! Key found. Starts with: {api_key[:4]}...")
else:
    print("❌ API Key is still None.")
print("-----------------------------------")