async function loadContainers(){
 try{
  const d=await api("/api/containers"), el=document.getElementById("containerPage");
  if(!el)return;

  if(!d.containers.available){
    el.innerHTML=`<div class="empty"><h2>Docker unavailable</h2><p>${escapeHtml(d.containers.reason||"Configure Docker access to see live containers.")}</p></div>`;
    return;
  }

  el.innerHTML=d.containers.items.length
   ? `<div class="service-cards">${d.containers.items.map(c=>`
      <div class="service-card">
        <h3>${escapeHtml(c.name)}</h3>
        <p>Image: ${escapeHtml(c.image)}</p>
        <span class="status ${statusClass(c.status)}">${escapeHtml(c.status)}</span>
        <p>Health: ${escapeHtml(c.health)}</p>
        <p>Ports: ${escapeHtml((c.ports||[]).join(", ")||"none")}</p>
      </div>
   `).join("")}</div>`
   : `<div class="empty"><h2>No containers found</h2></div>`;

 }catch(e){
  toast(e.message);
 }
}


async function loadServices(){
 try{
  const d=await api("/api/services"),
        el=document.getElementById("servicePage");

  if(!el)return;

  el.innerHTML=d.services.map(s=>`
    <div class="service-card">
      <h3>${escapeHtml(s.name)}</h3>
      <span class="status ${statusClass(s.status)}">${escapeHtml(s.status)}</span>
      <p>${escapeHtml(s.detail)}</p>
    </div>
  `).join("");

 }catch(e){
  toast(e.message);
 }
}


async function loadCI(){
 try{
  const d=await api("/api/ci-status"),
        el=document.getElementById("ciPage");

  if(!el)return;

  if(!d.available){
    el.innerHTML=`
      <div class="empty">
        <h2>CI/CD unavailable</h2>
        <p>${escapeHtml(d.message||"Configure GitHub integration in .env.")}</p>
      </div>
    `;
    return;
  }

  el.innerHTML=`
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Workflow</th>
            <th>Status</th>
            <th>Conclusion</th>
            <th>Branch</th>
            <th>Commit</th>
            <th>Link</th>
          </tr>
        </thead>

        <tbody>
          ${d.runs.map(x=>`
            <tr>
              <td>${escapeHtml(x.name)}</td>
              <td>${escapeHtml(x.status)}</td>
              <td>${escapeHtml(x.conclusion||"running")}</td>
              <td>${escapeHtml(x.branch)}</td>
              <td>${escapeHtml(x.sha)}</td>
              <td>
                <a class="tag"
                   href="${escapeHtml(x.html_url)}"
                   target="_blank"
                   rel="noopener">
                  GitHub ↗
                </a>
              </td>
            </tr>
          `).join("")}
        </tbody>
      </table>
    </div>
  `;

 }catch(e){
  toast(e.message);
 }
}


/* =========================================================
   DEPLOYMENT PAGE
   ========================================================= */

async function loadDeployments(){

 try{

  const d=await api("/api/deployments"),
        el=document.getElementById("deploymentPage");

  if(!el)return;

  const deployments=d.deployments || [];

  const countEl=document.getElementById("deploymentCount");

  if(countEl){
    countEl.textContent=deployments.length;
  }

  el.innerHTML=deployments.length
   ? deployments.map(x=>`
      <tr>
        <td>${escapeHtml(x.commit_hash)}</td>

        <td>
          <span class="deployment-branch-tag">
            ${escapeHtml(x.branch)}
          </span>
        </td>

        <td>
          <span class="status ${statusClass(x.status)}">
            ${escapeHtml(x.status)}
          </span>
        </td>

        <td>
          ${escapeHtml(x.environment)}
        </td>

        <td>
          ${escapeHtml(x.deployed_at||"—")}
        </td>

        <td>
          ${escapeHtml(x.message)}
        </td>
      </tr>
    `).join("")
   : `
      <tr>
        <td colspan="6" class="deployment-empty-cell">

          <div class="deployment-empty-state">

            <div class="deployment-empty-icon">
              🚀
            </div>

            <strong>No deployment records</strong>

            <span>
              Deployment records will appear here after a configured
              integration accepts a deployment request.
            </span>

          </div>

        </td>
      </tr>
    `;

  await loadDeploymentConfiguration();

 }catch(e){

  toast(e.message);

 }

}


