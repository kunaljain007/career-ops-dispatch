import fs from 'fs';
import { createTransporter, getSentEmails, saveSentEmail, getDailyCount } from './multi-smtp.mjs';

const POOL_PATH = './data/smtp_pool.json';
const UNREACHED_PATH = './data/extracted_not_reached.json';

const ATTACHMENTS = [
  { filename: 'Heatbolt_Teaser.pdf', path: 'E:\\heatbolt investment 2026\\E__heatbolt investment 2026_Heatbolt teaser.pdf' },
  { filename: 'endorsement.PNG', path: 'E:\\heatbolt investment 2026\\endorsement (1).PNG' }
];

const subject = 'Strategic Proposal: ₹10,000 Cr Controlled Thermal & Sustainable Packaging Platform';
const MAX_DAILY = 80;

function extractNameFromEmail(email) {
  if (!email) return "Partner";
  let parts = email.split('@')[0].split(/[._-]/);
  if (parts.length > 0 && parts[0].length > 0)
    return parts[0].charAt(0).toUpperCase() + parts[0].slice(1).toLowerCase();
  return "Partner";
}

function getHtmlContent(email) {
  const name = extractNameFromEmail(email);
  const genericNames = ['info','contact','admin','sales','hello','pitch','businessplans','avp','investment','dealflow','press','partnerships','biz','grants','proposals','decks','pitches'];
  const g = (name.length < 3 || genericNames.includes(name.toLowerCase())) ? "Team" : name;

  return `
  <div style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 650px; margin: 0 auto; color: #333; line-height: 1.6; padding: 20px; border: 1px solid #e0e0e0; border-radius: 8px; background-color: #ffffff;">
      <div style="border-bottom: 2px solid #2c3e50; padding-bottom: 15px; margin-bottom: 20px;">
          <h2 style="color: #2c3e50; margin: 0; font-size: 24px;">Strategic Proposal: Make-in-India Thermal Innovation</h2>
      </div>
      <p style="font-size: 16px;">Dear ${g},</p>
      <p style="font-size: 16px;">I hope this email finds you well.</p>
      <p style="font-size: 16px;">I am writing to present what I believe is a transformational <strong>Make-in-India</strong> opportunity with the potential to create a new multi-billion-dollar category in controlled thermal systems, sustainable packaging, and decentralized energy applications.</p>
      <div style="background-color: #f9f9f9; padding: 15px; border-left: 4px solid #3498db; margin: 20px 0;">
          <h3 style="margin-top: 0; color: #2980b9; font-size: 18px;">1️⃣ The Core Innovation</h3>
          <p style="margin-bottom: 0;"><strong>Heatbolt</strong> has developed a proprietary formulation-based controlled thermal activation system capable of generating up to 100°C heat using only water — <em>without electricity, LPG, flame, or external fuel</em>.</p>
      </div>
      <p style="font-size: 16px;">The system is embedded directly into trays, cups, pouches, containers, and modular packaging formats — enabling safe, on-demand heating anywhere.</p>
      <p style="font-size: 16px;">Our zero-electricity, flame-free tech has been validated via tactical trials with Indian commandos at the Siachen Glacier (-60°C), and is fully certified by CIPET and IISc Bangalore. This has immense potential for defense, disaster relief, FMCG, and off-grid remote operations.</p>
      <div style="background-color: #fff8e1; padding: 15px; border-left: 4px solid #f39c12; margin: 20px 0;">
          <p style="margin: 0 0 10px 0;">📌 <strong><a href="https://www.linkedin.com/posts/kumarpal-porwal_heatbolt-makeinindia-innovation-activity-7486186134474207232-dmlc?utm_source=share&utm_medium=member_desktop&rcm=ACoAADCMQfgBlla2PzcWL8PFVfmqWClRsXnc6hc" style="color: #d35400; text-decoration: underline;">Urgent Need to Solve the Problem</a></strong></p>
          <p style="margin: 0;">✅ <strong><a href="https://www.linkedin.com/posts/rohansachdeva20_makeinindia-innovation-foodtech-share-7483541963657605120-TCKs/?utm_source=share&utm_medium=member_desktop&rcm=ACoAADCMQfgBlla2PzcWL8PFVfmqWClRsXnc6hc" style="color: #27ae60; text-decoration: underline;">We Have the Solution</a></strong></p>
      </div>
      <div style="background-color: #f9f9f9; padding: 15px; border-left: 4px solid #27ae60; margin: 20px 0;">
          <h3 style="margin-top: 0; color: #229954; font-size: 18px;">2️⃣ Commercial Scale & Pipeline</h3>
          <p style="margin-bottom: 0;">We are preparing our commercial factory scale-up, backed by verified pre-orders and pipeline interest from market cornerstones including Indian Railways, Emirates, Haldirams, and ITC.</p>
      </div>
      <p style="font-size: 16px;">Based on ongoing discussions, our commercial pipeline is progressing toward an estimated demand of nearly 20 billion units per month, representing a potentially transformative long-term business opportunity.</p>
      <p style="font-size: 16px; font-weight: bold;">I would appreciate the opportunity to discuss how Heatbolt's platform could integrate with your operations or investment thesis. Could we schedule a brief introductory call?</p>
      <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
          <p style="margin: 0; font-size: 16px;">Best regards,</p>
          <p style="margin: 5px 0 0 0; font-size: 18px; font-weight: bold; color: #2c3e50;">Dr. Kumarpal Porwal</p>
          <p style="margin: 2px 0; font-size: 15px; color: #2980b9;">Founder, Heatbolt Technologies</p>
          <p style="margin: 0; font-size: 14px; color: #7f8c8d;">📱 +91 7353319757</p>
      </div>
  </div>;`;
}

