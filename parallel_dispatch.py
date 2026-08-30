"""
Parallel Email Dispatcher — 16 SMTP accounts, 80 emails each = 1280/run
"""
import json, smtplib, ssl, time, threading, sys, os
from email.message import EmailMessage
from datetime import datetime

import email.utils
import random

QUEUE_FILE = os.path.join(os.path.dirname(__file__), 'data', 'all_unsent_emails.json')
BATCH_PER_ACCOUNT = 80
DELAY = 1.0  # 1.0s safe delay to prevent rate-limit bounces
LOCK = threading.Lock()

def is_valid_email(email):
    if not email or '@' not in email:
        return False
    local, domain = email.rsplit('@', 1)
    if '.' not in domain or len(domain.split('.')[-1]) < 2:
        return False
    if 'xxxx' in email.lower() or 'xxxxx' in email.lower() or '*' in email:
        return False
    return True

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

EMAIL_SUBJECT = "If This Journey Has a Purpose, I Believe It Begins with You"

def get_greeting(to_addr):
    local = to_addr.split('@')[0]
    parts = [p for p in local.replace('_', '.').replace('-', '.').split('.') if p and not any(c.isdigit() for c in p)]
    generic = {'info', 'admin', 'contact', 'support', 'sales', 'careers', 'recruitment', 'grievances', 'shares', 'iepf', 'office', 'press', 'media', 'team', 'jobs', 'hello', 'general', 'procurement', 'marketing', 'investors', 'inquiry', 'enquiry', 'help', 'services', 'corp', 'service'}
    if parts and parts[0].lower() not in generic and len(parts[0]) > 1:
        return f"Dear {parts[0].capitalize()},"
    return "Dear Sir/Madam,"