/*
 * Reads the existing dashboard configuration.
 *
 * This does NOT modify your configuration.
 * It only tells the Deployment page what is already configured.
 */
async function loadDeploymentConfiguration(){

 try{

  const d=await api("/api/dashboard");

  const provider=d.config?.deployment_provider || "";
  const webhookConfigured=Boolean(d.config?.deployment_webhook_configured);

  const providerName=provider
    ? formatProviderName(provider)
    : "Not Configured";

  const providerEl=document.getElementById("deploymentProvider");
  const providerNameEl=document.getElementById("deploymentProviderName");
  const providerStatusEl=document.getElementById("deploymentProviderStatus");
  const descriptionEl=document.getElementById("deploymentProviderDescription");
  const integrationEl=document.getElementById("deploymentIntegration");
  const modalBadge=document.getElementById("deploymentModalProviderBadge");
  const configNotice=document.getElementById("deploymentConfigurationNotice");
  const modalWarning=document.getElementById("deploymentModalWarning");

  if(providerEl){
    providerEl.textContent=providerName;
  }

  if(providerNameEl){
    providerNameEl.textContent=providerName;
  }

  if(provider){

    if(providerStatusEl){
      providerStatusEl.textContent="Configured";
      providerStatusEl.className="deployment-provider-badge success";
    }

    if(modalBadge){
      modalBadge.textContent="Configured";
      modalBadge.className="deployment-provider-badge success";
    }

    if(descriptionEl){
      descriptionEl.textContent=webhookConfigured
        ? "Deployment webhook is configured and ready."
        : "Provider is selected, but the deployment webhook is not configured.";
    }

    if(integrationEl){
      integrationEl.textContent=webhookConfigured
        ? "Ready"
        : "Incomplete";
    }

    if(configNotice){

      if(webhookConfigured){
        configNotice.style.display="none";
      }else{
        configNotice.style.display="flex";
      }

    }

    if(modalWarning){

      if(webhookConfigured){
        modalWarning.style.display="none";
      }else{
        modalWarning.style.display="flex";
      }

    }

  }else{

    if(providerStatusEl){
      providerStatusEl.textContent="Not Configured";
      providerStatusEl.className="deployment-provider-badge neutral";
    }

    if(modalBadge){
      modalBadge.textContent="Not Configured";
      modalBadge.className="deployment-provider-badge neutral";
    }

    if(descriptionEl){
      descriptionEl.textContent=
        "No deployment provider is currently connected to DockFlow.";
    }

    if(integrationEl){
      integrationEl.textContent="Not Configured";
    }

    if(configNotice){
      configNotice.style.display="flex";
    }

    if(modalWarning){
      modalWarning.style.display="flex";
    }

  }

 }catch(e){

  console.warn("Deployment configuration check failed:",e);

 }

}


/*
 * Premium deployment modal
 */
async function deployNow(){

 const modal=document.getElementById("deploymentModal");

 if(!modal){
   return;
 }

 const branchInput=document.getElementById("deploymentBranchInput");
 const environmentInput=document.getElementById("deploymentEnvironmentInput");
 const commitInput=document.getElementById("deploymentCommitInput");

 if(branchInput){
   branchInput.value="main";
 }

 if(environmentInput){
   environmentInput.value="Production";
 }

 if(commitInput){
   commitInput.value="manual";
 }

 updateDeploymentSummary();

 modal.classList.add("open");
 modal.setAttribute("aria-hidden","false");

 document.body.classList.add("deployment-modal-open");

 await loadDeploymentConfiguration();

 setTimeout(()=>{
   branchInput?.focus();
 },150);

}


/*
 * Close modal
 */