async function runAgent(account, agentId, totalAgents) {
  const dailySent = getDailyCount(account.user);
  const remaining = MAX_DAILY - dailySent;
  if (remaining <= 0) {
    console.log(`[A${agentId}] ${account.user} already at daily limit (${dailySent}/${MAX_DAILY}). Skipping.`);
    return;
  }

  let transporter;
  try {
    transporter = await createTransporter(account);
  } catch(e) {
    console.log(`[A${agentId}] FAILED transporter for ${account.user}: ${e.message}`);
    return;
  }

  // Load queue — each agent gets every Nth email (modulo totalAgents)
  const unreached = JSON.parse(fs.readFileSync(UNREACHED_PATH, 'utf-8'));
  const allContacts = Array.isArray(unreached) ? unreached : Object.entries(unreached).map(([email, d]) => ({ email, ...d }));
  const myContacts = allContacts.filter((_, i) => i % totalAgents === agentId);

  console.log(`[A${agentId}] ${account.user} — ${remaining} slots left, ${myContacts.length} candidates assigned`);

  let sentCount = dailySent;
  let consecutiveErrors = 0;

  for (const contact of myContacts) {
    if (sentCount >= MAX_DAILY) break;

    const targetEmail = contact.email || contact;
    if (!targetEmail || typeof targetEmail !== 'string' || !targetEmail.includes('@')) continue;

    const alreadySent = getSentEmails();
    if (alreadySent[targetEmail.toLowerCase()]) continue;

    try {
      await transporter.sendMail({
        to: targetEmail, subject,
        html: getHtmlContent(targetEmail),
        from: `"Parshwa - Founder, Heatbolt" <${account.user}>`,
        cc: 'team.heatbolt@gmail.com',
        replyTo: 'founder.heatbolt@gmail.com',
        attachments: ATTACHMENTS
      });
      saveSentEmail(targetEmail, subject, account.user);
      sentCount++;
      consecutiveErrors = 0;
      console.log(`[A${agentId}][OK] ${targetEmail} via ${account.user} (${sentCount}/${MAX_DAILY})`);

      // Optimized safe delay: 12-25s to avoid Gmail block while accelerating speed
      const delay = 12000 + Math.floor(Math.random() * 13000);
      await new Promise(r => setTimeout(r, delay));
    } catch (e) {
      consecutiveErrors++;
      const msg = e.message.toLowerCase();
      console.log(`[A${agentId}][ERR] ${account.user} -> ${targetEmail}: ${e.message}`);

      if (msg.includes('limit') || msg.includes('spam') || msg.includes('quota') || msg.includes('blocked') || msg.includes('disabled') || msg.includes('lockdown')) {
        console.log(`[A${agentId}][STOP] ${account.user} hit Gmail limit. Done.`);
        break;
      }
      if (msg.includes('invalid login') || msg.includes('badcredentials') || msg.includes('authentication') || msg.includes('535')) {
        console.log(`[A${agentId}][STOP] ${account.user} auth failure. Done.`);
        break;
      }
      if (consecutiveErrors >= 3) {
        console.log(`[A${agentId}][STOP] ${account.user} 3 consecutive errors. Done.`);
        break;
      }
      const backoff = Math.min(60000, 10000 * Math.pow(2, consecutiveErrors));
      await new Promise(r => setTimeout(r, backoff));
    }
  }

  try { transporter.close(); } catch(_) {}
  console.log(`[A${agentId}][DONE] ${account.user} finished at ${sentCount}/${MAX_DAILY}`);
}

