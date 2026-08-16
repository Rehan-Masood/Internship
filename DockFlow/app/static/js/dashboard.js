let requestChart, responseChart;
const fmt=n=>new Intl.NumberFormat().format(n);
function stat(label,value,icon,trend="Actual backend value"){
 return `<div class="stat"><div class="stat-top"><span>${label}</span><span class="stat-icon">${icon}</span></div><div class="stat-value">${value}</div><div class="trend">✓ ${trend}</div></div>`;
}
function statusClass(s){s=(s||"").toLowerCase(); return s.includes("fail")||s.includes("unhealthy")?"bad":s.includes("warn")?"warn":s.includes("not")||s.includes("unavailable")?"neutral":""}
async function loadDashboard(showToast=false){
 try{
  const d=await api("/api/dashboard"), m=d.metrics;
  document.getElementById("stats").innerHTML=[
   stat("Total Requests",fmt(m.total_requests),"⌁"),
   stat("Avg Response Time",`${m.avg_response_ms}ms`,"◷"),
   stat("Uptime",formatUptime(d.health.uptime_seconds),"♢"),
   stat("Deployments",fmt(m.deployments),"🚀"),
   stat("Failed Builds",fmt(m.failed_builds),"⚠")
  ].join("");
  document.getElementById("avgResponse").textContent=`${m.avg_response_ms}ms`;
  renderRequestChart(m.history); renderResponseChart(m);
  document.getElementById("containerSummary").innerHTML=d.containers.available
   ? (d.containers.items.length?d.containers.items.slice(0,6).map(c=>`<div class="list-row"><span>${c.name}</span><span class="status ${statusClass(c.status)}">${c.status}</span></div>`).join(""):`<div class="empty">No containers found.</div>`)
   : `<div class="list-row"><span>Docker</span><span class="status neutral">Unavailable</span></div>`;
  document.getElementById("systemStatus").innerHTML=d.services.map(s=>`<div class="list-row"><span>${s.name}</span><span class="status ${statusClass(s.status)}">${s.status}</span></div>`).join("");
  document.getElementById("deployments").innerHTML=d.deployments.length?d.deployments.map(x=>`<tr><td>${x.commit_hash}</td><td>${x.branch}</td><td><span class="status ${statusClass(x.status)}">${x.status}</span></td><td>${x.environment}</td><td>${x.deployed_at||"—"}</td><td>${x.duration_seconds||0}s</td></tr>`).join(""):`<tr><td colspan="6">No deployment records yet.</td></tr>`;
  document.getElementById("activity").innerHTML=d.activities.length?d.activities.map(x=>`<div class="activity-row"><div class="activity-icon">●</div><div><b>${x.title}</b><small>${x.detail}</small></div><span class="activity-time">${x.created_at}</span></div>`).join(""):`<div class="empty">No activity yet.</div>`;
  document.getElementById("services").innerHTML=d.services.map(s=>`<div class="list-row"><span>${s.name}</span><span class="status ${statusClass(s.status)}">${s.status}</span></div>`).join("");
  const sys=d.system;
  document.getElementById("resources").innerHTML=[
   `<div class="resource">${sys.cpu_percent}%</div>`,
   `<div class="resource">${sys.memory_percent}%</div>`,
   `<div class="resource">${sys.disk_percent}%</div>`
  ].join("");
  document.getElementById("environment").innerHTML=`<div class="env-big">${d.config.environment}</div><div>Version <b>${d.config.version}</b></div><div>Health <b class="status">● ${d.health.status}</b></div>`;
  document.getElementById("pipeline").innerHTML=["Code Push","Build Image","Run Tests","Deploy","Health Check"].map(x=>`<div class="pipe"><span>${x}</span><b>Backend-driven</b></div>`).join("");
  if(showToast)toast("Dashboard refreshed from live APIs");
 }catch(e){toast(e.message)}
}
function formatUptime(s){const d=Math.floor(s/86400),h=Math.floor(s%86400/3600),m=Math.floor(s%3600/60);return d?`${d}d ${h}h`:h?`${h}h ${m}m`:`${m}m`}
function renderRequestChart(history){
 const ctx=document.getElementById("requestChart"); if(!ctx)return;
 if(requestChart)requestChart.destroy();
 requestChart=new Chart(ctx,{type:"line",data:{labels:history.map(x=>x.label),datasets:[
  {label:"Requests",data:history.map(x=>x.requests),borderColor:"#a855f7",backgroundColor:"#a855f722",fill:true,tension:.35},
  {label:"Errors",data:history.map(x=>x.errors),borderColor:"#ec4899",backgroundColor:"#ec489922",fill:true,tension:.35}
 ]},options:{responsive:true,plugins:{legend:{labels:{color:"#aeb8d0",font:{size:10}}}},scales:{x:{ticks:{color:"#697696",font:{size:9}},grid:{display:false}},y:{ticks:{color:"#697696",font:{size:9}},grid:{color:"#1b2748"}}}}});
}
function renderResponseChart(m){
 const ctx=document.getElementById("responseChart"); if(!ctx)return;
 if(responseChart)responseChart.destroy();
 const v=m.avg_response_ms;
 const data=v===0?[1,0,0,0]:[v<100?1:0,v>=100&&v<250?1:0,v>=250&&v<500?1:0,v>=500?1:0];
 responseChart=new Chart(ctx,{type:"doughnut",data:{labels:["<100ms","100–250ms","250–500ms",">500ms"],datasets:[{data,backgroundColor:["#22c55e","#3b82f6","#f97316","#f43f5e"],borderWidth:0}]},options:{cutout:"72%",plugins:{legend:{display:false}}}});
}
loadDashboard();
setInterval(()=>loadDashboard(false),10000);
