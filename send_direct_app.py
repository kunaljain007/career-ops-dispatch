import smtplib
import json
import sys
import os
from email.message import EmailMessage

sys.stdout.reconfigure(encoding='utf-8')

pool = json.load(open('data/smtp_pool.json'))
sender = next((a for a in pool if a.get('user') and a.get('pass')), None)

if not sender:
    print('Error: No SMTP account available')
    sys.exit(1)

msg = EmailMessage()
msg['From'] = f"Dr. Kumarpal Porwal <{sender['user']}>"
msg['To'] = 'james@leveragelivelocal.com'
msg['Subject'] = 'Application: Head of Operations (Remote) — Dr. Kumarpal Porwal'

body = """Dear James,

I am writing to express my strong interest in the Head of Operations (Remote) position at Leverage Live Local.

As an experienced Operations & Transformation Leader (former Founder & Managing Director, and Chief of Staff at Vega Aviation), I specialize in scaling operational efficiency, streamlining cross-functional workflows, and driving high-velocity remote team execution.

Key Value Delivered:
• Operations & Automation: Architected distributed multi-agent systems boosting operational efficiency by 40% across engineering and operations.
• Commercial & Execution Rigor: Forged institutional partnerships with Amul, Defence Forces, and Emirates Flight Catering; delivered rigorous zero-defect execution.
• Remote Leadership: Proven track record driving distributed teams with clear OKRs, transparent asynchronous communication, and measurable performance tracking.

My resume is attached for your review. I would welcome a brief conversation to explore how I can support Leverage Live Local's operational scale.

Best regards,

Dr. Kumarpal Porwal
+91 73533 19757
founder.heatbolt@gmail.com
LinkedIn: https://www.linkedin.com/in/kumarpal-porwal
"""

msg.set_content(body)

# Attach resume
resume_path = 'C:/Users/My/Desktop/kumarpalshreeram.pdf'
if not os.path.exists(resume_path):
    resume_path = 'cv-cos.pdf'

with open(resume_path, 'rb') as f:
    pdf_data = f.read()
    msg.add_attachment(pdf_data, maintype='application', subtype='pdf', filename='Dr_Kumarpal_Porwal_Resume.pdf')

with smtplib.SMTP(sender.get('host', 'smtp.gmail.com'), int(sender.get('port', 587)), timeout=30) as s:
    s.starttls()
    s.login(sender['user'], sender['pass'])
    s.send_message(msg)

print('SUCCESS: Application sent directly to james@leveragelivelocal.com with resume attached')
