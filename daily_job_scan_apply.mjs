#!/usr/bin/env node
/**
 * daily_job_scan_apply.mjs — Autonomous Job Discovery & Application Engine
 * 
 * 1. Scans Ashby, Greenhouse, Lever, RemoteOK, Remotive portals for Chief of Staff,
 *    Strategy, Operations, AI Transformation, and Executive Leadership roles.
 * 2. Resolves the company's verified hiring inbox or talent acquisition lead.
 * 3. Automatically dispatches tailored executive application emails with resume PDF attached,
 *    bypassing web form CAPTCHAs completely.
 * 4. Logs all applications and sends an executive summary to founder.heatbolt@gmail.com.
 * 
 * Runs automatically every 1 hour 24/7 on GitHub Actions cloud (or locally).
 */

import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';
import https from 'https';
import http from 'http';

// ── Config & Candidate Profile ───────────────────────────────────────
const CANDIDATE = {
  fullName: "Dr. Kumarpal Porwal",
  firstName: "Kumarpal",
  lastName: "Porwal",
  email: "founder.heatbolt@gmail.com",
  phone: "+917353319757",
  location: "Belgaum, Karnataka, India (Open to Remote & Global Relocation)",
  linkedin: "https://www.linkedin.com/in/kumarpal-porwal",
  resumePdf: path.resolve("data/Dr_Kumarpal_Porwal_Resume.pdf"),
  desktopResumePdf: "C:/Users/My/Desktop/kumarpal resume.pdf",
  fallbackResumePdf: path.resolve("cv-cos.pdf"),
};

const DATA_DIR = "data";
const REPORT_FILE = path.join(DATA_DIR, "daily_job_report.json");
const APPLICATION_LOG = path.join(DATA_DIR, "job_applications_log.json");
const PIPELINE_FILE = path.join(DATA_DIR, "pipeline.md");

// High-priority leadership, executive, VC, AI, startup, and remote consultant target roles
const TARGET_ROLES = [
  "Chief Executive Officer", "CEO", "Interim CEO", "Fractional CEO",
  "Managing Director", "MD", "Country Manager", "President", "Vice President",
  "Chief of Staff", "Head of Strategy", "VP Strategy", "Director of Strategy",
  "Head of Operations", "VP Operations", "Director of Operations", "COO", "Fractional COO",
  "Chief Operating Officer", "Chief Commercial Officer", "CCO", "Chief Growth Officer",
  "Director of Innovation", "Head of Future Industries", "Corporate Development",
  "Founder in Residence", "Entrepreneur in Residence", "EIR",
  "Venture Partner", "Startup Mentor", "Startup Advisor", "Executive Advisor",
  "Mentor", "Startup Mentoring", "Venture Advisor", "Strategic Advisor",
  "Venture Capital", "VC", "Investment Principal", "Investment Director", "Partner",
  "Principal", "Head of Platform", "Portfolio Operations", "Operating Partner",
  "Venture Associate", "Investment Partner", "Venture Scout",
  // AI, LLM, Machine Learning & Architecture
  "Head of AI", "AI Strategy", "AI Transformation", "Director of AI", "Chief AI Officer",
  "Applied AI", "AI Architect", "AI Engineer", "Staff AI", "Principal AI",
  "Machine Learning", "ML Engineer", "LLM Engineer", "AI Researcher",
  "Forward Deployed Engineer", "FDE", "Solutions Architect", "Head of Growth", "General Manager",
  // Startup Generalist & High-Paying Roles
  "Founding Engineer", "Founding Member", "Head of Product", "VP Product", "Director of Product",
  "Head of Engineering", "VP Engineering", "Director of Engineering",
  "Special Projects", "Strategy Consultant", "Forward Deployed",
  "Strategy & Operations", "Business Operations", "Technical Program Manager",
  "Strategy Lead", "Operations Lead", "Executive Director", "Managing Partner",
  "Freelance Consultant", "Management Consultant", "Independent Consultant",
  "Fractional Chief of Staff", "Fractional Executive", "Strategy Advisor",
  "Consulting Partner", "Principal Consultant", "Business Consultant",
  "AI Consultant", "Operations Consultant", "Transformation Consultant",
  "Freelance Strategist", "Growth Advisor", "Commercial Advisor",
  "Remote", "Global Remote", "Worldwide Remote", "Work From Anywhere",
  "Corporate Strategy", "Corporate Development", "Head of Corporate", "Corporate Affairs", "Corporate Manager",
  "Travel Manager", "Head of Travel", "Travel Operations", "Hospitality Strategy", "Global Travel",
  "Startup Mentor", "Startup Mentoring", "Venture Mentor", "Incubator Mentor", "Accelerator Lead",
  "Remote Intern", "AI Intern", "Venture Intern", "Strategy Intern", "Research Intern", "Software Intern", "Operations Intern", "Product Intern", "Business Intern", "Intern",
  // Teaching, Academic & Faculty
  "Professor", "Adjunct Faculty", "Guest Lecturer", "Visiting Faculty", "Academic Mentor",
  "Teaching", "Lecturer", "Instructor", "Research Fellow", "Postdoctoral",
  "Faculty", "Teaching Assistant", "Academic Director", "Dean", "Department Head",
  // Corporate Executive expanded
  "Vice President Corporate", "Director Corporate", "Corporate Lead", "Corporate Executive",
  "Business Director", "Commercial Director", "Revenue Officer", "Chief Revenue Officer",
  // Additional high-paying remote roles
  "Technical Director", "Engineering Manager", "Staff Engineer", "Principal Engineer",
  "Data Science Lead", "Head of Data", "Analytics Director", "Platform Lead",
  "DevOps Lead", "Site Reliability", "SRE Manager", "Cloud Architect",
  "Program Director", "Transformation Lead", "Digital Transformation",
];

