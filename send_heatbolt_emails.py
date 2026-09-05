"""
Heatbolt Mass Mail-Merge Script
================================
Sends personalized outreach emails to all contacts from founder.heatbolt@gmail.com
CC: team.heatbolt@gmail.com

BEFORE RUNNING:
  1. Generate a Gmail App Password:
     → Go to https://myaccount.google.com/apppasswords
     → Create an app password for "Mail"
     → Copy the 16-character password
  2. Set it as an environment variable:
       set GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
  3. Run:  python send_heatbolt_emails.py
     Or dry-run first:  python send_heatbolt_emails.py --dry-run

Usage:
  python send_heatbolt_emails.py              # send all emails
  python send_heatbolt_emails.py --dry-run    # preview without sending
  python send_heatbolt_emails.py --test       # send 1 test to founder.heatbolt@gmail.com
  python send_heatbolt_emails.py --batch 10   # send in batches of 10 with 30s pause
"""

import smtplib
import os
import sys
import time
import csv
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

try:
    from contacts import CONTACTS
except ImportError:
    CONTACTS = []

# ─────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────
SENDER_EMAIL = "founder.heatbolt@gmail.com"
CC_EMAIL = "team.heatbolt@gmail.com"
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SUBJECT = "If This Journey Has a Purpose, I Believe It Begins with You"

LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, f"send_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-7s  %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(LOG_DIR, f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"))
    ]
)
log = logging.getLogger("heatbolt-mailer")


# ─────────────────────────────────────────────
# CATEGORY-SPECIFIC CUSTOMIZATION HOOKS
# ─────────────────────────────────────────────
CATEGORY_HOOKS = {
    "indian_institutional": (
        "Given {org}'s leadership in India's institutional investment landscape, "
        "I believe Heatbolt's proprietary thermal platform—now gaining strong traction with "
        "leading Indian corporates, government institutions, and global FMCG partners—could "
        "represent a compelling strategic opportunity aligned with {org}'s investment thesis."
    ),
    "global_pe": (
        "Given {org}'s track record in scaling transformative technology platforms globally, "
        "I believe Heatbolt's integrated portable thermal and packaging ecosystem—with demand "
        "indicators pointing to 20 billion+ units annually—presents the kind of category-defining "
        "opportunity that aligns with {org}'s growth capital mandate."
    ),
    "sovereign_wealth": (
        "Given {org}'s mandate to identify long-horizon, high-impact investments that "
        "address global challenges, I believe Heatbolt's sustainable thermal infrastructure "
        "platform—spanning food security, waste reduction, and humanitarian relief—presents "
        "a uniquely aligned opportunity for {org}'s portfolio."
    ),
    "family_office": (
        "Given {org}'s commitment to purpose-driven investments that blend commercial "
        "returns with meaningful global impact, I believe Heatbolt's innovation platform—"
        "addressing food waste, plastic reduction, and accessible nutrition—resonates deeply "
        "with the values-driven approach that distinguishes {org}."
    ),
    "bulge_bracket": (
        "Given {org}'s global reach and expertise in scaling transformative ventures through "
        "strategic capital and distribution, I believe Heatbolt's emerging technology platform—"
        "with active engagement from leading FMCG multinationals and sovereign entities—could "
        "present a differentiated opportunity for {org}'s {division} practice."
    ),
    "academic": (
        "Given your distinguished position in the academic and research community, "
        "I believe Heatbolt's proprietary thermal technology platform—rooted in applied science "
        "and addressing pressing global challenges—could present unique opportunities for "
        "collaboration, research partnerships, and knowledge exchange."
    ),
}