def build_email_content(to_addr):
    greeting = get_greeting(to_addr)
    
    text_content = f"""{greeting}

I hope this message finds you in good health and high spirits.

Today, I am writing to you not merely as the Founder of Heatbolt, but as an entrepreneur whose journey has been shaped by a deeply personal purpose.

For years, one question has stayed with me:
Can innovation do more than create convenience? Can it genuinely improve lives?

That single question became the foundation of everything I have built.

A Purpose Beyond Business

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

The Birth of Heatbolt

Instead of asking, "What product can I build?"
I began asking, "What problems deserve to be solved?"

Could we reduce food wastage?
Could we reduce dependence on conventional heating?
Could we rethink packaging?
Could we make hot food accessible anywhere?
Could India create an entirely new technology platform for the world?

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

More Than Heat — A New Packaging Ecosystem

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

Rather than solving a single problem, Heatbolt aims to address multiple interconnected challenges through one integrated platform.

Current Momentum & Execution

The response to Heatbolt has been highly encouraging. Today, we have achieved:
• 60,000+ stakeholder engagements across India and international markets.
• 1,000+ inbound calls and emails every day from corporates, government organizations, institutions, and international partners.
• Active engagements with leading global companies including Barilla, Nestlé, Mondelēz, Unilever, PepsiCo, Kraft Heinz, Mars, General Mills, Ajinomoto, Campbell's, The Coca-Cola Company, Starbucks, Yum! Brands, and McDonald's.
• Ongoing discussions across Indian Railways, airlines, defence, healthcare, pharmaceuticals, hospitality, food delivery, religious institutions, disaster relief, and industrial sectors.

Heatbolt has also been recently promoted by Startup India and Invest India, and is currently trending virally on the internet.

Commercial enquiries and market assessments indicate the potential to support manufacturing volumes exceeding 20 billion Heatbolt-enabled units annually, with demand continuing to grow across domestic and international markets.

Over the years, I have assembled a multidisciplinary team comprising scientists, food technologists, packaging specialists, manufacturing leaders, and domain specialists with decades of experience.

Together, we are building not only a product, but an organization capable of delivering this vision at global scale.

Links:
• Urgent Need to Solve the Problem: https://www.linkedin.com/posts/kumarpal-porwal_heatbolt-makeinindia-innovation-activity-7486186134474207232-dmlc
• We Have the Solution: https://www.linkedin.com/posts/rohansachdeva20_makeinindia-innovation-foodtech-share-7483541963657605120-TCKs

A Humble Request

Given your organization's track record in scaling transformative technology platforms globally, I believe Heatbolt's integrated portable thermal and packaging ecosystem—with demand indicators pointing to 20 billion+ units annually—presents the kind of category-defining opportunity that aligns with your organization's growth capital mandate.

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

    html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #1a1a1a; margin: 0; padding: 20px; }}
.container {{ max-width: 680px; margin: 0 auto; background: #ffffff; }}
p {{ margin: 0 0 16px 0; font-size: 15px; color: #2d3748; }}
h2 {{ font-size: 18px; color: #1a202c; margin-top: 28px; margin-bottom: 12px; font-weight: 700; border-bottom: 1px solid #edf2f7; padding-bottom: 6px; }}
.brand-box {{ background: #f7fafc; border-left: 4px solid #3182ce; padding: 16px; margin: 20px 0; border-radius: 0 8px 8px 0; }}
.brand-title {{ font-size: 18px; font-weight: 800; color: #2b6cb0; margin-bottom: 4px; }}
.brand-subtitle {{ font-size: 13px; font-weight: 600; color: #4a5568; margin-bottom: 12px; text-transform: uppercase; letter-spacing: 0.5px; }}
ul {{ margin: 0 0 16px 0; padding-left: 22px; }}
li {{ margin-bottom: 6px; font-size: 15px; color: #2d3748; }}
.link-box {{ background: #ebf8ff; border: 1px solid #bee3f8; padding: 14px 18px; border-radius: 8px; margin: 20px 0; }}
.link-box a {{ color: #2b6cb0; text-decoration: underline; font-weight: 600; }}
.signature {{ margin-top: 30px; padding-top: 20px; border-top: 2px solid #edf2f7; }}
.quote {{ font-style: italic; color: #718096; font-size: 14px; margin-top: 8px; }}
</style>
</head>
<body>
<div class="container">
  <p>{greeting}</p>
  <p>I hope this message finds you in good health and high spirits.</p>
  <p>Today, I am writing to you not merely as the Founder of Heatbolt, but as an entrepreneur whose journey has been shaped by a deeply personal purpose.</p>
  <p>For years, one question has stayed with me:<br><strong>Can innovation do more than create convenience? Can it genuinely improve lives?</strong></p>
  <p>That single question became the foundation of everything I have built.</p>

  <h2>A Purpose Beyond Business</h2>
  <p>Life has a way of changing our priorities.<br>Like countless families across the world, mine has experienced the pain of losing loved ones. I have seen how one illness can change the course of an entire family.</p>
  <p>When a father is lost, a family loses its pillar.<br>When a mother is lost, a home loses its heart.<br>When a son or daughter is lost, parents carry that pain for a lifetime.</p>
  <p>Behind every patient is an entire family whose lives are forever changed.</p>
  <p>Every year, cancer claims nearly 10 million lives globally, including more than 900,000 lives in India. Behind these numbers are people, families, and dreams.</p>
  <p>At the same time, billions of single-use plastic packages are discarded every year. Researchers continue to investigate the long-term health implications of microplastics and chemicals associated with certain plastic products. While the science is still evolving, reducing unnecessary plastic waste and advancing safer, more sustainable packaging is widely recognized as an important environmental and public-health priority.</p>
  <p>These realities reinforced a belief that has guided my entrepreneurial journey:<br><em>"Prevention is always better than cure."</em></p>
  <p>That belief became my purpose.</p>

  <h2>The Birth of Heatbolt</h2>
  <p>Instead of asking, "What product can I build?"<br>I began asking, "What problems deserve to be solved?"</p>
  <p>Could we reduce food wastage?<br>Could we reduce dependence on conventional heating?<br>Could we rethink packaging?<br>Could we make hot food accessible anywhere?<br>Could India create an entirely new technology platform for the world?</p>
  <p>Those questions led to the creation of Heatbolt.</p>

  <div class="brand-box">
    <div class="brand-title">HEATBOLT</div>
    <div class="brand-subtitle">Portable Thermal Infrastructure | Self-Heating Packaging | Sustainable Innovation</div>
    <p style="margin-bottom: 8px;">Heatbolt is a proprietary portable thermal platform capable of generating temperatures of up to 100°C using only water, without requiring:</p>
    <ul>
      <li>Electricity</li>
      <li>LPG or Gas</li>
      <li>Batteries</li>
      <li>Open Flame</li>
      <li>External Heating Infrastructure</li>
    </ul>
    <p style="margin-bottom: 0;">The technology integrates directly into cups, bowls, trays, pouches, lunch boxes, containers, and customized packaging, enabling consumers to enjoy freshly heated food and beverages anytime, anywhere.</p>
  </div>

  <p>But Heatbolt is more than a self-heating solution.<br>It is a new category of portable thermal infrastructure with applications across multiple industries and geographies.</p>

  <h2>More Than Heat — A New Packaging Ecosystem</h2>
  <p>Perhaps the most exciting aspect of Heatbolt is not the heat itself. It is the packaging.</p>
  <p>Our integrated packaging platform has the potential to provide up to one year of shelf life for selected ready-to-eat foods, beverages, nutritional products, and wellness solutions.</p>
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

  <h2>Current Momentum & Execution</h2>
  <p>The response to Heatbolt has been highly encouraging. Today, we have achieved:</p>
  <ul>
    <li><strong>60,000+</strong> stakeholder engagements across India and international markets.</li>
    <li><strong>1,000+</strong> inbound calls and emails every day from corporates, government organizations, institutions, and international partners.</li>
    <li><strong>Active engagements with leading global companies</strong> including Barilla, Nestlé, Mondelēz, Unilever, PepsiCo, Kraft Heinz, Mars, General Mills, Ajinomoto, Campbell's, The Coca-Cola Company, Starbucks, Yum! Brands, and McDonald's.</li>
    <li><strong>Ongoing discussions</strong> across Indian Railways, airlines, defence, healthcare, pharmaceuticals, hospitality, food delivery, religious institutions, disaster relief, and industrial sectors.</li>
    <li>Heatbolt has also been recently promoted by Startup India and Invest India, and is currently trending virally on the internet.</li>
  </ul>
  <p>Commercial enquiries and market assessments indicate the potential to support manufacturing volumes exceeding 20 billion Heatbolt-enabled units annually, with demand continuing to grow across domestic and international markets.</p>
  <p>Over the years, I have assembled a multidisciplinary team comprising scientists, food technologists, packaging specialists, manufacturing leaders, and domain specialists with decades of experience. Together, we are building not only a product, but an organization capable of delivering this vision at global scale.</p>

  <div class="link-box">
    <p style="margin-bottom: 6px;"><strong>Watch on LinkedIn:</strong></p>
    <p style="margin-bottom: 4px;">• <a href="https://www.linkedin.com/posts/kumarpal-porwal_heatbolt-makeinindia-innovation-activity-7486186134474207232-dmlc" target="_blank">Urgent Need to Solve the Problem</a></p>
    <p style="margin-bottom: 0;">• <a href="https://www.linkedin.com/posts/rohansachdeva20_makeinindia-innovation-foodtech-share-7483541963657605120-TCKs" target="_blank">We Have the Solution</a></p>
  </div>

  <h2>A Humble Request</h2>
  <p>Given your organization's track record in scaling transformative technology platforms globally, I believe Heatbolt's integrated portable thermal and packaging ecosystem—with demand indicators pointing to 20 billion+ units annually—presents the kind of category-defining opportunity that aligns with your organization's growth capital mandate.</p>
  <p>We are seeking strategic partners who believe that meaningful innovation can create commercial value while addressing important global challenges.</p>
  <p>Whether through strategic investment, manufacturing collaboration, commercialization partnerships, technology licensing, or market access, we believe Heatbolt has the potential to become one of India's next globally recognized technology platforms.</p>
  <p>I would be deeply honoured to present our technology, commercialization roadmap, and long-term vision in a brief 15-minute meeting at your convenience.</p>
  <p>Thank you very much for your valuable time and consideration. I sincerely look forward to the opportunity to connect and explore how we can build this journey together.</p>

  <div class="signature">
    <p style="margin-bottom: 4px;">With warm regards,</p>
    <p style="margin-bottom: 4px; font-weight: 700; color: #1a202c;">Dr. Kumarpal Porwal</p>
    <p style="margin-bottom: 4px; color: #4a5568;">Founder & CEO | Heatbolt</p>
    <p style="margin-bottom: 4px; color: #4a5568;">+91 73533 19757 | +91 88672 94189 (WhatsApp Preferred)</p>
    <p style="margin-bottom: 12px;"><a href="mailto:founder.heatbolt@gmail.com" style="color: #3182ce;">founder.heatbolt@gmail.com</a></p>
    <p class="quote">"If you want to walk fast, walk alone. If you want to walk far, walk together." — Ratan Tata</p>
    <p class="quote">"The future of convenience is not just portable food and beverages—it is portable heat."</p>
  </div>
</div>
</body>
</html>
"""
    return text_content, html_content

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
    msg['From']    = f"Dr. Kumarpal Porwal <{user}>"
    msg['Reply-To'] = "founder.heatbolt@gmail.com"
    msg['To']      = to_addr
    msg['Date']    = email.utils.formatdate(localtime=True)
    msg['Message-ID'] = email.utils.make_msgid(domain="gmail.com")
    
    text_part, html_part = build_email_content(to_addr)
    msg.set_content(text_part)
    msg.add_alternative(html_part, subtype='html')
    
    ctx = ssl.create_default_context()
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=20) as srv:
        srv.ehlo(); srv.starttls(context=ctx); srv.ehlo()
        srv.login(user, pw)
        srv.send_message(msg)

def worker(account, batch):
    user = account['user']
    pw   = account['pass']
    sent = 0; failed_addrs = []
    print(f"[START] {user} -> {len(batch)} emails")
    for addr in batch:
        if not is_valid_email(addr):
            print(f"  [SKIP INVALID] {user} -> {addr}")
            continue
        try:
            send_one(user, pw, addr)
            sent += 1
            print(f"  [OK] {user} -> {addr}")
        except Exception as e:
            failed_addrs.append(addr)
            print(f"  [FAIL] {user} -> {addr}: {e}", file=sys.stderr)
        time.sleep(random.uniform(0.9, 1.4))
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
