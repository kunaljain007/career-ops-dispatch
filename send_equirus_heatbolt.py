import smtplib
from email.message import EmailMessage
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

def send_equirus_email():
    sender_email = "team.heatbolt@gmail.com"
    app_password = "fusa vdmp mpqo kdmc"
    to_email = "rituraj.chaudhari@equirusasset.com"
    
    teaser_pdf = r"E:\heatbolt investment 2026\E__heatbolt investment 2026_Heatbolt teaser.pdf"
    endorsement_img = r"E:\heatbolt investment 2026\endorsement (1).PNG"

    subject = "Strategic Investment Opportunity: Heatbolt — Patented Zero-Electricity Thermal Platform"
    
    html_body = """
    <div style="font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #2D3748; max-width: 680px; margin: 0 auto; padding: 25px; border: 1px solid #E2E8F0; border-radius: 8px;">
      <p>Dear Rituraj,</p>
      
      <p>I hope this email finds you well.</p>
      
      <p>I am reaching out from <b>Heatbolt</b> on behalf of our Founder & CEO, <b>Dr. Kumarpal Porwal</b> (PhD in Green Hydrogen, IISc Bangalore, mentored by the late Shri Ratan Tata). Given Equirus Asset Management's strong track record in identifying high-growth compounding businesses and disruptive market leaders, we wanted to introduce our patented, deep-tech thermal infrastructure platform.</p>
      
      <h3 style="color: #DD6B20; border-bottom: 2px solid #ED8936; padding-bottom: 4px; display: inline-block;">What is Heatbolt?</h3>
      <p>Heatbolt is the world's first scalable, water-activated thermochemical platform generating <b>instant 100°C heat and steam using only a few drops of water</b> — completely eliminating the need for electricity, gas, LPG, batteries, or open flame.</p>
      
      <h3 style="color: #DD6B20; border-bottom: 2px solid #ED8936; padding-bottom: 4px; display: inline-block;">Commercial Traction & Strategic Milestones</h3>
      <ul>
        <li><b>Defence & Survival Validation:</b> Validated by the Indian Armed Forces under extreme high-altitude conditions (-60°C at Siachen Glacier).</li>
        <li><b>Enterprise & Institutional Pipeline:</b> Active discussions and LOIs with Indian Railways, leading FMCG/F&B giants (Haldiram, ITC, Kellogg's), and defense/disaster relief bodies.</li>
        <li><b>Attractive Unit Economics:</b> High ~50% unit contribution margin with global export potential across defense, ready-to-eat packaging, and off-grid utilities.</li>
        <li><b>National Endorsement:</b> Recognized and promoted by Startup India and Invest India.</li>
      </ul>
      
      <p>As we finalize our institutional growth round to scale commercial manufacturing and packaging integration, we believe Heatbolt represents a rare physical deep-tech asset with immense dual-use scale.</p>
      
      <p>Please find our <b>Executive Teaser PDF</b> attached for your review. We would welcome the opportunity to schedule a brief 15-minute introductory call next week.</p>
      
      <p style="margin-top: 25px;">Warm regards,</p>
      <p style="margin-bottom: 5px;"><b>Investment Relations Team</b><br>
      On behalf of <b>Dr. Kumarpal Porwal</b> (Founder & CEO)<br>
      Heatbolt | Shree Nakoda Parshwa Industries<br>
      📞 +91 73533 19757 | +91 88672 94189<br>
      ✉️ <a href="mailto:founder.heatbolt@gmail.com" style="color: #3182CE;">founder.heatbolt@gmail.com</a> | <a href="mailto:team.heatbolt@gmail.com" style="color: #3182CE;">team.heatbolt@gmail.com</a></p>
      
      <div style="margin-top: 20px; padding-top: 15px; border-top: 1px solid #E2E8F0; font-size: 12px; color: #718096; font-style: italic;">
        "Where infrastructure cannot follow, essential capability should."
      </div>
    </div>
    """
    
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = f'"Heatbolt Team" <{sender_email}>'
    msg['To'] = to_email
    msg['Reply-To'] = "founder.heatbolt@gmail.com"
    
    plain_text = (
        "Dear Rituraj,\n\n"
        "I hope this email finds you well.\n\n"
        "I am reaching out from Heatbolt on behalf of our Founder & CEO, Dr. Kumarpal Porwal. "
        "Given Equirus Asset Management's track record in backing market-leading growth businesses, "
        "we wanted to introduce Heatbolt — the world's first scalable, water-activated thermochemical heating platform "
        "generating instant 100°C heat without electricity, gas, or open flame.\n\n"
        "Our technology has been validated at the Siachen Glacier (-60°C) with the Indian Armed Forces, "
        "and is endorsed by Startup India & Invest India. Please find our Executive Teaser PDF attached.\n\n"
        "We would love to schedule a brief 15-minute introductory discussion next week.\n\n"
        "Warm regards,\n"
        "Heatbolt Team\n"
        "team.heatbolt@gmail.com | founder.heatbolt@gmail.com\n"
        "+91 73533 19757\n"
    )
    msg.set_content(plain_text)
    msg.add_alternative(html_body, subtype='html')
    
    # Attachments
    if os.path.exists(teaser_pdf):
        with open(teaser_pdf, 'rb') as f:
            pdf_data = f.read()
        msg.add_attachment(pdf_data, maintype='application', subtype='pdf', filename='Heatbolt_Executive_Teaser.pdf')
        print(f"Attached teaser: {teaser_pdf}")

    if os.path.exists(endorsement_img):
        with open(endorsement_img, 'rb') as f:
            img_data = f.read()
        msg.add_attachment(img_data, maintype='image', subtype='png', filename='StartupIndia_InvestIndia_Endorsement.png')
        print(f"Attached endorsement image: {endorsement_img}")

    print("Connecting to SMTP server...")
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=120)
    server.login(sender_email, app_password)
    print(f"Authenticated as {sender_email}")
    server.send_message(msg)
    server.quit()
    print(f"SUCCESS: Email sent to {to_email} via {sender_email}!")

if __name__ == "__main__":
    send_equirus_email()