def build_html_body(first_name: str, full_name: str, org: str, division: str, category: str) -> str:
    """Build a fully customized HTML email body."""

    hook_template = CATEGORY_HOOKS.get(category, CATEGORY_HOOKS["global_pe"])
    custom_hook = hook_template.format(org=org, division=division)

    return f"""\
<html>
<body style="font-family: Georgia, 'Times New Roman', serif; font-size: 15px; line-height: 1.75; color: #222; max-width: 680px; margin: auto;">

<p>Dear {first_name},</p>

<p>I hope this message finds you in good health and high spirits.</p>

<p>Today, I am writing to you not merely as the Founder of Heatbolt, but as an entrepreneur whose journey has been shaped by a deeply personal purpose.</p>

<p>For years, one question has stayed with me:<br>
<em>Can innovation do more than create convenience? Can it genuinely improve lives?</em><br>
That single question became the foundation of everything I have built.</p>

<h3 style="color: #b8860b;">A Purpose Beyond Business</h3>

<p>Life has a way of changing our priorities.</p>

<p>Like countless families across the world, mine has experienced the pain of losing loved ones. I have seen how one illness can change the course of an entire family.</p>

<p>When a father is lost, a family loses its pillar.<br>
When a mother is lost, a home loses its heart.<br>
When a son or daughter is lost, parents carry that pain for a lifetime.<br>
<strong>Behind every patient is an entire family whose lives are forever changed.</strong></p>

<p>Every year, cancer claims nearly <strong>10 million lives globally</strong>, including more than <strong>900,000 lives in India</strong>. Behind these numbers are people, families, and dreams.</p>

<p>At the same time, billions of single-use plastic packages are discarded every year. Researchers continue to investigate the long-term health implications of microplastics and chemicals associated with certain plastic products. While the science is still evolving, reducing unnecessary plastic waste and advancing safer, more sustainable packaging is widely recognized as an important environmental and public-health priority.</p>

<p>These realities reinforced a belief that has guided my entrepreneurial journey:<br>
<strong><em>"Prevention is always better than cure."</em></strong><br>
That belief became my purpose.</p>

<h3 style="color: #b8860b;">The Birth of Heatbolt</h3>

<p>Instead of asking, <em>"What product can I build?"</em><br>
I began asking, <em>"What problems deserve to be solved?"</em></p>

<ul>
<li>Could we reduce food wastage?</li>
<li>Could we reduce dependence on conventional heating?</li>
<li>Could we rethink packaging?</li>
<li>Could we make hot food accessible anywhere?</li>
<li>Could India create an entirely new technology platform for the world?</li>
</ul>

<p>Those questions led to the creation of <strong>Heatbolt</strong>.</p>

<table cellpadding="12" style="border: 2px solid #b8860b; border-radius: 6px; margin: 20px 0; width: 100%;">
<tr><td style="text-align: center;">
<h2 style="margin: 0; color: #b8860b;">HEATBOLT</h2>
<p style="margin: 4px 0 0 0; font-size: 13px; letter-spacing: 1px;">Portable Thermal Infrastructure &nbsp;|&nbsp; Self-Heating Packaging &nbsp;|&nbsp; Sustainable Innovation</p>
</td></tr>
</table>

<p>Heatbolt is a proprietary portable thermal platform capable of generating temperatures of up to <strong>100°C using only water</strong>, without requiring:</p>
<ul>
<li>Electricity</li>
<li>LPG or Gas</li>
<li>Batteries</li>
<li>Open Flame</li>
<li>External Heating Infrastructure</li>
</ul>

<p>The technology integrates directly into cups, bowls, trays, pouches, lunch boxes, containers, and customized packaging, enabling consumers to enjoy freshly heated food and beverages <strong>anytime, anywhere</strong>.</p>

<p>But Heatbolt is more than a self-heating solution.<br>
<strong>It is a new category of portable thermal infrastructure</strong> with applications across multiple industries and geographies.</p>

<h3 style="color: #b8860b;">More Than Heat — A New Packaging Ecosystem</h3>

<p>Perhaps the most exciting aspect of Heatbolt is not the heat itself.<br>
<strong>It is the packaging.</strong></p>

<p>Our integrated packaging platform has the potential to provide up to <strong>one year of shelf life</strong> for selected ready-to-eat foods, beverages, nutritional products, and wellness solutions.</p>

<p>This can help:</p>
<ul>
<li>Reduce food wastage.</li>
<li>Reduce dependence on refrigeration and cold-chain logistics.</li>
<li>Improve food accessibility in remote and underserved regions.</li>
<li>Support emergency preparedness and humanitarian relief.</li>
<li>Enable more sustainable packaging formats.</li>
<li>Create export-ready solutions for global markets.</li>
</ul>

<p>Rather than solving a single problem, Heatbolt aims to address multiple interconnected challenges through one integrated platform.</p>

<h3 style="color: #b8860b;">Current Momentum &amp; Execution</h3>

<p>The response to Heatbolt has been highly encouraging. Today, we have achieved:</p>
<ul>
<li><strong>60,000+</strong> stakeholder engagements across India and international markets.</li>
<li><strong>1,000+</strong> inbound calls and emails every day from corporates, government organizations, institutions, and international partners.</li>
<li>Active engagements with leading global companies including <strong>Barilla, Nestlé, Mondelēz, Unilever, PepsiCo, Kraft Heinz, Mars, General Mills, Ajinomoto, Campbell's, The Coca-Cola Company, Starbucks, Yum! Brands, and McDonald's</strong>.</li>
<li>Ongoing discussions across Indian Railways, airlines, defence, healthcare, pharmaceuticals, hospitality, food delivery, religious institutions, disaster relief, and industrial sectors.</li>
</ul>

<p>Heatbolt has also been recently promoted by <strong>Startup India</strong> and <strong>Invest India</strong>, and is currently trending virally on the internet.</p>

<p>Commercial enquiries and market assessments indicate the potential to support manufacturing volumes exceeding <strong>20 billion Heatbolt-enabled units annually</strong>, with demand continuing to grow across domestic and international markets.</p>

<p>Over the years, I have assembled a multidisciplinary team comprising scientists, food technologists, packaging specialists, manufacturing leaders, and domain specialists with decades of experience.</p>

<p>Together, we are building not only a product, but an organization capable of delivering this vision at global scale.</p>

<p>
<a href="https://www.linkedin.com/posts/kumarpal-porwal_heatbolt-makeinindia-innovation-activity-7486186134474207232-dmlc" style="color: #b8860b; font-weight: bold;">🔗 Urgent Need to Solve the Problem</a>
&nbsp;&nbsp;&nbsp;
<a href="https://www.linkedin.com/posts/rohansachdeva20_makeinindia-innovation-foodtech-share-7483541963657605120-TCKs" style="color: #b8860b; font-weight: bold;">🔗 We Have the Solution</a>
</p>

<h3 style="color: #b8860b;">A Humble Request</h3>

<p>{custom_hook}</p>

<p>We are seeking strategic partners who believe that meaningful innovation can create commercial value while addressing important global challenges.</p>

<p>Whether through strategic investment, manufacturing collaboration, commercialization partnerships, technology licensing, or market access, we believe Heatbolt has the potential to become one of India's next globally recognized technology platforms.</p>

<p>I would be deeply honoured to present our technology, commercialization roadmap, and long-term vision in a brief <strong>15-minute meeting</strong> at your convenience.</p>

<p>Thank you very much for your valuable time and consideration. I sincerely look forward to the opportunity to connect and explore how we can build this journey together.</p>

<p style="margin-top: 30px;">
With warm regards,<br><br>
<strong>Dr. Kumarpal Porwal</strong><br>
Founder &amp; CEO | <strong>Heatbolt</strong><br>
+91 73533 19757 | +91 88672 94189 (WhatsApp Preferred)<br>
<a href="mailto:founder.heatbolt@gmail.com">founder.heatbolt@gmail.com</a>
</p>

<p style="margin-top: 20px; font-style: italic; color: #666; border-left: 3px solid #b8860b; padding-left: 12px;">
"If you want to walk fast, walk alone. If you want to walk far, walk together." — Ratan Tata<br><br>
"The future of convenience is not just portable food and beverages—it is portable heat."
</p>

</body>
</html>
"""