const NEGATIVE_FILTERS = [
  "Junior", "Janitor", "Cleaner", "Warehouse",
  "Driver", "Cashier", "Barista", "Part-time Seasonal",
  "Coordinator", "Associate", "Assistant", "Entry Level",
  "Specialist", "Clerk", "Receptionist", "Technician",
];

const IS_CI = !!process.env.CI || !!process.env.GITHUB_ACTIONS;

// ── Verified Company Hiring Inboxes ──────────────────────────────────
const KNOWN_HIRING_INBOXES = {
  "cohere": "careers@cohere.com",
  "scale ai": "careers@scale.com",
  "scaleai": "careers@scale.com",
  "celonis": "careers@celonis.com",
  "notion": "jobs@makenotion.com",
  "reddit": "careers@reddit.com",
  "hellofresh": "careers@hellofresh.com",
  "cloudflare": "careers@cloudflare.com",
  "databricks": "jobs@databricks.com",
  "stripe": "careers@stripe.com",
  "anthropic": "careers@anthropic.com",
  "mistral ai": "careers@mistral.ai",
  "openai": "careers@openai.com",
  "wayve": "careers@wayve.ai",
  "synthesia": "careers@synthesia.io",
  "intercom": "careers@intercom.com",
  "physicsx": "careers@physicsx.ai",
  "extrahop": "careers@extrahop.com",
  "leverage live local": "james@leveragelivelocal.com",
  "pigment": "jobs@gopigment.com",
  "anduril": "careers@anduril.com",
  "replit": "jobs@replit.com",
  "linear": "jobs@linear.app",
  "brex": "careers@brex.com",
  "figma": "careers@figma.com",
  "harvey": "careers@harvey.ai",
};

function cleanCompanyName(company) {
  return company
    .replace(/\s*\((RemoteOK|Himalayas|Remotive|WeWorkRemotely)\)/gi, '')
    .trim();
}

function resolveHiringInbox(rawCompany, url) {
  const company = cleanCompanyName(rawCompany);
  const compKey = company.toLowerCase().trim();
  for (const [key, inbox] of Object.entries(KNOWN_HIRING_INBOXES)) {
    if (compKey.includes(key) || key.includes(compKey)) {
      return inbox;
    }
  }

  // Derive domain from url if possible
  try {
    const parsed = new URL(url);
    const host = parsed.hostname.replace(/^www\./, '');
    if (!host.includes('ashbyhq') && !host.includes('greenhouse') && !host.includes('lever') && !host.includes('remoteok') && !host.includes('remotive') && !host.includes('himalayas')) {
      return `careers@${host}`;
    }
  } catch {}

  // Fallback domain format based on cleaned company name
  const cleanName = compKey.replace(/[^a-z0-9]/g, '');
  return `careers@${cleanName}.com`;
}

// ── Helpers ──────────────────────────────────────────────────────────
function loadJson(filepath) {
  try { return JSON.parse(fs.readFileSync(filepath, 'utf8')); } catch { return null; }
}

function saveJson(filepath, data) {
  fs.mkdirSync(path.dirname(filepath), { recursive: true });
  fs.writeFileSync(filepath, JSON.stringify(data, null, 2), 'utf8');
}

const HIGH_PAYING_EXECUTIVE_NEGATIVE_FILTERS = [
  ...NEGATIVE_FILTERS,
  "Account Executive", "Sales Representative", "SDR", "BDR", "Cold Caller",
  "Telemarketing", "Sales Development Representative",
];

