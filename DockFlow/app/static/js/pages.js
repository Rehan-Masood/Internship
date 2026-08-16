
async function loadContainers(){
 try{
  const d=await api("/api/containers"), el=document.getElementById("containerPage");
  if(!el)return;
  if(!d.containers.available){
    el.innerHTML=`<div class="empty"><h2>Docker unavailable</h2><p>${d.containers.reason||"Configure Docker access to see live containers."}</p></div>`;
    return;
  }
  el.innerHTML=d.containers.items.length
   ? `<div class="service-cards">${d.containers.items.map(c=>`<div class="service-card"><h3>${escapeHtml(c.name)}</h3><p>Image: ${escapeHtml(c.image)}</p><span class="status ${statusClass(c.status)}">${escapeHtml(c.status)}</span><p>Health: ${escapeHtml(c.health)}</p><p>Ports: ${escapeHtml((c.ports||[]).join(", ")||"none")}</p></div>`).join("")}</div>`
   : `<div class="empty"><h2>No containers found</h2></div>`;
 }catch(e){toast(e.message)}
}
async function loadServices(){
 try{
  const d=await api("/api/services"), el=document.getElementById("servicePage"); if(!el)return;
  el.innerHTML=d.services.map(s=>`<div class="service-card"><h3>${escapeHtml(s.name)}</h3><span class="status ${statusClass(s.status)}">${escapeHtml(s.status)}</span><p>${escapeHtml(s.detail)}</p></div>`).join("");
 }catch(e){toast(e.message)}
}
async function loadCI(){
 try{
  const d=await api("/api/ci-status"),el=document.getElementById("ciPage"); if(!el)return;
  if(!d.available){el.innerHTML=`<div class="empty"><h2>CI/CD unavailable</h2><p>${escapeHtml(d.message||"Configure GitHub integration in .env.")}</p></div>`;return}
  el.innerHTML=`<div class="table-wrap"><table><thead><tr><th>Workflow</th><th>Status</th><th>Conclusion</th><th>Branch</th><th>Commit</th><th>Link</th></tr></thead><tbody>${d.runs.map(x=>`<tr><td>${escapeHtml(x.name)}</td><td>${escapeHtml(x.status)}</td><td>${escapeHtml(x.conclusion||"running")}</td><td>${escapeHtml(x.branch)}</td><td>${escapeHtml(x.sha)}</td><td><a class="tag" href="${x.html_url}" target="_blank" rel="noopener">GitHub ↗</a></td></tr>`).join("")}</tbody></table></div>`;
 }catch(e){toast(e.message)}
}
async function loadDeployments(){
 try{
  const d=await api("/api/deployments"),el=document.getElementById("deploymentPage"); if(!el)return;
  el.innerHTML=d.deployments.length?d.deployments.map(x=>`<tr><td>${escapeHtml(x.commit_hash)}</td><td>${escapeHtml(x.branch)}</td><td><span class="status ${statusClass(x.status)}">${escapeHtml(x.status)}</span></td><td>${escapeHtml(x.environment)}</td><td>${escapeHtml(x.deployed_at||"—")}</td><td>${escapeHtml(x.message)}</td></tr>`).join(""):`<tr><td colspan="6">No deployment records.</td></tr>`;
 }catch(e){toast(e.message)}
}
async function loadLogs(){
 try{
  const d=await api("/api/logs"),el=document.getElementById("logsPage"); if(!el)return;
  el.innerHTML=d.logs.map(x=>`<tr><td>${escapeHtml(x.created_at)}</td><td>${escapeHtml(x.level)}</td><td>${escapeHtml(x.service)}</td><td>${escapeHtml(x.message)}</td></tr>`).join("") || `<tr><td colspan="4">No logs yet.</td></tr>`;
 }catch(e){toast(e.message)}
}
async function loadMonitoring(){
 try{
  const d=await api("/api/monitoring"),el=document.getElementById("monitorPage"); if(!el)return;
  el.innerHTML=[
   ["CPU",`${d.cpu_percent}%`,"⌁"],["Memory",`${d.memory_percent}%`,"▣"],["Disk",`${d.disk_percent}%`,"◫"],
   ["Requests",d.requests,"⌁"],["Errors",d.errors,"⚠"],["Avg Response",`${d.avg_response_ms}ms`,"◷"]
  ].map(x=>`<div class="stat"><div class="stat-top"><span>${x[0]}</span><span class="stat-icon">${x[2]}</span></div><div class="stat-value">${x[1]}</div><div class="trend">Live backend metric</div></div>`).join("");
  const raw=document.getElementById("monitorRaw"); if(raw)raw.textContent=JSON.stringify(d,null,2);
 }catch(e){toast(e.message)}
}
function loadSettings(){
 const el=document.getElementById("settingsPage"); if(!el)return;
 api("/api/dashboard").then(d=>{
  const items=[
   ["Application Environment",d.config.environment],
   ["Version",d.config.version],
   ["Database","Configured"],
   ["Health Endpoint","/health"],
   ["GitHub Actions",d.ci.available?"Configured":"Not Configured"],
   ["Docker",d.containers.available?"Available":"Unavailable"]
  ];
  el.innerHTML=items.map(x=>`<div class="setting"><b>${escapeHtml(x[0])}</b><span class="status ${statusClass(x[1])}">${escapeHtml(x[1])}</span></div>`).join("");
 }).catch(e=>toast(e.message));
}
function statusClass(s){
 s=(s||"").toLowerCase();
 return s.includes("fail")||s.includes("unhealthy")?"bad":
        s.includes("warn")?"warn":
        s.includes("not")||s.includes("unavailable")?"neutral":"";
}
function escapeHtml(s){
 return String(s).replace(/[&<>"']/g,m=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[m]));
}

// Initial load + live polling for every page.
if(document.getElementById("containerPage")){loadContainers();setInterval(loadContainers,10000);}
if(document.getElementById("servicePage")){loadServices();setInterval(loadServices,10000);}
if(document.getElementById("ciPage")){loadCI();setInterval(loadCI,10000);}
if(document.getElementById("deploymentPage")){loadDeployments();setInterval(loadDeployments,10000);}
if(document.getElementById("logsPage")){loadLogs();setInterval(loadLogs,5000);}
if(document.getElementById("monitorPage")){loadMonitoring();setInterval(loadMonitoring,10000);}
if(document.getElementById("settingsPage")){loadSettings();setInterval(loadSettings,15000);}
