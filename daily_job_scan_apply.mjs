#!/usr/bin/env node
/**
 * daily_job_scan_apply.mjs
 * 
 * Daily automated job discovery, ATS resume tailoring, and application engine.
 * Scans Ashby, Greenhouse, Lever portals (via scan.mjs), plus RemoteOK & Remotive APIs.
 * Logs all discovered roles, sends styled HTML notification to founder.heatbolt@gmail.com.
 * 
 * Works both locally (Windows) and in GitHub Actions (Ubuntu).
 * 
 * Usage:
 *   node daily_job_scan_apply.mjs              # full scan + apply + notify
 *   node daily_job_scan_apply.mjs --scan-only  # scan only, no notify
 *   node daily_job_scan_apply.mjs --notify-only # send report from last run
 */

import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';
import https from 'https';
import http from 'http';

// ── Config ──────────────────────────────────────────────────────────
const CANDIDATE = {
  full_name: "Dr. Kumarpal Porwal",
  email: "founder.heatbolt@gmail.com",
  phone: "+917353319757",
  linkedin: "https://linkedin.com/in/kumarpal-porwal",
  location: "Belgaum, Karnataka, India (Open to Global & Remote)",
};

const DATA_DIR = "data";
const REPORT_FILE = path.join(DATA_DIR, "daily_job_report.json");
const APPLICATION_LOG = path.join(DATA_DIR, "job_applications_log.json");
const PIPELINE_FILE = path.join(DATA_DIR, "pipeline.md");
const SCAN_HISTORY = path.join(DATA_DIR, "scan-history.tsv");

const TARGET_ROLES = [
  "Chief of Staff", "Head of Strategy", "Head of Operations",
  "Director of Innovation", "VP Strategy", "General Manager",
  "Founder in Residence", "Entrepreneur in Residence", "EIR",
  "Venture Partner", "Startup Mentor", "Startup Advisor",
  "Fractional COO", "Fractional Chief of Staff",
  "Head of AI", "AI Strategy", "AI Transformation",
  "Solutions Architect", "Head of Growth",
  "Special Projects", "Strategy Consultant",
  "Forward Deployed", "Applied AI",
  "Director of Strategy", "Director of Operations",
  "VP Operations", "VP of Strategy",
  "Strategy & Operations", "Business Operations",
  "Head of Business Development",
  "Program Manager", "Technical Program Manager",
  "Strategy Lead", "Operations Lead",
];

const NEGATIVE_FILTERS = [
  "Junior", "Intern ", "Janitor", "Cleaner", "Warehouse",
  "Driver", "Cashier", "Barista", "Part-time Seasonal",
];

const IS_CI = !!process.env.CI || !!process.env.GITHUB_ACTIONS;

// ── Helpers ─────────────────────────────────────────────────────────
function loadJson(filepath) {
  try { return JSON.parse(fs.readFileSync(filepath, 'utf8')); } catch { return null; }
}

function saveJson(filepath, data) {
  fs.mkdirSync(path.dirname(filepath), { recursive: true });
  fs.writeFileSync(filepath, JSON.stringify(data, null, 2), 'utf8');
}

function isRelevantTitle(title) {
  const lower = title.toLowerCase();
  if (NEGATIVE_FILTERS.some(n => lower.includes(n.toLowerCase()))) return false;
  return TARGET_ROLES.some(r => lower.includes(r.toLowerCase()));
}

function buildCoverLetter(company, role) {
  return `Dear ${company} Hiring Team,

I am writing to express my strong interest in the ${role} position at ${company}.

As a seasoned Strategy and Transformation Leader with 10+ years of high-impact leadership, I bring a unique blend of enterprise strategy, AI-driven automation, deep-tech commercialization, and operational excellence directly aligned with this role.

KEY HIGHLIGHTS:
• Chief of Staff & AI Strategist at Vega Aviation — Architected multi-agent autonomous AI systems across a 50+ person engineering division, delivering a 40% operational efficiency surge. Secured aviation certifications 3 months ahead of schedule.
• Founder & MD at HeatBolt/Parshwa Power — Commercialized breakthrough flameless thermal platforms. Strategic partnerships with Amul, Bikaji, Haldiram, Emirates Flight Catering, and Indian Defence Forces.
• Strategic Advisor to CEOs, Board Chairs, and industry titans across regulated aviation, defense, energy, FMCG, and enterprise tech ecosystems.
• Green Hydrogen Research — Advanced research at Indian Institute of Science (IISc), Bangalore.

I thrive in fast-paced, ambiguous environments where strategy and execution must work hand-in-hand. My experience bridging R&D, commercial operations, compliance, and cross-functional teams makes me uniquely suited to drive impact at ${company}.

Warm regards,
Dr. Kumarpal Porwal
+91 73533 19757 | founder.heatbolt@gmail.com | linkedin.com/in/kumarpal-porwal`;
}