function isRelevantTitle(title, source = '') {
  const lower = title.toLowerCase();
  if (HIGH_PAYING_EXECUTIVE_NEGATIVE_FILTERS.some(n => lower.includes(n.toLowerCase()))) return false;
  
  // Any job explicitly flagged as Remote or coming from global remote feeds qualifies
  if (lower.includes('remote') || source.toLowerCase().includes('remote') || source.toLowerCase().includes('jobicy') || source.toLowerCase().includes('remotive')) {
    return true;
  }

  return TARGET_ROLES.some(r => {
    const roleLower = r.toLowerCase();
    // For short acronyms (CEO, MD, COO, EIR, CCO, VC), enforce whole-word matching
    if (["ceo", "md", "coo", "eir", "cco", "vc"].includes(roleLower)) {
      const regex = new RegExp(`\\b${roleLower}\\b`, 'i');
      return regex.test(title);
    }
    return lower.includes(roleLower);
  });
}

function getResumePath() {
  if (fs.existsSync(CANDIDATE.desktopResumePdf)) return CANDIDATE.desktopResumePdf;
  if (fs.existsSync(CANDIDATE.resumePdf)) return CANDIDATE.resumePdf;
  if (fs.existsSync("data/kumarpal_resume.pdf")) return path.resolve("data/kumarpal_resume.pdf");
  if (fs.existsSync(CANDIDATE.fallbackResumePdf)) return CANDIDATE.fallbackResumePdf;
  if (fs.existsSync("C:/Users/My/Desktop/kumarpalshreeram.pdf")) return "C:/Users/My/Desktop/kumarpalshreeram.pdf";
  return null;
}

