import smtplib
import json
import os
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

# Target batch to send right now
targets = [
    {
        "name": "Sajjan Jindal",
        "role": "Chairman & Managing Director",
        "organization": "JSW Group",
        "email": "sajjan.jindal@jsw.in",
        "subject": "Strategic Investment & Global Clean-Tech Commercialisation Opportunity - HeatBolt (JSW Group)"
    },
    {
        "name": "Sudha Murty",
        "role": "Chairperson & Trustee",
        "organization": "Murty Trust",
        "email": "smurty.office@murtytrust.org",
        "subject": "Partnership & Impact Innovation Opportunity - HeatBolt Flameless Thermal Tech (Murty Trust)"
    },
    {
        "name": "Akash Ambani",
        "role": "Chairman",
        "organization": "Reliance Jio Infocomm",
        "email": "ambania@jio.com",
        "subject": "Strategic Investment & Mass Ecosystem Commercialisation - HeatBolt (Reliance Jio)"
    },
    {
        "name": "Saurabh Agrawal",
        "role": "Group Chief Financial Officer",
        "organization": "Tata Sons",
        "email": "saurabh.agarwal@tata.com",
        "subject": "Strategic Investment & Industrial Commercialisation Collaboration - HeatBolt (Tata Sons)"
    },
    {
        "name": "Ankur Verma",
        "role": "Senior Vice President, Group Strategy",
        "organization": "Tata Sons",
        "email": "Ankur.verma@tata.com",
        "subject": "Strategic Investment & Deep-Tech Hardware Commercialisation - HeatBolt (Tata Sons)"
    },
    {
        "name": "Secretariat / Leadership Desk",
        "role": "Leadership Desk",
        "organization": "Startup Accelerator Chamber of Commerce (SACC India)",
        "email": "info@saccindia.org",
        "subject": "Deep-Tech Manufacturing & Institutional Ecosystem Partnership - HeatBolt (SACC India)"
    },
    {
        "name": "David Drummond",
        "role": "Former Chief Legal Officer & SVP Corporate Development, Alphabet / Google | Board Member & Investor",
        "organization": "Office of David Drummond",
        "email": "officeofdaviddrummond@gmail.com",
        "subject": "Strategic Deep-Tech Hard-Tech Commercialisation & Global Expansion - HeatBolt"
    },
    {
        "name": "Kate Chichi",
        "role": "Partner / Investment Team",
        "organization": "RTP Global (rtp.vc)",
        "email": "kate@rtp.vc",
        "subject": "Seed/Growth Investment Opportunity - HeatBolt Flameless Self-Heating Hardware (RTP Global)"
    },
    {
        "name": "Lux Capital Communications & Investment Team",
        "role": "Investment Desk",
        "organization": "Lux Capital",
        "email": "comms@luxcapital.com",
        "subject": "Deep-Tech Physical Hardware & Materials Investment - HeatBolt (Lux Capital)"
    },
    {
        "name": "Golden Gate Ventures Investor Team",
        "role": "Investor Relations & Deal Team",
        "organization": "Golden Gate Ventures",
        "email": "investors@goldengate.vc",
        "subject": "Cross-Border Deep-Tech Physical Hardware Investment Opportunity - HeatBolt (Golden Gate Ventures)"
    },
    {
        "name": "Justin Hall",
        "role": "Partner",
        "organization": "Golden Gate Ventures",
        "email": "justin@goldengate.vc",
        "subject": "Deep-Tech Physical Hardware Scaling & Growth Equity - HeatBolt (Golden Gate Ventures)"
    },
    {
        "name": "Sameer Mehta",
        "role": "Co-Founder & CEO",
        "organization": "boAt / Imagine Marketing",
        "email": "sameer.mehta@imaginemarketingindia.com",
        "subject": "Strategic Hardware Innovation & Consumer Product Commercialisation - HeatBolt (boAt / Imagine Marketing)"
    },
    {
        "name": "Congruent Ventures Investment Team",
        "role": "Investment Desk",
        "organization": "Congruent Ventures",
        "email": "investors@congruentvc.com",
        "subject": "Early-Stage Climate Tech & Circular Packaging Hardware Investment - HeatBolt (Congruent Ventures)"
    },
    {
        "name": "Congruent Ventures General Inquiries Desk",
        "role": "General Operations Desk",
        "organization": "Congruent Ventures",
        "email": "info@congruentvc.com",
        "subject": "Sustainable Hardware & Deep-Tech Partnership Inquiry - HeatBolt (Congruent Ventures)"
    }
]