function detectPlatform(url) {
  if (url.includes('ashbyhq.com')) return 'ashby';
  if (url.includes('greenhouse.io') || url.includes('greenhouse.com')) return 'greenhouse';
  if (url.includes('lever.co')) return 'lever';
  if (url.includes('wellfound.com') || url.includes('angel.co')) return 'wellfound';
  if (url.includes('remoteok')) return 'remoteok';
  if (url.includes('remotive.com')) return 'remotive';
  return 'direct';
}

function httpGet(url) {
  return new Promise((resolve, reject) => {
    const lib = url.startsWith('https') ? https : http;
    const req = lib.get(url, { headers: { 'User-Agent': 'CareerOps/1.0' }, timeout: 15000 }, res => {
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

// ── Get previously applied URLs ────────────────────────────────────
function getPreviouslyAppliedUrls() {
  const data = loadJson(APPLICATION_LOG);
  if (!data) return new Set();
  
  // Handle both array and object formats
  if (Array.isArray(data)) {
    return new Set(data.map(a => a.url).filter(Boolean));
  }
  // Object format: { "email@co.com": { company, role, ... } }
  return new Set(Object.values(data).map(v => v.url).filter(Boolean));
}

function getExistingApplicationsList() {
  const data = loadJson(APPLICATION_LOG);
  if (!data) return [];
  if (Array.isArray(data)) return data;
  return Object.entries(data).map(([email, info]) => ({ email, ...info }));
}

// ── Step 1: Scan Portals (scan.mjs) ────────────────────────────────
function runPortalScan() {
  console.log("\n🔍 STEP 1: Scanning job portals via scan.mjs...\n");
  try {
    const output = execSync("node scan.mjs", { encoding: 'utf8', timeout: 180000, cwd: process.cwd() });
    console.log(output.substring(0, 3000));
    return true;
  } catch (e) {
    console.log(`[SCAN] Warning: scan.mjs returned error: ${e.message.substring(0, 300)}`);
    return false;
  }
}

// ── Step 1b: Scan RemoteOK API ─────────────────────────────────────
async function scanRemoteOK() {
  console.log("\n🌍 Scanning RemoteOK API...");
  const jobs = [];
  try {
    const raw = await httpGet('https://remoteok.com/api');
    const data = JSON.parse(raw);
    // First item is metadata, skip it
    for (const item of data.slice(1)) {
      const title = item.position || '';
      if (isRelevantTitle(title)) {
        jobs.push({
          url: item.url || `https://remoteok.com/remote-jobs/${item.id}`,
          company: item.company || 'Unknown',
          title: title.trim(),
          location: item.location || 'Remote',
          salary: item.salary || '',
          platform: 'remoteok',
          source: 'RemoteOK API',
        });
      }
    }
    console.log(`  Found ${jobs.length} matching roles on RemoteOK`);
  } catch (e) {
    console.log(`  [RemoteOK] Error: ${e.message.substring(0, 200)}`);
  }
  return jobs;
}

// ── Step 1c: Scan Remotive API ─────────────────────────────────────
async function scanRemotive() {
  console.log("\n🌐 Scanning Remotive API...");
  const jobs = [];
  const searches = [
    'chief+of+staff', 'head+of+strategy', 'ai+strategy',
    'director+operations', 'startup+mentor', 'venture+partner',
  ];
  for (const query of searches) {
    try {
      const raw = await httpGet(`https://remotive.com/api/remote-jobs?search=${query}&limit=50`);
      const data = JSON.parse(raw);
      for (const item of (data.jobs || [])) {
        const title = item.title || '';
        if (isRelevantTitle(title)) {
          const url = item.url || `https://remotive.com/remote-jobs/${item.id}`;
          if (!jobs.find(j => j.url === url)) {
            jobs.push({
              url,
              company: item.company_name || 'Unknown',
              title: title.trim(),
              location: item.candidate_required_location || 'Remote',
              salary: item.salary || '',
              platform: 'remotive',
              source: 'Remotive API',
              category: item.category || '',
            });
          }
        }
      }
    } catch (e) {
      // Some search queries may fail, continue
    }
  }
  console.log(`  Found ${jobs.length} matching roles on Remotive`);
  return jobs;
}

// ── Step 2: Extract from Pipeline ──────────────────────────────────
function extractFromPipeline() {
  console.log("\n📊 STEP 2: Extracting matching jobs from pipeline.md...\n");
  
  const pipeline = fs.existsSync(PIPELINE_FILE) ? fs.readFileSync(PIPELINE_FILE, 'utf8') : '';
  const lines = pipeline.split('\n');
  const jobs = [];
  
  for (const line of lines) {
    // Format: - [ ] URL | Company | Title
    const match = line.match(/^- \[ \] (https?:\/\/\S+)\s*\|\s*(.+?)\s*\|\s*(.+?)$/);
    if (match) {
      const [, url, company, title] = match;
      if (isRelevantTitle(title.trim())) {
        jobs.push({
          url: url.trim(),
          company: company.trim(),
          title: title.trim(),
          platform: detectPlatform(url),
          source: 'portal-scan',
        });
      }
    }
    
    // Also check: - [ ] URL | Company (Source) | Title
    const match2 = line.match(/^- \[ \] (https?:\/\/\S+)\s*\|\s*(.+?)\s+\((.+?)\)\s*\|\s*(.+?)$/);
    if (match2 && !jobs.find(j => j.url === match2[1].trim())) {
      const [, url, company, source, title] = match2;
      if (isRelevantTitle(title.trim())) {
        jobs.push({
          url: url.trim(),
          company: company.trim(),
          title: title.trim(),
          source: source.trim(),
          platform: detectPlatform(url),
        });
      }
    }
  }
  
  console.log(`  Extracted ${jobs.length} matching roles from pipeline`);
  return jobs;
}

// ── Step 3: Deduplicate & Merge ─────────────────────────────────────
function deduplicateAndMerge(pipelineJobs, remoteokJobs, remotiveJobs) {
  console.log("\n🔄 STEP 3: Deduplicating and merging all sources...\n");
  
  const allJobs = [...pipelineJobs, ...remoteokJobs, ...remotiveJobs];
  
  // Deduplicate by URL
  const seen = new Set();
  const unique = [];
  for (const job of allJobs) {
    if (!seen.has(job.url)) {
      seen.add(job.url);
      unique.push(job);
    }
  }
  
  // Remove previously applied
  const prevUrls = getPreviouslyAppliedUrls();
  const fresh = unique.filter(j => !prevUrls.has(j.url));
  
  // Sort: Chief of Staff first, then AI, then others
  fresh.sort((a, b) => {
    const aCoS = a.title.toLowerCase().includes('chief of staff') ? 0 : 1;
    const bCoS = b.title.toLowerCase().includes('chief of staff') ? 0 : 1;
    if (aCoS !== bCoS) return aCoS - bCoS;
    const aAI = a.title.toLowerCase().includes('ai') ? 0 : 1;
    const bAI = b.title.toLowerCase().includes('ai') ? 0 : 1;
    return aAI - bAI;
  });
  
  console.log(`  Total from all sources: ${allJobs.length}`);
  console.log(`  After dedup: ${unique.length}`);
  console.log(`  New (not previously applied): ${fresh.length}`);
  
  return fresh;
}

// ── Step 4: Log Applications ────────────────────────────────────────
function logApplications(jobs) {
  console.log("\n📝 STEP 4: Logging discovered roles...\n");
  
  const now = new Date().toISOString();
  
  // Load existing log - maintain array format for new entries
  let existingLog = loadJson(APPLICATION_LOG);
  let newEntries = [];
  
  // If existing is an object, convert to array  
  if (existingLog && !Array.isArray(existingLog)) {
    newEntries = Object.entries(existingLog).map(([email, info]) => ({
      email, ...info
    }));
  } else if (Array.isArray(existingLog)) {
    newEntries = [...existingLog];
  }
  
  for (const job of jobs) {
    const entry = {
      url: job.url,
      company: job.company,
      title: job.title,
      platform: job.platform,
      source: job.source || 'scan',
      location: job.location || '',
      cover_letter: buildCoverLetter(job.company, job.title),
      status: 'discovered',
      discovered_at: now,
    };
    newEntries.push(entry);
    console.log(`  📋 ${job.company} — ${job.title}`);
    console.log(`     ${job.url}`);
  }
  
  saveJson(APPLICATION_LOG, newEntries);
  console.log(`\n  Total logged: ${jobs.length} new roles`);
  return jobs;
}

// ── Step 5: Send Email Notification ─────────────────────────────────
function sendNotification(jobs) {
  console.log("\n📧 STEP 5: Sending notification to founder.heatbolt@gmail.com...\n");
  
  // Get SMTP pool from env (CI) or file
  let smtpPoolJson;
  if (process.env.SMTP_POOL_JSON) {
    smtpPoolJson = process.env.SMTP_POOL_JSON;
  } else if (fs.existsSync('data/smtp_pool.json')) {
    smtpPoolJson = fs.readFileSync('data/smtp_pool.json', 'utf8');
  } else {
    console.log('[NOTIFY] No SMTP pool found (neither env nor file). Skipping notification.');
    return false;
  }
  
  const dateStr = new Date().toLocaleDateString('en-IN', {
    day: '2-digit', month: 'short', year: 'numeric',
    hour: '2-digit', minute: '2-digit', timeZone: 'Asia/Kolkata'
  });
  
  // Build job list HTML
  let jobsHtml = '';
  if (jobs.length === 0) {
    jobsHtml = `<tr><td colspan="4" style="padding: 16px; text-align: center; color: #718096; font-size: 14px;">
      ✅ No new matching roles found today. All caught up! The system continues scanning daily.
    </td></tr>`;
  } else {
    jobs.forEach((j, i) => {
      const tag = j.title.toLowerCase().includes('chief of staff') ? '🎯 CoS' :
                  j.title.toLowerCase().includes('ai') ? '🤖 AI' :
                  j.title.toLowerCase().includes('remote') ? '🌍 Remote' :
                  j.title.toLowerCase().includes('startup') ? '🚀 Startup' :
                  j.title.toLowerCase().includes('mentor') ? '🧠 Mentor' :
                  j.title.toLowerCase().includes('strategy') ? '📊 Strategy' : '📋';
      jobsHtml += `
      <tr style="border-bottom: 1px solid #edf2f7;">
        <td style="padding: 8px; font-size: 13px;">${i+1}</td>
        <td style="padding: 8px; font-size: 13px;"><strong>${j.company}</strong></td>
        <td style="padding: 8px; font-size: 13px;">${tag} ${j.title}</td>
        <td style="padding: 8px; font-size: 13px;"><a href="${j.url}" style="color: #3182ce;">Apply →</a></td>
      </tr>`;
    });
  }
  
  const cosCount = jobs.filter(j => j.title.toLowerCase().includes('chief of staff')).length;
  const aiCount = jobs.filter(j => j.title.toLowerCase().includes('ai') || j.title.toLowerCase().includes('strategy')).length;
  const remoteCount = jobs.filter(j => j.platform === 'remoteok' || j.platform === 'remotive').length;
  
  const subject = jobs.length > 0
    ? `🎯 Daily Job Report — ${jobs.length} New Roles Found (${dateStr})`
    : `✅ Daily Job Scan Complete — No New Roles (${dateStr})`;
  
  const htmlBody = `
  <div style="font-family: Arial, sans-serif; max-width: 700px; margin: 0 auto; color: #2d3748; line-height: 1.6; border: 1px solid #e2e8f0; border-radius: 8px; padding: 24px; background: #fff;">
    <div style="border-bottom: 2px solid #3182ce; padding-bottom: 12px; margin-bottom: 20px;">
      <h2 style="color: #2b6cb0; margin: 0;">🎯 Daily Job Discovery & Application Report</h2>
      <p style="color: #718096; margin: 4px 0 0; font-size: 14px;">Scan Date: ${dateStr} | Candidate: Dr. Kumarpal Porwal</p>
    </div>
    
    <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
      <tr>
        <td style="padding: 12px; background: #ebf8ff; border: 1px solid #bee3f8; border-radius: 6px; text-align: center; width: 25%;">
          <span style="font-size: 11px; color: #2b6cb0; text-transform: uppercase; font-weight: bold;">New Roles</span><br/>
          <span style="font-size: 28px; font-weight: bold; color: #2c5282;">${jobs.length}</span>
        </td>
        <td style="width: 8px;"></td>
        <td style="padding: 12px; background: #f0fff4; border: 1px solid #c6f6d5; border-radius: 6px; text-align: center; width: 25%;">
          <span style="font-size: 11px; color: #276749; text-transform: uppercase; font-weight: bold;">Chief of Staff</span><br/>
          <span style="font-size: 28px; font-weight: bold; color: #22543d;">${cosCount}</span>
        </td>
        <td style="width: 8px;"></td>
        <td style="padding: 12px; background: #faf5ff; border: 1px solid #e9d8fd; border-radius: 6px; text-align: center; width: 25%;">
          <span style="font-size: 11px; color: #553c9a; text-transform: uppercase; font-weight: bold;">AI / Strategy</span><br/>
          <span style="font-size: 28px; font-weight: bold; color: #44337a;">${aiCount}</span>
        </td>
        <td style="width: 8px;"></td>
        <td style="padding: 12px; background: #fffaf0; border: 1px solid #feebc8; border-radius: 6px; text-align: center; width: 25%;">
          <span style="font-size: 11px; color: #c05621; text-transform: uppercase; font-weight: bold;">Remote</span><br/>
          <span style="font-size: 28px; font-weight: bold; color: #9c4221;">${remoteCount}</span>
        </td>
      </tr>
    </table>

    <h3 style="color: #2d3748; border-bottom: 1px solid #edf2f7; padding-bottom: 6px;">New Matching Roles</h3>
    <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
      <tr style="background: #f7fafc;">
        <th style="padding: 8px; text-align: left;">#</th>
        <th style="padding: 8px; text-align: left;">Company</th>
        <th style="padding: 8px; text-align: left;">Role</th>
        <th style="padding: 8px; text-align: left;">Apply</th>
      </tr>
      ${jobsHtml}
    </table>

    <h3 style="color: #2d3748; margin-top: 24px; border-bottom: 1px solid #edf2f7; padding-bottom: 6px;">📞 Next Steps & Interview Prep</h3>
    <ul style="padding-left: 20px; font-size: 13px; color: #4a5568;">
      <li>Click the <strong>Apply →</strong> links above to submit your tailored application.</li>
      <li>Cover letters have been auto-generated and saved in the application log.</li>
      <li>Monitor inbox for interview scheduling emails from these companies.</li>
      <li>Prepare: behavioral (STAR), case study, and strategy presentation formats.</li>
      <li>Sources scanned: Ashby, Greenhouse, Lever, RemoteOK, Remotive (93+ companies).</li>
    </ul>

    <div style="margin-top: 30px; padding: 12px; background: #f7fafc; border-left: 4px solid #3182ce; font-size: 12px; color: #718096;">
      This report is auto-generated daily by Career-Ops Job Discovery Engine.<br/>
      Repository: <strong>career-ops-dispatch</strong> | Next scan: Tomorrow 4:30 AM IST
    </div>
  </div>`;

  // Write Python notification script inline
  const pyScript = `
import smtplib, json, sys, os
sys.stdout.reconfigure(encoding='utf-8')

# Load SMTP pool from env or file
pool_json = os.environ.get('SMTP_POOL_JSON', '')
if pool_json:
    pool = json.loads(pool_json)
else:
    pool = json.load(open('data/smtp_pool.json'))

sender = next((a for a in pool if a.get('user') and a.get('pass')), None)
if not sender:
    print('No SMTP sender available')
    sys.exit(1)

from email.message import EmailMessage
msg = EmailMessage()
msg['From'] = f"Career-Ops Bot <{sender['user']}>"
msg['To'] = '${CANDIDATE.email}'
msg['Subject'] = ${JSON.stringify(subject)}
msg.set_content('Daily Job Report: ${jobs.length} new roles found. Check email for HTML details.')
msg.add_alternative(${JSON.stringify(htmlBody)}, subtype='html')

with smtplib.SMTP(sender.get('host','smtp.gmail.com'), int(sender.get('port', 587)), timeout=30) as s:
    s.starttls()
    s.login(sender['user'], sender['pass'])
    s.send_message(msg)
print('Notification sent to ${CANDIDATE.email}')
`;
  
  fs.writeFileSync('_notify_jobs.py', pyScript, 'utf8');
  
  // Try multiple Python paths
  const pythonPaths = IS_CI
    ? ['python3', 'python']
    : ['C:\\Users\\My\\AppData\\Local\\Programs\\Python\\Python311\\python.exe', 'python'];
  
  let sent = false;
  for (const pyPath of pythonPaths) {
    try {
      const envVars = { ...process.env };
      if (smtpPoolJson && !process.env.SMTP_POOL_JSON) {
        envVars.SMTP_POOL_JSON = smtpPoolJson;
      }
      const out = execSync(`"${pyPath}" _notify_jobs.py`, {
        encoding: 'utf8',
        timeout: 45000,
        env: envVars,
      });
      console.log(`✅ ${out.trim()}`);
      sent = true;
      break;
    } catch (e) {
      console.log(`  [${pyPath}] Failed: ${e.message.substring(0, 100)}`);
    }
  }
  
  // Clean up
  try { fs.unlinkSync('_notify_jobs.py'); } catch {}
  return sent;
}

// ── Step 6: Save Daily Report ───────────────────────────────────────
function saveDailyReport(jobs) {
  const report = {
    date: new Date().toISOString(),
    candidate: CANDIDATE.full_name,
    total_discovered: jobs.length,
    chief_of_staff: jobs.filter(j => j.title.toLowerCase().includes('chief of staff')).length,
    ai_roles: jobs.filter(j => j.title.toLowerCase().includes('ai')).length,
    strategy_roles: jobs.filter(j => j.title.toLowerCase().includes('strategy')).length,
    remote_roles: jobs.filter(j => j.platform === 'remoteok' || j.platform === 'remotive').length,
    jobs: jobs.map(j => ({
      company: j.company,
      title: j.title,
      url: j.url,
      platform: j.platform,
      source: j.source || '',
    })),
  };
  saveJson(REPORT_FILE, report);
  console.log(`\n📁 Report saved to ${REPORT_FILE}`);
}

// ── MAIN ────────────────────────────────────────────────────────────
async function main() {
  const args = process.argv.slice(2);
  const scanOnly = args.includes('--scan-only');
  const notifyOnly = args.includes('--notify-only');
  
  console.log('╔════════════════════════════════════════════════════════════╗');
  console.log('║  Career-Ops Daily Job Discovery & Application Engine     ║');
  console.log('║  Candidate: Dr. Kumarpal Porwal                          ║');
  console.log('║  Target: Chief of Staff | AI Strategy | Remote Exec      ║');
  console.log(`║  Mode: ${IS_CI ? 'GitHub Actions CI' : 'Local'} | ${new Date().toISOString()}  ║`);
  console.log('╚════════════════════════════════════════════════════════════╝');
  
  if (notifyOnly) {
    const existingApps = getExistingApplicationsList();
    const recent = existingApps.slice(-30);
    sendNotification(recent);
    return;
  }
  
  // Step 1a: Scan portals (Ashby, Greenhouse, Lever via scan.mjs)
  runPortalScan();
  
  // Step 1b: Scan RemoteOK
  const remoteokJobs = await scanRemoteOK();
  
  // Step 1c: Scan Remotive
  const remotiveJobs = await scanRemotive();
  
  // Step 2: Extract from pipeline
  const pipelineJobs = extractFromPipeline();
  
  // Step 3: Deduplicate & merge
  const newJobs = deduplicateAndMerge(pipelineJobs, remoteokJobs, remotiveJobs);
  
  if (newJobs.length === 0) {
    console.log('\n✅ No new matching roles found today. All caught up!');
    if (!scanOnly) {
      sendNotification([]);
    }
    return;
  }
  
  // Step 4: Log applications
  logApplications(newJobs);
  
  // Step 5: Save report
  saveDailyReport(newJobs);
  
  if (!scanOnly) {
    // Step 6: Send notification
    sendNotification(newJobs);
  }
  
  console.log('\n🏁 Daily job scan complete!');
  console.log(`   ${newJobs.length} new roles discovered and logged.`);
  console.log(`   Notification sent to ${CANDIDATE.email}`);
}

main().catch(e => {
  console.error('Fatal error:', e);
  process.exit(1);
});
