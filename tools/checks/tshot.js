// Headless check of research.html By Type groups (lists each group and its IDs). Serve on :8766 first.
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
 const p = await b.newPage(); const errs=[]; p.on('pageerror', e => errs.push(e.message));
 await p.goto('http://localhost:8766/research.html'); await p.evaluate(() => showView('type'));
 console.log(await p.evaluate(() => [...document.querySelectorAll('.doc-section')].map(s => s.querySelector('h3').textContent + ': ' + [...s.querySelectorAll('.doc-title')].map(x=>x.textContent.slice(0,9)).join(',')).join('\n')));
 await p.evaluate(() => showView('date')); console.log('errors', errs); await b.close(); })();
