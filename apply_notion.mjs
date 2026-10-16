import { chromium } from 'playwright';
import path from 'path';
import fs from 'fs';

const CANDIDATE = {
  fullName: 'Dr. Kumarpal Porwal',
  firstName: 'Kumarpal',
  lastName: 'Porwal',
  email: 'founder.heatbolt@gmail.com',
  phone: '+917353319757',
  location: 'Belgaum, Karnataka, India',
  linkedin: 'https://www.linkedin.com/in/kumarpal-porwal',
  resume: path.resolve('C:/Users/My/Desktop/kumarpalshreeram.pdf'),
};

async function applyNotion() {
  console.log('Targeting Notion Chief of Staff, Sales...');
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
  });
  const page = await context.newPage();

  try {
    await page.goto('https://jobs.ashbyhq.com/notion/c5c69246-74db-4960-a0e0-7945be6c30ae', { waitUntil: 'networkidle', timeout: 35000 });
    await page.waitForTimeout(2000);

    // Click Apply for this job if on overview
    const applyTab = page.locator('button:has-text("Apply for this Job"), button:has-text("Apply")').first();
    if (await applyTab.isVisible().catch(() => false)) {
      await applyTab.click();
      await page.waitForTimeout(2000);
    }

    // 1. Upload resume
    const fileInput = page.locator('input[type="file"]').first();
    if (await fileInput.count() > 0 && fs.existsSync(CANDIDATE.resume)) {
      await fileInput.setInputFiles(CANDIDATE.resume);
      console.log('Uploaded resume to Notion');
      await page.waitForTimeout(2500);
    }

    // 2. Full Name
    const nameInput = page.locator('input[name="name"], input[placeholder*="Type here" i]').first();
    if (await nameInput.isVisible().catch(() => false)) {
      await nameInput.fill(CANDIDATE.fullName);
      console.log('Filled Full Name:', CANDIDATE.fullName);
    }

    // 3. Email
    const emailInput = page.locator('input[name="email"], input[type="email"]').first();
    if (await emailInput.isVisible().catch(() => false)) {
      await emailInput.fill(CANDIDATE.email);
    }

    // 4. Phone
    const phoneInput = page.locator('input[name="phoneNumber"], input[type="tel"]').first();
    if (await phoneInput.isVisible().catch(() => false)) {
      await phoneInput.fill(CANDIDATE.phone);
    }

    // 5. LinkedIn
    const liInput = page.locator('input[name*="linkedin" i]:not([type="checkbox"]), input[placeholder*="linkedin" i]:not([type="checkbox"])').first();
    if (await liInput.isVisible().catch(() => false)) {
      await liInput.fill(CANDIDATE.linkedin);
    }

    // 6. Cover letter / Note
    const coverText = `Dear Notion Hiring Team,

I am writing to express my enthusiastic interest in the Chief of Staff, Sales position at Notion.

Throughout my leadership career—both as Founder & MD of HeatBolt/Parshwa Power commercializing platforms with Amul, Defence Forces, and Emirates Flight Catering, and as Chief of Staff at Vega Aviation driving a 40% efficiency boost—I have specialized in unblocking teams, driving GTM alignment, and creating executive clarity from ambiguity.

Key Highlights:
• Chief of Staff Execution: Spearheaded cross-functional operational rhythms and deployed autonomous systems across high-velocity teams.
• Enterprise Commercialization: Negotiated multi-million dollar institutional partnerships with zero-defect execution.
• Agile & Remote Alignment: Seasoned in asynchronous OKR management, executive communication, and high-trust leadership.

Warm regards,
Dr. Kumarpal Porwal
founder.heatbolt@gmail.com | +91 73533 19757`;

    const notes = page.locator('textarea').first();
    if (await notes.isVisible().catch(() => false)) {
      await notes.fill(coverText);
      console.log('Filled cover letter in Notion');
    }

    await page.waitForTimeout(1000);
    await page.screenshot({ path: 'data/notion_fixed_filled.png' });
    console.log('Captured data/notion_fixed_filled.png');

    // Submit button
    const submitBtn = page.locator('button:has-text("Submit Application"), button[type="submit"]:has-text("Submit")').first();
    if (await submitBtn.isVisible({ timeout: 2000 }).catch(() => false)) {
      await submitBtn.click({ force: true });
      console.log('Clicked Submit Application on Notion form');
      await page.waitForTimeout(4000);

      const body = await page.innerText('body').catch(() => '');
      if (body.toLowerCase().includes('thank') || body.toLowerCase().includes('received')) {
        console.log('VERIFIED: Notion Application Submitted 100%!');
      } else {
        console.log('Submitted, checking confirmation text.');
      }
      await page.screenshot({ path: 'data/notion_after_submit.png' });
    }

  } catch (err) {
    console.error('Error on Notion:', err.message);
  } finally {
    await browser.close();
  }
}

applyNotion().catch(console.error);
