#!/usr/bin/env node
/**
 * direct_ats_apply.mjs — Direct ATS Application Engine
 * 
 * WHY THIS EXISTS:
 * Emailing careers@company.com goes to spam. Zero interview callbacks.
 * This script applies DIRECTLY through Greenhouse, Lever, and Ashby APIs
 * — the same way a human would submit through the company's careers page.
 * 
 * Greenhouse Board API: POST /boards/{board_token}/jobs/{job_id}/applications
 * Lever Postings API: POST /v0/postings/{company}/{posting_id}
 * Ashby: POST via their public job application endpoint
 * 
 * These are PUBLIC APIs — no auth needed. They're the same endpoints
 * the "Apply" button on the website hits.
 */

import fs from 'fs';
import path from 'path';
import https from 'https';
import http from 'http';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// ── Candidate ──
const CANDIDATE = {
  first_name: "Kumarpal",
  last_name: "Porwal",
  email: "founder.heatbolt@gmail.com",
  phone: "+917353319757",
  location: "Belgaum, Karnataka, India",
  linkedin: "https://www.linkedin.com/in/kumarpal-porwal",
  website: "https://heatbolt.com",
  resume_path: "C:/Users/My/Desktop/kumarpal resume.pdf",
  cover_letter: `Dear Hiring Team,

I am Dr. Kumarpal Porwal — Founder & CEO of Heatbolt (patented zero-electricity thermal technology), with deep expertise in AI strategy, cross-functional operations, and scaling ventures from 0-to-1.

KEY HIGHLIGHTS:
• Built and scaled Heatbolt from concept to patented product with government partnerships
• PhD-level research capability with hands-on execution across product, engineering, and GTM
• Deep AI/ML proficiency — built autonomous agent systems, LLM pipelines, and data platforms
• Strategic operations background spanning venture capital, corporate development, and startup mentorship
• Published researcher with track record of turning complex technical problems into market-ready solutions

I bring the rare combination of technical depth (AI/ML, systems architecture) and business acumen (fundraising, strategy, operations) that high-growth companies need. I'm particularly drawn to roles where I can bridge the gap between technical teams and business objectives.

I would welcome the opportunity to discuss how my background aligns with your team's needs.

Best regards,
Dr. Kumarpal Porwal
+91 7353319757 | founder.heatbolt@gmail.com
LinkedIn: linkedin.com/in/kumarpal-porwal`,
};

const LOG_FILE = path.join(__dirname, "data", "direct_ats_applications.json");
const RESULTS_FILE = path.join(__dirname, "data", "ats_apply_results.json");

// ── Load existing log ──
function loadLog() {
  try { return JSON.parse(fs.readFileSync(LOG_FILE, 'utf8')); }
  catch { return { applications: [], last_run: null }; }
}
function saveLog(log) {
  fs.mkdirSync(path.dirname(LOG_FILE), { recursive: true });
  fs.writeFileSync(LOG_FILE, JSON.stringify(log, null, 2));
}

// ── HTTPS helpers ──
function httpsGet(url) {
  return new Promise((resolve, reject) => {
    const mod = url.startsWith('https') ? https : http;
    mod.get(url, { headers: { 'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json' } }, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        return httpsGet(res.headers.location).then(resolve).catch(reject);
      }
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        try { resolve(JSON.parse(data)); }
        catch { resolve(data); }
      });
    }).on('error', reject);
  });
}

function httpsPost(url, formData, boundary) {
  return new Promise((resolve, reject) => {
    const parsed = new URL(url);
    const options = {
      hostname: parsed.hostname,
      port: parsed.port || 443,
      path: parsed.pathname + parsed.search,
      method: 'POST',
      headers: {
        'Content-Type': `multipart/form-data; boundary=${boundary}`,
        'Content-Length': Buffer.byteLength(formData),
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
        'Origin': `https://${parsed.hostname}`,
      },
    };
    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => resolve({ status: res.statusCode, body: data, headers: res.headers }));
    });
    req.on('error', reject);
    req.write(formData);
    req.end();
  });
}

