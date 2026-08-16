function toast(message){
  const el=document.getElementById("toast"); if(!el)return;
  el.textContent=message; el.classList.add("show"); setTimeout(()=>el.classList.remove("show"),3000);
}
function toggleSidebar(){document.getElementById("sidebar")?.classList.toggle("open")}
function toggleTheme(){document.body.classList.toggle("light-mode"); toast("Theme toggled")}
async function api(url, options={}){
  const r=await fetch(url,options);
  const data=await r.json().catch(()=>({}));
  if(!r.ok) throw new Error(data.message||`HTTP ${r.status}`);
  return data;
}
async function healthCheck(){
  try{const d=await api("/api/health"); toast(`Health: ${d.status}`)}catch(e){toast(e.message)}
}
async function triggerCI(){
  try{const d=await api("/cicd/trigger",{method:"POST",headers:{"Content-Type":"application/json"},body:"{}"}); toast(d.message)}catch(e){toast(e.message)}
}
async function deployNow(){
  const branch=prompt("Branch to deploy:","main"); if(!branch)return;
  try{const d=await api("/deployments/deploy",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({branch,environment:"Production",commit:"manual"})}); toast(d.message)}catch(e){toast(e.message)}
}
