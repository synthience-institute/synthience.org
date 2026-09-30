// Headless check (Playwright + /opt/pw-browsers/chromium) of companion pages at 390/1200 px: overflow, script errors, research.html verification-stack order. Serve the repo on :8766 first (python3 -m http.server 8766).
const { chromium } = require(process.env.PWREQ || 'playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const errs = [];
  for (const w of [390, 1200]) {
    const p = await b.newPage({ viewport: { width: w, height: 900 } });
    p.on('pageerror', e => errs.push(w + ' ' + e.message));
    for (const u of ['index.html', 'research.html#verification-stack', 'about.html', 'faq.html', 'glossary.html', 'updates.html',
                     'research/SF0037.html', 'research/SF0038.html', 'research/SF0039.html', 'research/SF0040.html']) {
      await p.goto('http://localhost:8766/' + u); await p.waitForTimeout(300);
      const ov = await p.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
      console.log(w, u, 'overflow', ov);
      if (u.startsWith('research.html')) {
        const t = await p.evaluate(() => { const s = document.getElementById('topic-verification'); return [document.querySelector('.doc-section h3').textContent, [...s.querySelectorAll('.doc-title')].map(x => x.textContent.slice(0, 7)).join(','), Math.round(s.getBoundingClientRect().top)]; });
        console.log('  first group / order / top:', JSON.stringify(t));
      }
      const safe = u.replace(/[\/#.]/g, '_');
      if (['index.html','research.html#verification-stack','updates.html'].includes(u)) await p.screenshot({ path: `c_${w}_${safe}.png` });
    }
  }
  console.log('errors', errs);
  await b.close();
})();