function closeDeploymentModal(){

 const modal=document.getElementById("deploymentModal");

 if(!modal){
   return;
 }

 modal.classList.remove("open");
 modal.setAttribute("aria-hidden","true");

 document.body.classList.remove("deployment-modal-open");

 resetDeploymentSubmitButton();

}


/*
 * Submit deployment
 */
async function submitDeployment(event){

 event.preventDefault();

 const branchInput=document.getElementById("deploymentBranchInput");
 const environmentInput=document.getElementById("deploymentEnvironmentInput");
 const commitInput=document.getElementById("deploymentCommitInput");

 const branch=(branchInput?.value||"").trim();
 const environment=(environmentInput?.value||"Production").trim();
 const commit=(commitInput?.value||"manual").trim();

 if(!branch){

   branchInput?.focus();

   toast("Please enter a branch.");

   return;

 }

 updateDeploymentSummary();

 setDeploymentSubmitLoading(true);

 try{

   const d=await api(
     "/deployments/deploy",
     {
       method:"POST",
       headers:{
         "Content-Type":"application/json"
       },
       body:JSON.stringify({
         branch,
         environment,
         commit
       })
     }
   );

   toast(d.message || "Deployment request processed.");

   closeDeploymentModal();

   await loadDeployments();

 }catch(e){

   toast(e.message);

 }finally{

   resetDeploymentSubmitButton();

 }

}


/*
 * Live summary inside modal
 */
function updateDeploymentSummary(){

 const branch=document.getElementById("deploymentBranchInput")?.value || "main";
 const environment=document.getElementById("deploymentEnvironmentInput")?.value || "Production";
 const commit=document.getElementById("deploymentCommitInput")?.value || "manual";

 const summaryBranch=document.getElementById("summaryBranch");
 const summaryEnvironment=document.getElementById("summaryEnvironment");
 const summaryCommit=document.getElementById("summaryCommit");

 if(summaryBranch){
   summaryBranch.textContent=branch;
 }

 if(summaryEnvironment){
   summaryEnvironment.textContent=environment;
 }

 if(summaryCommit){
   summaryCommit.textContent=commit;
 }

 const topBranch=document.getElementById("deploymentBranch");

 if(topBranch){
   topBranch.textContent=branch;
 }

 const topEnvironment=document.getElementById("deploymentEnvironment");

 if(topEnvironment){
   topEnvironment.textContent=environment;
 }

 const targetBranch=document.getElementById("deploymentTargetBranch");

 if(targetBranch){
   targetBranch.textContent=branch;
 }

 const targetEnvironment=document.getElementById("deploymentTarget");

 if(targetEnvironment){
   targetEnvironment.textContent=environment;
 }

}


/*
 * Loading state
 */
function setDeploymentSubmitLoading(loading){

 const button=document.getElementById("deploymentSubmitButton");
 const icon=document.getElementById("deploymentSubmitIcon");
 const text=document.getElementById("deploymentSubmitText");

 if(!button)return;

 button.disabled=loading;

 if(loading){

   button.classList.add("loading");

   if(icon){
     icon.textContent="◌";
   }

   if(text){
     text.textContent="Starting Deployment...";
   }

 }else{

   button.classList.remove("loading");

   if(icon){
     icon.textContent="🚀";
   }

   if(text){
     text.textContent="Start Deployment";
   }

 }

}


function resetDeploymentSubmitButton(){

 setDeploymentSubmitLoading(false);

}


/*
 * Provider name formatting
 */
function formatProviderName(provider){

 const value=String(provider||"").trim();

 if(!value){
   return "Not Configured";
 }

 return value
   .replace(/[-_]/g," ")
   .replace(/\b\w/g,char=>char.toUpperCase());

}


/*
 * Close modal using Escape
 */
document.addEventListener("keydown",event=>{

 if(event.key==="Escape"){

   const modal=document.getElementById("deploymentModal");

   if(modal?.classList.contains("open")){
     closeDeploymentModal();
   }

 }

});


/*
 * Update summary while typing/selecting.
 */
document.addEventListener("input",event=>{

 if(
   event.target?.id==="deploymentBranchInput" ||
   event.target?.id==="deploymentCommitInput"
 ){
   updateDeploymentSummary();
 }

});


