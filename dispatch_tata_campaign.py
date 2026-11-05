# -*- coding: utf-8 -*-
"""
Dedicated Tata Diwali Campaign Dispatcher
Distributes the Tata leadership email across all 16 active SMTP accounts in rotation.
"""
import json, smtplib, time, os, sys, uuid
from email.message import EmailMessage
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\My\.gemini\antigravity\scratch\career-ops"
DATA_DIR = os.path.join(BASE_DIR, "data")
LOGS_DIR = os.path.join(DATA_DIR, "logs")

SMTP_FILE = os.path.join(DATA_DIR, "smtp_pool.json")
TATA_FILE = os.path.join(DATA_DIR, "tata_target_inboxes.json")
MASTER_SENT = os.path.join(LOGS_DIR, "master_all_sent.json")
HTML_FILE = os.path.join(DATA_DIR, "heatbolt_tata_diwali_followup.html")

SUBJECT = "Wishing Tata Leadership a Very Happy Diwali | Strategic Association with HeatBolt"
CC_EMAIL = "team.heatbolt@gmail.com"
REPLY_TO = "founder.heatbolt@gmail.com"

# Load Targets
with open(TATA_FILE, "r", encoding="utf-8") as f:
    tata_targets = json.load(f)

# Load SMTP Pool
with open(SMTP_FILE, "r", encoding="utf-8") as f:
    smtp_pool = json.load(f)

# Load HTML
with open(HTML_FILE, "r", encoding="utf-8") as f:
    html_content = f.read()

plain_content = """Dear Tata Leadership Team,

Wishing you and your families a very Happy Diwali! May the festival of lights bring prosperity, happiness and new beginnings.

I am writing to explore a strategic association between HeatBolt and the Tata Group to develop and scale a new category of portable thermal technology.

1. Our Innovation
HeatBolt combines proprietary water-activated heating technology with specially engineered packaging, enabling food and beverages to be heated without electricity, LPG, gas or external heating infrastructure.

2. Strategic Group-Wide Opportunities
We see potential applications across Tata Consumer Products, Tata Chemicals, Tata Motors, Indian Hotels, Tata Neu and other relevant Tata businesses, spanning food, FMCG, mobility, hospitality and emergency preparedness.

3. Global Growth Potential
We are witnessing encouraging interest across international FMCG, food, beverage, defence, railway and hospitality sectors, with opportunities to build a globally scalable platform originating from India.

4. Investment & Strategic Partnership
We are exploring approximately USD 12 million in strategic investment to accelerate R&D, manufacturing scale-up, validation and global commercialisation. We would welcome Tata's participation as a strategic investor and/or technology, manufacturing or commercialisation partner.

5. A Request for Engagement
I would be grateful for an opportunity to personally present the technology, demonstrate our progress, introduce our team and explore potential synergies with the appropriate Tata leadership.

Our ambition extends beyond building a product—we aspire to establish a globally relevant technology and packaging platform from India. We believe Tata could be an exceptional strategic partner in this journey.

Looking forward to the opportunity to connect.

Warm regards,

Dr. Kumarpal Hasmukh Porwal
Founder – HeatBolt
Shree Nakoda Parshwa Industries
LinkedIn: https://www.linkedin.com/in/kumarpal-porwal/
Direct / WhatsApp: +91 73533 19757 | +91 88672 94189
Email: founder.heatbolt@gmail.com
"""

print(f"Loaded {len(tata_targets)} Tata targets.")
print(f"Loaded {len(smtp_pool)} SMTP sender accounts.")

MAX_PER_SMTP = 18
target_quota = min(len(tata_targets), len(smtp_pool) * MAX_PER_SMTP)
print(f"Planned batch size for this rotation: {target_quota} emails.")

sent_records = []
failed_records = []
smtp_usage = {i: 0 for i in range(len(smtp_pool))}

current_smtp_idx = 0

for idx, target in enumerate(tata_targets[:target_quota]):
    # Rotate SMTP
    attempts = 0
    while attempts < len(smtp_pool):
        if smtp_usage[current_smtp_idx] < MAX_PER_SMTP:
            break
        current_smtp_idx = (current_smtp_idx + 1) % len(smtp_pool)
        attempts += 1
    
    if attempts >= len(smtp_pool):
        print("All SMTP accounts reached daily quota.")
        break
    
    sender_account = smtp_pool[current_smtp_idx]
    user = sender_account["user"]
    pwd = sender_account["pass"]
    host = sender_account.get("host", "smtp.gmail.com")
    port = sender_account.get("port", 587)
    
    msg = EmailMessage()
    msg["From"] = user
    msg["To"] = target
    msg["CC"] = CC_EMAIL
    msg["Reply-To"] = REPLY_TO
    msg["List-Unsubscribe"] = f"<mailto:{REPLY_TO}?subject=unsubscribe>"
    msg["Message-ID"] = f"<{uuid.uuid4().hex}@heatbolt.com>"
    msg["Subject"] = SUBJECT
    
    msg.set_content(plain_content)
    msg.add_alternative(html_content, subtype="html")
    
    success = False
    try:
        with smtplib.SMTP(host, port, timeout=20) as server:
            server.starttls()
            server.login(user, pwd)
            server.send_message(msg)
            success = True
    except Exception as e:
        print(f"[{idx+1}/{target_quota}] FAILED -> {target} via {user}: {e}")
        failed_records.append({"to": target, "error": str(e), "via": user})
    
    if success:
        smtp_usage[current_smtp_idx] += 1
        rec = {
            "to": target,
            "from": user,
            "type": "tata_diwali_followup",
            "time": datetime.now().isoformat()
        }
        sent_records.append(rec)
        print(f"[{idx+1}/{target_quota}] SENT -> {target} (via {user} | {smtp_usage[current_smtp_idx]}/{MAX_PER_SMTP})")
    
    # Rotate to next sender for load balancing
    current_smtp_idx = (current_smtp_idx + 1) % len(smtp_pool)
    
    # Polite pacing between sends (15-25 seconds)
    time.sleep(18)

# Log to master sent
if sent_records:
    if os.path.exists(MASTER_SENT):
        with open(MASTER_SENT, "r", encoding="utf-8") as f:
            try:
                master_history = json.load(f)
            except Exception:
                master_history = []
    else:
        master_history = []
    
    master_history.extend(sent_records)
    with open(MASTER_SENT, "w", encoding="utf-8") as f:
        json.dump(master_history, f, indent=2, ensure_ascii=False)
    
    # Save today's log
    today_log = os.path.join(LOGS_DIR, f"tata_diwali_sent_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(today_log, "w", encoding="utf-8") as f:
        json.dump(sent_records, f, indent=2, ensure_ascii=False)
    
    print(f"\nDispatched {len(sent_records)} Tata emails successfully! Logged to {today_log}")
