const path=require('path'),fs=require('fs');
const bundle='C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const {chromium}=require(path.join(bundle,'playwright'));const sharp=require(path.join(bundle,'sharp'));
const {pathToFileURL}=require('url');
(async()=>{
 const root=path.resolve(__dirname,'..'),templates=JSON.parse(fs.readFileSync(path.join(root,'placements.json')));
 const browser=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});
 const page=await browser.newPage({viewport:{width:1080,height:1350},deviceScaleFactor:1});const qa=[];
 for(const t of templates){
  for(const clean of [false,true]){
   await page.goto(pathToFileURL(path.join(__dirname,t.id+(clean?'-clean':'')+'.html')).href);await page.evaluate(()=>document.fonts.ready);
   const result=await page.evaluate(()=>{
    const errors=[];
    for(const e of document.querySelectorAll('.card *')){
     const r=e.getBoundingClientRect();
     if(r.width&&r.height&&(r.left<88||r.right>992||r.bottom>1252))errors.push(e.className+': outside safe area');
     if(e.clientWidth&&e.scrollWidth>e.clientWidth+2)errors.push(e.className+': overflow');
    }
    const labels=[...document.querySelectorAll('.compare-label')].map(e=>e.getBoundingClientRect().top);
    if(labels.length===2&&Math.abs(labels[0]-labels[1])>.1)errors.push('comparison labels not aligned');
    const regions=[...document.querySelectorAll('.library-title,.library-lead,.library-slot,.side-point,.sequence-note,.compare-label,.compare-note,.big-question,.focus-explain,.focus-note,.library-footer')];
    for(let i=0;i<regions.length;i++)for(let j=i+1;j<regions.length;j++){
     const a=regions[i].getBoundingClientRect(),b=regions[j].getBoundingClientRect();
     if(Math.min(a.right,b.right)-Math.max(a.left,b.left)>1&&Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top)>1)errors.push(regions[i].className+' overlaps '+regions[j].className);
    }
    return {errors,compareTop:labels};
   });
   if(result.errors.length)throw new Error(t.id+': '+result.errors.join(','));
   const p=path.join(root,clean?'backgrounds':'previews',t.id+'.png');await page.locator('.card').screenshot({path:p});
   const m=await sharp(p).metadata();if(m.width!==1080||m.height!==1350)throw new Error('Invalid size');
   await sharp(p).resize(360,450).png().toFile(path.join(root,'qa',t.id+(clean?'-clean':'')+'-mobile.png'));
   qa.push({template:t.id,clean,...result});
  }
  const rects=t.slots.map(s=>`<rect x="${s.x}" y="${s.y}" width="${s.width}" height="${s.height}" fill="white"/>`).join('');
  await sharp(path.join(root,'backgrounds',t.id+'.png')).ensureAlpha().composite([{input:Buffer.from(`<svg width="1080" height="1350">${rects}</svg>`),blend:'dest-out'}]).png().toFile(path.join(root,'overlays',t.id+'.png'));
  const {data,info}=await sharp(path.join(root,'overlays',t.id+'.png')).ensureAlpha().raw().toBuffer({resolveWithObject:true});
  for(let y=0;y<1350;y++)for(let x=0;x<1080;x++){
   const inside=t.slots.some(s=>x>=s.x&&x<s.x+s.width&&y>=s.y&&y<s.y+s.height);
   if(data[(y*info.width+x)*4+3] !== (inside?0:255))throw new Error(t.id+' invalid alpha');
  }
 }
 await browser.close();fs.writeFileSync(path.join(root,'qa/layout-check.json'),JSON.stringify(qa,null,2));
 console.log('PASS: 5 templates, 15 PNGs, safe bounds/alignment/transparent video windows.');
})();