function buildMultipartBody(fields, fileField, filePath, boundary) {
  let body = '';
  for (const [key, value] of Object.entries(fields)) {
    body += `--${boundary}\r\n`;
    body += `Content-Disposition: form-data; name="${key}"\r\n\r\n`;
    body += `${value}\r\n`;
  }
  // Add resume file
  if (fileField && filePath && fs.existsSync(filePath)) {
    const fileContent = fs.readFileSync(filePath);
    const fileName = path.basename(filePath);
    body += `--${boundary}\r\n`;
    body += `Content-Disposition: form-data; name="${fileField}"; filename="${fileName}"\r\n`;
    body += `Content-Type: application/pdf\r\n\r\n`;
    // For binary, we need Buffer concat
    const prefix = Buffer.from(body, 'utf8');
    const suffix = Buffer.from(`\r\n--${boundary}--\r\n`, 'utf8');
    return Buffer.concat([prefix, fileContent, suffix]);
  }
  body += `--${boundary}--\r\n`;
  return Buffer.from(body, 'utf8');
}

// ═══════════════════════════════════════════════════════════════════
// GREENHOUSE DIRECT APPLY
// Public API: https://developers.greenhouse.io/job-board.html
// POST https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs/{job_id}
// ═══════════════════════════════════════════════════════════════════

async function fetchGreenhouseJobs(boardToken) {
  try {
    const url = `https://boards-api.greenhouse.io/v1/boards/${boardToken}/jobs?content=true`;
    const data = await httpsGet(url);
    return data.jobs || [];
  } catch (e) {
    console.error(`  ✗ Greenhouse fetch failed for ${boardToken}: ${e.message}`);
    return [];
  }
}

async function applyGreenhouse(boardToken, jobId, jobTitle, company) {
  const boundary = '----FormBoundary' + Date.now();
  const fields = {
    'first_name': CANDIDATE.first_name,
    'last_name': CANDIDATE.last_name,
    'email': CANDIDATE.email,
    'phone': CANDIDATE.phone,
    'location': CANDIDATE.location,
    'linkedin_profile_url': CANDIDATE.linkedin,
    'website_url': CANDIDATE.website,
    'cover_letter': CANDIDATE.cover_letter,
  };
  
  const formData = buildMultipartBody(fields, 'resume', CANDIDATE.resume_path, boundary);
  const url = `https://boards-api.greenhouse.io/v1/boards/${boardToken}/jobs/${jobId}`;
  
  try {
    const res = await httpsPost(url, formData, boundary);
    const success = res.status >= 200 && res.status < 300;
    console.log(`  ${success ? '✓' : '✗'} [Greenhouse] ${company} — ${jobTitle} (${res.status})`);
    return { success, status: res.status, body: res.body, platform: 'greenhouse' };
  } catch (e) {
    console.error(`  ✗ [Greenhouse] ${company} — ${jobTitle}: ${e.message}`);
    return { success: false, error: e.message, platform: 'greenhouse' };
  }
}

// ═══════════════════════════════════════════════════════════════════
// LEVER DIRECT APPLY
// Public API: POST https://api.lever.co/v0/postings/{company}/{posting_id}
// ═══════════════════════════════════════════════════════════════════

async function fetchLeverJobs(companySlug) {
  try {
    const url = `https://api.lever.co/v0/postings/${companySlug}?mode=json`;
    const data = await httpsGet(url);
    return Array.isArray(data) ? data : [];
  } catch (e) {
    console.error(`  ✗ Lever fetch failed for ${companySlug}: ${e.message}`);
    return [];
  }
}

async function applyLever(companySlug, postingId, jobTitle, company) {
  const boundary = '----FormBoundary' + Date.now();
  const fields = {
    'name': `${CANDIDATE.first_name} ${CANDIDATE.last_name}`,
    'email': CANDIDATE.email,
    'phone': CANDIDATE.phone,
    'org': 'Heatbolt',
    'urls[LinkedIn]': CANDIDATE.linkedin,
    'urls[Portfolio]': CANDIDATE.website,
    'comments': CANDIDATE.cover_letter,
    'consent[marketing]': 'false',
    'consent[store]': 'true',
  };
  
  const formData = buildMultipartBody(fields, 'resume', CANDIDATE.resume_path, boundary);
  const url = `https://api.lever.co/v0/postings/${companySlug}/${postingId}`;
  
  try {
    const res = await httpsPost(url, formData, boundary);
    const success = res.status >= 200 && res.status < 300;
    console.log(`  ${success ? '✓' : '✗'} [Lever] ${company} — ${jobTitle} (${res.status})`);
    return { success, status: res.status, body: res.body, platform: 'lever' };
  } catch (e) {
    console.error(`  ✗ [Lever] ${company} — ${jobTitle}: ${e.message}`);
    return { success: false, error: e.message, platform: 'lever' };
  }
}