# Load templates
with open(r"C:\Users\My\.gemini\antigravity\scratch\career-ops\data\heatbolt_aesthetic_template.html", "r", encoding="utf-8") as f:
    html_template = f.read()

with open(r"C:\Users\My\.gemini\antigravity\scratch\career-ops\data\heatbolt_canonical_template.json", "r", encoding="utf-8-sig") as f:
    text_template = json.load(f).get("body_text", "")

# Load smtp pool
with open(r"C:\Users\My\.gemini\antigravity\scratch\career-ops\data\smtp_pool.json", "r", encoding="utf-8") as f:
    smtp_pool = json.load(f)

# Load sent list
sent_file = r"C:\Users\My\.gemini\antigravity\scratch\career-ops\data\sent_emails.json"
with open(sent_file, "r", encoding="utf-8-sig") as f:
    sent_list = json.load(f)

sent_emails_set = set()
for item in sent_list:
    if isinstance(item, dict):
        email_val = item.get("email") or item.get("to") or ""
        if email_val:
            sent_emails_set.add(email_val.strip().lower())
    elif isinstance(item, str):
        sent_emails_set.add(item.strip().lower())

print(f"Loaded {len(smtp_pool)} SMTP pool accounts.")
print(f"Loaded {len(sent_list)} sent records ({len(sent_emails_set)} unique emails).")

# Select active SMTP accounts with rotation
account_idx = 0
success_count = 0
skipped_count = 0
fail_count = 0

for target in targets:
    t_email = target["email"].strip()
    if t_email.lower() in sent_emails_set:
        print(f"SKIP (Already sent): {t_email}")
        skipped_count += 1
        continue

    # Pick next SMTP account
    smtp_account = smtp_pool[account_idx % len(smtp_pool)]
    account_idx += 1

    smtp_user = smtp_account.get("email") or smtp_account.get("user")
    smtp_pass = smtp_account.get("pass") or smtp_account.get("password")

    msg = MIMEMultipart("alternative")
    msg["From"] = f"Dr. Kumarpal Porwal - HeatBolt <{smtp_user}>"
    msg["To"] = t_email
    msg["Subject"] = target["subject"]
    msg["Reply-To"] = "kumarpalporwal8@gmail.com"

    msg.attach(MIMEText(text_template, "plain", "utf-8"))
    msg.attach(MIMEText(html_template, "html", "utf-8"))

    sent_successfully = False
    for attempt in range(2):
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587, timeout=25)
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(smtp_user, t_email, msg.as_string())
            server.quit()
            sent_successfully = True
            break
        except Exception as e:
            print(f"Attempt {attempt+1} failed for {t_email} via {smtp_user}: {e}")
            smtp_account = smtp_pool[(account_idx + 3) % len(smtp_pool)]
            account_idx += 1
            smtp_user = smtp_account.get("email") or smtp_account.get("user")
            smtp_pass = smtp_account.get("pass") or smtp_account.get("password")
            time.sleep(2)

    if sent_successfully:
        success_count += 1
        sent_entry = {
            "to": t_email,
            "email": t_email,
            "from": smtp_user,
            "subject": target["subject"],
            "status": "sent",
            "timestamp": datetime.now().isoformat(),
            "name": target["name"],
            "role": target["role"],
            "organization": target["organization"]
        }
        sent_list.append(sent_entry)
        sent_emails_set.add(t_email.lower())
        print(f"SUCCESS: Dispatched to {target['name']} <{t_email}> via {smtp_user}")
        time.sleep(1.5)
    else:
        fail_count += 1
        print(f"FAILED: Could not dispatch to {t_email}")

# Save updated sent list
with open(sent_file, "w", encoding="utf-8") as f:
    json.dump(sent_list, f, indent=2, ensure_ascii=False)

print(f"\nBATCH SUMMARY: Success: {success_count}, Skipped: {skipped_count}, Failed: {fail_count}")
print(f"Total Sent List Size Now: {len(sent_list)}")