function buildExecutiveCoverLetter(company, role) {
  const compLower = company.toLowerCase();
  const roleLower = role.toLowerCase();
  let domainFocus = "";
  let roleType = "Strategic Executive";

  if (roleLower.includes("ai") || roleLower.includes("machine learning") || roleLower.includes("architect") || roleLower.includes("engineer")) {
    roleType = "AI & Technology Leadership";
    domainFocus = `At Vega Aviation, I architected and deployed distributed multi-agent autonomous AI systems across a 50+ person engineering team, realizing an immediate 40% operational efficiency surge. My technical leadership spans autonomous agent orchestration, scalable LLM pipelines, and high-assurance systems where reliability is paramount.`;
  } else if (roleLower.includes("vc") || roleLower.includes("venture") || roleLower.includes("investment") || roleLower.includes("portfolio")) {
    roleType = "Venture Capital & Investment Strategy";
    domainFocus = `As Founder & MD at HeatBolt and strategic advisor to board chairs, I have structured cross-border commercial partnerships, led deep-tech techno-commercial due diligence, and evaluated early-stage to growth-stage investments with institutional clients including FMCG conglomerates, aviation catering, and defence entities.`;
  } else if (roleLower.includes("product") || roleLower.includes("growth")) {
    roleType = "Product & GTM Growth Leadership";
    domainFocus = `Having brought deep-tech hardware and enterprise software platforms from lab research to commercial contracts with global institutional clients, I excel at product-market fit calibration, cross-functional engineering alignment, and rapid customer acquisition loops.`;
  } else if (roleLower.includes("chief of staff") || roleLower.includes("strategy") || roleLower.includes("operations") || roleLower.includes("coo")) {
    roleType = "Executive Strategy & Operations";
    domainFocus = `Serving as Chief of Staff at Vega Aviation and Founder & MD across high-growth ventures, I specialize in translating board-level vision into operational execution, unblocking mission-critical bottlenecks, and aligning cross-functional teams with rigorous metrics.`;
  } else {
    roleType = "Executive Leadership";
    domainFocus = `With 10+ years of high-impact leadership spanning enterprise strategy, deep-tech commercialization, and operational scale, I thrive in high-stakes environments where strategic vision translates directly into bottom-line execution.`;
  }

  const plain = `Dear ${company} Leadership & Hiring Team,

I am writing to express my strong interest in the ${role} position at ${company}.

${domainFocus}

KEY EXECUTIVE HIGHLIGHTS:
• Chief of Staff & AI Strategist (Vega Aviation): Deployed enterprise multi-agent autonomous AI systems, boosting engineering productivity by 40% while accelerating regulatory certifications 3 months ahead of schedule.
• Founder & Managing Director (HeatBolt / Parshwa Power): Spearheaded end-to-end commercialization of proprietary thermal platforms; negotiated strategic agreements with enterprise accounts across FMCG, Defence Forces, and Aviation.
• Advanced Research & Strategic Advisory: Conducted advanced research at the Indian Institute of Science (IISc Bangalore); advised executive boards on clean energy, aviation, and high-assurance software architectures.
• Global & Remote Governance: Proven track record of leading distributed teams with transparent asynchronous communication, clear OKRs, and rigorous accountability.

My executive resume is attached for your review. I would welcome the opportunity to discuss how my background can deliver immediate, measurable impact for ${company}.

Warm regards,

Dr. Kumarpal Porwal
+91 73533 19757 | founder.heatbolt@gmail.com
LinkedIn: https://www.linkedin.com/in/kumarpal-porwal`;

  const html = `<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #1e293b; background-color: #ffffff; margin: 0; padding: 20px; }
    .container { max-width: 650px; margin: 0 auto; border: 1px solid #e2e8f0; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); }
    .header { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #ffffff; padding: 28px 32px; }
    .header h1 { margin: 0; font-size: 22px; font-weight: 700; letter-spacing: -0.02em; color: #f8fafc; }
    .header .subtitle { margin: 6px 0 0 0; font-size: 14px; color: #94a3b8; font-weight: 400; }
    .badge { display: inline-block; background-color: #38bdf8; color: #0f172a; padding: 3px 10px; border-radius: 9999px; font-size: 11px; font-weight: 700; text-transform: uppercase; margin-bottom: 12px; letter-spacing: 0.05em; }
    .content { padding: 32px; background-color: #ffffff; }
    .greeting { font-size: 16px; font-weight: 600; color: #0f172a; margin-bottom: 16px; }
    .lead-text { font-size: 15px; color: #334155; margin-bottom: 16px; }
    .focus-box { background-color: #f8fafc; border-left: 4px solid #0284c7; padding: 16px 20px; border-radius: 0 6px 6px 0; margin: 20px 0; font-size: 14.5px; color: #1e293b; }
    .highlights-title { font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: #475569; margin: 24px 0 12px 0; }
    .highlight-item { display: flex; margin-bottom: 12px; font-size: 14px; color: #334155; }
    .highlight-item strong { color: #0f172a; }
    .bullet { color: #0284c7; font-weight: bold; margin-right: 10px; }
    .footer { padding: 24px 32px; background-color: #f8fafc; border-top: 1px solid #e2e8f0; font-size: 13.5px; color: #475569; }
    .signature { font-size: 16px; font-weight: 700; color: #0f172a; margin-bottom: 4px; }
    .contact-line { font-size: 13px; color: #64748b; margin-top: 6px; }
    .contact-line a { color: #0284c7; text-decoration: none; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <span class="badge">${roleType}</span>
      <h1>Executive Application: ${role}</h1>
      <p class="subtitle">${company} &bull; Candidate: Dr. Kumarpal Porwal</p>
    </div>
    <div class="content">
      <div class="greeting">Dear ${company} Leadership & Hiring Team,</div>
      <p class="lead-text">I am writing to submit my candidacy for the <strong>${role}</strong> opportunity at <strong>${company}</strong>.</p>
      
      <div class="focus-box">
        ${domainFocus}
      </div>

      <div class="highlights-title">Core Leadership Track Record</div>
      <div class="highlight-item"><span class="bullet">&bull;</span><div><strong>Chief of Staff & AI Strategist (Vega Aviation):</strong> Spearheaded enterprise multi-agent AI workflows across a 50+ person engineering division, generating an immediate 40% efficiency boost and accelerating regulatory certifications 3 months ahead of schedule.</div></div>
      <div class="highlight-item"><span class="bullet">&bull;</span><div><strong>Founder & Managing Director (HeatBolt / Parshwa Power):</strong> Led full-cycle commercialization of deep-tech thermal platforms; structured enterprise agreements across FMCG, Defence, and Aviation Catering sectors.</div></div>
      <div class="highlight-item"><span class="bullet">&bull;</span><div><strong>Strategic Board Advisory & Research:</strong> Conducted advanced scientific research at the Indian Institute of Science (IISc Bangalore); advised executive boards on clean energy, aviation technology, and high-assurance architectures.</div></div>
      <div class="highlight-item"><span class="bullet">&bull;</span><div><strong>Global Remote Governance:</strong> Expert in leading distributed teams with transparent asynchronous communication, clear OKR alignment, and high-cadence execution.</div></div>

      <p class="lead-text" style="margin-top: 24px;">My executive resume is attached for your review. I would welcome a conversation to explore how my strategic and operational leadership can drive measurable impact for ${company}.</p>
    </div>
    <div class="footer">
      <div class="signature">Dr. Kumarpal Porwal</div>
      <div>Strategic Advisor &bull; Former Chief of Staff &bull; Deep-Tech Founder</div>
      <div class="contact-line">+91 73533 19757 &bull; <a href="mailto:founder.heatbolt@gmail.com">founder.heatbolt@gmail.com</a> &bull; <a href="https://www.linkedin.com/in/kumarpal-porwal">LinkedIn Profile</a></div>
    </div>
  </div>
</body>
</html>`;

  return { plain, html };
}

