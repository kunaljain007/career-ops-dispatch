import base64
import re

with open('C:/Users/My/.gemini/antigravity/scratch/career-ops/heatbolt_national_traction.png', 'rb') as f:
    b64_img = base64.b64encode(f.read()).decode('utf-8')
    data_uri = f"data:image/png;base64,{b64_img}"

with open('C:/Users/My/.gemini/antigravity/scratch/career-ops/HEATBOLT_Defence_Strategic_Briefing.html', 'r', encoding='utf-8') as f:
    html = f.read()

new_slide = f'''
<!-- 19b-2 NATIONAL VALIDATION & INDUSTRY EVIDENCE (IMAGE SLIDE) -->
<section class="slide">
  <header class="shead"><span class="kicker">National Credibility &amp; High-Level Validation</span><span class="snum"></span></header>
  <div class="sbody">
    <h2 class="anim">National Titans, <span class="g">AMUL</span> &amp; Global Aviation</h2>
    <div class="rule anim"></div>
    <div class="grid g2 anim" style="align-items:center;gap:20px">
      <div style="background:var(--panel);border:1px solid var(--line2);padding:10px;box-shadow:0 8px 24px rgba(0,0,0,0.06);position:relative">
        <div style="font-family:var(--mono);font-size:9.5px;letter-spacing:0.18em;color:var(--gold);text-transform:uppercase;margin-bottom:8px;padding:4px 8px;background:var(--gold-dim)">
          // OFFICIAL EVIDENCE: SHRI RATAN TATA CONSULTATION · AMUL LETTER · EMIRATES CATERING
        </div>
        <img src="{data_uri}" alt="National Evidence &amp; Endorsements" style="width:100%;height:auto;display:block;border:1px solid var(--line);border-radius:2px">
      </div>
      <div class="grid" style="gap:10px">
        <div class="card">
          <div class="ct"><span class="n">PATRIARCHAL ENDORSEMENT</span>Shri Ratan N. Tata Direct Consultation</div>
          <div class="cd">Personal strategic consultation reviewing Heatbolt's flameless thermal technology for sovereign defence resilience and national grassroots impact.</div>
        </div>
        <div class="card">
          <div class="ct"><span class="n">COOPERATIVE GIANT (AMUL)</span>GCMMF Ltd Written Intent to Collaborate</div>
          <div class="cd">Official letter from Purchase Division: <i>"We know the potential of the concept, which can bring revolution in fmcg sector, we are interested for collaboration..."</i></div>
        </div>
        <div class="card">
          <div class="ct"><span class="n">GLOBAL AVIATION SUPPLY</span>Emirates Flight Catering Onboarding</div>
          <div class="cd">Formal international airline vendor qualification and commercial onboarding for self-heating in-flight and expeditionary meal solutions.</div>
        </div>
        <div class="card">
          <div class="ct"><span class="n">SURGING MARKET TRACTION</span>Bikaji Foods &amp; Tier-1 Summits</div>
          <div class="cd">CFO-level strategic engagement for commercial scaling, Techceleration 2023 showcase, and daily surging demand across India.</div>
        </div>
      </div>
    </div>
    <div class="note anim" style="margin-top:16px">
      <b>VERIFIED NATIONAL TRACTION —</b> Backed by India's most respected industrial leadership, national cooperatives, and international aviation supply chains.
    </div>
  </div>
</section>
'''

target = '<!-- 19c ENDORSEMENTS & VALIDATION -->'
if target in html:
    html = html.replace(target, new_slide + '\n' + target)
    print("Inserted new slide into HTML before 19c!")
else:
    print("Target not found in HTML!")

with open('C:/Users/My/.gemini/antigravity/scratch/career-ops/HEATBOLT_Defence_Strategic_Briefing.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated HEATBOLT_Defence_Strategic_Briefing.html successfully!")
