import json, os, smtplib, ssl, sys, time
from email.message import EmailMessage

QUEUE_FILE = os.path.join(os.path.dirname(__file__), 'data', 'all_unsent_emails.json')
BATCH_SIZE = 80
DELAY_SECS = 0.5  # 0.5s between sends → ~120/min, safely under Gmail's 500/day limit

# --- SMTP config from environment (GitHub Secrets) ---
SMTP_HOST = os.getenv('SMTP_HOST', '').strip()
SMTP_PORT_RAW = os.getenv('SMTP_PORT', '587').strip()
SMTP_USER = os.getenv('SMTP_USER', '').strip()
SMTP_PASS = os.getenv('SMTP_PASS', '').strip()
FROM_ADDR = os.getenv('SMTP_FROM', SMTP_USER).strip() or SMTP_USER

def validate_config():
    missing = [k for k, v in {
        'SMTP_HOST': SMTP_HOST,
        'SMTP_USER': SMTP_USER,
        'SMTP_PASS': SMTP_PASS,
    }.items() if not v]
    if missing:
        print(f"ERROR: Missing required secrets: {', '.join(missing)}", file=sys.stderr)
        print("Please add them at: GitHub repo → Settings → Secrets and variables → Actions → New repository secret", file=sys.stderr)
        sys.exit(1)

def get_smtp_port():
    try:
        return int(SMTP_PORT_RAW) if SMTP_PORT_RAW else 587
    except ValueError:
        print(f"WARNING: Invalid SMTP_PORT '{SMTP_PORT_RAW}', defaulting to 587", file=sys.stderr)
        return 587

def load_queue():
    with open(QUEUE_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_queue(q):
    with open(QUEUE_FILE, 'w', encoding='utf-8') as f:
        json.dump(q, f, indent=2)

def send_email(to_addr, smtp_port):
    msg = EmailMessage()
    msg['Subject'] = 'Career Outreach'
    msg['From'] = FROM_ADDR
    msg['To'] = to_addr
    msg.set_content(
        "Hello,\n\n"
        "I hope this message finds you well. I'm reaching out regarding a career opportunity "
        "and would love to connect.\n\n"
        "Best regards"
    )
    context = ssl.create_default_context()
    with smtplib.SMTP(SMTP_HOST, smtp_port, timeout=15) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)

def main():
    validate_config()
    smtp_port = get_smtp_port()

    queue = load_queue()
    if not queue:
        print('Queue is empty — all emails have been dispatched!')
        return

    batch = queue[:BATCH_SIZE]
    remaining = queue[BATCH_SIZE:]

    sent = 0
    failed = 0
    failed_addrs = []

    print(f"Starting dispatch: {len(batch)} emails from queue of {len(queue)} total")
    print(f"SMTP: {SMTP_HOST}:{smtp_port} as {SMTP_USER}")

    for i, addr in enumerate(batch, 1):
        try:
            send_email(addr, smtp_port)
            print(f"[{i}/{len(batch)}] ✓ Sent to {addr}")
            sent += 1
        except Exception as e:
            print(f"[{i}/{len(batch)}] ✗ Failed {addr}: {e}", file=sys.stderr)
            failed += 1
            failed_addrs.append(addr)
        time.sleep(DELAY_SECS)

    # Put failed ones back at the front of the remaining queue so they retry next run
    save_queue(failed_addrs + remaining)

    print(f"\n--- Summary ---")
    print(f"Sent:    {sent}")
    print(f"Failed:  {failed}")
    print(f"Remaining in queue: {len(failed_addrs) + len(remaining)}")

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        sys.exit(1)