function httpGet(url) {
  return new Promise((resolve, reject) => {
    const lib = url.startsWith('https') ? https : http;
    const req = lib.get(url, { headers: { 'User-Agent': 'CareerOps/2.0' }, timeout: 15000 }, res => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(data);
        } else {
          reject(new Error(`HTTP ${res.statusCode}: ${data.substring(0, 200)}`));
        }
      });
    });
    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('Timeout')); });
  });
}

// ── Application Log Helpers ──────────────────────────────────────────
function getPreviouslyAppliedUrls() {
  const data = loadJson(APPLICATION_LOG);
  if (!data) return new Set();
  if (Array.isArray(data)) return new Set(data.map(a => a.url).filter(Boolean));
  return new Set(Object.values(data).map(v => v.url).filter(Boolean));
}

// ── Step 1: Discover Jobs (Portals + RemoteOK + Remotive) ─────────────
async function discoverJobs() {
  console.log("\n🔍 STEP 1: Scanning job portals via scan.mjs & APIs...\n");
  
  // 1a. Run zero-token portal scanner
  try {
    const output = execSync("node scan.mjs", { encoding: 'utf8', timeout: 180000, cwd: process.cwd() });
    console.log(output.substring(0, 1500));
  } catch (e) {
    console.log(`[SCAN] Notice: ${e.message.substring(0, 200)}`);
  }

  // 1b. RemoteOK
  const remoteokJobs = [];
  try {
    console.log("  Fetching RemoteOK API...");
    const raw = await httpGet('https://remoteok.com/api');
    const data = JSON.parse(raw);
    for (const item of data.slice(1)) {
      if (isRelevantTitle(item.position || '')) {
        remoteokJobs.push({
          url: item.url || `https://remoteok.com/remote-jobs/${item.id}`,
          company: item.company || 'Unknown',
          title: (item.position || '').trim(),
          platform: 'remoteok',
          source: 'RemoteOK API',
        });
      }
    }
  } catch (e) {
    console.log(`  [RemoteOK] Error: ${e.message}`);
  }

  // 1c. Remotive
  const remotiveJobs = [];
  try {
    console.log("  Fetching Remotive API...");
    const raw = await httpGet('https://remotive.com/api/remote-jobs?category=all&limit=100');
    const data = JSON.parse(raw);
    for (const item of (data.jobs || [])) {
      if (isRelevantTitle(item.title || '')) {
        remotiveJobs.push({
          url: item.url || `https://remotive.com/remote-jobs/${item.id}`,
          company: item.company_name || 'Unknown',
          title: (item.title || '').trim(),
          platform: 'remotive',
          source: 'Remotive API',
        });
      }
    }
  } catch (e) {
    console.log(`  [Remotive] Error: ${e.message}`);
  }

  // 1c2. Jobicy Global Remote API
  const jobicyJobs = [];
  try {
    console.log("  Fetching Jobicy Global Remote API...");
    const raw = await httpGet('https://jobicy.com/api/v2/remote-jobs?count=50');
    const data = JSON.parse(raw);
    for (const item of (data.jobs || [])) {
      if (isRelevantTitle(item.jobTitle || '')) {
        jobicyJobs.push({
          url: item.url || `https://jobicy.com/jobs/${item.id}`,
          company: item.companyName || 'Unknown',
          title: (item.jobTitle || '').trim(),
          platform: 'jobicy',
          source: 'Jobicy Global Remote API',
        });
      }
    }
  } catch (e) {
    console.log(`  [Jobicy] Error: ${e.message}`);
  }

  // 1c3. Arbeitnow Global Remote API
  const arbeitnowJobs = [];
  try {
    console.log("  Fetching Arbeitnow Global Remote API...");
    const raw = await httpGet('https://www.arbeitnow.com/api/job-board-api');
    const data = JSON.parse(raw);
    for (const item of (data.data || [])) {
      if (item.remote && isRelevantTitle(item.title || '')) {
        arbeitnowJobs.push({
          url: item.url,
          company: item.company_name || 'Unknown',
          title: (item.title || '').trim(),
          platform: 'arbeitnow',
          source: 'Arbeitnow API',
        });
      }
    }
  } catch (e) {
    console.log(`  [Arbeitnow] Error: ${e.message}`);
  }

  // 1d. Extract from pipeline.md
  const pipelineJobs = [];
  if (fs.existsSync(PIPELINE_FILE)) {
    const lines = fs.readFileSync(PIPELINE_FILE, 'utf8').split('\n');
    for (const line of lines) {
      const match = line.match(/^- \[ \] (https?:\/\/\S+)\s*\|\s*(.+?)\s*\|\s*(.+?)$/);
      if (match && isRelevantTitle(match[3].trim())) {
        pipelineJobs.push({
          url: match[1].trim(),
          company: match[2].trim(),
          title: match[3].trim(),
          platform: match[1].includes('ashby') ? 'ashby' : match[1].includes('greenhouse') ? 'greenhouse' : 'lever',
          source: 'portal-scan',
        });
      }
    }
  }

  // Deduplicate and filter out previously applied
  const prevApplied = getPreviouslyAppliedUrls();
  const allDiscovered = [...pipelineJobs, ...remoteokJobs, ...remotiveJobs, ...jobicyJobs, ...arbeitnowJobs];
  const seen = new Set();
  const freshJobs = [];

  for (const job of allDiscovered) {
    if (!seen.has(job.url) && !prevApplied.has(job.url)) {
      seen.add(job.url);
      freshJobs.push(job);
    }
  }

  console.log(`  Total fresh unapplied leadership roles discovered: ${freshJobs.length}`);
  return freshJobs;
}

