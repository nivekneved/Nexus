/**
 * Nexus Unified Navigation & Daemon Controller
 * Standardizes sidebar navigation, active tab highlight, 24/7 scheduler toggle,
 * user account display, and mobile/desktop collapse across all pages.
 */

// 1. Toggle Nexus Scheduler (Daemon)
async function toggleNexusScheduler(btnEl) {
  const btn = btnEl || document.getElementById("btnToggleDaemon");
  const label = document.getElementById("daemonLabel");
  const dot = document.getElementById("daemonDot");
  const prevText = btn ? btn.textContent.trim() : "Start All";
  if (btn) {
    btn.disabled = true;
    btn.textContent = prevText.includes("Stop") ? "Stopping..." : "Starting...";
  }
  try {
    const res = await fetch("/api/scheduler/toggle", { method: "POST" });
    const data = await res.json();
    const isRunning = !!data.scheduler_running;
    if (dot) {
      if (isRunning) dot.classList.add("active");
      else dot.classList.remove("active");
    }
    if (label) {
      label.textContent = isRunning ? "Scheduler: Active (24/7)" : "Scheduler: Stopped";
    }
    if (btn) {
      btn.textContent = isRunning ? "Stop All" : "Start All";
      btn.style.backgroundColor = isRunning ? "rgba(239, 68, 68, 0.12)" : "";
      btn.style.color = isRunning ? "#ef4444" : "";
      btn.style.borderColor = isRunning ? "#ef4444" : "";
    }
    if (typeof window.updateDaemonUI === "function") {
      window.updateDaemonUI(isRunning);
    }
    if (typeof window.showToast === "function") {
      window.showToast(data.message || (isRunning ? "Scheduler & Agents Active" : "Scheduler Stopped"), isRunning ? "success" : "info");
    }
  } catch (err) {
    console.error("Scheduler toggle failed:", err);
    if (btn) btn.textContent = prevText;
    if (typeof window.showToast === "function") {
      window.showToast("Scheduler error: " + err.message, "error");
    } else {
      alert("Failed to toggle scheduler: " + err.message);
    }
  } finally {
    if (btn) btn.disabled = false;
  }
}
window.toggleNexusScheduler = toggleNexusScheduler;
window.handleToggleScheduler = toggleNexusScheduler;

// 2. Sync Scheduler and Account State
async function syncNexusStatus() {
  try {
    const res = await fetch("/api/status");
    if (res.ok) {
      const d = await res.json();
      const isRunning = !!d.scheduler_running;
      const dot = document.getElementById("daemonDot");
      const label = document.getElementById("daemonLabel");
      const btn = document.getElementById("btnToggleDaemon");
      if (dot) {
        if (isRunning) dot.classList.add("active");
        else dot.classList.remove("active");
      }
      if (label) {
        label.textContent = isRunning ? "Scheduler: Active (24/7)" : "Scheduler: Stopped";
      }
      if (btn) {
        btn.textContent = isRunning ? "Stop All" : "Start All";
        btn.style.backgroundColor = isRunning ? "rgba(239, 68, 68, 0.12)" : "";
        btn.style.color = isRunning ? "#ef4444" : "";
        btn.style.borderColor = isRunning ? "#ef4444" : "";
      }

      // Account info
      const emailEl = document.getElementById("sidebarEmail");
      const avatarEl = document.getElementById("avatarLetter");
      const email = d.account_email || d.email || "deven@nexus.mu";
      if (emailEl) emailEl.textContent = email;
      if (avatarEl && email) avatarEl.textContent = email.charAt(0).toUpperCase();
    }
  } catch (e) {
    console.warn("Nexus status sync:", e);
  }
}

// 3. Highlight Active Navigation Item based on URL
function updateActiveNavLink() {
  const path = window.location.pathname.toLowerCase();

  // Clear existing active flags in sidebar
  document.querySelectorAll(".nav-menu .nav-item, #navDashboardLink").forEach(el => {
    el.classList.remove("active");
  });

  if (path === "/" || path === "/index.html" || path === "") {
    const dash = document.getElementById("navDashboardLink");
    if (dash) dash.classList.add("active");
  } else if (path.startsWith("/seek")) {
    const el = document.getElementById("navItemSeek");
    if (el) el.classList.add("active");
  } else if (path.startsWith("/connect")) {
    const el = document.getElementById("navItemConnect");
    if (el) el.classList.add("active");
  } else if (path.startsWith("/operations") || path.startsWith("/propose")) {
    const el = document.getElementById("navItemPropose");
    if (el) el.classList.add("active");
  } else if (path.startsWith("/commerce") || path.startsWith("/sell")) {
    const el = document.getElementById("navItemSell");
    if (el) el.classList.add("active");
  } else if (path.startsWith("/workforce") || path.startsWith("/quote") || path.startsWith("/invoice")) {
    const el = document.getElementById("navItemInvoice");
    if (el) el.classList.add("active");
  } else if (path.startsWith("/revenue")) {
    const el = document.getElementById("navItemRevenueCockpit");
    if (el) el.classList.add("active");
  } else if (path.startsWith("/autopilot")) {
    const el = document.getElementById("navItemAutopilot");
    if (el) el.classList.add("active");
  } else if (path.startsWith("/terminal")) {
    const el = document.getElementById("navItemTerminal");
    if (el) el.classList.add("active");
  } else if (path.startsWith("/addons")) {
    const el = document.getElementById("navItemAddons");
    if (el) el.classList.add("active");
  } else if (path.startsWith("/simulator")) {
    const el = document.getElementById("navItemSimulator");
    if (el) el.classList.add("active");
  } else if (path.startsWith("/sovereign")) {
    const el = document.getElementById("navItemSovereign");
    if (el) el.classList.add("active");
  }
}

// 4. Sidebar Toggle & State Persistence
function initSidebarToggle() {
  const toggleBtn = document.getElementById("btnToggleSidebar");
  const sidebar = document.getElementById("appSidebar");
  if (!sidebar) return;

  const isCollapsed = localStorage.getItem("nexus_sidebar_collapsed") === "true";
  if (isCollapsed) {
    sidebar.classList.add("collapsed");
  }

  if (toggleBtn) {
    toggleBtn.addEventListener("click", () => {
      sidebar.classList.toggle("collapsed");
      localStorage.setItem("nexus_sidebar_collapsed", sidebar.classList.contains("collapsed"));
    });
  }
}

