import json, os, smtplib, ssl, sys
from email.message import EmailMessage

QUEUE_FILE = os.path.join(os.path.dirname(__file__), 'data', 'all_unsent_emails.json')
BATCH_SIZE = 80

SMTP_HOST = os.getenv('SMTP_HOST')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SMTP_USER = os.getenv('SMTP_USER')
SMTP_PASS = os.getenv('SMTP_PASS')
FROM_ADDR = os.getenv('SMTP_FROM', SMTP_USER)

def load_queue():
    with open(QUEUE_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_queue(q):
    with open(QUEUE_FILE, 'w', encoding='utf-8') as f:
        json.dump(q, f, indent=2)

def send_email(to_addr):
    msg = EmailMessage()
    msg['Subject'] = 'Automated Outreach'
    msg['From'] = FROM_ADDR
    msg['To'] = to_addr
    msg.set_content('Hello, this is an automated message.')
    context = ssl.create_default_context()
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls(context=context)
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)

def main():
    queue = load_queue()
    if not queue:
        print('Queue empty – nothing to send.')
        return
    batch = queue[:BATCH_SIZE]
    remaining = queue[BATCH_SIZE:]
    for addr in batch:
        print(f'Sending to {addr}...')
        send_email(addr)
    save_queue(remaining)
    print(f'Sent {len(batch)} emails, {len(remaining)} remain in queue.')

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print('Error:', e, file=sys.stderr)
        sys.exit(1)