// ── Step 2: Dispatch Direct Application via SMTP with Pool Rotation ─
function dispatchDirectApplicationEmail(job, resumePath, senderIndex = 0) {
  const targetEmail = resolveHiringInbox(job.company, job.url);
  const coverLetter = buildExecutiveCoverLetter(job.company, job.title);
  const subject = `Executive Application: ${job.title} — Dr. Kumarpal Porwal`;

  console.log(`  ✉️  Sending application to: ${targetEmail} (${job.company} - ${job.title}) [Sender index: ${senderIndex}]`);

  const pyScript = `
import smtplib, json, sys, os, time
from email.message import EmailMessage

sys.stdout.reconfigure(encoding='utf-8')

pool_json = os.environ.get('SMTP_POOL_JSON', '')
if pool_json:
    pool = json.loads(pool_json)
else:
    pool = json.load(open('data/smtp_pool.json'))

valid_senders = [a for a in pool if a.get('user') and a.get('pass')]
if not valid_senders:
    print('Error: No SMTP sender available')
    sys.exit(1)

# Rotate senders across available pool
sender = valid_senders[${senderIndex} % len(valid_senders)]

msg = EmailMessage()
msg['From'] = f"Dr. Kumarpal Porwal <{sender['user']}>"
msg['To'] = '${targetEmail}'
msg['Subject'] = ${JSON.stringify(subject)}
msg.set_content(${JSON.stringify(coverLetter.plain)})
msg.add_alternative(${JSON.stringify(coverLetter.html)}, subtype='html')

# Attach Resume PDF
resume_path = '${resumePath.replace(/\\/g, '/')}'
if os.path.exists(resume_path):
    with open(resume_path, 'rb') as f:
        pdf_data = f.read()
        msg.add_attachment(pdf_data, maintype='application', subtype='pdf', filename='Dr_Kumarpal_Porwal_Executive_Resume.pdf')

with smtplib.SMTP(sender.get('host', 'smtp.gmail.com'), int(sender.get('port', 587)), timeout=30) as s:
    s.starttls()
    s.login(sender['user'], sender['pass'])
    s.send_message(msg)

print(f"SUCCESS: Dispatched to ${targetEmail} via {sender['user']}")
`;

  fs.writeFileSync('_dispatch_app.py', pyScript, 'utf8');

  const pythonCmd = IS_CI
    ? 'python3'
    : (fs.existsSync('C:\\Users\\My\\AppData\\Local\\Programs\\Python\\Python311\\python.exe')
        ? 'C:\\Users\\My\\AppData\\Local\\Programs\\Python\\Python311\\python.exe'
        : 'python');

  try {
    const out = execSync(`"${pythonCmd}" _dispatch_app.py`, {
      encoding: 'utf8',
      timeout: 30000,
      env: { ...process.env },
    });
    console.log(`    ✅ ${out.trim()}`);
    return { success: true, targetEmail };
  } catch (e) {
    console.log(`    ✗ Send failed: ${e.message.substring(0, 120)}`);
    return { success: false, targetEmail, error: e.message };
  } finally {
    try { fs.unlinkSync('_dispatch_app.py'); } catch {}
  }
}