def build_plain_body(first_name: str, full_name: str, org: str, division: str, category: str) -> str:
    """Build a plain-text fallback."""
    hook_template = CATEGORY_HOOKS.get(category, CATEGORY_HOOKS["global_pe"])
    custom_hook = hook_template.format(org=org, division=division)

    return f"""\
Dear {first_name},

I hope this message finds you in good health and high spirits.

Today, I am writing to you not merely as the Founder of Heatbolt, but as an entrepreneur whose journey has been shaped by a deeply personal purpose.

For years, one question has stayed with me:
Can innovation do more than create convenience? Can it genuinely improve lives?
That single question became the foundation of everything I have built.

--- A PURPOSE BEYOND BUSINESS ---

Life has a way of changing our priorities.

Like countless families across the world, mine has experienced the pain of losing loved ones. I have seen how one illness can change the course of an entire family.

When a father is lost, a family loses its pillar.
When a mother is lost, a home loses its heart.
When a son or daughter is lost, parents carry that pain for a lifetime.
Behind every patient is an entire family whose lives are forever changed.

Every year, cancer claims nearly 10 million lives globally, including more than 900,000 lives in India. Behind these numbers are people, families, and dreams.

At the same time, billions of single-use plastic packages are discarded every year. Researchers continue to investigate the long-term health implications of microplastics and chemicals associated with certain plastic products. While the science is still evolving, reducing unnecessary plastic waste and advancing safer, more sustainable packaging is widely recognized as an important environmental and public-health priority.

These realities reinforced a belief that has guided my entrepreneurial journey:
"Prevention is always better than cure."
That belief became my purpose.

--- THE BIRTH OF HEATBOLT ---

Instead of asking, "What product can I build?"
I began asking, "What problems deserve to be solved?"

• Could we reduce food wastage?
• Could we reduce dependence on conventional heating?
• Could we rethink packaging?
• Could we make hot food accessible anywhere?
• Could India create an entirely new technology platform for the world?

Those questions led to the creation of Heatbolt.

HEATBOLT
Portable Thermal Infrastructure | Self-Heating Packaging | Sustainable Innovation

Heatbolt is a proprietary portable thermal platform capable of generating temperatures of up to 100°C using only water, without requiring:
• Electricity
• LPG or Gas
• Batteries
• Open Flame
• External Heating Infrastructure

The technology integrates directly into cups, bowls, trays, pouches, lunch boxes, containers, and customized packaging, enabling consumers to enjoy freshly heated food and beverages anytime, anywhere.

But Heatbolt is more than a self-heating solution.
It is a new category of portable thermal infrastructure with applications across multiple industries and geographies.

--- MORE THAN HEAT — A NEW PACKAGING ECOSYSTEM ---

Perhaps the most exciting aspect of Heatbolt is not the heat itself.
It is the packaging.

Our integrated packaging platform has the potential to provide up to one year of shelf life for selected ready-to-eat foods, beverages, nutritional products, and wellness solutions.

This can help:
• Reduce food wastage.
• Reduce dependence on refrigeration and cold-chain logistics.
• Improve food accessibility in remote and underserved regions.
• Support emergency preparedness and humanitarian relief.
• Enable more sustainable packaging formats.
• Create export-ready solutions for global markets.

--- CURRENT MOMENTUM & EXECUTION ---

The response to Heatbolt has been highly encouraging. Today, we have achieved:
• 60,000+ stakeholder engagements across India and international markets.
• 1,000+ inbound calls and emails every day from corporates, government organizations, institutions, and international partners.
• Active engagements with leading global companies including Barilla, Nestlé, Mondelēz, Unilever, PepsiCo, Kraft Heinz, Mars, General Mills, Ajinomoto, Campbell's, The Coca-Cola Company, Starbucks, Yum! Brands, and McDonald's.
• Ongoing discussions across Indian Railways, airlines, defence, healthcare, pharmaceuticals, hospitality, food delivery, religious institutions, disaster relief, and industrial sectors.

Heatbolt has also been recently promoted by Startup India and Invest India, and is currently trending virally on the internet.

Commercial enquiries and market assessments indicate the potential to support manufacturing volumes exceeding 20 billion Heatbolt-enabled units annually, with demand continuing to grow across domestic and international markets.

Urgent Need to Solve the Problem:
https://www.linkedin.com/posts/kumarpal-porwal_heatbolt-makeinindia-innovation-activity-7486186134474207232-dmlc

We Have the Solution:
https://www.linkedin.com/posts/rohansachdeva20_makeinindia-innovation-foodtech-share-7483541963657605120-TCKs

--- A HUMBLE REQUEST ---

{custom_hook}

We are seeking strategic partners who believe that meaningful innovation can create commercial value while addressing important global challenges.

Whether through strategic investment, manufacturing collaboration, commercialization partnerships, technology licensing, or market access, we believe Heatbolt has the potential to become one of India's next globally recognized technology platforms.

I would be deeply honoured to present our technology, commercialization roadmap, and long-term vision in a brief 15-minute meeting at your convenience.

Thank you very much for your valuable time and consideration. I sincerely look forward to the opportunity to connect and explore how we can build this journey together.

With warm regards,

Dr. Kumarpal Porwal
Founder & CEO | Heatbolt
+91 73533 19757 | +91 88672 94189 (WhatsApp Preferred)
founder.heatbolt@gmail.com

"If you want to walk fast, walk alone. If you want to walk far, walk together." — Ratan Tata

"The future of convenience is not just portable food and beverages—it is portable heat."
"""


