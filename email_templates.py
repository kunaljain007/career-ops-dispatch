"""
Heatbolt Mass Mail-Merge Script
================================
Sends personalized outreach emails to all contacts from founder.heatbolt@gmail.com
CC: team.heatbolt@gmail.com

BEFORE RUNNING:
  1. Generate a Gmail App Password:
     ??? Go to https://myaccount.google.com/apppasswords
     ??? Create an app password for "Mail"
     ??? Copy the 16-character password
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

# ???????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????
# CONFIGURATION
# ???????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????
SENDER_EMAIL = "founder.heatbolt@gmail.com"
CC_EMAIL = "team.heatbolt@gmail.com"
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SUBJECT = "If This Journey Has a Purpose, I Believe It Begins with You"

def build_plain_body(first_name: str, full_name: str, org: str, division: str, category: str) -> str:
    return f"""Dear {first_name},

I hope this message finds you in good health and high spirits.

We have successfully concluded our high-level meetings in Delhi with the Ministry of Defence, Ministry of Home Affairs, Ministry of Railways, and several other stakeholders, receiving encouraging responses regarding HeatBolt’s potential applications.

We are also seeing growing international interest, with Nestlé exploring potential introduction across 192 countries and Barilla Group across 100 countries, alongside discussions with other global industry leaders.

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
"Prevention is always better than cure." That belief became my purpose.

The Birth of Heatbolt
Instead of asking, "What product can I build?"
I began asking, "What problems deserve to be solved?"
- Could we reduce food wastage?
- Could we reduce dependence on conventional heating?
- Could we rethink packaging?
- Could we make hot food accessible anywhere?
- Could India create an entirely new technology platform for the world?

Those questions led to the creation of Heatbolt.

HEATBOLT
Portable Thermal Infrastructure | Self-Heating Packaging | Sustainable Innovation
Heatbolt is a proprietary portable thermal platform capable of generating temperatures of up to 100°C using only water, without requiring Electricity, LPG or Gas, Batteries, Open Flame, or External Heating Infrastructure.

More Than Heat — A New Packaging Ecosystem
Our integrated packaging platform has the potential to provide up to one year of shelf life for selected ready-to-eat foods, beverages, nutritional products, and wellness solutions.

This can help:
- Reduce food wastage.
- Reduce dependence on refrigeration and cold-chain logistics.
- Improve food accessibility in remote and underserved regions.
- Support emergency preparedness and humanitarian relief.
- Enable more sustainable packaging formats.
- Create export-ready solutions for global markets.

Current Momentum & Execution
The response to Heatbolt has been highly encouraging:
- 60,000+ stakeholder engagements across India and international markets.
- 1,000+ inbound calls and emails every day from corporates, government organizations, institutions, and international partners.
- Active engagements with leading global companies including Barilla, Nestlé, Mondelēz, Unilever, PepsiCo, Kraft Heinz, Mars, General Mills, Ajinomoto, Campbell's, The Coca-Cola Company, Starbucks, Yum! Brands, and McDonald's.
- Ongoing discussions across Indian Railways, airlines, defence, healthcare, pharmaceuticals, hospitality, food delivery, religious institutions, disaster relief, and industrial sectors.
- Promoted by Startup India and Invest India, currently trending virally.
- Commercial enquiries indicate potential to support manufacturing volumes exceeding 20 billion Heatbolt-enabled units annually.

A Humble Request
Given your organization’s track record in scaling transformative technology platforms globally, I believe Heatbolt’s integrated portable thermal and packaging ecosystem presents a category-defining opportunity that aligns with your mandate.

Whether through strategic investment, manufacturing collaboration, commercialization partnerships, technology licensing, or market access, we believe Heatbolt has the potential to become one of India’s next globally recognized technology platforms.

I would be deeply honoured to present our technology, commercialization roadmap, and long-term vision in a brief 15-minute meeting at your convenience.

Thank you very much for your valuable time and consideration.

With warm regards,

Dr. Kumarpal Porwal
Founder & CEO | Heatbolt
+91 73533 19757 | +91 88672 94189 (WhatsApp Preferred)
founder.heatbolt@gmail.com