function saveResumePromptToDesktop() {
  const desktopPath = 'C:\\Users\\My\\Desktop\\Resume_Prompt_Career_Ops.txt';
  const now = new Date().toISOString();
  const content = `# Resume Prompt for Career Ops Background Task
# Last Updated: ${now}

## Session Summary
- **Target Limit Per SMTP**: 80 emails per account across 16 accounts (Max daily capacity: 1,280 emails).
- **Status**: Completed today's quota batch across all available accounts.
- **Pacing**: Optimized 12-25 sec jitter delay per email for safety.

## How to Resume Tomorrow
To resume sending emails tomorrow:
\`\`\`bash
cd C:\\Users\\My\\.gemini\\antigravity\\scratch\\career-ops
node turbo-swarm-16.mjs
\`\`\`

## System Architecture Reference
- **Script**: \`turbo-swarm-16.mjs\` (Runs 16 parallel agents simultaneously, 1 per SMTP account).
- **Deduplication**: Automatically tracked in \`outreach-campaign.csv\` and \`data/sent_emails.json\`.
`;
  try {
    fs.writeFileSync(desktopPath, content, 'utf-8');
    console.log(`\n✅ Session summary & Resume Prompt saved to Desktop: ${desktopPath}`);
  } catch (err) {
    console.error(`Failed to write Resume Prompt to Desktop: ${err.message}`);
  }
}

async function main() {
  const pool = JSON.parse(fs.readFileSync(POOL_PATH, 'utf-8'));
  // Deduplicate pool by user
  const seen = new Set();
  const uniquePool = pool.filter(a => {
    if (seen.has(a.user)) return false;
    seen.add(a.user);
    return true;
  });

  const totalAgents = uniquePool.length;
  console.log(`\n🚀 TURBO SWARM — ${totalAgents} parallel agents launching`);
  console.log(`📧 Each agent: up to ${MAX_DAILY} emails, 12-25s delay`);
  console.log(`⏱️  ETA: ~20-30 minutes to exhaust daily quota\n`);

  // Launch ALL agents simultaneously
  const promises = uniquePool.map((account, i) => runAgent(account, i, totalAgents));
  await Promise.all(promises);

  console.log(`\n🎉 ALL AGENTS COMPLETE FOR TODAY.`);
  saveResumePromptToDesktop();
}

main().catch(e => console.error('Fatal:', e));
