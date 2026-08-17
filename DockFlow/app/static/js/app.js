function toast(message) {
  const el = document.getElementById("toast");
  if (!el) return;

  el.textContent = message;
  el.classList.add("show");

  clearTimeout(window.__dockflowToastTimer);

  window.__dockflowToastTimer = setTimeout(() => {
    el.classList.remove("show");
  }, 3000);
}


function toggleSidebar() {
  document.getElementById("sidebar")?.classList.toggle("open");
}


function toggleTheme() {
  document.body.classList.toggle("light-mode");
  toast("Theme toggled");
}


async function api(url, options = {}) {
  const r = await fetch(url, options);

  const data = await r.json().catch(() => ({}));

  if (!r.ok) {
    throw new Error(data.message || `HTTP ${r.status}`);
  }

  return data;
}


async function healthCheck() {
  try {
    const d = await api("/api/health");
    toast(`Health: ${d.status}`);
  } catch (e) {
    toast(e.message);
  }
}


async function triggerCI() {
  try {
    const d = await api("/cicd/trigger", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: "{}"
    });

    toast(d.message);
  } catch (e) {
    toast(e.message);
  }
}


async function deployNow() {
  const branch = prompt("Branch to deploy:", "main");

  if (!branch) return;

  try {
    const d = await api("/deployments/deploy", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        branch,
        environment: "Production",
        commit: "manual"
      })
    });

    toast(d.message);

    // Refresh notifications after a deployment.
    if (typeof loadNotifications === "function") {
      setTimeout(() => loadNotifications(true), 500);
    }

    // Refresh dashboard data if we are currently on the dashboard.
    if (typeof loadDashboard === "function") {
      setTimeout(() => loadDashboard(false), 700);
    }

  } catch (e) {
    toast(e.message);

    if (typeof loadNotifications === "function") {
      setTimeout(() => loadNotifications(true), 500);
    }
  }
}


/* =========================================================
   DOCKFLOW NOTIFICATIONS
   ========================================================= */

let notificationOpen = false;
let notificationRefreshTimer = null;

const NOTIFICATION_READ_KEY = "dockflow_read_notifications";


function getReadNotificationIds() {
  try {
    const raw = localStorage.getItem(NOTIFICATION_READ_KEY);

    if (!raw) {
      return [];
    }

    const parsed = JSON.parse(raw);

    return Array.isArray(parsed) ? parsed : [];

  } catch (e) {
    return [];
  }
}


function saveReadNotificationIds(ids) {
  try {
    // Keep the localStorage entry small.
    const unique = [...new Set(ids)].slice(-100);

    localStorage.setItem(
      NOTIFICATION_READ_KEY,
      JSON.stringify(unique)
    );

  } catch (e) {
    // Ignore localStorage errors.
  }
}


function markNotificationAsRead(id) {
  if (id === undefined || id === null) {
    return;
  }

  const ids = getReadNotificationIds();

  if (!ids.includes(String(id))) {
    ids.push(String(id));
    saveReadNotificationIds(ids);
  }
}


function markAllNotificationsAsRead() {
  const items = window.__dockflowNotifications || [];

  const ids = items
    .map(item => item.id)
    .filter(id => id !== undefined && id !== null)
    .map(id => String(id));

  saveReadNotificationIds(ids);

  renderNotifications(items);
}


function notificationStatusClass(item) {
  const text = `${item.title || ""} ${item.detail || ""}`.toLowerCase();

  if (
    text.includes("failed") ||
    text.includes("error") ||
    text.includes("unhealthy") ||
    text.includes("cancel")
  ) {
    return "bad";
  }

  if (
    text.includes("warning") ||
    text.includes("warn")
  ) {
    return "warn";
  }

  return "success";
}


function notificationIcon(item) {
  const text = `${item.title || ""} ${item.detail || ""}`.toLowerCase();

  if (
    text.includes("deploy")
  ) {
    return "🚀";
  }

  if (
    text.includes("build") ||
    text.includes("ci")
  ) {
    return "⚙";
  }

  if (
    text.includes("error") ||
    text.includes("failed") ||
    text.includes("unhealthy")
  ) {
    return "⚠";
  }

  if (
    text.includes("health")
  ) {
    return "♥";
  }

  return "●";
}


function formatNotificationTime(value) {
  if (!value) {
    return "Just now";
  }

  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return String(value);
  }

  const diff = Date.now() - date.getTime();

  if (diff < 60 * 1000) {
    return "Just now";
  }

  if (diff < 60 * 60 * 1000) {
    return `${Math.floor(diff / (60 * 1000))}m ago`;
  }

  if (diff < 24 * 60 * 60 * 1000) {
    return `${Math.floor(diff / (60 * 60 * 1000))}h ago`;
  }

  return date.toLocaleDateString([], {
    month: "short",
    day: "numeric"
  });
}


