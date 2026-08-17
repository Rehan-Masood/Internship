let requestChart;
let responseChart;

let selectedDays = 30;

const fmt = n => new Intl.NumberFormat().format(n);


function stat(
  label,
  value,
  icon,
  trend = "Actual backend value"
) {
  return `
    <div class="stat">
      <div class="stat-top">
        <span>${label}</span>
        <span class="stat-icon">${icon}</span>
      </div>

      <div class="stat-value">${value}</div>

      <div class="trend">
        ✓ ${trend}
      </div>
    </div>
  `;
}


function statusClass(s) {
  s = (s || "").toLowerCase();

  return s.includes("fail") ||
    s.includes("unhealthy")
    ? "bad"
    : s.includes("warn")
    ? "warn"
    : s.includes("not") ||
      s.includes("unavailable")
    ? "neutral"
    : "";
}


/* =========================================================
   DATE RANGE FILTER
   ========================================================= */

function ensureDashboardDateFilter() {
  const pageHead = document.querySelector(".page-head");

  if (!pageHead) {
    return null;
  }

  const headActions =
    pageHead.querySelector(".head-actions");

  if (!headActions) {
    return null;
  }

  let select = document.getElementById(
    "dashboardDateFilter"
  );

  if (select) {
    return select;
  }

  select = document.createElement("select");

  select.id = "dashboardDateFilter";
  select.className = "select dashboard-date-filter";
  select.setAttribute(
    "aria-label",
    "Dashboard date range"
  );

  select.innerHTML = `
    <option value="7">Last 7 Days</option>
    <option value="30" selected>Last 30 Days</option>
    <option value="90">Last 90 Days</option>
  `;

  /*
 * Put the functional date filter immediately
 * before the Refresh button.
 */
const refreshButton = headActions.querySelector(
  'button[onclick="loadDashboard(true)"]'
);

if (refreshButton) {
  headActions.insertBefore(select, refreshButton);
} else {
  headActions.appendChild(select);
}
  select.addEventListener("change", () => {
    selectedDays = Number(select.value) || 30;

    loadDashboard(true);
  });

  return select;
}


function initializeDashboardFilter() {
  const filter = ensureDashboardDateFilter();

  if (filter) {
    filter.value = String(selectedDays);
  }
}


/* =========================================================
   DASHBOARD LOADING
   ========================================================= */

async function loadDashboard(showToast = false) {
  try {
    initializeDashboardFilter();

    const url =
      `/api/dashboard?days=${encodeURIComponent(selectedDays)}`;

    const d = await api(url);

    const m = d.metrics;

    document.getElementById("stats").innerHTML = [
      stat(
        "Total Requests",
        fmt(m.total_requests),
        "⌁"
      ),

      stat(
        "Avg Response Time",
        `${m.avg_response_ms}ms`,
        "◷"
      ),

      stat(
        "Uptime",
        formatUptime(d.health.uptime_seconds),
        "♢"
      ),

      stat(
        "Deployments",
        fmt(m.deployments),
        "🚀"
      ),

      stat(
        "Failed Builds",
        fmt(m.failed_builds),
        "⚠"
      )
    ].join("");


    document.getElementById(
      "avgResponse"
    ).textContent = `${m.avg_response_ms}ms`;


    renderRequestChart(m.history);

    renderResponseChart(m);


    /* -----------------------------------------------------
       Container Summary
       ----------------------------------------------------- */

    document.getElementById(
      "containerSummary"
    ).innerHTML = d.containers.available

      ? (
          d.containers.items.length

            ? d.containers.items
                .slice(0, 6)
                .map(c => `
                  <div class="list-row">
                    <span>${escapeHtml(c.name)}</span>

                    <span class="status ${statusClass(c.status)}">
                      ${escapeHtml(c.status)}
                    </span>
                  </div>
                `)
                .join("")

            : `
              <div class="empty">
                No containers found.
              </div>
            `
        )

      : `
          <div class="list-row">
            <span>Docker</span>
            <span class="status neutral">
              Unavailable
            </span>
          </div>
        `;


    /* -----------------------------------------------------
       System Status
       ----------------------------------------------------- */

    document.getElementById(
      "systemStatus"
    ).innerHTML = d.services
      .map(s => `
        <div class="list-row">
          <span>${escapeHtml(s.name)}</span>

          <span class="status ${statusClass(s.status)}">
            ${escapeHtml(s.status)}
          </span>
        </div>
      `)
      .join("");


    /* -----------------------------------------------------
       Deployments
       ----------------------------------------------------- */

    document.getElementById(
      "deployments"
    ).innerHTML = d.deployments.length

      ? d.deployments
          .map(x => `
            <tr>
              <td>${escapeHtml(x.commit_hash)}</td>

              <td>${escapeHtml(x.branch)}</td>

              <td>
                <span class="status ${statusClass(x.status)}">
                  ${escapeHtml(x.status)}
                </span>
              </td>

              <td>${escapeHtml(x.environment)}</td>

              <td>${escapeHtml(x.deployed_at || "—")}</td>

              <td>${x.duration_seconds || 0}s</td>
            </tr>
          `)
          .join("")

      : `
          <tr>
            <td colspan="6">
              No deployment records yet.
            </td>
          </tr>
        `;


    /* -----------------------------------------------------
       Activity
       ----------------------------------------------------- */

    document.getElementById(
      "activity"
    ).innerHTML = d.activities.length

      ? d.activities
          .map(x => `
            <div class="activity-row">
              <div class="activity-icon">
                ●
              </div>

              <div>
                <b>${escapeHtml(x.title)}</b>
                <small>${escapeHtml(x.detail)}</small>
              </div>

              <span class="activity-time">
                ${escapeHtml(x.created_at)}
              </span>
            </div>
          `)
          .join("")

      : `
          <div class="empty">
            No activity yet.
          </div>
        `;


    /* -----------------------------------------------------
       Services
       ----------------------------------------------------- */

    document.getElementById(
      "services"
    ).innerHTML = d.services
      .map(s => `
        <div class="list-row">
          <span>${escapeHtml(s.name)}</span>

          <span class="status ${statusClass(s.status)}">
            ${escapeHtml(s.status)}
          </span>
        </div>
      `)
      .join("");


    /* -----------------------------------------------------
       System Resources
       ----------------------------------------------------- */

    const sys = d.system;

    document.getElementById(
      "resources"
    ).innerHTML = [
      `<div class="resource">${sys.cpu_percent}%</div>`,
      `<div class="resource">${sys.memory_percent}%</div>`,
      `<div class="resource">${sys.disk_percent}%</div>`
    ].join("");


    /* -----------------------------------------------------
       Environment
       ----------------------------------------------------- */

    document.getElementById(
      "environment"
    ).innerHTML = `
      <div class="env-big">
        ${escapeHtml(d.config.environment)}
      </div>

      <div>
        Version
        <b>${escapeHtml(d.config.version)}</b>
      </div>

      <div>
        Health
        <b class="status">
          ● ${escapeHtml(d.health.status)}
        </b>
      </div>
    `;


    /* -----------------------------------------------------
       Pipeline
       ----------------------------------------------------- */

    document.getElementById(
      "pipeline"
    ).innerHTML = [
      "Code Push",
      "Build Image",
      "Run Tests",
      "Deploy",
      "Health Check"
    ]
      .map(x => `
        <div class="pipe">
          <span>${x}</span>
          <b>Backend-driven</b>
        </div>
      `)
      .join("");


    if (showToast) {
      toast(
        `Dashboard refreshed — last ${selectedDays} days`
      );
    }

  } catch (e) {
    toast(e.message);
  }
}