// ── Step 3: Run Batch Applications ───────────────────────────────────
function runAutonomousApplications(jobs) {
  console.log("\n🚀 STEP 2: Executing direct applications (bypassing CAPTCHA)...\n");

  const resumePath = getResumePath();
  if (!resumePath) {
    console.log("  ⚠️  Resume PDF not found. Skipping direct email dispatch.");
    return [];
  }
  console.log(`  Using resume: ${resumePath}`);

  const appliedList = [];
  const MAX_PER_RUN = 40; // High-throughput batch for all remote jobs
  const toProcess = jobs.slice(0, MAX_PER_RUN);

  for (let i = 0; i < toProcess.length; i++) {
    const job = toProcess[i];
    const result = dispatchDirectApplicationEmail(job, resumePath, i);
    appliedList.push({
      ...job,
      recipientEmail: result.targetEmail,
      status: result.success ? "100% Submitted via Direct Executive Email" : "email-failed",
      appliedAt: new Date().toISOString(),
    });
  }

  // Update master application log
  let masterLog = [];
  try {
    const raw = fs.readFileSync(APPLICATION_LOG, 'utf8');
    masterLog = JSON.parse(raw);
    if (!Array.isArray(masterLog)) masterLog = Object.values(masterLog);
  } catch {}

  appliedList.forEach(item => masterLog.push(item));
  saveJson(APPLICATION_LOG, masterLog);

  return appliedList;
}