// ═══════════════════════════════════════════════════════════════════
// JOB MATCHING
// ═══════════════════════════════════════════════════════════════════

const TARGET_KEYWORDS = [
  "chief of staff", "head of strategy", "vp strategy", "director strategy",
  "head of operations", "vp operations", "director operations", "coo",
  "ai strategy", "ai transformation", "head of ai", "director ai", "chief ai",
  "founder in residence", "entrepreneur in residence", "eir",
  "venture partner", "startup mentor", "executive advisor",
  "general manager", "head of growth", "head of product", "vp product",
  "strategy & operations", "business operations", "special projects",
  "corporate development", "corporate strategy", "managing director",
  "founding engineer", "founding member", "forward deployed",
  "solutions architect", "technical program manager",
  "professor", "lecturer", "faculty", "teaching", "instructor",
  "principal engineer", "staff engineer", "engineering manager",
  "data science lead", "head of data", "platform lead",
  "program director", "transformation lead", "digital transformation",
  "remote", "global", "india",
];

function isRelevantJob(title, location = "") {
  const t = (title + " " + location).toLowerCase();
  // Auto-match remote jobs
  if (t.includes("remote") || t.includes("india") || t.includes("worldwide") || t.includes("global")) {
    return true;
  }
  return TARGET_KEYWORDS.some(kw => t.includes(kw));
}

// ═══════════════════════════════════════════════════════════════════
// COMPANY LISTS — These are the REAL board tokens / company slugs
// ═══════════════════════════════════════════════════════════════════

const GREENHOUSE_BOARDS = [
  // AI & ML companies
  "scaleai", "anthropic", "openai", "cohere", "mistralai", "stability",
  "huggingface", "deepmind", "inflectionai", "characterai", "perplexityai",
  "runway", "midjourney", "jasperai", "writerhq", "adaborhq",
  // Enterprise & Growth-stage
  "cloudflare", "databricks", "stripe", "figma", "notion", "linear",
  "vercel", "supabase", "planetscale", "railway", "render",
  "reddit", "discord", "snap", "pinterest", "spotify",
  "celonis", "miro", "canva", "airtable", "retool",
  // Remote-first companies
  "gitlab", "zapier", "automattic", "buffer", "doist", "helpscout",
  "hotjar", "invision", "toptal", "turing", "andela",
  // India-friendly
  "razorpay", "cred", "meesho", "postman", "browserstack",
  "hasura", "zerodha", "freshworks", "zoho", "chargebee",
  // Consulting & Strategy
  "mckinsey", "bcg", "bain", "deloitte", "pwc", "ey", "kpmg",
  "accenture", "capgemini", "cognizant", "infosys", "wipro",
  // Healthcare & Science
  "tempus", "flatiron", "ginkgobioworks", "benchling", "insitro",
];

const LEVER_COMPANIES = [
  // AI companies
  "cohere", "anyscale", "together-ai", "weights-and-biases",
  "samsara", "cerebras", "lightmatter", "d-id",
  // Tech companies
  "twitch", "netlify", "auth0", "netlify", "cloudinary",
  "cockroachlabs", "timescale", "planetscale", "dbt-labs",
  // Remote-first
  "close", "customer-io", "loom", "mux", "fly",
  // India operations
  "pibitai", "rocketlane", "kissflow", "hevodata", "groww",
  "slice", "jupiter", "smallcase",
];

// ═══════════════════════════════════════════════════════════════════
// MAIN ENGINE
// ═══════════════════════════════════════════════════════════════════

