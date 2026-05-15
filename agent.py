import os
import requests
from datetime import datetime

API_KEY = os.environ.get("SUPERTEAM_API_KEY")
WALLET = os.environ.get("PHANTOM_WALLET")

def search_tasks():
    url = "https://superteam.fun/api/agents/listings/live"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            tasks = response.json()
            print(f"[{datetime.now()}] ✅ Found {len(tasks)} tasks")
            for task in tasks[:5]:
                print(f"  - {task.get('title', 'No title')}: {task.get('rewardAmount', '?')} USDC")
        else:
            print(f"[{datetime.now()}] ❌ Error: {response.status_code}")
    except Exception as e:
        print(f"[{datetime.now()}] ⚠️ Exception: {e}")

if __name__ == "__main__":
    print("🚀 Superteam Agent starting...")
    print(f"💰 Wallet: {WALLET}")
    search_tasks()
    print("✅ Done.")
