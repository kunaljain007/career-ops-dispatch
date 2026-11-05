# -*- coding: utf-8 -*-
"""
Multi-Corporate Strategic Customizer for HeatBolt Outreach
Builds targeted, highly tailored executive proposals for:
1. Reliance Industries (Jio, Reliance Retail, Defence, New Energy)
2. Aditya Birla Group (Grasim, Hindalco, AB Retail, UltraTech)
3. Mahindra & Mahindra (Defence, Farm/Auto Mobility, Hospitality, Club Mahindra)
4. Sun Pharma & Healthcare Leaders (Emergency care, clinical patient nutrition)
5. Torrent Group (Torrent Pharma, Torrent Power, Gas infrastructure)
6. Gates Foundation & Global Impact Funds (Humanitarian relief, malnutrition, zero-infrastructure warmth)
"""

import json, os, sys

CORPORATE_PROFILES = {
    "reliance": {
        "name": "Reliance Leadership Team",
        "org_name": "Reliance Industries & Jio-Retail Ecosystem",
        "synergies": (
            "We see massive transformative synergies across <strong>Reliance Retail (Smart Bazaar, Fresh), JioMart, "
            "Defence & Homeland Security, and New Energy platforms</strong> — packaging millions of fresh, self-heated daily meals "
            "and expanding into cold-chain-free retail logistics across 18,000+ stores nationwide."
        ),
        "investment_ask": "USD 12–15 million in strategic growth capital or joint venture commercialization",
        "vision_hook": "Deploying indigenous, zero-emission thermal infrastructure across India's largest retail and strategic logistics network."
    },
    "aditya_birla": {
        "name": "Aditya Birla Leadership Team",
        "org_name": "Aditya Birla Group",
        "synergies": (
            "We see high-value synergies across <strong>Aditya Birla Retail, Grasim Industries, and Hindalco</strong> "
            "for advanced sustainable packaging substrates, circular materials, and massive institutional distribution across "
            "industrial, retail, and consumer portfolios."
        ),
        "investment_ask": "USD 10–12 million in strategic investment and manufacturing co-development",
        "vision_hook": "Combining world-class materials engineering with revolutionary self-heating thermal architecture."
    },
    "mahindra": {
        "name": "Mahindra Leadership Team",
        "org_name": "Mahindra Group",
        "synergies": (
            "Direct operational synergies across <strong>Mahindra Defence Systems, Club Mahindra (remote hospitality), "
            "and Farm/Commercial Fleet Mobility</strong> — delivering Siachen-validated, zero-emission portable heating without "
            "electricity or open flames in remote terrain, defence missions, and extreme weather."
        ),
        "investment_ask": "USD 10 million in strategic capital and defence-grade supply chain integration",
        "vision_hook": "Enabling zero-electricity thermal mobility for remote terrain, defence forces, and off-grid hospitality."
    },
    "sunpharma": {
        "name": "Sun Pharma Leadership Team",
        "org_name": "Sun Pharma & Healthcare Ecosystem",
        "synergies": (
            "Vital applications in <strong>clinical enteral nutrition, emergency patient warming, disaster relief medicine, "
            "and temperature-controlled therapeutic food distribution</strong> across rural healthcare networks without reliance on cold chains."
        ),
        "investment_ask": "USD 8–10 million strategic investment & clinical distribution partnership",
        "vision_hook": "Redefining therapeutic access and clinical nutrition in underserved medical zones."
    },
    "torrent": {
        "name": "Torrent Leadership Team",
        "org_name": "Torrent Group",
        "synergies": (
            "Compelling intersections across <strong>Torrent Pharma (clinical formulations & nutrition) and Torrent Power/Gas "
            "(clean thermal energy transition)</strong>, replacing traditional LPG/combustion with clean water-activated heat."
        ),
        "investment_ask": "USD 8–10 million in strategic venture partnership",
        "vision_hook": "Pioneering the transition from carbon-heavy heating to water-activated green thermal power."
    },
    "gates_foundation": {
        "name": "Gates Foundation & Global Health Leadership",
        "org_name": "The Bill & Melinda Gates Foundation / Global Impact Mandates",
        "synergies": (
            "Planetary humanitarian impact: <strong>eradicating food spoilage, extending shelf-life to 1 year without refrigeration, "
            "and delivering hot nutritional rations to conflict zones, refugee corridors, and flood/famine regions</strong> with zero electrical infrastructure."
        ),
        "investment_ask": "USD 12 million catalytic grant / impact investment for global malnutrition & emergency humanitarian deployment",
        "vision_hook": "A planetary-scale, zero-infrastructure solution to child malnutrition and disaster relief logistics."
    }
}

