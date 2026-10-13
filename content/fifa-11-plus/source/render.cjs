// FIFA 11+ 카드 렌더 + 측정. 사용: node render.cjs  (Playwright 전역 설치 경로 또는 NODE_PATH 사용)
const path=require('path'),fs=require('fs');
let pw;try{pw=require('playwright')}catch(e){pw=require('/opt/node-tools/node_modules/playwright')}
const {pathToFileURL}=require('url');
(async()=>{
 const root=path.resolve(__dirname,'..');
 const browser=await pw.chromium.launch({headless:true});
 const page=await browser.newPage({viewport:{width:1200,height:1500},deviceScaleFactor:1});
 await page.goto(pathToFileURL(path.join(__dirname,'cards.html')).href);
 await page.evaluate(()=>document.fonts.ready);
 const report=[];
 const ids=await page.$$eval('article.card',a=>a.map(e=>e.id));
 for(const id of ids){
  const r=await page.evaluate((id)=>{
   const card=document.getElementById(id),cr=card.getBoundingClientRect();const errors=[];let bottom=0;const sizes={};
   const leaves=[...card.querySelectorAll('*')].filter(e=>!e.closest('.card-frame')&&getComputedStyle(e).display!=='none'&&getComputedStyle(e).visibility!=='hidden');
   for(const e of leaves){
    // 텍스트 노드는 Range로 실제 줄 경계 측정
    for(const n of e.childNodes){if(n.nodeType===3&&n.textContent.trim()){
      const rg=document.createRange();rg.selectNodeContents(n);
      for(const b of rg.getClientRects()){const t=b.top-cr.top,bt=b.bottom-cr.top,l=b.left-cr.left,rt=b.right-cr.left;
        bottom=Math.max(bottom,bt);if(l<87.5||rt>992.5||t<95.5||bt>1252.5)errors.push(id+' text outside safe: '+n.textContent.trim().slice(0,20)+` (${l|0},${t|0},${rt|0},${bt|0})`);}
      const fs=getComputedStyle(e).fontSize;sizes[e.className||e.tagName]=fs;}}
    if(e.matches('.cover-art,.video-slot,.pill,.box')){const b=e.getBoundingClientRect();bottom=Math.max(bottom,b.bottom-cr.top);
      if(b.left-cr.left<87.5||b.right-cr.left>992.5||b.bottom-cr.top>1252.5)errors.push(id+' block outside safe: '+e.className);}
    if(e.clientWidth&&e.scrollWidth>e.clientWidth+1&&getComputedStyle(e).overflow!=='visible')errors.push(id+' overflow '+e.className);
   }
   // 겹침(주요 블록)
   const blocks=[...card.querySelectorAll(':scope > :not(.card-frame):not(.curve)')];
   for(let i=0;i<blocks.length;i++)for(let j=i+1;j<blocks.length;j++){const a=blocks[i].getBoundingClientRect(),b=blocks[j].getBoundingClientRect();
    if(Math.min(a.right,b.right)-Math.max(a.left,b.left)>1&&Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top)>1)errors.push(id+' overlap '+blocks[i].className+' / '+blocks[j].className);}
   return {id,contentBottom:Math.round(bottom*10)/10,bottomGap:Math.round((1316-bottom)*10)/10,sizes,errors};
  },id);
  report.push(r);
  await page.locator('#'+id).screenshot({path:path.join(root,'exports',id.replace('c','')+'.png')});
 }
 // 영상 카드: 안내 문구 없는 배경
 await page.evaluate(()=>document.getElementById('c05').classList.add('clean'));
 await page.locator('#c05').screenshot({path:path.join(root,'video-template','05-video-background.png')});
 await browser.close();
 fs.writeFileSync(path.join(root,'qa','layout-check.json'),JSON.stringify(report,null,2));
 for(const r of report)console.log(r.id,'contentBottom',r.contentBottom,'gap',r.bottomGap,r.errors.length?'ERR '+r.errors.join(' | '):'OK');
})();
