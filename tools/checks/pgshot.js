// Headless check of a PG page, the guides index and updates.html: overflow, image sizes, broken internal links, screenshots. Serve on :8766 first.
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }); const errs=[];
 for (const w of [390, 1200]) { const p = await b.newPage({ viewport: { width: w, height: 900 } }); p.on('pageerror', e => errs.push(e.message));
  for (const u of ['practitioner-guides/PG-016.html','practitioner-guides.html','updates.html']) {
   await p.goto('http://localhost:8766/'+u); await p.waitForTimeout(400);
   console.log(w,u,'overflow',await p.evaluate(()=>document.documentElement.scrollWidth-window.innerWidth));
   if (u.startsWith('practitioner-guides/')) {
     const r = await p.evaluate(()=>{const imgs=[...document.images].filter(i=>i.src.includes('PG-016'));return imgs.map(i=>[i.naturalWidth,Math.round(i.getBoundingClientRect().width)]);});
     console.log('  images natural/displayed', JSON.stringify(r));
     const bad = await p.evaluate(()=>[...document.querySelectorAll('main a')].map(a=>a.getAttribute('href')).filter(h=>h&&!h.startsWith('http')));
     for (const h of bad){ const r=await p.request.get('http://localhost:8766/practitioner-guides/'+h); if(r.status()!==200) console.log('  BROKEN',h,r.status()); }
     if (w==1200){ await p.locator('figure.wide').scrollIntoViewIfNeeded(); await p.screenshot({path:'pg016_fig.png'}); await p.evaluate(()=>window.scrollTo(0,0)); await p.screenshot({path:'pg016_top.png'}); }
   }
   if (u=='practitioner-guides.html') console.log('  listed', await p.evaluate(()=>document.body.innerText.includes('PG-016')));
  } }
 console.log('errors',errs); await b.close(); })();