def send_email(smtp_conn, to_email: str, desk_email: str, subject: str, html_body: str, plain_body: str):
    """Compose and send a single email."""
    msg = MIMEMultipart("alternative")
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email
    msg["Cc"] = CC_EMAIL
    msg["Subject"] = subject
    msg["X-Priority"] = "1"
    msg["Importance"] = "High"
    msg["X-MSMail-Priority"] = "High"
    msg["Reply-To"] = SENDER_EMAIL

    msg.attach(MIMEText(plain_body, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    recipients = [to_email, CC_EMAIL]
    if desk_email and desk_email.strip():
        recipients.append(desk_email)

    smtp_conn.sendmail(SENDER_EMAIL, recipients, msg.as_string())


def main():
    dry_run = "--dry-run" in sys.argv
    test_mode = "--test" in sys.argv
    batch_size = 10  # default
    for i, arg in enumerate(sys.argv):
        if arg == "--batch" and i + 1 < len(sys.argv):
            batch_size = int(sys.argv[i + 1])

    app_password = os.environ.get("GMAIL_APP_PASSWORD", "").strip()

    if not dry_run and not app_password:
        print("\n" + "=" * 60)
        print("ERROR: GMAIL_APP_PASSWORD environment variable not set.")
        print()
        print("Steps to fix:")
        print("  1. Go to https://myaccount.google.com/apppasswords")
        print("  2. Sign in to founder.heatbolt@gmail.com")
        print("  3. Generate an App Password for 'Mail'")
        print("  4. Run:  set GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx")
        print("  5. Then re-run this script.")
        print()
        print("Or use --dry-run to preview emails without sending.")
        print("=" * 60)
        sys.exit(1)

    # Deduplicate by email address
    seen_emails = set()
    unique_contacts = []
    for c in CONTACTS:
        email = c[4].lower()
        if email not in seen_emails:
            seen_emails.add(email)
            unique_contacts.append(c)
        else:
            log.warning(f"Skipping duplicate: {c[1]} <{c[4]}>")

    total = len(unique_contacts)
    log.info(f"{'DRY RUN — ' if dry_run else ''}Processing {total} unique contacts")

    # CSV log
    csv_file = open(LOG_FILE, "w", newline="", encoding="utf-8")
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["timestamp", "status", "name", "email", "desk_email", "org", "category", "error"])

    smtp = None
    if not dry_run:
        log.info(f"Connecting to {SMTP_HOST}:{SMTP_PORT}...")
        smtp = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(SENDER_EMAIL, app_password)
        log.info("SMTP login successful ✓")

    sent = 0
    failed = 0

    for idx, (first_name, full_name, org, division, email, desk_email, category) in enumerate(unique_contacts, 1):

        if test_mode:
            email = SENDER_EMAIL  # send test to self
            desk_email = ""
            log.info(f"TEST MODE: redirecting to {email}")

        try:
            html = build_html_body(first_name, full_name, org, division, category)
            plain = build_plain_body(first_name, full_name, org, division, category)

            if dry_run:
                log.info(f"[{idx}/{total}] PREVIEW: {full_name} <{email}> ({org}) — {category}")
                # Save first 3 previews as HTML files
                if idx <= 3:
                    preview_path = os.path.join(LOG_DIR, f"preview_{idx}_{first_name}.html")
                    with open(preview_path, "w", encoding="utf-8") as f:
                        f.write(html)
                    log.info(f"  → Saved preview: {preview_path}")
            else:
                send_email(smtp, email, desk_email, SUBJECT, html, plain)
                log.info(f"[{idx}/{total}] SENT ✓ {full_name} <{email}> + desk:{desk_email}")
                sent += 1

            csv_writer.writerow([
                datetime.now().isoformat(), "sent" if not dry_run else "preview",
                full_name, email, desk_email, org, category, ""
            ])

            if test_mode:
                log.info("Test email sent. Exiting.")
                break

            # Rate limiting: pause between batches to avoid Gmail throttling
            if not dry_run and idx % batch_size == 0 and idx < total:
                pause = 30
                log.info(f"  ⏸  Pausing {pause}s after batch of {batch_size}...")
                time.sleep(pause)

        except Exception as e:
            failed += 1
            log.error(f"[{idx}/{total}] FAILED ✗ {full_name} <{email}>: {e}")
            csv_writer.writerow([
                datetime.now().isoformat(), "failed",
                full_name, email, desk_email, org, category, str(e)
            ])

    csv_file.close()

    if smtp:
        smtp.quit()

    log.info("=" * 50)
    log.info(f"COMPLETE — Sent: {sent}  Failed: {failed}  Total: {total}")
    log.info(f"Log saved: {LOG_FILE}")
    log.info("=" * 50)


if __name__ == "__main__":
    main()
