#!/usr/bin/env node
// Run: node scripts/verify-ring-guardian-cloudflare-mcp.mjs
// Read-only integration smoke test. No credentials, resource creation, or paid API calls.
import assert from "node:assert/strict";
const BASE = "https://ring-guardian-alexa-mcp.interplanetary-fund.workers.dev";
async function rpc(id,method,params={}) {
  const r=await fetch(BASE+"/mcp",{method:"POST",headers:{"content-type":"application/json","accept":"application/json, text/event-stream","mcp-protocol-version":"2025-11-25"},body:JSON.stringify({jsonrpc:"2.0",id,method,params})});
  assert.equal(r.status,200,method+" returned HTTP "+r.status);
  const data=await r.json();
  assert.equal(data.id,id);
  assert.ok(data.result,JSON.stringify(data));
  return data.result;
}
const health=await (await fetch(BASE+"/health")).json();
assert.equal(health.ok,true);
assert.equal(health.mode,"fictional-demo-only");
assert.equal(health.ring_connected,false);
assert.equal(health.alexa_plus_registered,false);
const init=await rpc(1,"initialize",{protocolVersion:"2025-11-25",capabilities:{},clientInfo:{name:"hackathon-smoke-test",version:"1.0.0"}});
assert.equal(init.protocolVersion,"2025-11-25");
const tools=await rpc(2,"tools/list");
assert.deepEqual(tools.tools.map(t=>t.name).sort(),["get_investigation_status","get_package_timeline","get_simulated_evidence","list_demo_packages"].sort());
const response=await rpc(3,"tools/call",{name:"list_demo_packages",arguments:{}});
const packages=JSON.parse(response.content[0].text);
assert.equal(packages.length,5);
for (const p of packages) {
 assert.equal(p.simulation,true);
 for(const tool of ["get_package_timeline","get_simulated_evidence","get_investigation_status"]){
  const result=await rpc(10+packages.indexOf(p)*3+["get_package_timeline","get_simulated_evidence","get_investigation_status"].indexOf(tool),"tools/call",{name:tool,arguments:{package_id:p.package_id}});
  assert.equal(result.isError,false);
  const payload=JSON.parse(result.content[0].text);
  assert.equal(payload.package_id,p.package_id);
 }
}
console.log("PASS: MCP initialize, tool discovery and all 5 fictional package scenarios (15 detail calls)");
console.log("NOT VERIFIED: Alexa+ registration, official Ring APIs, user authentication, camera footage, production data.");