document.addEventListener("change",event=>{

 if(event.target?.id==="deploymentEnvironmentInput"){
   updateDeploymentSummary();
 }

});


async function loadLogs(){

 try{

  const d=await api("/api/logs"),
        el=document.getElementById("logsPage");

  if(!el)return;

  el.innerHTML=d.logs.map(x=>`
    <tr>
      <td>${escapeHtml(x.created_at)}</td>
      <td>${escapeHtml(x.level)}</td>
      <td>${escapeHtml(x.service)}</td>
      <td>${escapeHtml(x.message)}</td>
    </tr>
  `).join("") || `
    <tr>
      <td colspan="4">No logs yet.</td>
    </tr>
  `;

 }catch(e){
  toast(e.message);
 }

}


async function loadMonitoring(){

 try{

  const d=await api("/api/monitoring"),
        el=document.getElementById("monitorPage");

  if(!el)return;

  el.innerHTML=[
   ["CPU",`${d.cpu_percent}%`,"⌁"],
   ["Memory",`${d.memory_percent}%`,"▣"],
   ["Disk",`${d.disk_percent}%`,"◫"],
   ["Requests",d.requests,"⌁"],
   ["Errors",d.errors,"⚠"],
   ["Avg Response",`${d.avg_response_ms}ms`,"◷"]
  ].map(x=>`
    <div class="stat">
      <div class="stat-top">
        <span>${x[0]}</span>
        <span class="stat-icon">${x[2]}</span>
      </div>

      <div class="stat-value">
        ${x[1]}
      </div>

      <div class="trend">
        Live backend metric
      </div>
    </div>
  `).join("");

  const raw=document.getElementById("monitorRaw");

  if(raw){
    raw.textContent=JSON.stringify(d,null,2);
  }

 }catch(e){
  toast(e.message);
 }

}


function loadSettings(){

 const el=document.getElementById("settingsPage");

 if(!el)return;

 api("/api/dashboard").then(d=>{

  const items=[
   ["Application Environment",d.config.environment],
   ["Version",d.config.version],
   ["Database","Configured"],
   ["Health Endpoint","/health"],
   ["GitHub Actions",d.ci.available?"Configured":"Not Configured"],
   ["Docker",d.containers.available?"Available":"Unavailable"]
  ];

  el.innerHTML=items.map(x=>`
    <div class="setting">
      <b>${escapeHtml(x[0])}</b>
      <span class="status ${statusClass(x[1])}">
        ${escapeHtml(x[1])}
      </span>
    </div>
  `).join("");

 }).catch(e=>toast(e.message));

}


function statusClass(s){

 s=(s||"").toLowerCase();

 return s.includes("fail")||s.includes("unhealthy")
   ?"bad"
   :s.includes("warn")
   ?"warn"
   :s.includes("not")||s.includes("unavailable")
   ?"neutral"
   :"";

}


function escapeHtml(s){

 return String(s).replace(
   /[&<>"']/g,
   m=>({
     "&":"&amp;",
     "<":"&lt;",
     ">":"&gt;",
     '"':"&quot;",
     "'":"&#039;"
   }[m])
 );

}


/* =========================================================
   INITIAL LOAD + LIVE POLLING
   ========================================================= */

if(document.getElementById("containerPage")){
 loadContainers();
 setInterval(loadContainers,10000);
}

if(document.getElementById("servicePage")){
 loadServices();
 setInterval(loadServices,10000);
}

if(document.getElementById("ciPage")){
 loadCI();
 setInterval(loadCI,10000);
}

if(document.getElementById("deploymentPage")){
 loadDeployments();
 setInterval(loadDeployments,10000);
}

if(document.getElementById("logsPage")){
 loadLogs();
 setInterval(loadLogs,5000);
}

if(document.getElementById("monitorPage")){
 loadMonitoring();
 setInterval(loadMonitoring,10000);
}

if(document.getElementById("settingsPage")){
 loadSettings();
 setInterval(loadSettings,15000);
}