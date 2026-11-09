import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
from datetime import datetime

to_email = "Sakshi.Pagnis@ltts.com"
smtp_user = "kumarpalporwal8@gmail.com"
smtp_pass = "tbyy owhw uoyp vovq"

subject = "Executive Leadership & Engineering Strategy / Strategic Advisory Opportunity - Dr. Kumarpal Porwal (L&T Technology Services)"

plain_text = """Dear Sakshi,

I hope this email finds you well.

I am writing to express my strong interest in exploring strategic executive leadership, technology advisory, or engineering strategy leadership opportunities with L&T Technology Services (LTTS).

With an extensive background leading deep-tech hardware engineering, advanced thermodynamics, zero-carbon innovations, and cross-functional technology scale-ups, I have spearheaded transformative hardware ventures and complex multi-disciplinary systems:

- Founder & Deep-Tech Architect of HeatBolt (Shree Nakoda Parshwa Industries), pioneering patented flameless catalytic self-heating physical hardware architectures and industrial thermodynamics.
- Cross-Functional Leadership: Directed end-to-end design, patent portfolio strategy, rigorous regulatory compliance, and scalable manufacturing workflows.
- Strategic Execution: Proven expertise in steering cross-domain engineering teams, driving R&D commercialisation, industrial client partnerships, and enterprise operations.

Given LTTS's pioneering leadership across global engineering R&D (ER&D), smart manufacturing, and sustainable engineering solutions, I would welcome the opportunity to connect with you and discuss how my deep-tech engineering and strategic leadership experience can add immediate value to LTTS's strategic initiatives.

You can also review my work and portfolio at https://heatbolt-in.web.app/

Thank you for your time and consideration. I look forward to the possibility of speaking with you.

Warm regards,

Dr. Kumarpal Porwal
Founder & Deep-Tech Engineering Architect
Phone: +91 73533 19757
Direct Email: kumarpalporwal8@gmail.com
Web: https://heatbolt-in.web.app/
Belgaum, Karnataka, India
"""

html_content = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #2d3748; margin: 0; padding: 20px; background-color: #f7fafc; }
  .card { max-width: 640px; margin: 0 auto; background: #ffffff; border-radius: 8px; border: 1px solid #e2e8f0; padding: 32px; }
  .header { border-bottom: 2px solid #3182ce; padding-bottom: 16px; margin-bottom: 24px; }
  .name { font-size: 20px; font-weight: 700; color: #1a202c; }
  .subtitle { font-size: 14px; color: #718096; margin-top: 4px; }
  .content { font-size: 15px; color: #4a5568; }
  .highlight-box { background: #edf2f7; border-left: 4px solid #3182ce; padding: 14px 18px; margin: 20px 0; border-radius: 0 6px 6px 0; }
  ul { margin: 10px 0; padding-left: 20px; }
  li { margin-bottom: 8px; }
  .contact-footer { margin-top: 28px; padding-top: 20px; border-top: 1px solid #e2e8f0; font-size: 14px; color: #718096; }
</style>
</head>
<body>
<div class="card">
  <div class="header">
    <div class="name">Dr. Kumarpal Porwal</div>
    <div class="subtitle">Executive Engineering Leader | Deep-Tech Architect & Strategist</div>
  </div>
  <div class="content">
    <p>Dear Sakshi,</p>
    <p>I hope this email finds you well.</p>
    <p>I am writing to express my strong interest in exploring strategic executive leadership, technology advisory, or engineering strategy leadership opportunities with <strong>L&T Technology Services (LTTS)</strong>.</p>
    
    <div class="highlight-box">
      <strong>Core Engineering & Leadership Highlights:</strong>
      <ul>
        <li><strong>Deep-Tech Innovation & Thermodynamics:</strong> Founder & Chief Architect behind HeatBolt, pioneering patented flameless catalytic self-heating physical hardware architectures and clean thermal distribution systems.</li>
        <li><strong>End-to-End Scaled Execution:</strong> Directed product design, multi-disciplinary ER&D, patent drafting, industrial safety compliance, and production tooling.</li>
        <li><strong>Enterprise Strategic Leadership:</strong> Track record of bridging complex hardware engineering with corporate strategy, technology licensing, and commercial partnerships.</li>
      </ul>
    </div>

    <p>Given LTTS's global leadership across smart enterprise engineering, industrial IoT, and sustainable technologies, I would welcome the opportunity to discuss how my deep-tech engineering and strategic execution background can drive value across your engineering leadership programs.</p>

    <p>You can also review our work and portfolio at <a href="https://heatbolt-in.web.app/" style="color: #3182ce; text-decoration: none; font-weight: 600;">heatbolt-in.web.app</a>.</p>

    <div class="contact-footer">
      <strong>Dr. Kumarpal Porwal</strong><br>
      Founder & Deep-Tech Engineering Architect<br>
      Direct Email: <a href="mailto:kumarpalporwal8@gmail.com" style="color: #3182ce;">kumarpalporwal8@gmail.com</a><br>
      Mobile: +91 73533 19757<br>
      Belgaum, Karnataka, India
    </div>
  </div>
</div>
</body>
</html>
"""

msg = MIMEMultipart("alternative")
msg["From"] = f"Dr. Kumarpal Porwal <{smtp_user}>"
msg["To"] = to_email
msg["Subject"] = subject
msg["Reply-To"] = smtp_user

msg.attach(MIMEText(plain_text, "plain", "utf-8"))
msg.attach(MIMEText(html_content, "html", "utf-8"))

try:
    server = smtplib.SMTP("smtp.gmail.com", 587, timeout=25)
    server.starttls()
    server.login(smtp_user, smtp_pass)
    server.sendmail(smtp_user, to_email, msg.as_string())
    server.quit()

    sent_file = r"C:\Users\My\.gemini\antigravity\scratch\career-ops\data\sent_emails.json"
    with open(sent_file, "r", encoding="utf-8-sig") as f:
        sent_list = json.load(f)

    entry = {
        "to": to_email,
        "email": to_email,
        "from": smtp_user,
        "subject": subject,
        "status": "sent",
        "timestamp": datetime.now().isoformat(),
        "name": "Sakshi Pagnis",
        "role": "Talent Acquisition / HR Leader",
        "organization": "L&T Technology Services (LTTS)",
        "type": "executive_career_opportunity"
    }
    sent_list.append(entry)

    with open(sent_file, "w", encoding="utf-8") as f:
        json.dump(sent_list, f, indent=2, ensure_ascii=False)

    print(f"SUCCESS: Career opportunity email sent to Sakshi Pagnis <{to_email}> via {smtp_user}")
except Exception as e:
    print(f"ERROR sending to {to_email}: {e}")
