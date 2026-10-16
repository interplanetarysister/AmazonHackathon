'use strict';
/* Version 2: local-first import and evidence UX. This does not authenticate
 * consumer Amazon/Blink/Gmail accounts or run an unattended push daemon. */
(() => {
  const E = id => document.getElementById(id);
  const message = text => { E('v2-message').textContent = text; };
  const rows = [];
  let selectedClip = null;
  let lastUPSStatus = null;

  function line(root, text, tag='p', className='sub') {
    const node = document.createElement(tag);
    node.textContent = text;
    if (className) node.className = className;
    root.append(node);
    return node;
  }
  function externalLink(root, url, title) {
    if (!/^https:\/\/[a-z0-9.-]+\//i.test(url)) return;
    const a = document.createElement('a');
    a.href = url;
    a.rel = 'noopener noreferrer';
    a.target = '_blank';
    a.textContent = title + ' ↗';
    root.append(a);
    return a;
  }
  function decorateResolution(root, result) {
    const first = result.first_action || {};
    const area = document.createElement('div');
    area.className = 'notice';
    area.style.marginTop = '10px';
    line(area, 'First action: ' + (first.name || 'Check the most recent carrier update'), 'strong', '');
    line(area, first.explanation || 'Carrier update not yet available.');
    if (first.tracking_url) externalLink(area, first.tracking_url, 'Check tracking update now');
    const contact = result.carrier_contact || {};
    if (contact.phone && /^\d{10,15}$/.test(contact.phone)) {
      const a = document.createElement('a');
      a.href = 'tel:+' + contact.phone;
      a.textContent = 'Call ' + result.current_claim?.replaceAll('_',' ') + ' carrier: ' + contact.display_phone;
      a.style.display = 'block';
      area.append(a);
    }
    if (contact.support_url) externalLink(area, contact.support_url, 'Open official customer support');
    line(area, result.evidence_prompt || 'Would you like to include footage in the report?');
    const clipButton = document.createElement('button');
    clipButton.type = 'button';
    clipButton.className = 'secondary';
    clipButton.textContent = 'Choose footage for evidence ZIP';
    clipButton.onclick = () => { E('v2-camera-file').scrollIntoView({behavior:'smooth',block:'center'});E('v2-camera-file').focus(); };
    area.append(clipButton);
    line(area, 'This draft and these links do not submit a report or place a phone call.');
    root.append(area);
  }
  async function capabilities() {
    try {
      const r = await tool('get_connection_capabilities');
      const root = E('provider-status');
      root.replaceChildren();
      for (const p of r.providers) {
        const el = document.createElement('p');
        el.style.margin = '5px 0';
        const name = document.createElement('strong');
        name.textContent = p.name + ': ';
        el.append(name, document.createTextNode(p.state.replaceAll('_',' ') + ' · ' + p.feature));
        root.append(el);
      }
    } catch (error) {
      E('provider-status').textContent = 'Connection status unavailable: ' + (error.message || String(error));
    }
  }
  async function readSmallFile(input, max) {
    const file = input.files?.[0];
    if (!file) return null;
    if (file.size > max) throw Error('Selected file is too large for a local preview.');
    return file.text();
  }
  function applyPreview(fields, direction=null) {
    for (const attr of ['label','carrier','eta']) {
      if (fields[attr]) E(attr).value = fields[attr];
    }
    if (direction) E('direction').value = direction;
    E('label').focus();
    E('extract-note').textContent = 'Review every detail before saving. This is imported text, not verified carrier data.';
  }
  E('eml-file').onchange = async () => {
    try {
      const raw = await readSmallFile(E('eml-file'), 16000);
      if (!raw) return;
      const data = await tool('parse_email_notice', {text:raw});
      applyPreview(data.fields || {});
      message('Email fields previewed. No Gmail account was connected or scanned.');
    } catch (e) { message('Email preview failed: '+e.message); }
  };
  function sanitizedShippingCSV(raw) {
    // Parse quoted CSV locally; remove name, address, email, phone and full
    // tracking numbers BEFORE anything is sent to the localhost MCP server.
    const records=[];let record=[],field='',quoted=false;
    for(let i=0;i<raw.length;i++){
      const c=raw[i];
      if(c==='"'){if(quoted&&raw[i+1]==='"'){field+='"';i++;}else quoted=!quoted;}
      else if(c===','&&!quoted){record.push(field);field='';}
      else if((c==='\n'||c==='\r')&&!quoted){
        record.push(field);field='';if(record.some(x=>x.trim()))records.push(record);record=[];
        if(c==='\r'&&raw[i+1]==='\n')i++;
      }else field+=c;
    }
    if(quoted)throw Error('CSV contains an unfinished quoted field.');
    record.push(field);if(record.some(x=>x.trim()))records.push(record);
    if(!records.length)throw Error('CSV has no rows.');
    const allowed=new Set(['package','name','item','product','order_name','product_title',
      'carrier','shipping_carrier','shipping_company','courier','eta','expected_delivery',
      'estimated_delivery','delivery_date','tracking_hint','tracking_suffix','tracking_last4']);
    // "name" refers only to package name; sender/recipient names are not included.
    const headers=records[0].map(h=>h.trim().toLowerCase().replaceAll(' ','_'));
    const indices=headers.map((h,i)=>allowed.has(h)?i:-1).filter(i=>i>=0);
    if(!indices.length)throw Error('No package/carrier/ETA columns recognized.');
    const clean=(value)=>'"'+String(value||'').slice(0,120).replaceAll('"','""')+'"';
    return [indices.map(i=>clean(headers[i])).join(','),
      ...records.slice(1,21).map(row=>indices.map(i=>clean(row[i])).join(','))].join('\n');
  }
  E('csv-file').onchange = async () => {
    try {
      rows.length = 0;
      const raw = await readSmallFile(E('csv-file'), 28000);
      if (!raw) return;
      const data = await tool('preview_shipping_export', {text:sanitizedShippingCSV(raw)});
      rows.push(...data.rows);
      const chooser = E('csv-choose');
      chooser.replaceChildren();
      if (!rows.length) {
        chooser.disabled = true;
        line(E('provider-status'), 'No recognized CSV shipments were found.');
        return;
      }
      for (let i=0; i<rows.length; i++) {
        const option = document.createElement('option');
        option.value = String(i);
        option.textContent = (rows[i].label || 'Package '+(i+1))+' · '+(rows[i].carrier||'Carrier unknown');
        chooser.append(option);
      }
      chooser.disabled = false;
      applyPreview(rows[0], 'outgoing');
      message(rows.length + ' outgoing shipping records available for review; nothing imported until saved.');
    } catch (e) { message('CSV preview failed: '+e.message); }
  };
  E('csv-choose').onchange = () => {
    const row = rows[Number(E('csv-choose').value)];
    if (row) applyPreview(row, 'outgoing');
  };
  function trackingInput() {
    const number = E('ups-number').value.trim().toUpperCase();
    if (!/^[A-Z0-9]{7,34}$/.test(number)) throw Error('Enter a valid 7–34 character UPS tracking number.');
    return number;
  }
  E('ups-check').onclick = async () => {
    try {
      const r = await tool('check_ups_tracking',{tracking_number:trackingInput()});
      lastUPSStatus = r;
      E('ups-status').textContent =
        'UPS ' + r.environment + ': ' + r.status_description +
        ' · event time ' + (r.carrier_event_at||'not supplied') +
        '. This is the carrier report, not recipient confirmation.';
    } catch (e) { lastUPSStatus=null;E('ups-status').textContent='UPS check unavailable: '+e.message; }
  };
  E('ups-sync').onclick = async () => {
    if (!activeId) { E('ups-status').textContent='Choose a saved UPS package first.';return; }
    const current = list.find(d=>d.id===activeId);
    if (!current || !current.carrier.toLowerCase().includes('ups')) {
      E('ups-status').textContent='Choose a UPS delivery to save a UPS response.';return;
    }
    try {
      const before = current.carrier_status;
      const result = await tool('sync_ups_tracking',{
        delivery_id:activeId, tracking_number:trackingInput(), idempotency_key:key()
      });
      setProof(result);
      await refresh();
      await loadActions();
      E('ups-status').textContent='Official UPS scan checked and saved in the local timeline. Source is marked as sandbox or production.';
      const after = list.find(d=>d.id===activeId)?.carrier_status;
      if (before !== after) await notifyChange(activeId, 'UPS status changed: '+(after||'unknown'));
    } catch (e) { E('ups-status').textContent='UPS update failed: '+e.message; }
  };

  async function selectionChanged(delivery) {
    try {
      const response = await tool('get_notification_preferences');
      const row = response.preferences.find(p=>p.delivery_id===delivery.id);
      E('v2-alert-enabled').checked = Boolean(row?.enabled);
      E('v2-message').textContent = 'Alerts: '+(row?.enabled?'selected for this package':'off for this package')+
        '. Local notifications while the page is open only; background push is not configured.';
    } catch(e) { message('Could not check alert preferences: '+e.message); }
  }
  E('v2-alert-enabled').onchange = async () => {
    if (!activeId) { E('v2-alert-enabled').checked=false; message('Choose a package first.');return; }
    const enabled=E('v2-alert-enabled').checked;
    try {
      const result=await tool('set_notification_preference',{delivery_id:activeId,enabled,idempotency_key:key()});
      setProof(result);
      await loadActions();
      message('Alert preference saved for this package. This demo has no background push server.');
    } catch(e) { E('v2-alert-enabled').checked=!enabled;message('Could not save preference: '+e.message); }
  };
  async function notification(title,body) {
    if (!('Notification' in window) || !window.isSecureContext) {
      message('System notifications require a secure context and browser notification support.');
      return false;
    }
    const permission = Notification.permission==='granted'?'granted':await Notification.requestPermission();
    if (permission!=='granted') { message('Phone notification permission was not granted.');return false; }
    try {
      if ('serviceWorker' in navigator) {
        const worker = await navigator.serviceWorker.register('/notify-sw.js');
        await worker.showNotification(title,{body,tag:'delivery-guardian-test'});
      } else {
        new Notification(title,{body});
      }
      return true;
    }catch(e){message('Notification preview unavailable: '+e.message);return false;}
  }
  async function notifyChange(id, text) {
    const prefs = await tool('get_notification_preferences');
    if (!prefs.preferences.some(p=>p.delivery_id===id && Boolean(p.enabled))) return;
    await notification('Delivery Guardian',text);
  }
  E('v2-alert-test').onclick=async()=>{
    if(!activeId){message('Choose a delivery first.');return;}
    if(!E('v2-alert-enabled').checked){message('Enable alerts for this package before testing.');return;}
    const d=list.find(x=>x.id===activeId);
    if(await notification('Delivery Guardian · test for '+d.label,'This is an intentional preview, not a real carrier alert.'))
      message('Test notification requested. Only updates for this selected package are enabled.');
  };
  E('v2-camera-file').onchange = () => {
    selectedClip = E('v2-camera-file').files?.[0] || null;
    E('v2-include-video').checked=false;
    if(!selectedClip){message('No clip selected.');return;}
    message(selectedClip.name+' selected locally. No footage has been sent to a server.');
  };

  function crc32(bytes) {
    let value=0xffffffff;
    for(const b of bytes){
      value^=b;
      for(let bit=0;bit<8;bit++) value=(value>>>1)^((value&1)?0xedb88320:0);
    }
    return (value^0xffffffff)>>>0;
  }
  function makeZip(entries){
    const local=[], central=[];let offset=0;
    const u16=(dv,at,n)=>dv.setUint16(at,n,true);
    const u32=(dv,at,n)=>dv.setUint32(at,n>>>0,true);
    const enc=new TextEncoder();
    for(const entry of entries){
      const name=enc.encode(entry.name), bytes=entry.bytes, crc=crc32(bytes);
      if(name.length>65000 || bytes.length>25000000)throw Error('Attachment too large');
      const head=new Uint8Array(30), hd=new DataView(head.buffer);
      u32(hd,0,0x04034b50);u16(hd,4,20);u16(hd,6,0x0800);u16(hd,8,0);
      u32(hd,14,crc);u32(hd,18,bytes.length);u32(hd,22,bytes.length);u16(hd,26,name.length);
      local.push(head,name,bytes);
      const cent=new Uint8Array(46), cd=new DataView(cent.buffer);
      u32(cd,0,0x02014b50);u16(cd,4,20);u16(cd,6,20);u16(cd,8,0x0800);
      u32(cd,16,crc);u32(cd,20,bytes.length);u32(cd,24,bytes.length);
      u16(cd,28,name.length);u32(cd,42,offset);
      central.push(cent,name);
      offset+=head.length+name.length+bytes.length;
    }
    const directorySize=central.reduce((n,b)=>n+b.length,0);
    const tail=new Uint8Array(22),dv=new DataView(tail.buffer);
    u32(dv,0,0x06054b50);u16(dv,8,entries.length);u16(dv,10,entries.length);
    u32(dv,12,directorySize);u32(dv,16,offset);
    return new Blob([...local,...central,tail],{type:'application/zip'});
  }
  async function evidenceText(){
    if(!activeId)throw Error('Choose a saved package first.');
    const d=list.find(item=>item.id===activeId);
    const timeline=await tool('get_delivery_timeline',{delivery_id:activeId});
    const lines=[
      'Delivery Guardian v2 - case evidence (review before sharing)',
      'Provider claims are not confirmation a recipient received the package.',
      'Package: '+d.label,'Direction: '+(d.direction||'incoming'),'Carrier: '+d.carrier,
      'Current carrier status: '+d.carrier_status,
      'Person receipt status: '+d.receipt_status,
      'Generated at: '+new Date().toISOString(),'',
      ...timeline.events.flatMap(ev=>[
        'Event: '+ev.event_type,'Source: '+ev.source_type,
        'Claimed/observed time (UTC): '+(ev.claimed_at||'not supplied'),
        'Local-app recorded time (UTC): '+ev.recorded_at,
        'Details: '+ev.details,''
      ]),
      'User-selected camera evidence is separate from verified live Ring/Blink integration.',
      'No complaint has been submitted or support message sent by this app.'
    ];
    return lines.join('\n');
  }
  E('v2-zip').onclick=async()=>{
    try{
      const entries=[{name:'delivery-case.txt',bytes:new TextEncoder().encode(await evidenceText())}];
      if(E('v2-include-video').checked){
        if(!selectedClip)throw Error('Choose your camera clip first.');
        if(selectedClip.size>25000000)throw Error('Choose a clip under 25 MB.');
        if(!/^(video\/mp4|video\/webm|video\/quicktime|image\/jpeg|image\/png)$/.test(selectedClip.type))
          throw Error('Select a supported video or image clip.');
        const ext=selectedClip.type.startsWith('image/')?(selectedClip.type==='image/png'?'.png':'.jpg'):
                    (selectedClip.type==='video/webm'?'.webm':selectedClip.type==='video/quicktime'?'.mov':'.mp4');
        entries.push({name:'user-selected-camera-evidence'+ext,bytes:new Uint8Array(await selectedClip.arrayBuffer())});
      }
      const zip=makeZip(entries),url=URL.createObjectURL(zip),a=document.createElement('a');
      a.href=url;a.download='delivery-guardian-case.zip';document.body.append(a);a.click();a.remove();
      setTimeout(()=>URL.revokeObjectURL(url),3000);
      message('Evidence ZIP saved locally. Review it and confirm whether your carrier accepts ZIP and the original clip type.');
    }catch(e){message('Could not prepare ZIP: '+e.message);}
  };
  window.DGv2={decorateResolution,selectionChanged};
  capabilities();
  if(activeId){
    const selected=list.find(d=>d.id===activeId);
    if(selected)selectionChanged(selected);
  }
})();
