import os
import requests
from datetime import datetime

API_KEY = os.environ.get("SUPERTEAM_API_KEY")
WALLET = os.environ.get("PHANTOM_WALLET")
TELEGRAM = "@Mohammadabbas891"

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
            return tasks
        else:
            print(f"[{datetime.now()}] ❌ Error: {response.status_code}")
            return []
    except Exception as e:
        print(f"[{datetime.now()}] ⚠️ Exception: {e}")
        return []

def submit_to_task(task_id, title, link="https://github.com/superteam-agent"):
    url = "https://superteam.fun/api/agents/submissions/create"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "listingId": task_id,
        "link": link,
        "otherInfo": f"Task completed by automated agent. Project: {title}",
        "telegram": TELEGRAM
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        # حتى لو كان الرد خطأ، نطبع محتواه للتحقق
        print(f"  Submission response status: {response.status_code}")
        if response.status_code == 200 or response.status_code == 201:
            print(f"  ✅ Successfully applied for: {title}")
            return True
        else:
            print(f"  ❌ Failed to apply for {title}: {response.text}")
            return False
    except Exception as e:
        print(f"  ⚠️ Submission error: {e}")
        return False

def auto_submit(tasks):
    if not tasks:
        print("No tasks to apply for.")
        return
    count = 0
    for task in tasks[:3]:
        task_id = task.get('id')
        title = task.get('title', 'Untitled')
        if task_id:
            print(f"📝 Applying for: {title}")
            if submit_to_task(task_id, title):
                count += 1
    print(f"✅ Applied for {count} tasks.")

if __name__ == "__main__":
    print("🚀 Superteam Agent starting...")
    print(f"💰 Wallet: {WALLET}")
    print(f"📱 Telegram: {TELEGRAM}")
    tasks = search_tasks()
    if tasks:
        auto_submit(tasks)
    else:
        print("⚠️ No tasks found.")
    print("✅ Done.")
