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
msg['To'] = 'careers@extrahop.com'
msg['Subject'] = 'Application: Sr Solutions Architect (Remote) — Dr. Kumarpal Porwal'

body = """Dear ExtraHop Hiring Team,

I am writing to submit my application for the Sr Solutions Architect (Remote) role at ExtraHop.

With a rich background in systems architecture, enterprise technology integration, and complex root-cause resolution, I have consistently aligned technical capabilities with mission-critical customer outcomes.

Relevant Qualifications:
• Technical & Operational Leadership: Chief of Staff & AI Strategist at Vega Aviation; architected and deployed distributed multi-agent autonomous AI systems, generating an immediate 40% operational efficiency surge.
• Enterprise Problem-Solving: Extensive experience analyzing complex system topologies, network data, and application stacks to eliminate bottlenecks and optimize throughput.
• Deep-Tech Commercialization & Client Trust: Founder & MD at HeatBolt/Parshwa Power, forging long-term institutional partnerships with Amul, Defence Forces, and Emirates Flight Catering under rigorous standards.
• PhD in Green Hydrogen (IISc Bangalore Research): Advanced technical rigor, quantitative analysis, and rapid mastery of proprietary technology stacks.

My resume is attached for your review. I look forward to discussing how I can deliver exceptional architecture and client outcomes for ExtraHop.

Sincerely,

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

print('SUCCESS: Application sent directly to careers@extrahop.com with resume attached')
