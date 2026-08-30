"""
Parallel Email Dispatcher — 16 SMTP accounts, 80 emails each = 1280/run
"""
import json, smtplib, ssl, time, threading, sys, os
from email.message import EmailMessage
from datetime import datetime

QUEUE_FILE = os.path.join(os.path.dirname(__file__), 'data', 'all_unsent_emails.json')
BATCH_PER_ACCOUNT = 80
DELAY = 0.5
LOCK = threading.Lock()

SMTP_ACCOUNTS = [
    {"user": "techxp.kunaljain@gmail.com",          "pass": "vghy qddq govv ffij"},
    {"user": "trillionmemberclub@gmail.com",         "pass": "eeai tzpl mhyi pfgl"},
    {"user": "cofounder.heatbolt@gmail.com",         "pass": "nefq jmor vvrn wslf"},
    {"user": "git.kumarpalporwal98@gmail.com",       "pass": "uagy dyjm ggkh carr"},
    {"user": "team.heatbolt@gmail.com",              "pass": "fusa vdmp mpqo kdmc"},
    {"user": "marketing.heatbolt@gmail.com",         "pass": "xjaa rgja mgad dume"},
    {"user": "founder.parshwapower@gmail.com",       "pass": "adji giov teqz ehlv"},
    {"user": "cofounder.parshwapower@gmail.com",     "pass": "dvml ecqu uhzg yyis"},
    {"user": "cofounder1.parshwapower@gmail.com",    "pass": "dvho tzmy lseq hyel"},
    {"user": "kumarpalporwal8@gmail.com",            "pass": "vupu oubh acle vvxf"},
    {"user": "techhp.kunaljain@gmail.com",           "pass": "rtqz oqjp jaxp vspp"},
    {"user": "teambrandvibes@gmail.com",             "pass": "llum talv mato onwm"},
    {"user": "superreachconsultant@gmail.com",       "pass": "ixmh dmft gubl xira"},
    {"user": "hydronext6@gmail.com",                 "pass": "htvz gcgh tygy msdw"},
    {"user": "jainakshita876@gmail.com",             "pass": "sykw pvxc rioy dphb"},
    {"user": "founder.heatbolt@gmail.com",           "pass": "klyc waca kpmi qgoj"},
]

EMAIL_SUBJECT = "Career Opportunity — Dr. Kumarpal Porwal, Founder Heatbolt"
EMAIL_BODY = """Hello,

I am Dr. Kumarpal Porwal, Founder of Heatbolt — a deep-tech company building AI-powered infrastructure.

I am reaching out to explore collaboration, investment, or partnership opportunities.

Our technology has been validated by the Indian government and we are scaling rapidly.

Would you be open to a 15-minute call this week?

Best regards,
Dr. Kumarpal Porwal
Founder, Heatbolt
founder.heatbolt@gmail.com | +91 7353319757"""

results = {}

def load_queue():
    with open(QUEUE_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_queue(q):
    with open(QUEUE_FILE, 'w', encoding='utf-8') as f:
        json.dump(q, f, indent=2)

def send_one(user, pw, to_addr):
    msg = EmailMessage()
    msg['Subject'] = EMAIL_SUBJECT
    msg['From']    = user
    msg['To']      = to_addr
    msg.set_content(EMAIL_BODY)
    ctx = ssl.create_default_context()
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=15) as srv:
        srv.ehlo(); srv.starttls(context=ctx); srv.ehlo()
        srv.login(user, pw)
        srv.send_message(msg)

def worker(account, batch):
    user = account['user']
    pw   = account['pass']
    sent = 0; failed_addrs = []
    print(f"[START] {user} -> {len(batch)} emails")
    for addr in batch:
        try:
            send_one(user, pw, addr)
            sent += 1
            print(f"  [OK] {user} -> {addr}")
        except Exception as e:
            failed_addrs.append(addr)
            print(f"  [FAIL] {user} -> {addr}: {e}", file=sys.stderr)
        time.sleep(DELAY)
    with LOCK:
        results[user] = {"sent": sent, "failed_addrs": failed_addrs}
    print(f"[DONE] {user}: {sent} sent, {len(failed_addrs)} failed")

def main():
    print(f"\n{'='*60}")
    print(f"PARALLEL DISPATCH: {len(SMTP_ACCOUNTS)} accounts x {BATCH_PER_ACCOUNT} = up to {len(SMTP_ACCOUNTS)*BATCH_PER_ACCOUNT} emails")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    queue = load_queue()
    print(f"Queue: {len(queue)} emails pending\n")
    if not queue:
        print("Queue empty.")
        return

    threads = []
    offset = 0
    for acct in SMTP_ACCOUNTS:
        slice_ = queue[offset: offset + BATCH_PER_ACCOUNT]
        if not slice_:
            break
        offset += len(slice_)
        t = threading.Thread(target=worker, args=(acct, slice_), daemon=True)
        threads.append(t)

    remaining_after = queue[offset:]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    all_failed = []
    for acct in SMTP_ACCOUNTS:
        r = results.get(acct['user'], {})
        all_failed.extend(r.get('failed_addrs', []))

    save_queue(all_failed + remaining_after)

    total_sent  = sum(r.get('sent', 0) for r in results.values())
    total_fail  = sum(len(r.get('failed_addrs', [])) for r in results.values())

    print(f"\n{'='*60}")
    print(f"DONE: {total_sent} sent, {total_fail} failed (re-queued)")
    print(f"Remaining in queue: {len(all_failed + remaining_after)}")
    print(f"Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