/* =========================================================
   HELPERS
   ========================================================= */

function formatUptime(s) {
  const d = Math.floor(s / 86400);
  const h = Math.floor(
    (s % 86400) / 3600
  );
  const m = Math.floor(
    (s % 3600) / 60
  );

  return d
    ? `${d}d ${h}h`
    : h
    ? `${h}h ${m}m`
    : `${m}m`;
}


function escapeHtml(value) {
  const div = document.createElement("div");

  div.textContent =
    value == null ? "" : String(value);

  return div.innerHTML;
}


/* =========================================================
   REQUEST CHART
   ========================================================= */

function renderRequestChart(history) {
  const ctx = document.getElementById(
    "requestChart"
  );

  if (!ctx) {
    return;
  }

  if (requestChart) {
    requestChart.destroy();
  }

  requestChart = new Chart(ctx, {
    type: "line",

    data: {
      labels: history.map(
        x => x.label
      ),

      datasets: [
        {
          label: "Requests",

          data: history.map(
            x => x.requests
          ),

          borderColor: "#a855f7",
          backgroundColor: "#a855f722",

          fill: true,
          tension: 0.35
        },

        {
          label: "Errors",

          data: history.map(
            x => x.errors
          ),

          borderColor: "#ec4899",
          backgroundColor: "#ec489922",

          fill: true,
          tension: 0.35
        }
      ]
    },

    options: {
      responsive: true,

      plugins: {
        legend: {
          labels: {
            color: "#aeb8d0",
            font: {
              size: 10
            }
          }
        }
      },

      scales: {
        x: {
          ticks: {
            color: "#697696",
            font: {
              size: 9
            }
          },

          grid: {
            display: false
          }
        },

        y: {
          ticks: {
            color: "#697696",
            font: {
              size: 9
            }
          },

          grid: {
            color: "#1b2748"
          }
        }
      }
    }
  });
}


/* =========================================================
   RESPONSE TIME CHART
   ========================================================= */

function renderResponseChart(m) {
  const ctx = document.getElementById(
    "responseChart"
  );

  if (!ctx) {
    return;
  }

  if (responseChart) {
    responseChart.destroy();
  }

  const v = Number(m.avg_response_ms) || 0;

  const data =
    v === 0

      ? [1, 0, 0, 0]

      : [
          v < 100 ? 1 : 0,
          v >= 100 && v < 250 ? 1 : 0,
          v >= 250 && v < 500 ? 1 : 0,
          v >= 500 ? 1 : 0
        ];


  responseChart = new Chart(ctx, {
    type: "doughnut",

    data: {
      labels: [
        "<100ms",
        "100–250ms",
        "250–500ms",
        ">500ms"
      ],

      datasets: [
        {
          data,

          backgroundColor: [
            "#22c55e",
            "#3b82f6",
            "#f97316",
            "#f43f5e"
          ],

          borderWidth: 0
        }
      ]
    },

    options: {
      cutout: "72%",

      plugins: {
        legend: {
          display: false
        }
      }
    }
  });
}


/* =========================================================
   INITIALIZATION
   ========================================================= */

document.addEventListener(
  "DOMContentLoaded",
  () => {
    initializeDashboardFilter();
    loadDashboard(false);

    setInterval(
      () => loadDashboard(false),
      10000
    );
  }
);