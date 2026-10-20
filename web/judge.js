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
 const cam=$('judge-video');cam.replaceChildren();
 node('p','Blink-style camera timeline (SIMULATION). Real third-party footage below is only an illustration, unrelated to these package records.',cam);
 const names=p.issue==='received'?['delivery','received']:p.issue==='possible_theft'?['delivery','theft']:p.issue==='missing_at_dropoff'?['delivery']:['delivery'];
 for(const name of names){const v=data.camera_clips[name];node('p',name.replaceAll('_',' ')+' — '+v.credit+' — '+v.license,cam);link('Watch actual licensed '+name+' footage',v.url,cam);
 if(name==='theft'){const vid=document.createElement('video');vid.controls=true;vid.preload='none';vid.style.width='100%';vid.style.maxHeight='240px';vid.src='/demo-media/porch-pirates-cc-by-3.0.mp4';cam.appendChild(vid);node('p','To enable this playable MP4, run python scripts/prepare_demo_video.py with ffmpeg installed. Otherwise use the credited source link above.',cam);}
 }
 $('judge-claim-result').textContent=p.claim_status==='demo_claim_submitted'?'Previous demo claim saved: '+p.claim_notes:'';
}
$('judge-load').onclick=async()=>{try{data=await call('judge_demo_dashboard');render();$('judge-claim-result').textContent='';}catch(e){$('judge-connections').textContent='Load failed: '+e.message}};
$('judge-claim').onclick=async()=>{if(!data||!selected){$('judge-claim-result').textContent='Select a demo package first.';return;}try{const x=await call('judge_demo_claim',{case_id:selected,notes:$('judge-notes').value});$('judge-claim-result').textContent='DEMO ONLY: '+x.status+' — '+x.note;data=await call('judge_demo_dashboard');render();}catch(e){$('judge-claim-result').textContent='Not filed: '+e.message}};
})();