"If you want to walk fast, walk alone. If you want to walk far, walk together." — Ratan Tata
"The future of convenience is not just portable food and beverages — it is portable heat."
"""

def build_html_body(first_name: str, full_name: str, org: str, division: str, category: str) -> str:
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height: 1.68; color: #1f2937; margin: 0; padding: 24px; background-color: #f9fafb; }}
  .card {{ max-width: 680px; margin: 0 auto; background: #ffffff; border-radius: 12px; padding: 36px 40px; border: 1px solid #e5e7eb; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); }}
  .badge {{ display: inline-block; background: #0f172a; color: #ffffff; padding: 4px 12px; border-radius: 9999px; font-size: 11px; font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 20px; }}
  h1 {{ font-size: 22px; font-weight: 700; color: #0f172a; margin-top: 0; margin-bottom: 16px; line-height: 1.35; letter-spacing: -0.02em; }}
  h2 {{ font-size: 16px; font-weight: 600; color: #1e3a8a; margin-top: 28px; margin-bottom: 12px; border-left: 3px solid #2563eb; padding-left: 10px; }}
  p {{ font-size: 14.5px; margin: 14px 0; color: #374151; }}
  .highlight-box {{ background: #f0f9ff; border: 1px solid #bae6fd; border-radius: 8px; padding: 18px 20px; margin: 20px 0; font-size: 14px; color: #0369a1; }}
  ul {{ padding-left: 20px; margin: 12px 0; }}
  li {{ font-size: 14px; color: #4b5563; margin-bottom: 6px; }}
  .quote-box {{ border-left: 3px solid #e2e8f0; padding-left: 14px; font-style: italic; color: #64748b; margin: 22px 0; font-size: 13.5px; }}
  .footer {{ margin-top: 36px; padding-top: 24px; border-top: 1px solid #e5e7eb; font-size: 13.5px; color: #6b7280; }}
  .footer strong {{ color: #111827; }}
</style>
</head>
<body>
<div class="card">
  <div class="badge">Heatbolt | Sustainable Deep-Tech Platform</div>
  <h1>If This Journey Has a Purpose, I Believe It Begins with You</h1>
  
  <p>Dear {first_name},</p>
  <p>I hope this message finds you in good health and high spirits.</p>
  
  <p>We have successfully concluded our high-level meetings in Delhi with the <strong>Ministry of Defence, Ministry of Home Affairs, Ministry of Railways</strong>, and several other key stakeholders, receiving encouraging responses regarding HeatBolt&rsquo;s potential applications.</p>
  
  <p>We are also seeing growing international interest, with <strong>Nestl&eacute;</strong> exploring potential introduction across 192 countries and <strong>Barilla Group</strong> across 100 countries, alongside discussions with other global industry leaders.</p>
  
  <p>Today, I am writing to you not merely as the Founder of Heatbolt, but as an entrepreneur whose journey has been shaped by a deeply personal purpose.</p>
  
  <p>For years, one question has stayed with me:<br>
  <em>Can innovation do more than create convenience? Can it genuinely improve lives?</em><br>
  That single question became the foundation of everything I have built.</p>

  <h2>A Purpose Beyond Business</h2>
  <p>Life has a way of changing our priorities.</p>
  <p>Like countless families across the world, mine has experienced the pain of losing loved ones. I have seen how one illness can change the course of an entire family.</p>
  <p>When a father is lost, a family loses its pillar.<br>
  When a mother is lost, a home loses its heart.<br>
  When a son or daughter is lost, parents carry that pain for a lifetime.<br>
  Behind every patient is an entire family whose lives are forever changed.</p>
  
  <p>Every year, cancer claims nearly 10 million lives globally, including more than 900,000 lives in India. Behind these numbers are people, families, and dreams.</p>
  
  <p>At the same time, billions of single-use plastic packages are discarded every year. Researchers continue to investigate the long-term health implications of microplastics and chemicals associated with certain plastic products. While the science is still evolving, reducing unnecessary plastic waste and advancing safer, more sustainable packaging is widely recognized as an important environmental and public-health priority.</p>
  
  <div class="highlight-box">
    <strong>Core Operating Belief:</strong> &ldquo;Prevention is always better than cure.&rdquo; That belief became my purpose.
  </div>

  <h2>The Birth of Heatbolt</h2>
  <p>Instead of asking, <em>&ldquo;What product can I build?&rdquo;</em> I began asking, <em>&ldquo;What problems deserve to be solved?&rdquo;</em></p>
  <ul>
    <li>Could we reduce food wastage?</li>
    <li>Could we reduce dependence on conventional heating?</li>
    <li>Could we rethink packaging?</li>
    <li>Could we make hot food accessible anywhere?</li>
    <li>Could India create an entirely new technology platform for the world?</li>
  </ul>
  
  <p>Those questions led to the creation of <strong>Heatbolt</strong>.</p>
  
  <div style="background: #0f172a; color: #ffffff; padding: 18px 22px; border-radius: 8px; margin: 18px 0;">
    <div style="font-size: 15px; font-weight: 700; letter-spacing: 0.05em;">HEATBOLT</div>
    <div style="font-size: 12.5px; color: #94a3b8; margin-top: 2px;">Portable Thermal Infrastructure | Self-Heating Packaging | Sustainable Innovation</div>
    <div style="font-size: 13.5px; color: #e2e8f0; margin-top: 10px;">
      Capable of generating temperatures of up to <strong>100&deg;C using only water</strong>, without requiring Electricity, LPG or Gas, Batteries, Open Flame, or External Heating Infrastructure.
    </div>
  </div>

  <h2>More Than Heat &mdash; A New Packaging Ecosystem</h2>
  <p>Our integrated packaging platform has the potential to provide up to <strong>one year of shelf life</strong> for selected ready-to-eat foods, beverages, nutritional products, and wellness solutions.</p>
  <ul>
    <li>Reduce food wastage significantly.</li>
    <li>Reduce dependence on refrigeration and cold-chain logistics.</li>
    <li>Improve food accessibility in remote and underserved regions.</li>
    <li>Support emergency preparedness and humanitarian relief.</li>
    <li>Enable more sustainable packaging formats and export-ready global solutions.</li>
  </ul>

  <h2>Current Momentum &amp; Execution</h2>
  <ul>
    <li><strong>60,000+</strong> stakeholder engagements across India and international markets.</li>
    <li><strong>1,000+</strong> inbound calls and emails daily from corporates, government bodies, and international partners.</li>
    <li>Active engagements with Barilla, Nestl&eacute;, Mondelēz, Unilever, PepsiCo, Kraft Heinz, Mars, General Mills, Ajinomoto, Campbell&rsquo;s, The Coca-Cola Company, Starbucks, Yum! Brands, and McDonald&rsquo;s.</li>
    <li>Ongoing discussions across Indian Railways, airlines, defence, healthcare, hospitality, and disaster relief.</li>
    <li>Promoted by <strong>Startup India</strong> and <strong>Invest India</strong>.</li>
    <li>Commercial assessments indicate support for manufacturing volumes exceeding <strong>20 billion units annually</strong>.</li>
  </ul>

  <h2>A Humble Request</h2>
  <p>Given your organization&rsquo;s track record in scaling transformative platforms, I believe Heatbolt&rsquo;s integrated thermal and packaging ecosystem presents a category-defining opportunity that aligns with your mandate.</p>
  <p>Whether through strategic investment, manufacturing collaboration, commercialization partnerships, technology licensing, or market access, we believe Heatbolt has the potential to become one of India&rsquo;s next globally recognized technology platforms.</p>
  <p>I would be deeply honoured to present our technology, commercialization roadmap, and long-term vision in a brief 15-minute meeting at your convenience.</p>

  <div class="quote-box">
    &ldquo;If you want to walk fast, walk alone. If you want to walk far, walk together.&rdquo; &mdash; <em>Ratan Tata</em><br>
    &ldquo;The future of convenience is not just portable food and beverages &mdash; it is portable heat.&rdquo;
  </div>

  <div class="footer">
    <p>With warm regards,</p>
    <strong>Dr. Kumarpal Porwal</strong><br>
    Founder &amp; CEO | Heatbolt<br>
    +91 73533 19757 | +91 88672 94189 (WhatsApp Preferred)<br>
    <a href="mailto:founder.heatbolt@gmail.com" style="color: #2563eb;">founder.heatbolt@gmail.com</a>
  </div>
</div>
</body>
</html>"""
