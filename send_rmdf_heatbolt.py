import smtplib
from email.message import EmailMessage
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

def send_rmdf_email():
    sender_email = "founder.heatbolt@gmail.com"
    app_password = "klyc waca kpmi qgoj"
    
    to_emails = ["rmdf@rmdgroup.net"]
    cc_emails = ["rmdhariwal@manikchandgroup.com", "a_dhariwal@manikchandgroup.com"]
    
    teaser_pdf = r"E:\heatbolt investment 2026\E__heatbolt investment 2026_Heatbolt teaser.pdf"
    endorsement_img = r"E:\heatbolt investment 2026\endorsement (1).PNG"

    subject = "Strategic Partnership & Investment: Heatbolt — Zero-Electricity Thermal Platform"
    
    html_body = """
    <div style="font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #2D3748; max-width: 680px; margin: 0 auto; padding: 25px; border: 1px solid #E2E8F0; border-radius: 8px;">
      <p>Respected Dhariwal Ji & Trustees / Leadership of RMD Group & Foundation,</p>
      
      <p>Jai Jinendra,</p>
      
      <p>I hope this message finds you in great health and spirits.</p>
      
      <p>I am <b>Dr. Kumarpal Porwal</b>, Founder & CEO of <b>Heatbolt</b> (Shree Nakoda Parshwa Industries, Belagavi, Karnataka). Given RMD Group and RMD Foundation's legendary leadership across pan-India FMCG distribution, manufacturing excellence, and philanthropic humanitarian support, I am reaching out to introduce our patented, deep-tech thermal infrastructure platform.</p>
      
      <h3 style="color: #DD6B20; border-bottom: 2px solid #ED8936; padding-bottom: 4px; display: inline-block;">What is Heatbolt?</h3>
      <p>Heatbolt is the world's first scalable, water-activated thermochemical heating platform capable of instantly generating <b>controlled temperatures of up to 100°C using only a few drops of water</b> — completely eliminating the need for:</p>
      <ul>
        <li>Electricity or Batteries</li>
        <li>Gas / LPG / Open Flame</li>
        <li>Traditional Boiler or Heating Infrastructure</li>
      </ul>
      
      <h3 style="color: #DD6B20; border-bottom: 2px solid #ED8936; padding-bottom: 4px; display: inline-block;">Key Milestones & Validation</h3>
      <ul>
        <li><b>Defence & Survival Validation:</b> Tested and validated under extreme operational conditions (-60°C) with the Indian Armed Forces in high-altitude sectors (Siachen Glacier).</li>
        <li><b>Humanitarian & Disaster Relief:</b> Instant flameless heat, hot meals, and boiling water in off-grid disaster zones, relief camps, and remote outposts.</li>
        <li><b>Commercial Scale & Off-Grid Utility:</b> In active discussions and pilots with Indian Railways, leading FMCG/F&B giants, and international packaging distributors.</li>
        <li><b>Endorsed:</b> Promoted by Startup India, Invest India, and recognized as a transformative Make-in-India physical hardware platform.</li>
      </ul>
      
      <p>We are currently establishing strategic industrial partnerships and finalizing our institutional growth round to scale commercial production facilities and packaging integration.</p>
      
      <p>I have attached our <b>Executive Teaser PDF</b> for your review. I would consider it an absolute honor to present a brief 10–15 minute briefing and live demonstration at your convenience in Pune or virtually.</p>
      
      <p style="margin-top: 25px;">With highest regards and respect,</p>
      <p style="margin-bottom: 5px;"><b>Dr. Kumarpal Porwal</b><br>
      Founder & CEO — Heatbolt<br>
      Shree Nakoda Parshwa Industries<br>
      Belagavi, Karnataka, India<br>
      📞 +91 73533 19757 | +91 88672 94189<br>
      ✉️ <a href="mailto:founder.heatbolt@gmail.com" style="color: #3182CE;">founder.heatbolt@gmail.com</a></p>
      
      <div style="margin-top: 20px; padding-top: 15px; border-top: 1px solid #E2E8F0; font-size: 12px; color: #718096; font-style: italic;">
        "Where infrastructure cannot follow, essential capability should."
      </div>
    </div>
    """
    
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = f'"Dr. Kumarpal Porwal" <{sender_email}>'
    msg['To'] = ", ".join(to_emails)
    msg['Cc'] = ", ".join(cc_emails)
    msg['Reply-To'] = sender_email
    
    msg.set_content(
        "Respected Dhariwal Ji & Trustees / Leadership of RMD Group & Foundation,\n\n"
        "Jai Jinendra,\n\n"
        "I am Dr. Kumarpal Porwal, Founder & CEO of Heatbolt (Belagavi, Karnataka). "
        "Given RMD Group and RMD Foundation's legendary leadership across pan-India FMCG distribution, "
        "manufacturing excellence, and philanthropic humanitarian support, I am reaching out to introduce our patented, "
        "zero-electricity thermal infrastructure platform.\n\n"
        "Please find our Executive Teaser PDF attached for your review. "
        "I would be deeply honoured to present a brief 10-15 minute briefing at your convenience.\n\n"
        "With highest regards,\n"
        "Dr. Kumarpal Porwal\n"
        "Founder & CEO — Heatbolt\n"
        "+91 73533 19757 | +91 88672 94189\n"
        "founder.heatbolt@gmail.com\n"
    )
    msg.add_alternative(html_body, subtype='html')
    
    # Attachments
    if os.path.exists(teaser_pdf):
        with open(teaser_pdf, 'rb') as f:
            pdf_data = f.read()
        msg.add_attachment(pdf_data, maintype='application', subtype='pdf', filename='Heatbolt_Executive_Teaser.pdf')
        print(f"Attached teaser: {teaser_pdf}")
    else:
        print(f"Warning: Teaser not found at {teaser_pdf}")

    if os.path.exists(endorsement_img):
        with open(endorsement_img, 'rb') as f:
            img_data = f.read()
        msg.add_attachment(img_data, maintype='image', subtype='png', filename='StartupIndia_InvestIndia_Endorsement.png')
        print(f"Attached endorsement image: {endorsement_img}")

    all_recipients = to_emails + cc_emails
    print(f"Connecting to SMTP server...")
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=120)
    server.login(sender_email, app_password)
    print(f"Authenticated as {sender_email}")
    server.send_message(msg)
    server.quit()
    print(f"SUCCESS: Email sent to {all_recipients} via {sender_email}!")

if __name__ == "__main__":
    send_rmdf_email()