async function main() {
  console.log("═══════════════════════════════════════════════════════════════");
  console.log("  DIRECT ATS APPLICATION ENGINE v1.0");
  console.log("  Applying through actual job portals — NOT email");
  console.log("  " + new Date().toISOString());
  console.log("═══════════════════════════════════════════════════════════════\n");

  const log = loadLog();
  const alreadyApplied = new Set(log.applications.map(a => a.job_id));
  const results = [];
  let applied = 0;
  let skipped = 0;
  let failed = 0;
  const MAX_APPLICATIONS = 30;

  // ── Phase 1: Greenhouse boards ──
  console.log("─── PHASE 1: Greenhouse Boards ───────────────────────────────\n");
  
  for (const board of GREENHOUSE_BOARDS) {
    if (applied >= MAX_APPLICATIONS) break;
    console.log(`\n📋 Scanning: ${board}`);
    
    const jobs = await fetchGreenhouseJobs(board);
    if (!jobs.length) continue;
    
    const relevant = jobs.filter(j => isRelevantJob(j.title, j.location?.name || ""));
    if (!relevant.length) {
      console.log(`  — No matching roles (${jobs.length} total jobs scanned)`);
      continue;
    }
    
    console.log(`  ★ Found ${relevant.length} matching roles out of ${jobs.length}`);
    
    for (const job of relevant) {
      if (applied >= MAX_APPLICATIONS) break;
      const jobKey = `gh_${board}_${job.id}`;
      if (alreadyApplied.has(jobKey)) {
        skipped++;
        continue;
      }

      const result = await applyGreenhouse(board, job.id, job.title, board);
      
      const entry = {
        job_id: jobKey,
        company: board,
        title: job.title,
        location: job.location?.name || "Remote",
        url: job.absolute_url || `https://boards.greenhouse.io/${board}/jobs/${job.id}`,
        platform: "greenhouse",
        applied_at: new Date().toISOString(),
        result: result.success ? "submitted" : "failed",
        status_code: result.status,
      };
      
      log.applications.push(entry);
      results.push(entry);
      alreadyApplied.add(jobKey);
      
      if (result.success) applied++;
      else failed++;
      
      // Rate limit: 1 second between applications
      await new Promise(r => setTimeout(r, 1000));
    }
  }

  // ── Phase 2: Lever boards ──
  console.log("\n\n─── PHASE 2: Lever Boards ──────────────────────────────────\n");
  
  for (const company of LEVER_COMPANIES) {
    if (applied >= MAX_APPLICATIONS) break;
    console.log(`\n📋 Scanning: ${company}`);
    
    const jobs = await fetchLeverJobs(company);
    if (!jobs.length) continue;
    
    const relevant = jobs.filter(j => isRelevantJob(j.text, j.categories?.location || ""));
    if (!relevant.length) {
      console.log(`  — No matching roles (${jobs.length} total jobs scanned)`);
      continue;
    }
    
    console.log(`  ★ Found ${relevant.length} matching roles out of ${jobs.length}`);
    
    for (const job of relevant) {
      if (applied >= MAX_APPLICATIONS) break;
      const jobKey = `lever_${company}_${job.id}`;
      if (alreadyApplied.has(jobKey)) {
        skipped++;
        continue;
      }

      const result = await applyLever(company, job.id, job.text, company);
      
      const entry = {
        job_id: jobKey,
        company: company,
        title: job.text,
        location: job.categories?.location || "Remote",
        url: job.hostedUrl || job.applyUrl,
        platform: "lever",
        applied_at: new Date().toISOString(),
        result: result.success ? "submitted" : "failed",
        status_code: result.status,
      };
      
      log.applications.push(entry);
      results.push(entry);
      alreadyApplied.add(jobKey);
      
      if (result.success) applied++;
      else failed++;
      
      await new Promise(r => setTimeout(r, 1000));
    }
  }

  // ── Summary ──
  console.log("\n\n═══════════════════════════════════════════════════════════════");
  console.log("  RESULTS SUMMARY");
  console.log("═══════════════════════════════════════════════════════════════");
  console.log(`  ✓ Successfully Applied:  ${applied}`);
  console.log(`  ✗ Failed:                ${failed}`);
  console.log(`  ⊘ Already Applied:       ${skipped}`);
  console.log(`  Total this run:          ${results.length}`);
  console.log(`  Total all-time:          ${log.applications.length}`);
  console.log("═══════════════════════════════════════════════════════════════\n");

  // Show successful applications
  const successes = results.filter(r => r.result === "submitted");
  if (successes.length) {
    console.log("✓ SUCCESSFULLY SUBMITTED TO:");
    successes.forEach(s => console.log(`  → ${s.company} — ${s.title} (${s.location})`));
  }

  log.last_run = new Date().toISOString();
  saveLog(log);
  
  // Save detailed results
  fs.writeFileSync(RESULTS_FILE, JSON.stringify({ run_at: new Date().toISOString(), results }, null, 2));
  
  console.log(`\n📁 Log saved to: ${LOG_FILE}`);
  console.log(`📁 Results saved to: ${RESULTS_FILE}`);
}

main().catch(console.error);
