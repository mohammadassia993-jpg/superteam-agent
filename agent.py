import os
import requests
from datetime import datetime

API_KEY = os.environ.get("SUPERTEAM_API_KEY")
WALLET = os.environ.get("PHANTOM_WALLET")
TELEGRAM = "@Mohammadabbas891"  # تم إضافة اسم المستخدم الخاص بك

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
        "otherInfo": f"تم إنجاز هذه المهمة بواسطة وكيل آلي. العمل: {title}",
        "telegram": TELEGRAM
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            print(f"  ✅ تم التقديم على المهمة: {title}")
            return True
        else:
            print(f"  ❌ فشل التقديم على {title}: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ⚠️ خطأ في التقديم: {e}")
        return False

def auto_submit(tasks):
    """يتقدم تلقائياً على أول 3 مهام مناسبة"""
    if not tasks:
        print("لا توجد مهام للتقديم.")
        return
    count = 0
    for task in tasks[:3]:  # قدم على أول 3 مهام
        task_id = task.get('id')
        title = task.get('title', 'بدون عنوان')
        if task_id:
            print(f"📝 جاري التقديم على: {title}")
            submit_to_task(task_id, title)
            count += 1
    print(f"✅ تم التقديم على {count} مهمة.")

if __name__ == "__main__":
    print("🚀 Superteam Agent starting...")
    print(f"💰 Wallet: {WALLET}")
    print(f"📱 Telegram: {TELEGRAM}")
    
    # البحث عن المهام
    tasks = search_tasks()
    
    # التقديم التلقائي على المهام
    if tasks:
        auto_submit(tasks)
    else:
        print("⚠️ لم يتم العثور على مهام للتقديم.")
    
    print("✅ Done.")