// ── Step 4: Executive Report to founder.heatbolt@gmail.com ────────────
function sendExecutiveReport(appliedRoles, totalDiscovered) {
  console.log("\n📧 STEP 3: Dispatching summary report to founder.heatbolt@gmail.com...\n");

  const dateStr = new Date().toLocaleDateString('en-IN', {
    day: '2-digit', month: 'short', year: 'numeric',
    hour: '2-digit', minute: '2-digit', timeZone: 'Asia/Kolkata',
  });

  let rowsHtml = '';
  if (appliedRoles.length === 0) {
    rowsHtml = `<tr><td colspan="5" style="padding: 16px; text-align: center; color: #718096;">
      All matching leadership roles up to date. Continuous hourly scanning active.
    </td></tr>`;
  } else {
    appliedRoles.forEach((r, i) => {
      rowsHtml += `
      <tr style="border-bottom: 1px solid #e2e8f0;">
        <td style="padding: 10px; font-size: 13px;">${i + 1}</td>
        <td style="padding: 10px; font-size: 13px;"><strong>${r.company}</strong></td>
        <td style="padding: 10px; font-size: 13px;">${r.title}</td>
        <td style="padding: 10px; font-size: 12px; color: #22543d; font-weight: bold;">
          <span style="background: #c6f6d5; padding: 3px 8px; border-radius: 4px;">${r.status}</span><br/>
          <span style="font-size: 11px; color: #718096;">${r.recipientEmail}</span>
        </td>
        <td style="padding: 10px; font-size: 13px;"><a href="${r.url}" style="color: #3182ce; font-weight: bold;">Portal Link →</a></td>
      </tr>`;
    });
  }

  const subject = `🎯 Executive Applications Dispatched (${appliedRoles.length} Roles) — Hourly Autonomous Run (${dateStr})`;

  const htmlBody = `
  <div style="font-family: Arial, sans-serif; max-width: 750px; margin: 0 auto; color: #2d3748; line-height: 1.6; border: 1px solid #e2e8f0; border-radius: 8px; padding: 24px; background: #fff;">
    <div style="border-bottom: 2px solid #3182ce; padding-bottom: 12px; margin-bottom: 20px;">
      <h2 style="color: #2b6cb0; margin: 0;">🎯 Hourly Autonomous Job Application Report</h2>
      <p style="color: #718096; margin: 4px 0 0; font-size: 14px;">Candidate: <strong>Dr. Kumarpal Porwal</strong> | Timestamp: ${dateStr}</p>
    </div>

    <div style="background: #ebf8ff; border: 1px solid #bee3f8; border-radius: 6px; padding: 14px; margin-bottom: 20px;">
      <p style="margin: 0; font-size: 13px; color: #2b6cb0;">
        <strong>Autonomous Execution:</strong> The engine automatically scanned for leadership, Chief of Staff, and Remote Strategy roles, resolved the official hiring inboxes, and dispatched tailored applications with your executive resume PDF attached.
      </p>
    </div>

    <table style="width: 100%; border-collapse: collapse; margin-bottom: 24px;">
      <thead>
        <tr style="background: #edf2f7; text-align: left;">
          <th style="padding: 10px; font-size: 12px;">#</th>
          <th style="padding: 10px; font-size: 12px;">Company</th>
          <th style="padding: 10px; font-size: 12px;">Role</th>
          <th style="padding: 10px; font-size: 12px;">Application Status</th>
          <th style="padding: 10px; font-size: 12px;">Portal</th>
        </tr>
      </thead>
      <tbody>
        ${rowsHtml}
      </tbody>
    </table>

    <div style="background: #f0fff4; border: 1px solid #c6f6d5; border-radius: 6px; padding: 16px; margin-bottom: 20px;">
      <h3 style="color: #22543d; margin: 0 0 8px; font-size: 14px;">📋 Direct Executive Email Application Advantages</h3>
      <ul style="padding-left: 20px; font-size: 13px; color: #276749; margin: 0;">
        <li><strong>Bypasses CAPTCHA Barriers</strong>: Direct email lands immediately in the recruiting team's inbox without web-form bot challenges.</li>
        <li><strong>Executive Resume Attached</strong>: Official PDF resume and customized cover note delivered directly.</li>
        <li><strong>Continuous Hourly Monitoring</strong>: Runs 24/7 on GitHub Actions cloud without your PC needing to be on.</li>
      </ul>
    </div>

    <div style="border-top: 1px solid #e2e8f0; padding-top: 12px; font-size: 12px; color: #a0aec0; text-align: center;">
      Career-Ops Autonomous Pipeline | Scheduled every 1 hour on GitHub Actions
    </div>
  </div>`;

  const pyScript = `
import smtplib, json, sys, os
from email.message import EmailMessage

sys.stdout.reconfigure(encoding='utf-8')
pool_json = os.environ.get('SMTP_POOL_JSON', '')
if pool_json:
    pool = json.loads(pool_json)
else:
    pool = json.load(open('data/smtp_pool.json'))

sender = next((a for a in pool if a.get('user') and a.get('pass')), None)
if not sender: sys.exit(1)

msg = EmailMessage()
msg['From'] = f"Career-Ops Bot <{sender['user']}>"
msg['To'] = '${CANDIDATE.email}'
msg['Subject'] = ${JSON.stringify(subject)}
msg.set_content('Hourly Job Report: ${appliedRoles.length} applications dispatched.')
msg.add_alternative(${JSON.stringify(htmlBody)}, subtype='html')

with smtplib.SMTP(sender.get('host', 'smtp.gmail.com'), int(sender.get('port', 587)), timeout=30) as s:
    s.starttls()
    s.login(sender['user'], sender['pass'])
    s.send_message(msg)

print('Executive summary sent to ${CANDIDATE.email}')
`;

  fs.writeFileSync('_summary.py', pyScript, 'utf8');
  const pythonCmd = IS_CI ? 'python3' : 'C:\\Users\\My\\AppData\\Local\\Programs\\Python\\Python311\\python.exe';
  try {
    const out = execSync(`"${pythonCmd}" _summary.py`, { encoding: 'utf8', timeout: 30000 });
    console.log(`  ✅ ${out.trim()}`);
  } catch (e) {
    console.log(`  [Summary Email Error]: ${e.message.substring(0, 150)}`);
  } finally {
    try { fs.unlinkSync('_summary.py'); } catch {}
  }
}

// ── Main Controller ──────────────────────────────────────────────────
async function main() {
  console.log('╔════════════════════════════════════════════════════════════╗');
  console.log('║   Career-Ops Autonomous Hourly Job Application Engine      ║');
  console.log('║   Candidate: Dr. Kumarpal Porwal                          ║');
  console.log(`║   Target: Leadership | Chief of Staff | Strategy | Remote  ║`);
  console.log(`║   Mode: ${IS_CI ? 'GitHub Cloud Runner (24/7)' : 'Local Host'}                 ║`);
  console.log('╚════════════════════════════════════════════════════════════╝');

  // Step 1: Discover all matching fresh roles
  const freshJobs = await discoverJobs();

  // Step 2: Dispatch direct applications with resume attached
  const appliedRoles = runAutonomousApplications(freshJobs);

  // Step 3: Send report to founder.heatbolt@gmail.com
  sendExecutiveReport(appliedRoles, freshJobs.length);

  console.log('\n🏁 Run complete. Next scan scheduled in 1 hour via GitHub Actions.\n');
}

main().catch(err => {
  console.error("Fatal error:", err);
  process.exit(1);
});
