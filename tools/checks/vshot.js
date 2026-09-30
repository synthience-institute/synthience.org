// Headless screenshots of paper-page blocks (quickstart, cert, stack, def, obs-table) plus overflow at 390/1200. Serve on :8766 first.
const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
const shots=[['SF0038','.quickstart-block'],['SF0037','.quickstart-block'],['SF0037','.cert-block, pre, h3:has-text("Certification")'],['SF0039','.stack-block'],['SF0039','.def-block'],['SF0039','table.obs-table'],['SF0038','text=Example (illustrative)'],['SF0037','text=Two Illustrative Examples']];
for (const w of [390,1200]){const p=await b.newPage({viewport:{width:w,height:1000}});
 for (const id of ['SF0037','SF0038','SF0039','SF0040']){await p.goto('http://localhost:8766/research/'+id+'.html',{waitUntil:'domcontentloaded'});
  console.log(w,id,'overflow',await p.evaluate(()=>document.documentElement.scrollWidth-document.documentElement.clientWidth));}
 if(w==1200){let i=0;for(const [id,sel] of shots){await p.goto('http://localhost:8766/research/'+id+'.html',{waitUntil:'domcontentloaded'});const el=p.locator(sel).first();if(await el.count()){await el.scrollIntoViewIfNeeded();await p.screenshot({path:__dirname+`/v_${i}_${id}.png`});}else console.log('missing',id,sel);i++;}}
 await p.close();}
await b.close();})();