def generate_corporate_email(corp_key):
    corp = CORPORATE_PROFILES.get(corp_key)
    if not corp:
        raise ValueError(f"Unknown corporate key: {corp_key}")
    
    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height: 1.68; color: #1f2937; margin: 0; padding: 24px; background-color: #f8fafc; }}
  .card {{ max-width: 680px; margin: 0 auto; background: #ffffff; border-radius: 12px; padding: 36px 40px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); }}
  .badge {{ display: inline-block; background: #0f172a; color: #ffffff; padding: 4px 12px; border-radius: 9999px; font-size: 11px; font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 20px; }}
  h1 {{ font-size: 21px; font-weight: 700; color: #0f172a; margin-top: 0; margin-bottom: 16px; line-height: 1.35; }}
  h2 {{ font-size: 15px; font-weight: 600; color: #1e3a8a; margin-top: 24px; margin-bottom: 8px; border-left: 3px solid #2563eb; padding-left: 10px; }}
  p {{ font-size: 14.5px; margin: 12px 0; color: #374151; }}
  .highlight-box {{ background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; padding: 16px 20px; margin: 18px 0; font-size: 14px; color: #166534; }}
  .cta-container {{ text-align: center; margin: 26px 0 16px 0; }}
  .cta-btn {{ display: inline-block; background: #2563eb; color: #ffffff !important; text-decoration: none; padding: 12px 24px; border-radius: 8px; font-size: 14px; font-weight: 600; }}
  .footer {{ margin-top: 32px; padding-top: 20px; border-top: 1px solid #e2e8f0; font-size: 13px; color: #64748b; }}
</style>
</head>
<body>
<div class="card">
  <div class="badge">HeatBolt | Strategic Association</div>
  <h1>Strategic Association between HeatBolt &amp; {corp['org_name']}</h1>
  
  <p>Dear {corp['name']},</p>
  
  <p>I hope this note finds you in good health and high spirits.</p>
  
  <p>I am writing to explore a category-defining strategic association between <strong>HeatBolt and {corp['org_name']}</strong> to scale an entirely new class of portable thermal infrastructure originating from India.</p>

  <h2>1. The Technology &amp; Innovation</h2>
  <p>HeatBolt combines proprietary water-activated exothermic heating with specially engineered barrier packaging, capable of generating temperatures of <strong>up to 100&deg;C using only water</strong> &mdash; with zero reliance on electricity, LPG, batteries, or open flame.</p>

  <div class="highlight-box">
    <strong>Strategic Synergies with {corp['org_name']}:</strong><br>
    {corp['synergies']}
  </div>

  <h2>2. Validation &amp; Global Momentum</h2>
  <p>HeatBolt has achieved deep national and international validation:</p>
  <ul>
    <li>High-level engagements with the <strong>Prime Minister's Office (PMO)</strong> and key Union Ministries (Defence, Home Affairs, Railways).</li>
    <li>Validated by the <strong>Indian Defence Forces</strong> for operational tactical performance down to -60&deg;C.</li>
    <li>Commercial and technical discussions underway with global food and FMCG majors including Nestl&eacute; (192 countries), Barilla (100 countries), and Mondelēz (150 countries).</li>
    <li>Demand indicators pointing to <strong>20 billion+ units</strong> annual manufacturing potential.</li>
  </ul>

  <h2>3. Investment &amp; Partnership Scope</h2>
  <p>We are exploring <strong>{corp['investment_ask']}</strong> to accelerate automated manufacturing scale-up, global certification, and turnkey commercialization. We would welcome your participation as a cornerstone strategic investor or enterprise joint-venture partner.</p>

  <h2>4. Invitation to Connect</h2>
  <p>I would be deeply honoured to present our technology, live working prototypes, and commercialisation roadmap in a brief <strong>15-minute executive discussion</strong> with your leadership team.</p>

  <div class="cta-container">
    <a href="https://www.linkedin.com/in/kumarpal-porwal/" class="cta-btn" target="_blank">Connect with Dr. Kumarpal Porwal on LinkedIn &rarr;</a>
  </div>

  <div class="footer">
    Warm regards,<br><br>
    <strong>Dr. Kumarpal Hasmukh Porwal</strong><br>
    Founder &ndash; HeatBolt<br>
    Shree Nakoda Parshwa Industries<br>
    Ph.D., Green Hydrogen (IISc Bangalore) | Mentored by Late Shri Ratan Tata<br>
    Direct / WhatsApp: +91 73533 19757 | +91 88672 94189<br>
    Email: <a href="mailto:founder.heatbolt@gmail.com" style="color: #2563eb;">founder.heatbolt@gmail.com</a>
  </div>
</div>
</body>
</html>"""
    return html

# Generate templates
out_dir = r"C:\Users\My\.gemini\antigravity\scratch\career-ops\data\corporate_templates"
os.makedirs(out_dir, exist_ok=True)

for k in CORPORATE_PROFILES:
    content = generate_corporate_email(k)
    path = os.path.join(out_dir, f"heatbolt_{k}_strategic_proposal.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated: {path}")

print("\nAll corporate strategic proposals successfully generated!")