function ensureNotificationPanel() {
  const bell = document.getElementById("notificationButton");

  if (!bell) {
    return null;
  }

  let wrapper = document.getElementById("notificationWrapper");

  if (!wrapper) {
    wrapper = document.createElement("div");
    wrapper.id = "notificationWrapper";
    wrapper.className = "notification-wrapper";

    bell.parentNode.insertBefore(wrapper, bell);
    wrapper.appendChild(bell);
  }

  let panel = document.getElementById("notificationPanel");

  if (!panel) {
    panel = document.createElement("div");
    panel.id = "notificationPanel";
    panel.className = "notification-panel";
    panel.setAttribute("aria-hidden", "true");

    panel.innerHTML = `
      <div class="notification-panel-header">
        <div>
          <strong>Notifications</strong>
          <small>DockFlow activity</small>
        </div>

        <button
          type="button"
          class="notification-mark-read"
          id="markNotificationsRead"
        >
          Mark all read
        </button>
      </div>

      <div
        class="notification-list"
        id="notificationList"
      >
        <div class="notification-loading">
          Loading notifications...
        </div>
      </div>
    `;

    wrapper.appendChild(panel);

    document
      .getElementById("markNotificationsRead")
      ?.addEventListener("click", (event) => {
        event.stopPropagation();
        markAllNotificationsAsRead();
      });
  }

  return panel;
}


function renderNotifications(items) {
  const list = document.getElementById("notificationList");
  const dot = document.querySelector(".notification-dot");

  if (!list) {
    return;
  }

  const notifications = Array.isArray(items)
    ? items
    : [];

  window.__dockflowNotifications = notifications;

  const readIds = getReadNotificationIds();

  const unreadCount = notifications.filter(item => {
    return !readIds.includes(String(item.id));
  }).length;

  if (dot) {
    dot.textContent = unreadCount > 99
      ? "99+"
      : String(unreadCount);

    dot.classList.toggle(
      "has-notifications",
      unreadCount > 0
    );
  }

  if (!notifications.length) {
    list.innerHTML = `
      <div class="notification-empty">
        <div class="notification-empty-icon">✓</div>
        <strong>You're all caught up</strong>
        <span>No new DockFlow activity.</span>
      </div>
    `;

    return;
  }

  list.innerHTML = notifications.map(item => {
    const status = notificationStatusClass(item);
    const icon = notificationIcon(item);

    return `
      <button
        type="button"
        class="notification-item ${status}"
        data-notification-id="${item.id}"
      >
        <span class="notification-item-icon">
          ${icon}
        </span>

        <span class="notification-item-content">
          <strong>${escapeHtml(item.title || "DockFlow activity")}</strong>
          <small>${escapeHtml(item.detail || "")}</small>
          <em>${escapeHtml(formatNotificationTime(item.created_at))}</em>
        </span>

        <span class="notification-item-dot"></span>
      </button>
    `;
  }).join("");

  list.querySelectorAll(".notification-item").forEach(item => {
    item.addEventListener("click", () => {
      const id = item.dataset.notificationId;

      markNotificationAsRead(id);

      item.classList.add("read");

      renderNotifications(
        window.__dockflowNotifications || []
      );
    });
  });
}


function escapeHtml(value) {
  const div = document.createElement("div");
  div.textContent = value == null ? "" : String(value);
  return div.innerHTML;
}


async function loadNotifications(showToast = false) {
  try {
    const d = await api("/api/notifications");

    renderNotifications(d.notifications || []);

    if (showToast) {
      toast("Notifications refreshed");
    }

  } catch (e) {
    const list = document.getElementById("notificationList");

    if (list) {
      list.innerHTML = `
        <div class="notification-error">
          <strong>Unable to load notifications</strong>
          <span>${escapeHtml(e.message)}</span>
        </div>
      `;
    }

    if (showToast) {
      toast(e.message);
    }
  }
}


function toggleNotifications() {
  const panel = ensureNotificationPanel();

  if (!panel) {
    return;
  }

  notificationOpen = !notificationOpen;

  panel.classList.toggle(
    "open",
    notificationOpen
  );

  panel.setAttribute(
    "aria-hidden",
    notificationOpen ? "false" : "true"
  );

  if (notificationOpen) {
    loadNotifications(false);
  }
}


function closeNotifications() {
  const panel = document.getElementById("notificationPanel");

  if (!panel) {
    return;
  }

  notificationOpen = false;

  panel.classList.remove("open");
  panel.setAttribute("aria-hidden", "true");
}


function initializeNotifications() {
  const bell = document.getElementById("notificationButton");

  if (!bell) {
    return;
  }

  ensureNotificationPanel();

  bell.addEventListener("click", (event) => {
    event.stopPropagation();
    toggleNotifications();
  });

  document.addEventListener("click", (event) => {
    const wrapper = document.getElementById("notificationWrapper");

    if (
      notificationOpen &&
      wrapper &&
      !wrapper.contains(event.target)
    ) {
      closeNotifications();
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      closeNotifications();
    }
  });

  loadNotifications(false);

  clearInterval(notificationRefreshTimer);

  notificationRefreshTimer = setInterval(() => {
    loadNotifications(false);
  }, 15000);
}


document.addEventListener("DOMContentLoaded", () => {
  initializeNotifications();
});