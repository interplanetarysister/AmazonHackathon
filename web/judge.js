(()=>{'use strict';
const $=id=>document.getElementById(id);
let data=null,selected=null;
async function call(name,args={}){
 const r=await fetch('/mcp',{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json, text/event-stream','MCP-Protocol-Version':'2025-11-25'},body:JSON.stringify({jsonrpc:'2.0',id:Date.now(),method:'tools/call',params:{name,arguments:args}})});
 if(!r.ok)throw Error('MCP HTTP '+r.status);
 const j=await r.json();if(j.error)throw Error(j.error.message);
 if(j.result?.isError)throw Error(j.result.structuredContent?.error||'Demo request failed');
 return j.result.structuredContent;
}
function node(tag,txt,parent){const n=document.createElement(tag);if(txt!==null)n.textContent=txt;parent.appendChild(n);return n;}
function link(text,url,parent){const a=node('a',text,parent);a.href=url;a.target='_blank';a.rel='noopener noreferrer';a.style.display='block';return a;}
function render(){
 $('judge-connections').textContent='DEMO SERVICES: Gmail connected (mock inbox) • Blink connected (simulated camera) • UPS/FedEx/USPS/Amazon mock APIs. No real credentials used.';
 $('judge-inbox').replaceChildren();for(const mail of data.gmail_inbox){const b=node('button',mail.subject,$('judge-inbox'));b.type='button';b.className='secondary';b.style.display='block';b.style.margin='7px 0';b.onclick=()=>choose(mail.case_id);}
 $('judge-packages').replaceChildren();for(const p of data.packages){const b=node('button',p.id+' • '+p.carrier+' • '+p.label+' • '+p.status,$('judge-packages'));b.type='button';b.className='secondary';b.style.display='block';b.style.margin='7px 0';b.onclick=()=>choose(p.id);}
 if(selected)choose(selected);
}
function choose(id){
 selected=id;const p=data.packages.find(x=>x.id===id);if(!p)return;
 const root=$('judge-case');root.replaceChildren();
 node('h3',p.id+' • '+p.label,root);
 node('p','Mock '+p.carrier+' API: '+p.status.replaceAll('_',' ')+'. Scenario: '+p.issue.replaceAll('_',' '),root);
 for(const e of p.events)node('p',e.time+' — '+e.type.replaceAll('_',' ')+' (simulated timestamp)',root);
 node('p','Claim status: '+p.claim_status.replaceAll('_',' '),root);
 link('Open official '+p.carrier+' support/claim page (no submission)',p.support_url,root);
 if(p.last_scan){
   const loc=p.last_scan;
   node('p','Last simulated carrier scan: '+loc.label+' • '+loc.time+' • '+loc.meaning,root);
   const maps='https://www.google.com/maps/search/?api=1&query='+encodeURIComponent(loc.latitude+','+loc.longitude);
   const map=link('View last SIMULATED scan location on Google Maps',maps,root);
   map.setAttribute('aria-label','Open Google Maps for fictional last scan of '+p.id);
   node('p',loc.real_facility?'Real Amazon facility location (publicly documented); scan assignment and time are fictional. This is NOT actual tracking.':'Fictional demo coordinates only. Not real courier GPS or current package location.',root).className='sub';
   if(loc.facility_source)link('Verify facility location with Amazon',loc.facility_source,root);
 }
 const cam=$('judge-video');cam.replaceChildren();
 node('p','BLINK CONNECTED — SIMULATION. Matched to '+p.id+'. Actual third-party footage is illustrative and is NOT video of this fictional shipment.',cam);
 const scenes={
 'SIM-1001':[['Delivery captured','delivery'],['Possible package removal','theft']],
 'SIM-1002':[['Carrier-reported arrival window','delivery']],
 'SIM-1003':[['Last known illustrative handling','delivery']],
 'SIM-1004':[['Delivery window reference','delivery']],
 'SIM-1005':[['Arrival recorded','delivery'],['Package received','received']]
 };
 const player=document.createElement('video');player.controls=true;player.playsInline=true;player.preload='metadata';
 player.style.width='100%';player.style.aspectRatio='16 / 9';player.style.background='#091426';player.style.borderRadius='12px';
 player.setAttribute('aria-label','Simulated Blink playback for '+p.id);
 cam.appendChild(player);
 const note=node('p','Choose a recording below. This is NOT live Blink hardware.',cam);
 const local={
   delivery:'/demo-media/dropoff.mp4',
   received:'/demo-media/received.mp4',
   theft:'/demo-media/porch-pirates-cc-by-3.0.mp4'
 };
 let uploadedURL=null;
 const entries=scenes[p.id]||[['Delivery reference','delivery']];
 function play(src,label){
   player.pause();player.src=src;player.load();
   note.textContent='Now viewing: '+label+' — illustrative recorded footage matched to fictional '+p.id+'.';
   player.play().catch(()=>{note.textContent+=' Press Play to start.';});
 }
 for(const [label,kind] of entries){
   const asset=data.camera_clips[kind];
   const b=node('button','Play '+label,cam);b.type='button';b.className='secondary';b.style.margin='6px';
   b.onclick=()=>play(local[kind],label);
   node('p',asset.credit+' • '+asset.license,cam);
   link('Source and attribution for '+label,asset.url,cam);
 }
 const uploadLabel=node('label','Add your own Blink clip (optional; kept in this browser session)',cam);
 const upload=document.createElement('input');upload.type='file';upload.accept='video/*';
 upload.id='judge-video-upload';uploadLabel.htmlFor=upload.id;cam.appendChild(upload);
 upload.onchange=()=>{
   const file=upload.files?.[0];if(!file)return;
   if(!file.type.startsWith('video/')){note.textContent='Select a video file.';return;}
   if(file.size>150*1024*1024){note.textContent='Video must be under 150 MB.';return;}
   if(uploadedURL)URL.revokeObjectURL(uploadedURL);
   uploadedURL=URL.createObjectURL(file);
   play(uploadedURL,'User-provided local clip');
 };
 const preparation=node('p','Preloaded video uses locally prepared MP4 files. If a recording is unavailable, run the free media preparation script; original source links remain available.',cam);
 preparation.className='sub';
 $('judge-claim-result').textContent=p.claim_status==='demo_claim_submitted'?'Previous demo claim saved: '+p.claim_notes:'';
}
$('judge-load').onclick=async()=>{try{data=await call('judge_demo_dashboard');render();$('judge-claim-result').textContent='';}catch(e){$('judge-connections').textContent='Load failed: '+e.message}};
$('judge-claim').onclick=async()=>{if(!data||!selected){$('judge-claim-result').textContent='Select a demo package first.';return;}try{const x=await call('judge_demo_claim',{case_id:selected,notes:$('judge-notes').value});$('judge-claim-result').textContent='DEMO ONLY: '+x.status+' — '+x.note;data=await call('judge_demo_dashboard');render();}catch(e){$('judge-claim-result').textContent='Not filed: '+e.message}};
})();