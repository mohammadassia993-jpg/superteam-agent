import os
import requests
import time
import random
from datetime import datetime

# ================== إعدادات الوكيل ==================
API_KEY = os.environ.get("SUPERTEAM_API_KEY")
WALLET = os.environ.get("PHANTOM_WALLET")
TELEGRAM = "@Mohammadabbas891"  # غيّره إلى اسم مستخدمك

# عناوين API (ثابتة)
BASE_URL = "https://superteam.fun/api"
LISTINGS_URL = f"{BASE_URL}/agents/listings/live?take=50"  # نجلب حتى 50 مهمة
SUBMIT_URL = f"{BASE_URL}/agents/submissions/create"

# الحدود والتحكم
MAX_SUBMISSIONS_PER_RUN = 50          # أقصى تقديم في التشغيل الواحد
DELAY_BETWEEN_SUBMISSIONS = (2, 5)    # تأخير عشوائي بين التقديمات (ثواني)

# ================== الوظائف الأساسية ==================
def fetch_listings():
    """جلب المهام المتاحة (حتى 50 مهمة)"""
    headers = {"Authorization": f"Bearer {API_KEY}"}
    try:
        response = requests.get(LISTINGS_URL, headers=headers, timeout=30)
        if response.status_code == 200:
            data = response.json()
            # التأكد من أن البيانات هي قائمة
            if isinstance(data, list):
                return data
            else:
                print(f"⚠️ البيانات ليست قائمة: {type(data)}")
                return []
        else:
            print(f"❌ فشل جلب المهام: {response.status_code}")
            return []
    except Exception as e:
        print(f"⚠️ خطأ في الاتصال: {e}")
        return []

def is_agent_eligible(listing):
    """التحقق من أن المهمة مسموحة للوكلاء"""
    access = listing.get('agentAccess', 'HUMAN_ONLY')
    return access in ('AGENT_ALLOWED', 'AGENT_ONLY')

def submit_to_listing(listing):
    """تقديم طلب على مهمة محددة"""
    listing_id = listing.get('id')
    title = listing.get('title', 'بدون عنوان')
    
    payload = {
        "listingId": listing_id,
        "link": "https://github.com/superteam-agent",
        "otherInfo": f"تم تنفيذ هذه المهمة بواسطة وكيل آلي. المشروع: {title}",
        "telegram": TELEGRAM
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(SUBMIT_URL, headers=headers, json=payload, timeout=30)
        if response.status_code in (200, 201):
            print(f"  ✅ تم التقديم على: {title}")
            return True
        else:
            print(f"  ❌ فشل التقديم على {title}: {response.status_code} - {response.text[:100]}")
            return False
    except Exception as e:
        print(f"  ⚠️ خطأ في التقديم على {title}: {e}")
        return False

# ================== التشغيل الرئيسي ==================
if __name__ == "__main__":
    print("=" * 50)
    print(f"🚀 Superteam Agent - وضع التقديم الشامل")
    print(f"💰 المحفظة: {WALLET}")
    print(f"📱 تلغرام: {TELEGRAM}")
    print(f"⏰ الوقت: {datetime.now()}")
    print("=" * 50)
    
    # 1. جلب المهام
    print("📡 جلب المهام المتاحة...")
    all_listings = fetch_listings()
    print(f"📋 إجمالي المهام المستلمة: {len(all_listings)}")
    
    # 2. تصفية المهام المسموحة للوكلاء
    eligible = [l for l in all_listings if is_agent_eligible(l)]
    print(f"✅ المهام المسموحة للوكلاء: {len(eligible)}")
    
    if not eligible:
        print("⚠️ لا توجد مهام مسموحة للوكلاء حالياً.")
        exit(0)
    
    # 3. تحديد عدد التقديمات (كل المهام المتاحة، بحد أقصى 50)
    to_submit = eligible[:MAX_SUBMISSIONS_PER_RUN]
    print(f"📝 سيتم التقديم على {len(to_submit)} مهمة.")
    
    # 4. تقديم على كل مهمة مع تأخير
    success_count = 0
    for idx, task in enumerate(to_submit, 1):
        title = task.get('title', 'بدون عنوان')[:50]
        print(f"\n[{idx}/{len(to_submit)}] جاري التقديم على: {title}...")
        if submit_to_listing(task):
            success_count += 1
        
        # تأخير بين التقديمات (تجنب الحظر)
        if idx < len(to_submit):
            delay = random.uniform(*DELAY_BETWEEN_SUBMISSIONS)
            print(f"  ⏳ انتظار {delay:.1f} ثانية قبل التالي...")
            time.sleep(delay)
    
    # 5. ملخص النهائي
    print("\n" + "=" * 50)
    print(f"✅ انتهى التشغيل. نجح {success_count} من {len(to_submit)} تقديم.")
    print("💡 تذكر: سيتم إعلامك عبر البريد الإلكتروني عند الفوز بأي مهمة.")
    print("=" * 50)
