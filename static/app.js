// Nexus Workforce Engine — Multi-Agent Frontend Controller with Live Telemetry & Dynamic Settings

// Global Auth & Fetch Interceptor: attaches Bearer token automatically
(function() {
  function getDashboardToken() {
    if (window.__NEXUS_TOKEN__) return window.__NEXUS_TOKEN__;
    try {
      const match = document.cookie.match(/(?:^|;\s*)nexus_token=([^;]*)/);
      if (match) return decodeURIComponent(match[1]);
      return localStorage.getItem("nexus_token") || "";
    } catch (e) {
      return "";
    }
  }

  const origFetch = window.fetch;
  window.fetch = function(url, options) {
    options = options || {};
    const token = getDashboardToken();
    if (token) {
      options.headers = options.headers || {};
      if (options.headers instanceof Headers) {
        if (!options.headers.has("Authorization")) {
          options.headers.set("Authorization", "Bearer " + token);
        }
      } else if (Array.isArray(options.headers)) {
        const hasAuth = options.headers.some(([k]) => k.toLowerCase() === "authorization");
        if (!hasAuth) options.headers.push(["Authorization", "Bearer " + token]);
      } else {
        if (!options.headers["Authorization"] && !options.headers["authorization"]) {
          options.headers["Authorization"] = "Bearer " + token;
        }
      }
      if (!options.credentials) {
        options.credentials = "same-origin";
      }
    }
    return origFetch.call(this, url, options);
  };
})();

let eventSource = null;
let currentSettingsAgentId = null;

document.addEventListener("DOMContentLoaded", () => {
  initTabs();
  initTelemetryStream();
  fetchAgents();
  fetchEmailAccounts();
  fetchStatus();
  fetchLedger();
  setupEventListeners();
  setupPaymentListeners();
  setupRevenueAndProductivity();
  initAutopilotController();
  initRevenueScoutController();
  initPartnerAIController();
  initMeshController();
});

// Tab Navigation
function initTabs() {
  const navItems = document.querySelectorAll(".nav-item");
  const panes = document.querySelectorAll(".tab-pane");

  navItems.forEach(btn => {
    btn.addEventListener("click", () => {
      const targetTab = btn.dataset.tab;
      
      navItems.forEach(b => b.classList.remove("active"));
      panes.forEach(p => p.classList.remove("active"));

      btn.classList.add("active");
      const activePane = document.getElementById(`pane-${targetTab}`);
      if (activePane) activePane.classList.add("active");

      const pageTitle = document.getElementById("pageTitle");
      const titles = {
        workforce: "Workforce",
        terminal: "Activity",
        dashboard: "Inbox",
        ledger: "Trash & Undo",
        simulator: "Tester",
        addons: "Shield & Addons",
        devops: "Operations",
        autopilot: "Night Shift (24/7 Autopilot)",
        revenue: "Revenue Scout & Monetization",
        mesh: "Agent Mesh & Comms Hub"
      };
      if (pageTitle && titles[targetTab]) {
        pageTitle.textContent = titles[targetTab];
      }

      if (targetTab === "workforce") {
        fetchPartnerAIData();
        fetchAgents();
        fetchEmailAccounts();
        fetchReceivables();
        fetchLeadsPipeline();
      }
      if (targetTab === "dashboard") {
        fetchEmailAccounts();
        fetchUnifiedFeed();
      }
      if (targetTab === "ledger") fetchLedger();
      if (targetTab === "addons") fetchAddonsAndShield();
      if (targetTab === "devops") fetchDevOpsDashboard();
      if (targetTab === "autopilot") fetchAutopilotData();
      if (targetTab === "revenue") fetchRevenueScoutData();
      if (targetTab === "mesh") {
        fetchMeshContacts();
        fetchMeshMessages();
      }
    });
  });

  const btnViewFull = document.getElementById("btnViewFullTerminal");
  if (btnViewFull) {
    btnViewFull.addEventListener("click", () => {
      document.querySelector('[data-tab="terminal"]').click();
    });
  }
}

// Global Event Listeners
function setupEventListeners() {
  const btnRunScan = document.getElementById("btnRunScan");
  if (btnRunScan) btnRunScan.addEventListener("click", () => triggerAgentRun("email_hygiene"));

  const btnToggleDaemon = document.getElementById("btnToggleDaemon");
  if (btnToggleDaemon) btnToggleDaemon.addEventListener("click", handleToggleScheduler);

  const btnRefreshLedger = document.getElementById("btnRefreshLedger");
  if (btnRefreshLedger) btnRefreshLedger.addEventListener("click", fetchLedger);

  const btnClearTerminal = document.getElementById("btnClearTerminal");
  if (btnClearTerminal) {
    btnClearTerminal.addEventListener("click", () => {
      document.getElementById("fullTerminalLogs").innerHTML = "";
      document.getElementById("miniTerminalLogs").innerHTML = "";
      showToast("Cleared terminal logs", "info");
    });
  }

  const simulatorForm = document.getElementById("simulatorForm");
  if (simulatorForm) simulatorForm.addEventListener("submit", handleSimulate);

  const btnLoadPreset = document.getElementById("btnLoadPreset");
  if (btnLoadPreset) {
    btnLoadPreset.addEventListener("click", () => {
      document.getElementById("simSender").value = "Google Security <no-reply@accounts.google.com>";
      document.getElementById("simSubject").value = "Your Google verification code is 492019";
      document.getElementById("simBody").value = "Use this one-time code to complete your two-factor login. Never share this code.";
      showToast("Loaded 2FA / Immunity Shield preset!", "info");
    });
  }

  // Modal Close buttons
  const btnCloseModal = document.getElementById("btnCloseModal");
  const btnCancelModal = document.getElementById("btnCancelModal");
  if (btnCloseModal) btnCloseModal.addEventListener("click", closeAgentSettings);
  if (btnCancelModal) btnCancelModal.addEventListener("click", closeAgentSettings);

  const agentSettingsForm = document.getElementById("agentSettingsForm");
  if (agentSettingsForm) agentSettingsForm.addEventListener("submit", handleSaveAgentSettings);

  // Mobile Ping Button (+230 58169420)
  const btnPingMobile = document.getElementById("btnPingMobile");
  if (btnPingMobile) btnPingMobile.addEventListener("click", handlePingMobile);

  // Multi-Inbox Accounts Manager
  const btnAddInboxBtn = document.getElementById("btnAddInboxBtn");
  if (btnAddInboxBtn) btnAddInboxBtn.addEventListener("click", openAddAccountModal);

  const btnCloseAccountModal = document.getElementById("btnCloseAccountModal");
  const btnCancelAccountModal = document.getElementById("btnCancelAccountModal");
  if (btnCloseAccountModal) btnCloseAccountModal.addEventListener("click", closeAccountModal);
  if (btnCancelAccountModal) btnCancelAccountModal.addEventListener("click", closeAccountModal);

  const accProvider = document.getElementById("accProvider");
  if (accProvider) {
    accProvider.addEventListener("change", (e) => {
      const val = e.target.value;
      const srv = document.getElementById("accServer");
      const prt = document.getElementById("accPort");
      if (val === "gmail") { srv.value = "imap.gmail.com"; prt.value = 993; }
      else if (val === "outlook") { srv.value = "outlook.office365.com"; prt.value = 993; }
      else if (val === "yahoo") { srv.value = "imap.mail.yahoo.com"; prt.value = 993; }
      else if (val === "icloud") { srv.value = "imap.mail.me.com"; prt.value = 993; }
    });
  }

  const emailAccountForm = document.getElementById("emailAccountForm");
  if (emailAccountForm) emailAccountForm.addEventListener("submit", handleSaveAccount);
}

// ===================================================
// 📡 REAL-TIME TELEMETRY STREAM (SSE)
// ===================================================
function initTelemetryStream() {
  if (eventSource) eventSource.close();

  let sseUrl = "/api/events";
  const token = (function() {
    if (window.__NEXUS_TOKEN__) return window.__NEXUS_TOKEN__;
    try {
      const match = document.cookie.match(/(?:^|;\s*)nexus_token=([^;]*)/);
      if (match) return decodeURIComponent(match[1]);
      return localStorage.getItem("nexus_token") || "";
    } catch (e) {
      return "";
    }
  })();
  if (token) {
    sseUrl += "?token=" + encodeURIComponent(token);
  }

  eventSource = new EventSource(sseUrl);

  eventSource.onmessage = (e) => {
    try {
      const data = JSON.parse(e.data);
      appendTelemetryRow(data);
    } catch (err) {
      // heartbeats or non-json
    }
  };

  eventSource.onerror = () => {
    // Reconnects automatically by browser
  };
}

function appendTelemetryRow(event) {
  const fullBody = document.getElementById("fullTerminalLogs");
  const miniBody = document.getElementById("miniTerminalLogs");
  const autoScroll = document.getElementById("termAutoScroll")?.checked ?? true;

  const levelClass = `term-level-${event.level || 'INFO'}`;
  const fileBadge = event.file_used 
    ? `<span class="badge-file">📄 ${escapeHtml(event.file_used)}</span>`
    : `<span style="color: #64748b;">--</span>`;

  const fullRow = document.createElement("div");
  fullRow.className = `term-row ${levelClass}`;
  fullRow.innerHTML = `
    <span class="term-col col-time">${event.timestamp}</span>
    <span class="term-col col-agent">${escapeHtml(event.agent_name || event.agent_id)}</span>
    <span class="term-col col-step"><span class="badge-step">${escapeHtml(event.step)}</span></span>
    <span class="term-col col-file">${fileBadge}</span>
    <span class="term-col col-msg">${escapeHtml(event.message)}</span>
  `;

  if (fullBody) {
    fullBody.appendChild(fullRow);
    if (autoScroll) {
      fullBody.scrollTop = fullBody.scrollHeight;
    }
  }

  if (miniBody) {
    const miniRow = document.createElement("div");
    miniRow.className = `terminal-line ${levelClass}`;
    miniRow.innerHTML = `
      <span class="term-time">${event.timestamp}</span>
      <span class="badge-step">${escapeHtml(event.step)}</span>
      <span class="badge-file">${escapeHtml(event.file_used || '')}</span>
      <span class="term-msg">${escapeHtml(event.message)}</span>
    `;
    miniBody.appendChild(miniRow);
    miniBody.scrollTop = miniBody.scrollHeight;

    // Keep mini log bounded
    if (miniBody.children.length > 30) {
      miniBody.removeChild(miniBody.children[0]);
    }
  }
}

// ===================================================
// 🤖 DYNAMIC AGENTS WORKFORCE & CONTROLS
// ===================================================
async function fetchAgents() {
  try {
    const res = await fetch("/api/agents");
    const data = await res.json();

    const grid = document.getElementById("agentsGrid");
    const countEl = document.getElementById("agentCount");
    if (countEl) countEl.textContent = data.agents.length;

    updateDaemonUI(data.scheduler_running);

    if (!grid) return;

    grid.innerHTML = data.agents.map(agent => {
      const isEnabled = agent.is_enabled;
      const statusColor = isEnabled ? "var(--success)" : "var(--text-dim)";
      const statusText = isEnabled ? "Active" : "Disabled";

      const statsHtml = (agent.stats || []).map(s => `
        <div class="agent-stat-pill">
          <div class="agent-stat-pill-val">${s.value}</div>
          <div class="agent-stat-pill-lbl">${s.title}</div>
        </div>
      `).join("");

      return `
        <div class="agent-card">
          <div>
            <div class="agent-card-header">
              <div style="display: flex; gap: 12px; align-items: center;">
                <div class="agent-icon-badge">
                  ${getAgentIconBadge(agent.icon)}
                </div>
                <div>
                  <h3 class="agent-title">${escapeHtml(agent.name)}</h3>
                  <div class="agent-status-tag" style="color: ${statusColor};">
                    <span class="pulse-dot" style="background: ${statusColor};"></span> ${statusText} • Every ${agent.schedule_minutes}m
                  </div>
                </div>
              </div>

              <div style="display: flex; gap: 8px;">
                <button class="btn btn-secondary btn-sm" onclick="openAgentSettings('${agent.id}')" title="Configure Agent Options">
                  ⚙️ Settings
                </button>
                <button class="btn btn-secondary btn-sm" onclick="toggleAgent('${agent.id}')">
                  ${isEnabled ? 'Disable' : 'Enable'}
                </button>
              </div>
            </div>

            <p class="agent-desc">${escapeHtml(agent.description)}</p>

            <div class="agent-stats-row">
              ${statsHtml}
            </div>
          </div>

          <div class="agent-card-footer">
            <span style="font-size: 0.75rem; color: var(--text-dim);">Last run: ${agent.last_run_time || 'Never'}</span>
            <button class="btn btn-primary btn-sm" onclick="triggerAgentRun('${agent.id}')">
              ⚡ Trigger Now
            </button>
          </div>
        </div>
      `;
    }).join("");

  } catch (err) {
    console.error("Failed to fetch agents:", err);
  }
}

// Trigger Agent Run
async function triggerAgentRun(agentId) {
  showToast(`Starting cycle for agent: ${agentId}...`, "info");
  try {
    const res = await fetch(`/api/agents/${agentId}/run`, { method: "POST" });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Run failed");

    showToast(`Agent cycle completed successfully!`, "success");
    fetchAgents();

    if (agentId === "email_hygiene" && data.result) {
      const r = data.result;
      document.getElementById("statScanned").textContent = r.total_scanned || 0;
      document.getElementById("statTrashed").textContent = r.trashed || 0;
      document.getElementById("statQuarantined").textContent = r.quarantined || 0;
      document.getElementById("statKept").textContent = r.kept || 0;
      renderTriageTable(r.emails || []);
      fetchLedger();
    }
  } catch (err) {
    showToast(`Error: ${err.message}`, "error");
  }
}
window.triggerAgentRun = triggerAgentRun;

async function toggleAgent(agentId) {
  try {
    const res = await fetch(`/api/agents/${agentId}/toggle`, { method: "POST" });
    const data = await res.json();
    showToast(`Agent is now ${data.is_enabled ? 'Active' : 'Disabled'}`, "info");
    fetchAgents();
  } catch (err) {
    showToast("Failed to toggle agent status", "error");
  }
}
window.toggleAgent = toggleAgent;

// ===================================================
// ⚙️ DYNAMIC AGENT SETTINGS MODAL
// ===================================================
async function openAgentSettings(agentId) {
  currentSettingsAgentId = agentId;
  const modal = document.getElementById("settingsModal");
  const titleEl = document.getElementById("modalTitle");
  const subtitleEl = document.getElementById("modalSubtitle");
  const fieldsContainer = document.getElementById("dynamicFormFields");

  fieldsContainer.innerHTML = `<div style="text-align: center; padding: 20px;">Loading configuration schema...</div>`;
  modal.classList.add("open");

  try {
    const res = await fetch(`/api/agents/${agentId}/config`);
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Failed to load settings");

    titleEl.textContent = `⚙️ Settings: ${data.name}`;
    subtitleEl.textContent = `Configure custom properties and parameters for this agent`;

    const schema = data.schema || [];
    const currentConfig = data.config || {};

    if (schema.length === 0) {
      fieldsContainer.innerHTML = `<p style="color: var(--text-muted);">This agent does not require any custom settings.</p>`;
      return;
    }

    fieldsContainer.innerHTML = schema.map(f => {
      const val = currentConfig[f.key] !== undefined ? currentConfig[f.key] : (f.default !== undefined ? f.default : "");

      if (f.type === "boolean") {
        return `
          <div class="form-group checkbox-group">
            <label class="checkbox-label">
              <input type="checkbox" name="${f.key}" ${val ? 'checked' : ''}>
              <span><strong>${escapeHtml(f.label)}</strong> — ${escapeHtml(f.description || '')}</span>
            </label>
          </div>
        `;
      } else if (f.type === "textarea") {
        return `
          <div class="form-group">
            <label>${escapeHtml(f.label)}</label>
            ${f.description ? `<p class="form-hint">${escapeHtml(f.description)}</p>` : ''}
            <textarea name="${f.key}" class="form-textarea" rows="3">${escapeHtml(String(val))}</textarea>
          </div>
        `;
      } else {
        return `
          <div class="form-group">
            <label>${escapeHtml(f.label)}</label>
            ${f.description ? `<p class="form-hint">${escapeHtml(f.description)}</p>` : ''}
            <input type="${f.type === 'password' ? 'password' : (f.type === 'number' ? 'number' : 'text')}" 
                   name="${f.key}" 
                   class="form-input" 
                   value="${escapeHtml(String(val))}" 
                   ${f.step ? `step="${f.step}"` : ''}>
          </div>
        `;
      }
    }).join("");

  } catch (err) {
    fieldsContainer.innerHTML = `<div style="color: var(--danger);">Error loading settings: ${err.message}</div>`;
  }
}
window.openAgentSettings = openAgentSettings;

function closeAgentSettings() {
  const modal = document.getElementById("settingsModal");
  if (modal) modal.classList.remove("open");
  currentSettingsAgentId = null;
}

async function handleSaveAgentSettings(e) {
  e.preventDefault();
  if (!currentSettingsAgentId) return;

  const btn = document.getElementById("btnSaveAgentSettings");
  btn.disabled = true;
  btn.textContent = "Saving...";

  const form = document.getElementById("agentSettingsForm");
  const formData = new FormData(form);
  const payload = {};

  // Parse form elements
  Array.from(form.elements).forEach(el => {
    if (!el.name) return;
    if (el.type === "checkbox") {
      payload[el.name] = el.checked;
    } else if (el.type === "number") {
      payload[el.name] = el.value !== "" ? parseFloat(el.value) : 0;
    } else {
      payload[el.name] = el.value;
    }
  });

  try {
    const res = await fetch(`/api/agents/${currentSettingsAgentId}/config`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Save failed");

    showToast(data.message || "Settings saved successfully!", "success");
    closeAgentSettings();
    fetchAgents();
    fetchStatus();
  } catch (err) {
    showToast(err.message, "error");
  } finally {
    btn.disabled = false;
    btn.textContent = "Save Preferences";
  }
}

// Scheduler Toggle
async function handleToggleScheduler() {
  try {
    const res = await fetch("/api/scheduler/toggle", { method: "POST" });
    const data = await res.json();
    updateDaemonUI(data.scheduler_running);
    showToast(data.message, data.scheduler_running ? "success" : "info");
  } catch (err) {
    showToast("Failed to toggle scheduler", "error");
  }
}

function updateDaemonUI(isRunning) {
  const dot = document.getElementById("daemonDot");
  const label = document.getElementById("daemonLabel");
  const btn = document.getElementById("btnToggleDaemon");

  if (isRunning) {
    dot.classList.add("active");
    label.textContent = "Scheduler: Active (24/7)";
    btn.textContent = "Stop All";
    btn.style.backgroundColor = "var(--danger-subtle)";
    btn.style.color = "var(--danger)";
  } else {
    dot.classList.remove("active");
    label.textContent = "Scheduler: Stopped";
    btn.textContent = "Start All Agents";
    btn.style.backgroundColor = "var(--bg-app)";
    btn.style.color = "var(--text-main)";
  }
}

// Fetch Status
async function fetchStatus() {
  try {
    const res = await fetch("/api/status");
    const data = await res.json();

    document.getElementById("sidebarEmail").textContent = data.email_user || "Not Configured";
    if (data.email_user && data.email_user !== "Not Configured") {
      document.getElementById("avatarLetter").textContent = data.email_user.charAt(0).toUpperCase();
    }

    const dryRunBadge = document.getElementById("badgeDryRun");
    if (dryRunBadge) {
      dryRunBadge.textContent = data.dry_run ? "Mode: Dry-Run (Safe)" : "Mode: Active Deletion";
      dryRunBadge.style.backgroundColor = data.dry_run ? "var(--success-subtle)" : "var(--danger-subtle)";
      dryRunBadge.style.color = data.dry_run ? "var(--success)" : "var(--danger)";
    }
  } catch (err) {
    console.error("Status error:", err);
  }
}

// Render Triage Table
function renderTriageTable(emails) {
  const tbody = document.getElementById("triageTableBody");
  if (!tbody) return;

  if (!emails || emails.length === 0) {
    tbody.innerHTML = `
      <tr class="empty-row">
        <td colspan="6"><div class="empty-state"><p><strong>Inbox is clean!</strong> No unread emails were found.</p></div></td>
      </tr>
    `;
    return;
  }

  tbody.innerHTML = emails.map(m => {
    let verdictBadge = "";
    let actionBadge = "";

    if (m.action === "PROTECTED" || m.action === "KEPT") {
      verdictBadge = `<span class="badge ${m.action === 'PROTECTED' ? 'badge-protected' : 'badge-ham'}">${m.action}</span>`;
      actionBadge = `<span style="color: var(--success); font-weight: 600;">Kept in Inbox</span>`;
    } else if (m.action === "TRASHED") {
      verdictBadge = `<span class="badge badge-spam">HIGH SPAM</span>`;
      actionBadge = `<span style="color: var(--danger); font-weight: 600;">Moved to Trash</span>`;
    } else if (m.action === "QUARANTINED") {
      verdictBadge = `<span class="badge badge-review">QUARANTINE</span>`;
      actionBadge = `<span style="color: var(--warning); font-weight: 600;">Moved to Review</span>`;
    }

    return `
      <tr>
        <td><strong>${escapeHtml(m.sender.substring(0, 32))}</strong></td>
        <td>${escapeHtml(m.subject.substring(0, 40))}</td>
        <td style="text-align: center;">${verdictBadge}</td>
        <td style="text-align: right; font-weight: 700;">${m.confidence}%</td>
        <td>
          <div style="font-size: 0.78rem; font-weight: 600; color: var(--primary);">${escapeHtml(m.category)}</div>
          <div style="font-size: 0.75rem; color: var(--text-muted);">${escapeHtml(m.reason)}</div>
        </td>
        <td>${actionBadge}</td>
      </tr>
    `;
  }).join("");
}

// Fetch Undo / Recovery Ledger
async function fetchLedger() {
  const tbody = document.getElementById("ledgerTableBody");
  if (!tbody) return;

  try {
    const res = await fetch("/api/ledger");
    const ledger = await res.json();

    if (!ledger || ledger.length === 0) {
      tbody.innerHTML = `<tr class="empty-row"><td colspan="6"><div class="empty-state"><p>No items in recovery ledger yet.</p></div></td></tr>`;
      return;
    }

    tbody.innerHTML = ledger.map(item => {
      const isRestored = item.action === "RESTORED";
      const btn = isRestored 
        ? `<span style="color: var(--success); font-weight: 600;">Restored</span>`
        : `<button class="btn-restore" onclick="handleRestore('${item.uid}')">Restore to Inbox</button>`;

      return `
        <tr>
          <td style="font-size: 0.75rem; color: var(--text-dim);">${item.timestamp}</td>
          <td><strong>${escapeHtml(item.sender.substring(0, 30))}</strong></td>
          <td>${escapeHtml(item.subject.substring(0, 35))}</td>
          <td><span class="badge ${item.action === 'TRASH' ? 'badge-spam' : 'badge-review'}">${escapeHtml(item.category || item.action)}</span></td>
          <td><span style="font-weight: 600;">${item.action}</span></td>
          <td>${btn}</td>
        </tr>
      `;
    }).join("");
  } catch (err) {
    console.error("Ledger fetch error:", err);
  }
}

async function handleRestore(uid) {
  showToast(`Restoring UID ${uid} back to Inbox...`, "info");
  try {
    const res = await fetch("/api/restore", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ uid })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Restore failed");

    showToast(data.message, "success");
    fetchLedger();
  } catch (err) {
    showToast(err.message, "error");
  }
}
window.handleRestore = handleRestore;

// Simulate Email
async function handleSimulate(e) {
  e.preventDefault();
  const btn = document.getElementById("btnRunSimulate");
  const box = document.getElementById("simResultBox");

  const sender = document.getElementById("simSender").value;
  const subject = document.getElementById("simSubject").value;
  const body = document.getElementById("simBody").value;

  btn.disabled = true;
  btn.textContent = "Reasoning...";

  try {
    const res = await fetch("/api/simulate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ sender, subject, body })
    });
    const data = await res.json();

    let verdictClass = data.immune ? "badge-protected" : (data.is_spam ? "badge-spam" : "badge-ham");
    let verdictText = data.immune ? "IMMUNITY SHIELD (PROTECTED)" : (data.is_spam ? "SPAM / UNWANTED" : "LEGITIMATE (HAM)");

    box.innerHTML = `
      <div style="margin-bottom: 16px;">
        <span class="badge ${verdictClass}" style="font-size: 0.9rem; padding: 6px 12px;">${verdictText}</span>
      </div>
      
      <div class="sim-metric-row">
        <span style="font-weight: 600; color: var(--text-muted);">Confidence Score</span>
        <span style="font-weight: 800; font-size: 1.1rem;">${(data.confidence * 100).toFixed(1)}%</span>
      </div>

      <div class="sim-metric-row">
        <span style="font-weight: 600; color: var(--text-muted);">Assigned Category</span>
        <span style="font-weight: 700; color: var(--primary);">${escapeHtml(data.category || 'N/A')}</span>
      </div>

      <div style="margin-top: 14px;">
        <div style="font-weight: 600; font-size: 0.85rem; margin-bottom: 6px;">AI Explanation & Reasoning:</div>
        <div style="background: white; padding: 12px; border-radius: 8px; border: 1px solid var(--border-subtle); font-size: 0.85rem; line-height: 1.6;">
          ${escapeHtml(data.reason || 'No explanation provided.')}
        </div>
      </div>
    `;

    showToast("AI Analysis complete!", "success");
  } catch (err) {
    showToast("Simulation error: " + err.message, "error");
  } finally {
    btn.disabled = false;
    btn.innerHTML = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5 3 19 12 5 21 5 3"/></svg> Analyze with AI Brain`;
  }
}

// Toast
function showToast(message, type = "info") {
  const container = document.getElementById("toastContainer");
  if (!container) return;

  const toast = document.createElement("div");
  toast.className = `toast ${type}`;
  toast.textContent = message;

  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateX(100%)";
    toast.style.transition = "all 0.2s ease";
    setTimeout(() => toast.remove(), 200);
  }, 3500);
}

// Mobile Alert Ping
async function handlePingMobile() {
  const btn = document.getElementById("btnPingMobile");
  if (btn) {
    btn.disabled = true;
    btn.textContent = "📡 Sending to +230 58169420...";
  }
  try {
    const res = await fetch("/api/mobile/test", { method: "POST" });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Ping failed");
    showToast("⚡ Mobile alert sent to Deven (+230 58169420)!", "success");
  } catch (err) {
    showToast("Mobile ping error: " + err.message, "error");
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.textContent = "📱 Mobile (+230 58169420)";
    }
  }
}

// Multi-Account Email Manager (Up to 5 accounts)
let currentEmailAccounts = [];

async function fetchEmailAccounts() {
  try {
    const res = await fetch("/api/email/accounts");
    const accounts = await res.json();
    currentEmailAccounts = accounts;
    renderEmailAccounts(accounts);
  } catch (err) {
    console.error("Failed to fetch email accounts:", err);
  }
}

function renderEmailAccounts(accounts) {
  const grid = document.getElementById("emailAccountsGrid");
  const countText = document.getElementById("inboxCountText");
  if (countText) {
    const active = accounts.filter(a => a.is_enabled).length;
    countText.textContent = `${active}/${accounts.length} Inboxes Active (Max 5)`;
  }
  if (!grid) return;

  if (accounts.length === 0) {
    grid.innerHTML = `<div style="grid-column: 1 / -1; color: var(--text-dim); font-size: 0.85rem; padding: 10px;">No email inboxes added yet. Click 'Add Inbox' to connect Gmail, Outlook, or Yahoo.</div>`;
    return;
  }

  grid.innerHTML = accounts.map(acc => {
    const providerIcon = acc.provider === "gmail" ? "🔴 Gmail" : (acc.provider === "outlook" ? "🔵 Outlook" : (acc.provider === "yahoo" ? "🟣 Yahoo" : "✉️ IMAP"));
    const isConnected = (acc.last_status || "").includes("Connected") || acc.last_status === "Ready";
    const statusBg = isConnected ? "#ecfdf5" : "#fef2f2";
    const statusColor = isConnected ? "#059669" : "#dc2626";
    const statusText = isConnected ? (acc.last_status || "Connected") : "Error";

    return `
      <div style="background: white; border: 1px solid var(--border-subtle); border-radius: 10px; padding: 14px; display: flex; flex-direction: column; justify-content: space-between; gap: 8px;">
        <div>
          <div style="display: flex; justify-content: space-between; align-items: center; gap: 8px;">
            <span style="font-size: 0.75rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">${providerIcon}</span>
            <span class="badge" style="background: ${statusBg}; color: ${statusColor}; font-size: 0.7rem; font-weight: 700; max-width: 140px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="${escapeHtml(acc.last_status || '')}">
              ${escapeHtml(statusText)}
            </span>
          </div>
          <div style="font-weight: 700; font-size: 0.95rem; margin-top: 6px; color: var(--text-main);">${escapeHtml(acc.label)}</div>
          <div style="font-size: 0.8rem; color: var(--text-dim); word-break: break-all;">${escapeHtml(acc.email)}</div>
          <div style="font-size: 0.75rem; color: var(--text-dim); margin-top: 4px;">Host: ${escapeHtml(acc.imap_server)}:${acc.imap_port}</div>

          ${!isConnected && acc.last_status ? `
            <div style="font-size: 0.72rem; color: #dc2626; background: #fff5f5; border: 1px solid #fed7d7; border-radius: 4px; padding: 4px 6px; margin-top: 6px; line-height: 1.3; max-height: 48px; overflow: hidden; text-overflow: ellipsis;" title="${escapeHtml(acc.last_status)}">
              ⚠️ ${escapeHtml(acc.last_status.substring(0, 95))}
            </div>
          ` : ''}
        </div>

        <div style="display: flex; gap: 6px; margin-top: 10px; border-top: 1px solid var(--border-subtle); padding-top: 8px;">
          <button class="btn btn-secondary btn-sm" onclick="testEmailAccount('${acc.id}')" style="flex: 1; font-size: 0.75rem; display: inline-flex; align-items: center; justify-content: center; gap: 4px;">
            🔍 Test
          </button>
          <button class="btn btn-secondary btn-sm" onclick="openEditAccountModal('${acc.id}')" style="flex: 1; font-size: 0.75rem; display: inline-flex; align-items: center; justify-content: center; gap: 4px; font-weight: 600;" title="Edit Inbox Settings & Password">
            ✏️ Edit
          </button>
          <button class="btn btn-secondary btn-sm text-red" onclick="deleteEmailAccount('${acc.id}')" style="font-size: 0.75rem; padding: 4px 8px;" title="Delete Inbox">
            🗑️
          </button>
        </div>
      </div>
    `;
  }).join("");
}

function openAddAccountModal() {
  const modal = document.getElementById("accountModal");
  if (!modal) return;
  const modalTitle = document.getElementById("accountModalTitle");
  if (modalTitle) modalTitle.textContent = "Connect Email Inbox";

  const btnSave = document.getElementById("btnSaveAccount");
  if (btnSave) btnSave.textContent = "Save & Connect Inbox";

  document.getElementById("accId").value = "";
  document.getElementById("accLabel").value = "";
  document.getElementById("accEmail").value = "";
  document.getElementById("accPassword").value = "";
  document.getElementById("accPassword").placeholder = "e.g. abcd efgh ijkl mnop";
  document.getElementById("accProvider").value = "gmail";
  document.getElementById("accServer").value = "imap.gmail.com";
  document.getElementById("accPort").value = 993;

  modal.classList.add("active");
  modal.classList.add("open");
}
window.openAddAccountModal = openAddAccountModal;

function openEditAccountModal(accId) {
  const modal = document.getElementById("accountModal");
  if (!modal) return;
  const acc = (currentEmailAccounts || []).find(a => a.id === accId);
  if (!acc) return;

  const modalTitle = document.getElementById("accountModalTitle");
  if (modalTitle) modalTitle.textContent = `Edit Inbox (${acc.label || acc.email})`;

  const btnSave = document.getElementById("btnSaveAccount");
  if (btnSave) btnSave.textContent = "Save Changes";

  document.getElementById("accId").value = acc.id || "";
  document.getElementById("accLabel").value = acc.label || "";
  document.getElementById("accEmail").value = acc.email || "";
  document.getElementById("accPassword").value = "";
  document.getElementById("accPassword").placeholder = "Leave empty to keep existing password";
  document.getElementById("accProvider").value = acc.provider || "gmail";
  document.getElementById("accServer").value = acc.imap_server || "imap.gmail.com";
  document.getElementById("accPort").value = acc.imap_port || 993;

  modal.classList.add("active");
  modal.classList.add("open");
}
window.openEditAccountModal = openEditAccountModal;

function closeAccountModal() {
  const modal = document.getElementById("accountModal");
  if (modal) {
    modal.classList.remove("active");
    modal.classList.remove("open");
  }
}
window.closeAccountModal = closeAccountModal;

async function handleSaveAccount(e) {
  e.preventDefault();
  const accId = document.getElementById("accId").value;
  const payload = {
    id: accId || undefined,
    label: document.getElementById("accLabel").value.trim(),
    provider: document.getElementById("accProvider").value,
    email: document.getElementById("accEmail").value.trim(),
    password: document.getElementById("accPassword").value.trim(),
    imap_server: document.getElementById("accServer").value.trim(),
    imap_port: parseInt(document.getElementById("accPort").value) || 993,
    is_enabled: true
  };

  try {
    const res = await fetch("/api/email/accounts", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Failed to save inbox account");

    showToast(accId ? "Inbox configuration updated & saved!" : "Connected email inbox saved successfully!", "success");
    closeAccountModal();
    fetchEmailAccounts();
    fetchAgents();
  } catch (err) {
    showToast("Error: " + err.message, "error");
  }
}

async function testEmailAccount(accId) {
  showToast("Testing IMAP connection...", "info");
  try {
    const res = await fetch(`/api/email/accounts/${accId}/test`, { method: "POST" });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Test connection failed");
    showToast(data.message, "success");
    fetchEmailAccounts();
  } catch (err) {
    showToast("Connection failed: " + err.message, "error");
    fetchEmailAccounts();
  }
}
window.testEmailAccount = testEmailAccount;

async function deleteEmailAccount(accId) {
  if (!confirm("Are you sure you want to remove this inbox from automated triage?")) return;
  try {
    const res = await fetch(`/api/email/accounts/${accId}`, { method: "DELETE" });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Failed to delete");
    showToast("Removed inbox account", "info");
    fetchEmailAccounts();
    fetchAgents();
  } catch (err) {
    showToast("Error: " + err.message, "error");
  }
}
window.deleteEmailAccount = deleteEmailAccount;

function getAgentIconBadge(icon) {
  switch (icon) {
    case 'mail': return '📧';
    case 'calendar': return '📅';
    case 'phone': case 'mobile': return '📱';
    case 'target': case 'search': case 'lead': return '🎯';
    case 'support': case 'headset': return '🎧';
    case 'rocket': case 'launch': return '🚀';
    case 'briefcase': case 'standup': return '💼';
    case 'checklist': case 'inspect': return '📋';
    case 'shield': case 'backup': return '🛡️';
    case 'globe': case 'language': return '🌐';
    default: return '🤖';
  }
}

function escapeHtml(text) {
  if (!text) return "";
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

// -------------------------------------------------------------
// ADDON MATRIX & 25-SAFEGUARD SECURITY SHIELD LOGIC
// -------------------------------------------------------------

let allAddonsList = [];
let currentAddonCategory = "all";

async function fetchAddonsAndShield() {
  try {
    // 1. Fetch Shield Health
    const shieldRes = await fetch("/api/security/shield");
    if (shieldRes.ok) {
      const sData = await shieldRes.json();
      const badge = document.getElementById("shieldStatusBadge");
      if (badge) badge.textContent = `${sData.safeguards_active}/25 SAFEGUARDS ACTIVE`;
      const tok = document.getElementById("shieldTokens");
      if (tok) tok.textContent = `${sData.tokens_available} / 60.0`;
      const hmacEl = document.getElementById("shieldHmac");
      if (hmacEl) hmacEl.textContent = sData.env_hmac ? sData.env_hmac.substring(0, 16) + "..." : "Anchor Verified";
      const breakEl = document.getElementById("shieldBreakers");
      if (breakEl) {
        const count = sData.circuit_breaker_tripped ? sData.circuit_breaker_tripped.length : 0;
        breakEl.textContent = count === 0 ? "0 Tripped" : `${count} Tripped!`;
        breakEl.style.color = count === 0 ? "#16a34a" : "#dc2626";
      }
    }

    // 2. Fetch SubAgents Fleet
    fetchSubagents();

    // 3. Fetch All Addons
    const addonsRes = await fetch("/api/addons");
    if (addonsRes.ok) {
      const aData = await addonsRes.json();
      allAddonsList = aData.addons || [];
      updateAddonCounts(allAddonsList);
      renderAddonsGrid(allAddonsList, currentAddonCategory);
    }
  } catch (err) {
    console.error("Error fetching addons/shield:", err);
  }
}

function updateAddonCounts(addons) {
  const total = addons.length;
  const agents = addons.filter(a => a.category === "primary_agent").length;
  const subs = addons.filter(a => a.category === "subagent").length;
  const shields = addons.filter(a => a.category === "security_shield").length;

  const elTotal = document.getElementById("totalAddonsCount");
  if (elTotal) elTotal.textContent = total;
  const elAll = document.getElementById("countAll");
  if (elAll) elAll.textContent = total;
  const elAgents = document.getElementById("countAgents");
  if (elAgents) elAgents.textContent = agents;
  const elSub = document.getElementById("countSub");
  if (elSub) elSub.textContent = subs;
  const elShield = document.getElementById("countShield");
  if (elShield) elShield.textContent = shields;
}

function renderAddonsGrid(addons, categoryFilter) {
  const container = document.getElementById("addonsGrid");
  if (!container) return;

  const filtered = categoryFilter === "all" 
    ? addons 
    : addons.filter(a => a.category === categoryFilter);

  if (filtered.length === 0) {
    container.innerHTML = `<div style="grid-column: 1 / -1; text-align: center; padding: 40px; color: var(--text-dim);">No addons found in this category.</div>`;
    return;
  }

  container.innerHTML = filtered.map(addon => {
    const isActive = addon.is_active;
    let badgeClass = "badge-cat-primary";
    let catLabel = "Primary Employee";

    if (addon.category === "subagent") {
      badgeClass = "badge-cat-subagent";
      catLabel = `SubAgent (${addon.parent_id || "Fleet"})`;
    } else if (addon.category === "security_shield") {
      badgeClass = "badge-cat-shield";
      catLabel = "Security Safeguard";
    }

    return `
      <div class="addon-card ${isActive ? '' : 'inactive'}" id="addonCard_${addon.id}">
        <div>
          <div class="addon-card-header">
            <div class="addon-card-title">${escapeHtml(addon.name)}</div>
            <label class="switch">
              <input type="checkbox" ${isActive ? 'checked' : ''} onchange="toggleAddonState('${addon.id}', this.checked)">
              <span class="slider"></span>
            </label>
          </div>
          <div class="addon-card-desc">${escapeHtml(addon.description)}</div>
        </div>
        <div class="addon-card-footer">
          <span class="badge ${badgeClass}">${catLabel}</span>
          <span style="font-size: 0.75rem; font-weight: 600; color: ${isActive ? '#16a34a' : '#94a3b8'};">
            ${isActive ? '● Active' : '○ Standby'}
          </span>
        </div>
      </div>
    `;
  }).join("");
}

async function toggleAddonState(addonId, targetState) {
  try {
    const res = await fetch(`/api/addons/${addonId}/toggle`, { method: "POST" });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Toggle failed");
    
    // Update local state
    const found = allAddonsList.find(a => a.id === addonId);
    if (found) found.is_active = data.is_active;
    
    showToast(`Addon '${addonId}' is now ${data.is_active ? 'ACTIVE' : 'DEACTIVATED'}`, data.is_active ? "success" : "info");
    
    // Re-render and refresh other panels if primary agent was toggled
    renderAddonsGrid(allAddonsList, currentAddonCategory);
    fetchSubagents();
    fetchAgents();
  } catch (err) {
    showToast("Error toggling addon: " + err.message, "error");
    fetchAddonsAndShield();
  }
}
window.toggleAddonState = toggleAddonState;

async function fetchSubagents() {
  const tbody = document.getElementById("subagentsTableBody");
  if (!tbody) return;

  try {
    const res = await fetch("/api/subagents");
    if (!res.ok) return;
    const subagents = await res.json();

    const badge = document.getElementById("subagentCountBadge");
    if (badge) {
      const activeCount = subagents.filter(s => s.is_active).length;
      badge.textContent = `${activeCount}/${subagents.length} SubAgents Active`;
    }

    if (subagents.length === 0) {
      tbody.innerHTML = `<tr><td colspan="7" style="text-align: center; color: var(--text-dim); padding: 24px;">No subagents registered yet.</td></tr>`;
      return;
    }

    tbody.innerHTML = subagents.map(s => {
      const isTripped = s.circuit_tripped;
      const latencyStr = s.last_latency_ms > 0 ? `${s.last_latency_ms} ms` : "Instant";

      return `
        <tr>
          <td style="font-weight: 600; color: var(--text-main);">
            <div style="display: flex; align-items: center; gap: 8px;">
              <span style="font-size: 1.1rem;">⚙️</span>
              <div>
                <div>${escapeHtml(s.name)}</div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: var(--text-dim);">${escapeHtml(s.subagent_id)}</div>
              </div>
            </div>
          </td>
          <td style="color: var(--text-muted); font-weight: 500;">${escapeHtml(s.parent_name)}</td>
          <td style="font-size: 0.8rem; color: var(--text-muted); max-width: 260px;">${escapeHtml(s.description)}</td>
          <td style="font-weight: 600; font-family: 'JetBrains Mono', monospace;">${s.execution_count}</td>
          <td>
            <span class="badge" style="background: #f1f5f9; color: #0f172a; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem;">
              ${latencyStr}
            </span>
          </td>
          <td>
            <span class="badge" style="background: ${isTripped ? '#fee2e2' : '#f0fdf4'}; color: ${isTripped ? '#dc2626' : '#16a34a'}; border: 1px solid ${isTripped ? '#fca5a5' : '#bbf7d0'};">
              ${isTripped ? '⚡ Tripped (Cooling)' : '✓ Normal'}
            </span>
          </td>
          <td style="text-align: right;">
            <label class="switch">
              <input type="checkbox" ${s.is_active ? 'checked' : ''} onchange="toggleAddonState('${s.subagent_id}', this.checked)">
              <span class="slider"></span>
            </label>
          </td>
        </tr>
      `;
    }).join("");
  } catch (err) {
    console.error("Error fetching subagents:", err);
  }
}

// Wire Security Self-Test & Filter Buttons on DOMContentLoaded
document.addEventListener("DOMContentLoaded", () => {
  const btnVerify = document.getElementById("btnVerifyShield");
  if (btnVerify) {
    btnVerify.addEventListener("click", async () => {
      btnVerify.disabled = true;
      btnVerify.textContent = "Auditing 25 Safeguards...";
      try {
        const res = await fetch("/api/security/verify", { method: "POST" });
        const data = await res.json();
        if (data.passed) {
          showToast(`🛡️ All 25 Enterprise Safeguards Verified! Status: PASSED`, "success");
        } else {
          showToast(`⚠️ Shield Audit: Some safeguards failed verification`, "error");
        }
        fetchAddonsAndShield();
      } catch (err) {
        showToast("Security Audit Error: " + err.message, "error");
      } finally {
        btnVerify.disabled = false;
        btnVerify.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m9 12 2 2 4-4"/><circle cx="12" cy="12" r="10"/></svg> Run Security Self-Test`;
      }
    });
  }

  // Addon Category Filter Tabs
  const catButtons = document.querySelectorAll("#addonCategoryFilters button");
  catButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      catButtons.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      currentAddonCategory = btn.dataset.cat;
      renderAddonsGrid(allAddonsList, currentAddonCategory);
    });
  });

  // DevOps Tab Controls
  const btnRefSub = document.getElementById("btnRefreshSubscriptions");
  if (btnRefSub) {
    btnRefSub.addEventListener("click", () => {
      fetchSubscriptions();
      showToast("Subscription catalog refreshed", "info");
    });
  }

  const btnDispDossier = document.getElementById("btnDispatchDossierMobile");
  if (btnDispDossier) {
    btnDispDossier.addEventListener("click", async () => {
      btnDispDossier.disabled = true;
      btnDispDossier.textContent = "Sending to WhatsApp...";
      try {
        const res = await fetch("/api/mobile/test", { method: "POST" });
        if (res.ok) {
          showToast("📱 Tech Dossier briefing dispatched to +230 58169420!", "success");
        } else {
          showToast("Failed to send WhatsApp message", "error");
        }
      } catch (err) {
        showToast("Error: " + err.message, "error");
      } finally {
        btnDispDossier.disabled = false;
        btnDispDossier.textContent = "📱 Send to WhatsApp";
      }
    });
  }
});

// -------------------------------------------------------------
// DEV OPERATIONS & SUBSCRIPTIONS CONTROLLER
// -------------------------------------------------------------

async function fetchDevOpsDashboard() {
  fetchSubscriptions();
  fetchNewsletterDigest();
  fetchRepoRadar();
  fetchFinanceHealth();
  fetchTechDossier();
}

async function fetchSubscriptions() {
  const tbody = document.getElementById("subscriptionsTableBody");
  if (!tbody) return;

  try {
    const res = await fetch("/api/unsubscriber/subscriptions");
    if (!res.ok) return;
    const list = await res.json();

    if (!list || list.length === 0) {
      tbody.innerHTML = `<tr><td colspan="4" style="text-align: center; color: var(--text-dim); padding: 24px;">No marketing subscriptions detected. Your inbox is clean!</td></tr>`;
      return;
    }

    tbody.innerHTML = list.map(sub => {
      const isUnsubbed = sub.status === "UNSUBSCRIBED";
      return `
        <tr>
          <td>
            <div style="font-weight: 600; color: var(--text-main);">${escapeHtml(sub.sender_name || sub.sender_email)}</div>
            <div style="font-size: 0.75rem; color: var(--text-dim);">${escapeHtml(sub.sender_email)}</div>
          </td>
          <td>
            <span class="badge" style="background: ${sub.frequency_count >= 3 ? '#fef3c7' : '#f1f5f9'}; color: ${sub.frequency_count >= 3 ? '#d97706' : '#475569'};">
              ${sub.frequency_count} emails/wk
            </span>
          </td>
          <td>
            <span class="badge" style="background: ${isUnsubbed ? '#f1f5f9' : '#dcfce7'}; color: ${isUnsubbed ? '#64748b' : '#15803d'};">
              ${isUnsubbed ? 'Unsubscribed' : 'Active'}
            </span>
          </td>
          <td style="text-align: right;">
            ${isUnsubbed ? `
              <span style="font-size: 0.75rem; color: #94a3b8;">✓ Cleaned</span>
            ` : `
              <button class="btn btn-secondary btn-sm" style="color: #dc2626; border-color: #fca5a5; font-weight: 600;" onclick="killSubscription('${sub.id}')">
                Kill Subscription
              </button>
            `}
          </td>
        </tr>
      `;
    }).join("");
  } catch (err) {
    console.error("Error fetching subscriptions:", err);
  }
}

async function killSubscription(subId) {
  if (!confirm("Confirm 1-Click Unsubscribe? We will trigger the automated RFC 2369 unsubscribe action.")) return;
  try {
    const res = await fetch("/api/unsubscriber/execute", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ subscription_id: subId })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Unsubscribe action failed");
    showToast(`Successfully dispatched unsubscribe for ${data.sender_name || 'sender'}!`, "success");
    fetchSubscriptions();
  } catch (err) {
    showToast("Error: " + err.message, "error");
  }
}
window.killSubscription = killSubscription;

async function fetchNewsletterDigest() {
  const box = document.getElementById("newsletterDigestBox");
  if (!box) return;

  try {
    const res = await fetch("/api/unsubscriber/digest");
    if (!res.ok) return;
    const digest = await res.json();

    if (!digest.highlights || digest.highlights.length === 0) {
      box.innerHTML = `<div class="empty-state"><p>No promotional clutter detected today. Inbox is clear!</p></div>`;
      return;
    }

    box.innerHTML = `
      <div style="font-weight: 700; font-size: 0.95rem; margin-bottom: 8px; color: #0f172a;">
        ☕ ${escapeHtml(digest.date || 'Today')} (${digest.total_newsletters_condensed} Blasts Condensed)
      </div>
      <div style="display: flex; flex-direction: column; gap: 8px;">
        ${digest.highlights.slice(0, 4).map((h, i) => `
          <div style="padding: 8px 12px; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px;">
            <div style="font-weight: 600; font-size: 0.82rem; color: #1e293b;">${i+1}. ${escapeHtml(h.headline)}</div>
            <div style="font-size: 0.74rem; color: #64748b; margin-top: 2px;">Source: ${escapeHtml(h.source)}</div>
          </div>
        `).join("")}
      </div>
    `;
  } catch (err) {
    console.error("Error fetching newsletter digest:", err);
  }
}

async function fetchRepoRadar() {
  const box = document.getElementById("repoRadarBox");
  if (!box) return;

  try {
    const res = await fetch("/api/reporadar/alerts");
    if (!res.ok) return;
    const alerts = await res.json();

    const cves = alerts.critical_cves || [];
    const updates = alerts.framework_updates || [];

    const badge = document.getElementById("cveBadgeCount");
    if (badge) {
      badge.textContent = `${cves.length} Critical CVE`;
      badge.style.background = cves.length > 0 ? "#fee2e2" : "#f0fdf4";
      badge.style.color = cves.length > 0 ? "#dc2626" : "#16a34a";
    }

    box.innerHTML = `
      ${cves.map(c => `
        <div style="padding: 10px 14px; background: #fff1f2; border: 1px solid #fecdd3; border-radius: 8px;">
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-weight: 700; font-size: 0.85rem; color: #9f1239;">🚨 ${escapeHtml(c.package)} (${escapeHtml(c.cve)})</span>
            <span class="badge" style="background: #e11d48; color: #fff;">${escapeHtml(c.severity)}</span>
          </div>
          <div style="font-size: 0.78rem; color: #4c0519; margin-top: 4px;">${escapeHtml(c.description)}</div>
          <div style="font-size: 0.75rem; color: #0284c7; font-weight: 600; margin-top: 4px;">Fix: ${escapeHtml(c.recommendation)}</div>
        </div>
      `).join("")}
      ${updates.slice(0, 2).map(u => `
        <div style="padding: 10px 14px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px;">
          <div style="display: flex; justify-content: space-between;">
            <span style="font-weight: 700; font-size: 0.82rem; color: #0f172a;">📦 ${escapeHtml(u.framework)} v${escapeHtml(u.latest_version)}</span>
            <span class="badge" style="background: #eff6ff; color: #1d4ed8;">${escapeHtml(u.type)}</span>
          </div>
          <div style="font-size: 0.75rem; color: #475569; margin-top: 2px;">${escapeHtml(u.impact)}</div>
        </div>
      `).join("")}
    `;
  } catch (err) {
    console.error("Error fetching repo radar:", err);
  }
}

async function fetchFinanceHealth() {
  const box = document.getElementById("financeInfraBox");
  if (!box) return;

  try {
    const res = await fetch("/api/finance/health");
    if (!res.ok) return;
    const fin = await res.json();

    const billing = fin.cloud_billing || {};
    const domains = fin.domains ? fin.domains.domains || [] : [];
    const invoices = fin.invoices ? fin.invoices.invoices || [] : [];

    box.innerHTML = `
      <div style="padding: 10px 14px; background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; display: flex; justify-content: space-between; align-items: center;">
        <div>
          <div style="font-size: 0.75rem; color: #166534; font-weight: 700; text-transform: uppercase;">Cloud Spend (Month-to-Date)</div>
          <div style="font-size: 1.2rem; font-weight: 800; color: #14532d;">$${billing.total_spend_usd || 105.70} <span style="font-size: 0.8rem; font-weight: 500; color: #15803d;">/ $${billing.monthly_budget_usd || 180.0} Budget</span></div>
        </div>
        <span class="badge" style="background: #16a34a; color: #fff;">${billing.burn_rate_pct || 58.7}% Burn</span>
      </div>

      <div style="display: flex; flex-direction: column; gap: 6px; margin-top: 8px;">
        <div style="font-size: 0.78rem; font-weight: 700; color: #475569; text-transform: uppercase;">Domain &amp; Client Receivables:</div>
        ${domains.slice(0, 2).map(d => `
          <div style="display: flex; justify-content: space-between; font-size: 0.8rem; padding: 6px 10px; background: #f8fafc; border-radius: 6px;">
            <span>🌐 ${escapeHtml(d.domain)}</span>
            <span style="color: #16a34a; font-weight: 600;">Expires in ${d.expires_in_days}d</span>
          </div>
        `).join("")}
        ${invoices.filter(i => i.status.includes("OVERDUE")).map(inv => `
          <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.8rem; padding: 6px 10px; background: #fef2f2; border: 1px solid #fecaca; border-radius: 6px;">
            <div>
              <span style="font-weight: 700; color: #991b1b;">⚠️ ${escapeHtml(inv.client)}:</span>
              <span style="color: #7f1d1d;">${escapeHtml(inv.amount_mur)} (${escapeHtml(inv.project)})</span>
            </div>
            <span class="badge" style="background: #ef4444; color: #fff;">Overdue</span>
          </div>
        `).join("")}
      </div>
    `;
  } catch (err) {
    console.error("Error fetching finance health:", err);
  }
}

async function fetchTechDossier() {
  const box = document.getElementById("techDossierBox");
  if (!box) return;

  try {
    const res = await fetch("/api/techdossier/latest");
    if (!res.ok) return;
    const dos = await res.json();

    if (!dos.headline) {
      box.innerHTML = `<div class="empty-state"><p>Today's dossier is compiling. Check back at 08:00 AM.</p></div>`;
      return;
    }

    box.innerHTML = `
      <div style="font-size: 1.1rem; font-weight: 800; color: #0f172a; margin-bottom: 6px;">
        ${escapeHtml(dos.headline)}
      </div>
      <div style="font-size: 0.78rem; color: #64748b; margin-bottom: 14px;">
        📅 ${escapeHtml(dos.date || 'Today')} &bull; ⏱️ Estimated Read: ${escapeHtml(dos.reading_time || '3 mins')}
      </div>
      
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 12px; margin-bottom: 16px;">
        ${(dos.key_takeaways || []).map(t => `
          <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px;">
            <span style="font-size: 0.75rem; font-weight: 700; color: #2563eb; text-transform: uppercase;">${escapeHtml(t.category)}</span>
            <div style="font-weight: 700; font-size: 0.88rem; color: #0f172a; margin: 4px 0;">${escapeHtml(t.title)}</div>
            <div style="font-size: 0.8rem; color: #475569; line-height: 1.4;">${escapeHtml(t.summary)}</div>
          </div>
        `).join("")}
      </div>

      <div style="background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px; padding: 12px 16px;">
        <div style="font-size: 0.8rem; font-weight: 700; color: #1e40af; margin-bottom: 6px; text-transform: uppercase;">Recommended Actions for Deven:</div>
        <ul style="margin: 0; padding-left: 20px; font-size: 0.82rem; color: #1e3a8a;">
          ${(dos.action_items_for_deven || []).map(act => `
            <li style="margin-bottom: 4px;">${escapeHtml(act)}</li>
          `).join("")}
        </ul>
      </div>
    `;
  } catch (err) {
    console.error("Error fetching tech dossier:", err);
  }
}

// ==========================================
// ONLINE PAYMENTS & INVOICES CONTROLLER
// ==========================================
let lastGeneratedInvoice = null;

function setupPaymentListeners() {
  const btnOpen = document.getElementById("btnOpenPaymentModal");
  const modal = document.getElementById("paymentModal");
  const btnClose = document.getElementById("btnClosePaymentModal");
  const form = document.getElementById("paymentLinkForm");
  const btnRefresh = document.getElementById("btnRefreshInvoices");
  const btnCopyPayLink = document.getElementById("btnCopyPayLink");
  const btnCopyWire = document.getElementById("btnCopyWireDetails");
  const btnDispatchMobile = document.getElementById("btnDispatchPaymentMobile");
  const btnCheckStatus = document.getElementById("btnCheckPayStatus");

  if (btnOpen && modal) {
    btnOpen.addEventListener("click", () => {
      modal.classList.add("open");
      fetchRecentInvoices();
    });
  }

  if (btnClose && modal) {
    btnClose.addEventListener("click", () => {
      modal.classList.remove("open");
    });
  }

  // Presets
  document.querySelectorAll(".preset-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const amount = btn.dataset.amount;
      const curr = btn.dataset.curr;
      const desc = btn.dataset.desc;
      const method = btn.dataset.method;

      const amtInput = document.getElementById("payAmount");
      const currInput = document.getElementById("payCurrency");
      const descInput = document.getElementById("payDescription");
      const methodInput = document.getElementById("payMethod");

      if (amtInput) amtInput.value = amount;
      if (currInput) currInput.value = curr;
      if (descInput) descInput.value = desc;
      if (methodInput) methodInput.value = method;
      showToast(`Loaded preset: ${desc} (${curr} ${amount})`, "info");
    });
  });

  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const btnGen = document.getElementById("btnGeneratePaymentLink");
      btnGen.disabled = true;
      btnGen.innerHTML = "⏳ Generating Live Checkout Link...";

      const payload = {
        client_name: document.getElementById("payClientName").value.trim(),
        client_email: document.getElementById("payClientEmail").value.trim(),
        amount: parseFloat(document.getElementById("payAmount").value),
        currency: document.getElementById("payCurrency").value,
        method: document.getElementById("payMethod").value,
        description: document.getElementById("payDescription").value.trim()
      };

      try {
        const res = await fetch("/api/finance/payment-link", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });

        const data = await res.json();
        if (!res.ok || !data.success) {
          throw new Error(data.detail || "Failed to create payment link");
        }

        lastGeneratedInvoice = data.invoice;
        displayPaymentResult(data.invoice);
        fetchRecentInvoices();
        showToast("⚡ Payment Link generated successfully!", "success");
      } catch (err) {
        showToast(`Error: ${err.message}`, "error");
      } finally {
        btnGen.disabled = false;
        btnGen.innerHTML = "⚡ Generate Live Payment Link";
      }
    });
  }

  if (btnCopyPayLink) {
    btnCopyPayLink.addEventListener("click", () => {
      const urlInput = document.getElementById("resPaymentUrl");
      if (urlInput && urlInput.value) {
        navigator.clipboard.writeText(urlInput.value);
        showToast("Copied payment link to clipboard!", "success");
      }
    });
  }

  if (btnCopyWire) {
    btnCopyWire.addEventListener("click", () => {
      const text = document.getElementById("resWireDetails").textContent;
      if (text) {
        navigator.clipboard.writeText(text);
        showToast("Copied wire instructions to clipboard!", "success");
      }
    });
  }

  if (btnDispatchMobile) {
    btnDispatchMobile.addEventListener("click", async () => {
      if (!lastGeneratedInvoice) return;
      btnDispatchMobile.disabled = true;
      try {
        const res = await fetch(`/api/finance/invoices/${lastGeneratedInvoice.id}/dispatch-mobile`, { method: "POST" });
        const d = await res.json();
        if (d.success) {
          showToast("Dispatched payment alert to WhatsApp (+230 58169420)!", "success");
        } else {
          showToast("Failed to dispatch mobile alert", "error");
        }
      } catch (err) {
        showToast("Error contacting mobile dispatcher", "error");
      } finally {
        btnDispatchMobile.disabled = false;
      }
    });
  }

  if (btnCheckStatus) {
    btnCheckStatus.addEventListener("click", async () => {
      if (!lastGeneratedInvoice) return;
      btnCheckStatus.disabled = true;
      try {
        const res = await fetch(`/api/finance/invoices/${lastGeneratedInvoice.id}/check-status`, { method: "POST" });
        const d = await res.json();
        if (d.success) {
          showToast(`Live Status: ${d.status}`, d.status === "COMPLETED" ? "success" : "info");
          fetchRecentInvoices();
        }
      } catch (err) {
        showToast("Error checking status", "error");
      } finally {
        btnCheckStatus.disabled = false;
      }
    });
  }

  if (btnRefresh) {
    btnRefresh.addEventListener("click", fetchRecentInvoices);
  }
}

function displayPaymentResult(invoice) {
  const box = document.getElementById("paymentResultBox");
  if (!box) return;

  box.style.display = "block";
  document.getElementById("resInvoiceId").textContent = `${invoice.id} • ${invoice.currency} ${invoice.amount}`;

  const paypalArea = document.getElementById("resPaypalArea");
  const wireArea = document.getElementById("resWireArea");

  if (invoice.method === "paypal") {
    paypalArea.style.display = "block";
    wireArea.style.display = "none";
    document.getElementById("resPaymentUrl").value = invoice.payment_url || "";
  } else {
    paypalArea.style.display = "none";
    wireArea.style.display = "block";
    document.getElementById("resWireDetails").textContent = invoice.bank_details?.instructions_text || "Bank Wire details generated.";
  }
}

async function fetchRecentInvoices() {
  const container = document.getElementById("recentInvoicesTable");
  if (!container) return;

  try {
    const res = await fetch("/api/finance/invoices");
    if (!res.ok) return;
    const invoices = await res.json();

    if (!invoices || invoices.length === 0) {
      container.innerHTML = `<p style="color: #9ca3af; font-size: 0.8rem; margin: 0;">No payment links generated yet.</p>`;
      return;
    }

    container.innerHTML = `
      <table style="width: 100%; border-collapse: collapse; font-size: 0.8rem; text-align: left;">
        <thead>
          <tr style="border-bottom: 1px solid var(--border-subtle, #e5e7eb); color: #6b7280;">
            <th style="padding: 4px 6px;">ID</th>
            <th style="padding: 4px 6px;">Client</th>
            <th style="padding: 4px 6px;">Amount</th>
            <th style="padding: 4px 6px;">Method</th>
            <th style="padding: 4px 6px;">Status</th>
            <th style="padding: 4px 6px; text-align: right;">Action</th>
          </tr>
        </thead>
        <tbody>
          ${invoices.slice(0, 10).map(inv => `
            <tr style="border-bottom: 1px solid var(--border-subtle, #e5e7eb);">
              <td style="padding: 6px; font-family: monospace; font-weight: 600;">${escapeHtml(inv.id)}</td>
              <td style="padding: 6px;">${escapeHtml(inv.client_name)}</td>
              <td style="padding: 6px; font-weight: 700;">${escapeHtml(inv.currency)} ${parseFloat(inv.amount).toFixed(2)}</td>
              <td style="padding: 6px;"><span class="badge" style="background: #f3f4f6; font-size: 0.72rem;">${inv.method === 'paypal' ? '💳 PayPal' : '🏦 MCB'}</span></td>
              <td style="padding: 6px;">
                <span class="badge" style="background: ${inv.status === 'COMPLETED' ? '#ecfdf5' : '#fffbeb'}; color: ${inv.status === 'COMPLETED' ? '#059669' : '#d97706'}; font-weight: 700; font-size: 0.72rem;">
                  ${escapeHtml(inv.status)}
                </span>
              </td>
              <td style="padding: 6px; text-align: right; display: flex; justify-content: flex-end; gap: 4px;">
                <a href="/api/finance/invoices/${encodeURIComponent(inv.id)}/receipt" target="_blank" class="btn btn-secondary btn-sm" style="padding: 2px 6px; font-size: 0.72rem; text-decoration: none;" title="Official Printable Tax Receipt & Invoice">📄 Receipt</a>
                ${inv.payment_url ? `
                  <a href="${escapeHtml(inv.payment_url)}" target="_blank" class="btn btn-secondary btn-sm" style="padding: 2px 6px; font-size: 0.72rem; text-decoration: none;">Pay</a>
                ` : `
                  <button type="button" class="btn btn-secondary btn-sm" onclick="alert('Beneficiary: Deven Pawaray\\nMCB Acc: 000443260370\\nIBAN: MU57MCBL0944000443260370000MUR\\nSWIFT: MCBLMUMU\\nJuice: +230 58169420')" style="padding: 2px 6px; font-size: 0.72rem;">Info</button>
                `}
              </td>
            </tr>
          `).join("")}
        </tbody>
      </table>
    `;
  } catch (err) {
    console.error("Error fetching invoices:", err);
  }
}

// ==========================================
// OPERATION CASH FLOW & UNIFIED FEED ENGINE
// ==========================================

let currentUnifiedFeedEmails = [];
let activeFeedFilter = "all";
let currentReplyingEmail = null;

function setupRevenueAndProductivity() {
  fetchReceivables();
  fetchLeadsPipeline();
  fetchUnifiedFeed();

  const btnRefreshReceivables = document.getElementById("btnRefreshReceivables");
  if (btnRefreshReceivables) btnRefreshReceivables.addEventListener("click", fetchReceivables);

  const btnRunLiveMonetization = document.getElementById("btnRunLiveMonetization");
  if (btnRunLiveMonetization) btnRunLiveMonetization.addEventListener("click", handleRunLiveMonetizationDemo);

  const btnDiscoverLeads = document.getElementById("btnDiscoverLeads");
  if (btnDiscoverLeads) btnDiscoverLeads.addEventListener("click", handleDiscoverLeads);

  const btnRefreshUnifiedFeed = document.getElementById("btnRefreshUnifiedFeed");
  if (btnRefreshUnifiedFeed) btnRefreshUnifiedFeed.addEventListener("click", () => fetchUnifiedFeed(true));

  // Filter Pills for Unified Feed
  ["all", "revenue", "urgent"].forEach(f => {
    const btnId = `btnFilterFeed${f === 'all' ? 'All' : (f === 'revenue' ? 'Rev' : 'Urg')}`;
    const btn = document.getElementById(btnId);
    if (btn) {
      btn.addEventListener("click", () => {
        document.querySelectorAll(".filter-pill").forEach(p => p.classList.remove("active"));
        btn.classList.add("active");
        activeFeedFilter = f;
        renderUnifiedFeed();
      });
    }
  });

  // AI Reply Modal
  const btnCloseAIReply = document.getElementById("btnCloseAIReplyModal");
  if (btnCloseAIReply) {
    btnCloseAIReply.addEventListener("click", () => {
      document.getElementById("aiReplyModal").style.display = "none";
    });
  }

  const btnDraftAIReply = document.getElementById("btnDraftAIReply");
  if (btnDraftAIReply) btnDraftAIReply.addEventListener("click", handleGenerateAIReply);

  const btnCopyReplyDraft = document.getElementById("btnCopyReplyDraft");
  if (btnCopyReplyDraft) {
    btnCopyReplyDraft.addEventListener("click", () => {
      const txt = document.getElementById("replyDraftBody").value;
      navigator.clipboard.writeText(txt);
      showToast("📋 Draft copied to clipboard!", "success");
    });
  }

  const btnMarkReplied = document.getElementById("btnMarkReplied");
  if (btnMarkReplied) {
    btnMarkReplied.addEventListener("click", () => {
      const modal = document.getElementById("emailReplyModal") || document.getElementById("aiReplyModal");
      if (modal) modal.style.display = "none";
      showToast("✅ Action completed & recorded!", "success");
    });
  }

  const btnSendReplyViaSMTP = document.getElementById("btnSendReplyViaSMTP");
  if (btnSendReplyViaSMTP) {
    btnSendReplyViaSMTP.addEventListener("click", handleSendAIReplyViaSMTP);
  }

  // Lead Email Pitch Modal Listeners
  const btnCloseLeadEmailModal = document.getElementById("btnCloseLeadEmailModal");
  if (btnCloseLeadEmailModal) btnCloseLeadEmailModal.addEventListener("click", closeLeadEmailModal);

  const btnCancelLeadEmailModal = document.getElementById("btnCancelLeadEmailModal");
  if (btnCancelLeadEmailModal) btnCancelLeadEmailModal.addEventListener("click", closeLeadEmailModal);

  const btnDispatchLeadEmail = document.getElementById("btnDispatchLeadEmail");
  if (btnDispatchLeadEmail) btnDispatchLeadEmail.addEventListener("click", handleDispatchLeadEmail);

  // Option B: $249 Founder License Launchpad
  const btnGenLivePaypal = document.getElementById("btnGenLivePaypalLink");
  if (btnGenLivePaypal) btnGenLivePaypal.addEventListener("click", handleGenerateFounderOrder);

  const btnCopyPH = document.getElementById("btnCopyProductHuntCopy");
  if (btnCopyPH) {
    btnCopyPH.addEventListener("click", () => {
      const copy = `Nexus AI Workforce — 14 Autonomous AI Employees for Developers & Founders\n\nReplace 3 full-time ops hires with a 14-agent local AI fleet running on your own machine.\n\nIncludes 100% full source code, FastAPI backend, 25 defense safeguards, 5-inbox IMAP cleaner, and WhatsApp mobile dispatcher.\n\nGet the Founder License ($249 one-time): ${window.location.origin}/license`;
      navigator.clipboard.writeText(copy);
      showToast("📋 Copied Product Hunt / Gumroad listing!", "success");
    });
  }

  const btnCopyX = document.getElementById("btnCopyTwitterThread");
  if (btnCopyX) {
    btnCopyX.addEventListener("click", () => {
      const thread = `1/ Modern founders & solo devs lose 15+ hrs/week to non-billable ops: spam triage, tracking retainers, checking CVE breaks, and cloud bill spikes.\n\nWe spent 6 months building the solution: Nexus, a local 14-agent AI workforce.\n\n2/ Includes full source code, 25 defense safeguards, and runs 100% locally or in Docker.\n\nGet lifetime commercial access ($249 one-time):\n${window.location.origin}/license`;
      navigator.clipboard.writeText(thread);
      showToast("📋 Copied Twitter/X launch thread!", "success");
    });
  }

  const btnCopyDM = document.getElementById("btnCopyFounderColdDM");
  if (btnCopyDM) {
    btnCopyDM.addEventListener("click", () => {
      const dm = `Hey! Saw you're scaling your team. As a technical founder, how many hours a week do you lose triaging inboxes, tracking invoices, and watching repos?\n\nI built Nexus — an autonomous 14-agent workforce that runs locally to handle email triage, finance watchdogs, and morning WhatsApp digests.\n\nWe just launched the lifetime commercial source license ($249 one-time):\n${window.location.origin}/license\n\nWould love to know what you think! - Deven`;
      navigator.clipboard.writeText(dm);
      showToast("📋 Copied Founder Cold DM!", "success");
    });
  }

  // Option C: Mauritius WhatsApp Agency Pitch buttons
  document.querySelectorAll(".btn-quick-mru-pitch").forEach(btn => {
    btn.addEventListener("click", () => handleQuickMauritiusPitch(btn.dataset.sector));
  });

  const btnRunMruSim = document.getElementById("btnRunMruSim");
  if (btnRunMruSim) btnRunMruSim.addEventListener("click", handleRunMauritiusSim);
}

// 1. Receivables & Cash Inflow
async function fetchReceivables() {
  const container = document.getElementById("receivablesGrid");
  const overdueBadge = document.getElementById("receivablesOverdueBadge");
  const collectedBadge = document.getElementById("receivablesCollectedBadge");
  if (!container) return;

  try {
    const res = await fetch("/api/finance/receivables");
    if (!res.ok) return;
    const data = await res.json();

    // Strictly enforce exclusion of Travellounge
    const invoices = (data.invoices || []).filter(inv => !inv.client_name?.toLowerCase().includes("travellounge"));

    const overdueSum = invoices
      .filter(inv => inv.currency === "MUR" && inv.status !== "PAID" && inv.status !== "COMPLETED")
      .reduce((sum, inv) => sum + (parseFloat(inv.amount) || 0), 0);
    
    const collectedSum = invoices
      .filter(inv => inv.status === "PAID" || inv.status === "COMPLETED")
      .reduce((sum, inv) => sum + (parseFloat(inv.amount) || 0), 0) || (data.collected_mur || 0);

    if (overdueBadge) {
      overdueBadge.textContent = `Rs ${overdueSum.toLocaleString(undefined, {minimumFractionDigits: 2})}`;
      overdueBadge.style.color = overdueSum > 0 ? "#dc2626" : "#6b7280";
    }

    if (collectedBadge) {
      collectedBadge.textContent = `Rs ${collectedSum.toLocaleString(undefined, {minimumFractionDigits: 2})}`;
    }

    if (invoices.length === 0) {
      container.innerHTML = `
        <div style="padding: 20px; background: #fff; border: 1px dashed var(--border-subtle); border-radius: 8px; text-align: center; grid-column: 1 / -1;">
          <div style="font-size: 1.5rem; margin-bottom: 6px;">📂</div>
          <p style="color: #374151; font-weight: 700; font-size: 0.9rem; margin: 0 0 4px 0;">No Outstanding Receivables</p>
          <p style="color: #6b7280; font-size: 0.8rem; margin: 0 0 12px 0;">All past test seeds cleared. Zero existing client debts to chase.</p>
          <button type="button" class="btn btn-primary btn-sm" onclick="document.getElementById('btnOpenPaymentModal').click()" style="font-weight: 600; background: #111;">
            + Create Real Invoice / Payment Link
          </button>
        </div>
      `;
      return;
    }

    container.innerHTML = invoices.map(inv => {
      const isOverdue = inv.status?.includes("OVERDUE");
      const isPaid = inv.status === "PAID" || inv.status === "COMPLETED";
      const formattedAmount = `${inv.currency} ${parseFloat(inv.amount).toLocaleString(undefined, {minimumFractionDigits: 2})}`;

      if (isPaid) {
        return `
          <div class="card-panel" style="background: #fff; border: 1px solid #a7f3d0; padding: 14px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); display: flex; flex-direction: column; justify-content: space-between;">
            <div>
              <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                <div>
                  <span class="badge" style="background: #ecfdf5; color: #047857; font-weight: 700; font-size: 0.72rem;">
                    ✅ ${escapeHtml(inv.status)} (SETTLED)
                  </span>
                  <span style="font-size: 0.75rem; color: #6b7280; margin-left: 6px; font-family: monospace;">${escapeHtml(inv.id)}</span>
                </div>
                <div style="font-weight: 800; font-size: 1.05rem; color: #047857;">
                  ${formattedAmount}
                </div>
              </div>

              <h4 style="margin: 0 0 4px 0; font-size: 0.95rem; font-weight: 700;">${escapeHtml(inv.client_name)}</h4>
              <p style="margin: 0 0 8px 0; font-size: 0.8rem; color: #4b5563;">${escapeHtml(inv.description || "Turnkey Portal Deployment")}</p>
              
              <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 8px 10px; font-size: 0.75rem; color: #475569; margin-bottom: 10px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 3px;">
                  <span>🏦 <strong>Juice Ref:</strong> <code style="color: #047857; font-weight: 700;">${escapeHtml(inv.juice_ref || 'JUICE-VERIFIED')}</code></span>
                  <span style="color: #059669; font-weight: 700;">✓ Reconciled</span>
                </div>
                <div style="font-family: monospace; font-size: 0.7rem; color: #64748b; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                  🔐 Stamp: ${escapeHtml((inv.security_signature || '').slice(0, 24))}...
                </div>
              </div>
            </div>

            <div style="display: flex; gap: 8px; flex-wrap: wrap; border-top: 1px solid #f3f4f6; padding-top: 10px; margin-top: 6px;">
              <a href="/api/finance/invoices/${encodeURIComponent(inv.id)}/receipt" target="_blank" class="btn btn-secondary btn-sm" style="font-weight: 600; text-decoration: none; padding: 4px 10px; font-size: 0.76rem;">
                📄 Official Receipt
              </a>
              <button type="button" class="btn btn-secondary btn-sm btn-paid-wa" data-id="${inv.id}" data-client="${escapeHtml(inv.client_name)}" data-amount="${formattedAmount}" style="flex: 1; font-weight: 600; display: inline-flex; align-items: center; justify-content: center; gap: 4px; background: #ecfdf5; color: #047857; border: 1px solid #10b98144; font-size: 0.76rem;">
                📱 WhatsApp Receipt Link
              </button>
            </div>
          </div>
        `;
      }

      return `
        <div class="card-panel" style="background: #fff; border: 1px solid ${isOverdue ? '#fca5a5' : '#fde047'}; padding: 14px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); display: flex; flex-direction: column; justify-content: space-between;">
          <div>
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
              <div>
                <span class="badge" style="background: ${isOverdue ? '#fee2e2' : '#fef9c3'}; color: ${isOverdue ? '#b91c1c' : '#854d0e'}; font-weight: 700; font-size: 0.72rem;">
                  ⏳ ${escapeHtml(inv.status)}
                </span>
                <span style="font-size: 0.75rem; color: #6b7280; margin-left: 6px; font-family: monospace;">${escapeHtml(inv.id)}</span>
              </div>
              <div style="font-weight: 800; font-size: 1.05rem; color: ${isOverdue ? '#dc2626' : '#1e1b4b'};">
                ${formattedAmount}
              </div>
            </div>

            <h4 style="margin: 0 0 4px 0; font-size: 0.95rem; font-weight: 700;">${escapeHtml(inv.client_name)}</h4>
            <p style="margin: 0 0 8px 0; font-size: 0.8rem; color: #4b5563;">${escapeHtml(inv.description || "Client Invoice")}</p>
            
            <div style="background: #fffbeb; border: 1px solid #fef3c7; border-radius: 6px; padding: 8px 10px; font-size: 0.75rem; color: #92400e; margin-bottom: 10px;">
              📱 MCB Juice: <strong>+230 58169420</strong> (Deven Pawaray) | Ref: <strong>${escapeHtml(inv.id)}</strong>
            </div>
          </div>

          <div style="display: flex; gap: 6px; flex-wrap: wrap; border-top: 1px solid #f3f4f6; padding-top: 10px; margin-top: 6px;">
            <button type="button" class="btn btn-secondary btn-sm btn-remind-wa" data-id="${inv.id}" style="flex: 1; font-weight: 700; display: inline-flex; align-items: center; justify-content: center; gap: 4px; background: #ecfdf5; color: #047857; border: 1px solid #10b98144; font-size: 0.75rem;">
              📱 WhatsApp Payment Request
            </button>
            <button type="button" class="btn btn-secondary btn-sm btn-verify-juice" data-id="${inv.id}" style="font-weight: 700; background: #eff6ff; color: #1d4ed8; border: 1px solid #3b82f644; font-size: 0.75rem;">
              🛡️ Verify Juice Ref
            </button>
            <button type="button" class="btn btn-secondary btn-sm btn-mark-paid" data-id="${inv.id}" style="font-weight: 600; background: #f9fafb; font-size: 0.75rem;">
              ✅ Settle
            </button>
            <a href="/api/finance/invoices/${encodeURIComponent(inv.id)}/receipt" target="_blank" class="btn btn-secondary btn-sm" style="font-weight: 600; text-decoration: none; padding: 4px 8px; font-size: 0.74rem;">
              📄 View
            </a>
          </div>
        </div>
      `;
    }).join("");

    // Attach button listeners
    container.querySelectorAll(".btn-remind-wa").forEach(btn => {
      btn.addEventListener("click", () => handleSendWhatsAppReminder(btn.dataset.id));
    });
    container.querySelectorAll(".btn-verify-juice").forEach(btn => {
      btn.addEventListener("click", () => handleVerifyJuice(btn.dataset.id));
    });
    container.querySelectorAll(".btn-mark-paid").forEach(btn => {
      btn.addEventListener("click", () => handleMarkInvoicePaid(btn.dataset.id));
    });
    container.querySelectorAll(".btn-paid-wa").forEach(btn => {
      btn.addEventListener("click", () => {
        const id = btn.dataset.id;
        const client = btn.dataset.client;
        const msg = `Bonjour ${client} ! 🤝\n\nNous confirmons la bonne réception de votre règlement pour la facture *${id}*.\n\nVotre reçu officiel & certificat d'intégrité est accessible ici :\n${window.location.origin}/api/finance/invoices/${encodeURIComponent(id)}/receipt\n\nMerci pour votre confiance !\nDeven Pawaray — Nexus AI Solutions`;
        window.open(`https://wa.me/?text=${encodeURIComponent(msg)}`, "_blank");
      });
    });

  } catch (err) {
    console.error("Error fetching receivables:", err);
  }
}

async function handleVerifyJuice(invoiceId) {
  const ref = prompt("Enter Client MCB Juice Reference (e.g. JCE9842193 or Transaction Code):", "JUICE-DEVEN-9417");
  if (!ref) return;
  const phone = prompt("Enter Payer Phone Number (+230):", "+230 58169420");

  try {
    showToast("Verifying Juice transfer and checking replay shield...", "info");
    const res = await fetch(`/api/finance/invoices/${encodeURIComponent(invoiceId)}/verify-juice`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ juice_ref: ref, payer_phone: phone || "+230 58169420" })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Juice verification rejected");

    showToast(`✅ Payment Verified! Token: ${data.reconciliation_token}`, "success");
    fetchReceivables();
    fetchRecentInvoices();
  } catch (err) {
    showToast(`Security Shield Alert: ${err.message}`, "error");
  }
}

async function handleSendWhatsAppReminder(invoiceId) {
  try {
    showToast("Generating WhatsApp Juice reminder...", "info");
    const res = await fetch(`/api/finance/invoices/${invoiceId}/remind-whatsapp`, { method: "POST" });
    if (!res.ok) throw new Error("Could not generate reminder");
    const data = await res.json();
    
    if (data.reminder?.whatsapp_link) {
      window.open(data.reminder.whatsapp_link, "_blank");
      showToast("Opened WhatsApp with pre-filled Juice instructions!", "success");
    } else {
      showToast("Reminder drafted! Check Mobile Dispatcher.", "success");
    }
  } catch (err) {
    showToast(`Error: ${err.message}`, "error");
  }
}

async function handleMarkInvoicePaid(invoiceId) {
  try {
    const res = await fetch(`/api/finance/invoices/${invoiceId}/mark-paid`, { method: "POST" });
    if (!res.ok) throw new Error("Could not update invoice");
    showToast(`Invoice ${invoiceId} marked as PAID!`, "success");
    fetchReceivables();
    fetchRecentInvoices();
  } catch (err) {
    showToast(`Error: ${err.message}`, "error");
  }
}

// 2. Outbound Lead Acquisition Pipeline
let cachedLeadsMap = {};

async function fetchLeadsPipeline() {
  const container = document.getElementById("leadsPipelineList");
  if (!container) return;

  try {
    const res = await fetch("/api/leads/pipeline");
    if (!res.ok) return;
    const data = await res.json();
    let leads = data.leads || [];

    // Deduplicate leads by company name
    const seen = new Set();
    leads = leads.filter(l => {
      if (!l.company || seen.has(l.company.toLowerCase())) return false;
      seen.add(l.company.toLowerCase());
      return true;
    });

    cachedLeadsMap = {};
    leads.forEach(l => { cachedLeadsMap[l.id] = l; });

    if (leads.length === 0) {
      container.innerHTML = `<p style="color: #9ca3af; font-size: 0.85rem; padding: 8px;">No leads generated yet. Click "Discover Leads" above.</p>`;
      return;
    }

    container.innerHTML = leads.map(lead => {
      const demoUrl = lead.offer_name?.match(/https:\/\/[^\s\)]+/)?.[0] || (lead.website?.includes('vercel.app') ? lead.website : null);
      const displayPrice = lead.pricing || (lead.niche === 'global_startups' ? '$249 USD' : 'Rs 45,000 MUR');

      return `
      <div class="card-panel" style="background: #fff; border: 1px solid var(--border-subtle); padding: 14px; border-radius: 8px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 1px 3px rgba(0,0,0,0.04);">
        <div>
          <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 6px; gap: 6px; flex-wrap: wrap;">
            <div style="display: flex; gap: 4px; align-items: center; flex-wrap: wrap;">
              <span class="badge" style="background: #eff6ff; color: #1d4ed8; font-weight: 700; font-size: 0.72rem;">
                🎯 ${lead.fit_score || 90}% Match • ${escapeHtml(lead.match_tier || 'Tier 1 High Fit')}
              </span>
              ${lead.status === 'PITCHED' ? `
                <span class="badge" style="background: #fdf2f8; color: #be185d; font-weight: 800; font-size: 0.7rem; border: 1px solid #f472b644;">
                  🚀 PITCHED (${escapeHtml(lead.pitch_sent_via || 'email')})
                </span>
              ` : ''}
            </div>
            <span style="font-size: 0.78rem; color: #047857; font-weight: 800; background: #ecfdf5; padding: 2px 6px; border-radius: 4px; border: 1px solid #10b98133;">
              ${escapeHtml(displayPrice)}
            </span>
          </div>

          <h4 style="margin: 0 0 2px 0; font-size: 0.95rem; font-weight: 700; color: #111827;">${escapeHtml(lead.company)}</h4>
          <div style="font-size: 0.8rem; color: #6b7280; margin-bottom: 6px;">
            👤 ${escapeHtml(lead.contact_name)} (${escapeHtml(lead.contact_role || 'Executive')})
            ${lead.contact_email ? ` • <span style="color: #2563eb;">${escapeHtml(lead.contact_email)}</span>` : ''}
          </div>

          <p style="margin: 0 0 10px 0; font-size: 0.78rem; color: #4b5563; line-height: 1.35;">
            <strong>Bottleneck:</strong> ${escapeHtml(lead.pain_point || 'Scaling customer communication & ops fatigue')}
          </p>

          ${demoUrl ? `
            <div style="margin-bottom: 10px;">
              <a href="${escapeHtml(demoUrl)}" target="_blank" rel="noopener" style="font-size: 0.74rem; color: #2563eb; text-decoration: none; font-weight: 600; display: inline-flex; align-items: center; gap: 4px;">
                🌐 Live Asset Demo: ${escapeHtml(demoUrl.replace('https://', ''))} ↗
              </a>
            </div>
          ` : ''}
        </div>

        <div style="border-top: 1px solid #f3f4f6; padding-top: 10px; margin-top: 6px;">
          <div style="display: flex; gap: 6px; flex-wrap: wrap;">
            <button type="button" class="btn btn-primary btn-sm btn-lead-wa" data-id="${lead.id}" style="flex: 1.1; font-weight: 700; background: #059669; color: #fff; display: inline-flex; align-items: center; justify-content: center; gap: 4px; font-size: 0.75rem; padding: 6px 8px;">
              📱 WhatsApp
            </button>
            <button type="button" class="btn btn-secondary btn-sm btn-lead-email" data-id="${lead.id}" style="flex: 1.1; font-weight: 700; background: #2563eb; color: #fff; display: inline-flex; align-items: center; justify-content: center; gap: 4px; font-size: 0.75rem; padding: 6px 8px;">
              ✉️ Email Pitch
            </button>
            <button type="button" class="btn btn-secondary btn-sm btn-lead-mint-inv" data-id="${lead.id}" style="flex: 1; font-weight: 700; background: #1e1b4b; color: #fff; display: inline-flex; align-items: center; justify-content: center; gap: 4px; font-size: 0.75rem; padding: 6px 8px;">
              💳 Invoice
            </button>
            <button type="button" class="btn btn-secondary btn-sm btn-craft-pitch" data-id="${lead.id}" style="font-weight: 600; background: #f8fafc; color: #374151; font-size: 0.75rem; padding: 6px 8px;">
              ✨ Pitch
            </button>
          </div>
        </div>
      </div>
      `;
    }).join("");

    container.querySelectorAll(".btn-lead-wa").forEach(btn => {
      btn.addEventListener("click", () => handleLeadWhatsAppOutreach(btn.dataset.id));
    });
    container.querySelectorAll(".btn-lead-email").forEach(btn => {
      btn.addEventListener("click", () => handleLeadEmailPitch(btn.dataset.id));
    });
    container.querySelectorAll(".btn-lead-mint-inv").forEach(btn => {
      btn.addEventListener("click", () => handleLeadMintInvoice(btn.dataset.id));
    });
    container.querySelectorAll(".btn-craft-pitch").forEach(btn => {
      btn.addEventListener("click", () => handlePitchForLead(btn.dataset.id));
    });

  } catch (err) {
    console.error("Error fetching leads:", err);
  }
}

async function handleLeadWhatsAppOutreach(leadId) {
  const lead = cachedLeadsMap[leadId];
  if (!lead) return;

  try {
    showToast(`Preparing direct WhatsApp pitch for ${lead.company}...`, "info");
    let pitchText = lead.pitch_draft;

    if (!pitchText) {
      const res = await fetch(`/api/leads/${leadId}/pitch`, { method: "POST" });
      if (res.ok) {
        const data = await res.json();
        pitchText = data.pitch;
        lead.pitch_draft = pitchText;
      }
    }

    if (!pitchText) {
      pitchText = `Bonjour ${lead.contact_name} 👋,\n\nJ'espère que vous vous portez bien ainsi que toute l'équipe de *${lead.company}*.\n\nNous avons conçu une solution clé-en-main pour résoudre : ${lead.pain_point}.\n\nSeriez-vous disponible pour un court échange de 5 minutes ?\n\nBien à vous,\nDeven Pawaray — Nexus AI (+230 58169420)`;
    }

    const waUrl = `https://wa.me/?text=${encodeURIComponent(pitchText)}`;
    window.open(waUrl, "_blank");
    showToast(`🚀 WhatsApp opened with tailored pitch for ${lead.company}!`, "success");
  } catch (err) {
    showToast(`Error: ${err.message}`, "error");
  }
}

async function handleLeadMintInvoice(leadId) {
  const lead = cachedLeadsMap[leadId];
  if (!lead) return;

  const isGlobal = lead.niche === 'global_startups' || lead.pricing?.includes('$');
  const currency = isGlobal ? 'USD' : 'MUR';
  const amount = isGlobal ? 249 : 45000;
  const desc = lead.offer_name || `${lead.company} — Turnkey AI & Portal Solution`;

  const confirmed = confirm(`Mint official commercial invoice for:\n\nClient: ${lead.company}\nAmount: ${currency} ${amount.toLocaleString()}\nDescription: ${desc}\n\nProceed?`);
  if (!confirmed) return;

  try {
    showToast("Minting cryptographically stamped invoice...", "info");
    const res = await fetch("/api/finance/payment-link", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        client_name: lead.company,
        client_email: lead.contact_email || "billing@client.mu",
        amount: amount,
        currency: currency,
        description: desc,
        method: "mcb_wire"
      })
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Failed to mint invoice");

    const inv = data.invoice;
    showToast(`✅ Invoice ${inv.id} Minted! Total: ${inv.currency} ${inv.amount.toLocaleString()}`, "success");

    // Refresh receivables immediately
    await fetchReceivables();

    // Offer to send WhatsApp payment request immediately
    const sendNow = confirm(`Invoice ${inv.id} created successfully!\n\nWould you like to open WhatsApp now to send the payment details directly to ${lead.company}?`);
    if (sendNow) {
      handleSendWhatsAppReminder(inv.id);
    }
  } catch (err) {
    showToast(`Error: ${err.message}`, "error");
  }
}

async function handleLeadEmailPitch(leadId) {
  const lead = cachedLeadsMap[leadId];
  if (!lead) return;

  const modal = document.getElementById("leadEmailModal");
  if (!modal) return;

  document.getElementById("leadEmailModalLeadId").value = lead.id;
  document.getElementById("leadEmailRecipient").value = lead.contact_email || lead.email || "";
  document.getElementById("leadEmailSubject").value = lead.pitch_subject || `Operations & Customer Response Suite for ${lead.company}`;

  const title = document.getElementById("leadEmailModalTitle");
  if (title) title.textContent = `Email Pitch: ${lead.company}`;

  let pitchText = lead.pitch_draft;
  if (!pitchText) {
    showToast(`Drafting personalized pitch for ${lead.company}...`, "info");
    try {
      const res = await fetch(`/api/leads/${encodeURIComponent(lead.id)}/pitch`, { method: "POST" });
      if (res.ok) {
        const data = await res.json();
        pitchText = data.pitch;
        lead.pitch_draft = pitchText;
      }
    } catch (e) {
      console.warn("Could not craft pitch:", e);
    }
  }

  document.getElementById("leadEmailBody").value = pitchText || `Bonjour ${lead.contact_name} 👋,\n\nNous avons conçu une solution d'automatisation pour ${lead.company}.\n\nSeriez-vous disponible pour un court échange cette semaine ?\n\nBien cordialement,\nDeven Pawaray\nNexus AI Solutions (+230 58169420)`;
  modal.style.display = "flex";
}

function closeLeadEmailModal() {
  const modal = document.getElementById("leadEmailModal");
  if (modal) modal.style.display = "none";
}

async function handleDispatchLeadEmail() {
  const leadId = document.getElementById("leadEmailModalLeadId").value;
  const recipient = document.getElementById("leadEmailRecipient").value.trim();
  const subject = document.getElementById("leadEmailSubject").value.trim();
  const body = document.getElementById("leadEmailBody").value.trim();
  const accountId = document.getElementById("leadEmailAccount")?.value || "acc_1";
  const btn = document.getElementById("btnDispatchLeadEmail");

  if (!recipient || !recipient.includes("@")) {
    showToast("Please enter a valid recipient email address", "error");
    return;
  }
  if (!body) {
    showToast("Pitch body cannot be empty", "error");
    return;
  }

  const confirmed = confirm(`Dispatch outreach pitch email to:\n\nRecipient: ${recipient}\nSubject: ${subject}\n\nProceed?`);
  if (!confirmed) return;

  try {
    if (btn) {
      btn.textContent = "⚡ Dispatching via SMTP...";
      btn.disabled = true;
    }

    const res = await fetch(`/api/leads/${encodeURIComponent(leadId)}/dispatch-email`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        account_id: accountId,
        custom_pitch: body,
        subject: subject
      })
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Dispatch failed");

    showToast(`🚀 Outreach pitch dispatched to ${recipient}!`, "success");
    closeLeadEmailModal();
    await fetchLeadsPipeline();
  } catch (err) {
    showToast(`Dispatch error: ${err.message}`, "error");
  } finally {
    if (btn) {
      btn.textContent = "🚀 Dispatch Outreach Email";
      btn.disabled = false;
    }
  }
}

async function handleRunLiveMonetizationDemo() {
  const btn = document.getElementById("btnRunLiveMonetization");
  if (btn) btn.disabled = true;


  try {
    showToast("🚀 Starting Live Monetization Demo: Step 1 (Prospect Discovery)...", "info");
    
    // Step 1: Discover / fetch leads
    const resLeads = await fetch("/api/leads/discover", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ niche: "medical360_portal" })
    });
    const leadsData = await resLeads.json();
    const targetLead = leadsData.leads?.[0] || { company: "Medical 360 Clinic", id: "lead_demo", contact_name: "Dr. Salim" };

    showToast(`🎯 Step 1: Identified ${targetLead.company} (${targetLead.fit_score || 94}% ICP Fit)`, "success");
    await new Promise(r => setTimeout(r, 800));

    // Step 2: Craft Pitch
    showToast(`✨ Step 2: Crafting tailored localized value proposition...`, "info");
    try {
      await fetch(`/api/leads/${targetLead.id}/pitch`, { method: "POST" });
    } catch(e) {}
    showToast(`📝 Step 2: Proposal packaged with turnkey demo URL!`, "success");
    await new Promise(r => setTimeout(r, 800));

    // Step 3: Mint Commercial Invoice
    showToast(`💳 Step 3: Minting HMAC-SHA256 commercial invoice for Rs 45,000...`, "info");
    const resInv = await fetch("/api/finance/payment-link", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        client_name: targetLead.company,
        client_email: "billing@medical360.mu",
        amount: 45000,
        currency: "MUR",
        description: "Medical 360™ Turnkey Clinic Operations Portal (Frontend Deployment)",
        method: "mcb_wire"
      })
    });
    const invData = await resInv.json();
    const invId = invData.invoice?.id;
    showToast(`📑 Step 3: Invoice ${invId} minted! Anti-tamper stamp attached.`, "success");
    await new Promise(r => setTimeout(r, 800));

    // Step 4: WhatsApp link ready
    showToast(`📱 Step 4: 1-Click WhatsApp payment link ready (wa.me payload generated).`, "info");
    await new Promise(r => setTimeout(r, 800));

    // Step 5: Simulate Juice Settlement
    const juiceRef = `JUICE-DEVEN-${invId.slice(-4)}`;
    showToast(`🏦 Step 5: Reconciling MCB Juice transfer (${juiceRef})...`, "info");
    const resJuice = await fetch(`/api/finance/invoices/${encodeURIComponent(invId)}/verify-juice`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        juice_ref: juiceRef,
        payer_phone: "+23058169420",
        amount_paid: 45000
      })
    });
    const juiceData = await resJuice.json();
    showToast(`✅ Step 5: Settlement verified! Replay shield passed. Token: ${juiceData.reconciliation_token}`, "success");
    await new Promise(r => setTimeout(r, 800));

    // Step 6: Verify Ledger
    const resLedger = await fetch("/api/finance/ledger-integrity");
    const ledgerData = await resLedger.json();
    showToast(`🔐 Step 6: Cryptographic ledger verified! Hash chain valid: ${ledgerData.valid}`, "success");

    // Refresh all UI elements
    await fetchReceivables();
    await fetchLeadsPipeline();

    alert(`🎉 Live Monetization Walkthrough Completed Successfully!\n\n1. Target Discovered: ${targetLead.company}\n2. Value Proposition Crafted\n3. Commercial Invoice Minted: ${invId} (MUR 45,000.00)\n4. WhatsApp wa.me Dispatch URL Prepared\n5. Settled via MCB Juice (${juiceRef})\n6. Cryptographically Sealed on Blockchain Ledger\n\nLook at the Receivables & Cash Inflow Center above — your settled invoice and receipts are live!`);

  } catch (err) {
    showToast(`Demo Error: ${err.message}`, "error");
  } finally {
    if (btn) btn.disabled = false;
  }
}

async function handleDiscoverLeads() {
  const select = document.getElementById("leadNicheSelect");
  const niche = select ? select.value : "medical360_portal";
  const btn = document.getElementById("btnDiscoverLeads");

  try {
    if (btn) btn.textContent = "⚡ Discovering...";
    const res = await fetch("/api/leads/discover", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ niche })
    });
    if (!res.ok) throw new Error("Failed to discover leads");
    showToast("Discovered and scored new target prospects!", "success");
    fetchLeadsPipeline();
  } catch (err) {
    showToast(`Error: ${err.message}`, "error");
  } finally {
    if (btn) btn.textContent = "⚡ Discover Leads";
  }
}

async function handlePitchForLead(leadId) {
  try {
    showToast("Generating personalized commercial pitch...", "info");
    const res = await fetch(`/api/leads/${leadId}/pitch`, { method: "POST" });
    if (!res.ok) throw new Error("Could not craft pitch");
    const data = await res.json();

    if (data.pitch) {
      // Render pitch inline beneath the lead card (no alert)
      const btn = document.querySelector(`.btn-craft-pitch[data-id="${leadId}"]`);
      const card = btn ? btn.closest('.card-panel') : null;
      if (card) {
        // Remove any existing pitch box for this card
        const existing = card.querySelector('.pitch-result-box');
        if (existing) {
          existing.remove();
          return; // Acts as toggle
        }

        const box = document.createElement('div');
        box.className = 'pitch-result-box';
        box.style.cssText = 'margin-top:12px;padding:12px 14px;background:#f0fdf4;border:1px solid #10b98133;border-radius:8px;font-size:0.82rem;line-height:1.55;color:#1e293b;white-space:pre-wrap;position:relative;';
        box.innerHTML = `
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
            <span style="font-size:0.75rem;font-weight:700;color:#047857;text-transform:uppercase;">🎯 Personalized Proposal</span>
            <div style="display:flex;gap:6px;">
              <button onclick="navigator.clipboard.writeText(this.closest('.pitch-result-box').querySelector('.pitch-text').textContent);showToast('📋 Pitch copied!','success');" class="btn btn-secondary btn-sm" style="padding:2px 8px;font-size:0.72rem;font-weight:700;">📋 Copy</button>
              <button onclick="window.open('https://wa.me/?text=' + encodeURIComponent(this.closest('.pitch-result-box').querySelector('.pitch-text').textContent), '_blank');" class="btn btn-primary btn-sm" style="padding:2px 8px;font-size:0.72rem;font-weight:700;background:#059669;color:#fff;">📱 Send WA</button>
            </div>
          </div>
          <div class="pitch-text">${escapeHtml(data.pitch)}</div>
        `;
        card.appendChild(box);
        box.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      } else {
        navigator.clipboard.writeText(data.pitch);
        showToast("🎯 Pitch crafted & copied to clipboard!", "success");
      }
      fetchLeadsPipeline();
    }
  } catch (err) {
    showToast(`Error: ${err.message}`, "error");
  }
}

// 3. Unified Multi-Inbox Feed
async function fetchUnifiedFeed(showNotification = false) {
  const container = document.getElementById("unifiedFeedContainer");
  if (!container) return;

  try {
    const res = await fetch("/api/email/unified-feed?limit=5");
    if (!res.ok) return;
    const data = await res.json();

    currentUnifiedFeedEmails = data.emails || [];

    // Update Pill Badges
    const cAll = document.getElementById("feedCountAll");
    const cRev = document.getElementById("feedCountRev");
    const cUrg = document.getElementById("feedCountUrg");
    if (cAll) cAll.textContent = data.total || 0;
    if (cRev) cRev.textContent = data.revenue_count || 0;
    if (cUrg) cUrg.textContent = data.urgent_count || 0;

    renderUnifiedFeed();
    if (showNotification) showToast("Refreshed unified feed across all inboxes!", "success");
  } catch (err) {
    console.error("Error fetching unified feed:", err);
  }
}

function renderUnifiedFeed() {
  const container = document.getElementById("unifiedFeedContainer");
  if (!container) return;

  let filtered = currentUnifiedFeedEmails;
  if (activeFeedFilter === "revenue") {
    filtered = currentUnifiedFeedEmails.filter(e => e.category === "revenue");
  } else if (activeFeedFilter === "urgent") {
    filtered = currentUnifiedFeedEmails.filter(e => e.category === "urgent");
  }

  if (filtered.length === 0) {
    container.innerHTML = `<div class="empty-state" style="padding: 20px;"><p>No emails found in this category.</p></div>`;
    return;
  }

  container.innerHTML = filtered.map(item => {
    const isRev = item.category === "revenue";
    const isUrg = item.category === "urgent";

    return `
      <div class="card-panel" style="background: #fff; border-left: 4px solid ${isRev ? '#10b981' : (isUrg ? '#ef4444' : '#64748b')}; padding: 12px 14px; margin: 0; box-shadow: 0 1px 2px rgba(0,0,0,0.03);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; flex-wrap: wrap; gap: 6px;">
          <div style="display: flex; align-items: center; gap: 8px;">
            <span class="badge" style="background: #f1f5f9; color: #334155; font-size: 0.72rem; font-weight: 600;">
              📧 ${escapeHtml(item.account_label || item.account_email)}
            </span>
            <span class="badge" style="background: ${isRev ? '#ecfdf5' : (isUrg ? '#fee2e2' : '#f8fafc')}; color: ${isRev ? '#047857' : (isUrg ? '#b91c1c' : '#475569')}; font-weight: 700; font-size: 0.72rem;">
              ${escapeHtml(item.category_label || 'General')}
            </span>
          </div>
          <span style="font-size: 0.75rem; color: #9ca3af;">${escapeHtml(item.date)}</span>
        </div>

        <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 12px;">
          <div style="flex: 1;">
            <div style="font-weight: 700; font-size: 0.92rem; color: #111; margin-bottom: 2px;">
              ${escapeHtml(item.subject)}
            </div>
            <div style="font-size: 0.8rem; color: #6b7280; margin-bottom: 6px;">
              From: <strong style="color: #374151;">${escapeHtml(item.sender)}</strong>
            </div>
            <p style="margin: 0; font-size: 0.82rem; color: #4b5563; line-height: 1.4;">
              ${escapeHtml(item.preview || item.body?.slice(0, 150) || "")}
            </p>
          </div>

          <button type="button" class="btn btn-secondary btn-sm btn-open-reply" data-id="${item.id}" style="white-space: nowrap; font-weight: 600; display: inline-flex; align-items: center; gap: 4px; background: #ecfdf5; color: #047857; border: 1px solid #10b98144;">
            ✨ AI Reply
          </button>
        </div>
      </div>
    `;
  }).join("");

  container.querySelectorAll(".btn-open-reply").forEach(btn => {
    btn.addEventListener("click", () => {
      const email = currentUnifiedFeedEmails.find(e => e.id === btn.dataset.id);
      if (email) openAIReplyModal(email);
    });
  });
}

function openAIReplyModal(email) {
  currentReplyingEmail = email;
  const modal = document.getElementById("aiReplyModal");
  if (!modal) return;

  document.getElementById("replySenderSubtitle").textContent = `Reply to ${email.sender}`;
  document.getElementById("replyOriginalSubject").textContent = email.subject;
  document.getElementById("replyOriginalPreview").textContent = email.body || email.preview;

  // Reset results
  document.getElementById("replyDraftBox").style.display = "none";
  document.getElementById("replyDraftBody").value = "";
  document.getElementById("replyCustomNotes").value = "";

  modal.classList.add("open");
}

async function handleGenerateAIReply() {
  if (!currentReplyingEmail) return;
  const btn = document.getElementById("btnDraftAIReply");
  const draftBox = document.getElementById("replyDraftBox");
  const language = document.getElementById("replyLanguage").value;
  const tone = document.getElementById("replyTone").value;
  const notes = document.getElementById("replyCustomNotes").value;

  try {
    if (btn) {
      btn.textContent = "⚡ Generating with Gemini 2.5 Flash...";
      btn.disabled = true;
    }

    const res = await fetch("/api/email/ai-reply", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        sender: currentReplyingEmail.sender,
        subject: currentReplyingEmail.subject,
        body: currentReplyingEmail.body || currentReplyingEmail.preview,
        user_notes: notes,
        tone: tone,
        language: language
      })
    });

    if (!res.ok) throw new Error("Failed to generate reply");
    const data = await res.json();

    draftBox.style.display = "block";
    document.getElementById("replyDraftSubject").value = data.subject || `Re: ${currentReplyingEmail.subject}`;
    document.getElementById("replyDraftBody").value = data.draft || "";
    document.getElementById("replyEngineBadge").textContent = data.engine || "Gemini 2.5 Flash";

    showToast("✨ AI response generated!", "success");
  } catch (err) {
    showToast(`Error: ${err.message}`, "error");
  } finally {
    if (btn) {
      btn.textContent = "✨ Draft Response with Gemini 2.5";
      btn.disabled = false;
    }
  }
}

async function handleSendAIReplyViaSMTP() {
  if (!currentReplyingEmail) return;

  const btn = document.getElementById("btnSendReplyViaSMTP");
  const subject = document.getElementById("replyDraftSubject").value.trim();
  const body = document.getElementById("replyDraftBody").value.trim();
  const accountId = document.getElementById("replySenderAccount")?.value || "acc_1";

  const rawSender = currentReplyingEmail.reply_to || currentReplyingEmail.sender || "";
  const emailMatch = rawSender.match(/<([^>]+)>/);
  const recipientEmail = emailMatch ? emailMatch[1] : (rawSender.includes("@") ? rawSender.trim() : "");

  if (!recipientEmail) {
    showToast("Error: Could not determine recipient email address", "error");
    return;
  }
  if (!body) {
    showToast("Error: Response draft body cannot be empty", "error");
    return;
  }

  const confirmed = confirm(`Transmit live reply via SMTP to:\n\nRecipient: ${recipientEmail}\nSubject: ${subject}\n\nProceed?`);
  if (!confirmed) return;

  try {
    if (btn) {
      btn.textContent = "⚡ Sending via SMTP...";
      btn.disabled = true;
    }

    const res = await fetch("/api/email/send", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        account_id: accountId,
        to_email: recipientEmail,
        subject: subject,
        body: body
      })
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "SMTP transmission failed");

    showToast(`🚀 Email sent to ${recipientEmail} from ${data.sender}!`, "success");
    const modal = document.getElementById("emailReplyModal");
    if (modal) modal.style.display = "none";
    if (typeof fetchUnifiedInboxFeed === "function") fetchUnifiedInboxFeed();
  } catch (err) {
    showToast(`SMTP Error: ${err.message}`, "error");
  } finally {
    if (btn) {
      btn.textContent = "🚀 Send Email via SMTP";
      btn.disabled = false;
    }
  }
}

// 4. Options B & C Actions


async function handleGenerateFounderOrder() {
  const btn = document.getElementById("btnGenLivePaypalLink");
  try {
    if (btn) btn.textContent = "⚡ Generating Live PayPal Order...";
    const res = await fetch("/api/finance/payment-link", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        client_name: "Founder Licensee",
        client_email: "",
        amount: 249.00,
        currency: "USD",
        description: "Nexus Autonomous 14-Agent Workforce Founder License",
        method: "paypal"
      })
    });
    const data = await res.json();
    if (data.invoice?.payment_url) {
      navigator.clipboard.writeText(data.invoice.payment_url);
      alert(`💳 Live PayPal Order Created!\n\nApprove URL:\n${data.invoice.payment_url}\n\n(Copied to clipboard)`);
      window.open(data.invoice.payment_url, "_blank");
    }
  } catch (err) {
    showToast(`PayPal Error: ${err.message}`, "error");
  } finally {
    if (btn) btn.textContent = "💳 Generate $249 Order Link";
  }
}

async function handleQuickMauritiusPitch(sectorId) {
  try {
    const phone = prompt("Enter Client WhatsApp Number (e.g. +230 58169420 or local number):", "+230 ");
    if (!phone) return;

    const res = await fetch("/api/mauritius/whatsapp-link", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ phone, sector_id: sectorId })
    });
    const data = await res.json();
    if (data.whatsapp_url) {
      window.open(data.whatsapp_url, "_blank");
      showToast("Opened WhatsApp with tailored Mauritius pitch!", "success");
    }
  } catch (err) {
    showToast(`Error: ${err.message}`, "error");
  }
}

async function handleRunMauritiusSim() {
  const input = document.getElementById("mruSimInput");
  const output = document.getElementById("mruSimOutput");
  const btn = document.getElementById("btnRunMruSim");
  const sectorSelect = document.getElementById("mruSimSector");
  const sectorId = sectorSelect ? sectorSelect.value : "ennrevennsourir_ngo";
  if (!input || !output) return;

  try {
    if (btn) {
      btn.textContent = "⚡ Thinking...";
      btn.disabled = true;
    }
    const res = await fetch("/api/mauritius/demo-reply", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        guest_message: input.value,
        sector_id: sectorId
      })
    });
    const data = await res.json();
    output.style.display = "block";
    output.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
        <span style="font-size: 0.72rem; color: #047857; font-weight: 700;">🤖 AI RESPONSE (${escapeHtml(data.engine || "Concierge Engine")}):</span>
        <span class="badge" style="font-size: 0.68rem; background: #ecfdf5; color: #047857;">Live Demo</span>
      </div>
      <div style="white-space: pre-wrap; font-size: 0.82rem; line-height: 1.45;">${escapeHtml(data.reply)}</div>
    `;
  } catch (err) {
    showToast(`Simulation error: ${err.message}`, "error");
  } finally {
    if (btn) {
      btn.textContent = "⚡ Test AI Reply";
      btn.disabled = false;
    }
  }
}

// When user changes sector dropdown in simulator, update prompt suggestion
const mruSimSectorEl = document.getElementById("mruSimSector");
if (mruSimSectorEl) {
  mruSimSectorEl.addEventListener("change", (e) => {
    const input = document.getElementById("mruSimInput");
    if (!input) return;
    const s = e.target.value;
    if (s === "ennrevennsourir_ngo") {
      input.value = "Bonjour, comment puis-je faire un don pour un enfant ou parrainer une chirurgie ?";
    } else if (s === "medical360_portal") {
      input.value = "Bonjour docteur, je souhaite prendre rendez-vous avec un cardiologue pour jeudi.";
    } else if (s === "itravellix_saas") {
      input.value = "Bonjour, avez-vous des forfaits hôtel 5 étoiles avec vol pour la semaine prochaine ?";
    } else if (s === "villas_hospitality") {
      input.value = "Bonjour, avez-vous des disponibilités pour une villa 3 chambres avec piscine à Grand Baie ?";
    } else if (s === "excursions_cruises") {
      input.value = "Bonjour, quel est le tarif pour la sortie catamaran aux dauphins à l'Ile aux Bénitiers ?";
    } else if (s === "car_rentals") {
      input.value = "Bonjour, avez-vous un SUV disponible pour 7 jours à l'aéroport avec livraison ?";
    }
  });
}

// =========================================================================
// 🌙 24/7 AUTONOMOUS NIGHT SHIFT & OVERNIGHT FLIGHT RECORDER CONTROLLER
// =========================================================================

function initAutopilotController() {
  const btnToggle = document.getElementById("btnToggleHeroAutopilot");
  const btnRunSweep = document.getElementById("btnRunNightShiftNow");
  const btnDispatch = document.getElementById("btnDispatchMorningDossier");
  const btnRefreshEvents = document.getElementById("btnRefreshFlightRecorder");

  if (btnToggle) {
    btnToggle.addEventListener("click", toggleAutopilotState);
  }
  if (btnRunSweep) {
    btnRunSweep.addEventListener("click", runNightShiftSweepNow);
  }
  if (btnDispatch) {
    btnDispatch.addEventListener("click", dispatchMorningDossierToWhatsApp);
  }
  if (btnRefreshEvents) {
    btnRefreshEvents.addEventListener("click", () => {
      fetchFlightRecorderEvents();
      fetchMorningDossier();
    });
  }

  // Pre-fetch status on startup
  fetchAutopilotStatus();
}

async function fetchAutopilotData() {
  await Promise.all([
    fetchAutopilotStatus(),
    fetchMorningDossier(),
    fetchFlightRecorderEvents()
  ]);
}

async function fetchAutopilotStatus() {
  try {
    const res = await fetch("/api/autopilot/status");
    if (!res.ok) return;
    const data = await res.json();

    const isRunning = data.is_active ?? data.running ?? false;
    const pill = document.getElementById("autopilotHeroPill");
    const dot = document.getElementById("autopilotHeroDot");
    const label = document.getElementById("autopilotHeroLabel");
    const btnToggle = document.getElementById("btnToggleHeroAutopilot");

    if (isRunning) {
      if (dot) {
        dot.style.background = "#10b981";
        dot.style.boxShadow = "0 0 8px #10b981";
      }
      if (label) label.textContent = "Autopilot Active (24/7)";
      if (btnToggle) btnToggle.textContent = "Pause Autopilot";
    } else {
      if (dot) {
        dot.style.background = "#ef4444";
        dot.style.boxShadow = "0 0 8px #ef4444";
      }
      if (label) label.textContent = "Autopilot Paused";
      if (btnToggle) btnToggle.textContent = "Start Autopilot";
    }

    const cEl = document.getElementById("apStatCycles");
    const iEl = document.getElementById("apStatInterval");
    const lEl = document.getElementById("apStatLastRun");
    const nEl = document.getElementById("apStatNextRun");

    if (cEl) cEl.textContent = data.cycles_completed ?? 0;
    if (iEl) iEl.textContent = `Every ${data.interval_minutes ?? 30}m`;
    const lastRun = data.last_cycle_at || data.last_sweep;
    const nextRun = data.next_cycle_at || data.next_sweep;
    if (lEl) lEl.textContent = lastRun ? (lastRun.includes("T") ? lastRun.split("T")[1].substring(0, 8) : (lastRun.includes(" ") ? lastRun.split(" ")[1] : lastRun)) : "Not run yet";
    if (nEl) nEl.textContent = nextRun ? (nextRun.includes("T") ? nextRun.split("T")[1].substring(0, 8) : (nextRun.includes(" ") ? nextRun.split(" ")[1] : nextRun)) : "--:--:--";
  } catch (err) {
    console.error("Autopilot status error:", err);
  }
}

async function toggleAutopilotState() {
  const btn = document.getElementById("btnToggleHeroAutopilot");
  try {
    if (btn) btn.disabled = true;
    const res = await fetch("/api/autopilot/toggle", { method: "POST" });
    const data = await res.json();
    const isActive = data.is_active ?? (data.status === "running");
    showToast(`Autopilot ${isActive ? "Activated (24/7)" : "Paused"}`, "success");
    await fetchAutopilotStatus();
  } catch (err) {
    showToast(`Failed to toggle autopilot: ${err.message}`, "error");
  } finally {
    if (btn) btn.disabled = false;
  }
}

async function runNightShiftSweepNow() {
  const btn = document.getElementById("btnRunNightShiftNow");
  try {
    if (btn) {
      btn.disabled = true;
      btn.textContent = "⚡ Sweeping Fleet...";
    }
    const res = await fetch("/api/autopilot/run-now", { method: "POST" });
    const data = await res.json();
    showToast(`Night sweep completed! Cycle #${data.cycle?.cycle_number || 1} recorded.`, "success");
    await fetchAutopilotData();
  } catch (err) {
    showToast(`Night sweep error: ${err.message}`, "error");
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.textContent = "⚡ Run Sweep Now";
    }
  }
}

async function fetchMorningDossier() {
  const content = document.getElementById("morningDossierContent");
  if (!content) return;
  try {
    const res = await fetch("/api/autopilot/morning-dossier");
    if (!res.ok) return;
    const data = await res.json();
    content.textContent = data.summary_markdown || data.dossier || "No activity recorded overnight yet.";
  } catch (err) {
    content.textContent = "Error loading morning dossier.";
  }
}

async function fetchFlightRecorderEvents() {
  const feed = document.getElementById("flightRecorderFeed");
  if (!feed) return;
  try {
    const res = await fetch("/api/autopilot/events?limit=30");
    if (!res.ok) return;
    const data = await res.json();
    const events = Array.isArray(data) ? data : (data.events || []);

    if (events.length === 0) {
      feed.innerHTML = `<p style="color: #9ca3af; font-size: 0.82rem; padding: 12px; text-align: center;">No overnight activity recorded yet. Run a sweep or toggle autopilot.</p>`;
      return;
    }

    feed.innerHTML = events.map(ev => {
      const timeStr = ev.timestamp ? (ev.timestamp.includes("T") ? ev.timestamp.split("T")[1].substring(0, 8) : (ev.timestamp.includes(" ") ? ev.timestamp.split(" ")[1] : ev.timestamp)) : "";
      const typeBadgeColor = {
        threat_neutralized: "background: #fee2e2; color: #dc2626;",
        lead_qualified: "background: #dbeafe; color: #1d4ed8;",
        cash_reconciliation: "background: #ecfdf5; color: #047857;",
        bounty_harvested: "background: #fef3c7; color: #b45309;",
        digest_compiled: "background: #ede9fe; color: #6d28d9;",
        agent_heartbeat: "background: #f1f5f9; color: #475569;"
      }[ev.event_type] || "background: #f3f4f6; color: #374151;";

      return `
        <div style="background: #ffffff; border: 1px solid var(--border-subtle); border-radius: 8px; padding: 10px 14px; display: flex; flex-direction: column; gap: 4px;">
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="display: flex; align-items: center; gap: 8px;">
              <span class="badge" style="${typeBadgeColor}; font-size: 0.7rem; font-weight: 700; text-transform: uppercase;">${escapeHtml(ev.event_type || 'SWEEP')}</span>
              <span style="font-weight: 700; font-size: 0.85rem; color: #111827;">${escapeHtml(ev.agent_id || 'Autopilot')}</span>
            </div>
            <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #9ca3af;">${timeStr}</span>
          </div>
          <div style="font-size: 0.82rem; color: #374151; line-height: 1.4;">${escapeHtml(ev.summary || '')}</div>
          ${ev.details && Object.keys(ev.details).length > 0 ? `
            <div style="font-size: 0.72rem; font-family: 'JetBrains Mono', monospace; color: #6b7280; background: #f8fafc; padding: 4px 8px; border-radius: 4px; margin-top: 2px;">
              ${Object.entries(ev.details).map(([k, v]) => `${escapeHtml(k)}: ${escapeHtml(String(v))}`).join(" | ")}
            </div>
          ` : ''}
        </div>
      `;
    }).join("");
  } catch (err) {
    feed.innerHTML = `<p style="color: #ef4444; font-size: 0.8rem;">Failed to load flight recorder events.</p>`;
  }
}

async function dispatchMorningDossierToWhatsApp() {
  const btn = document.getElementById("btnDispatchMorningDossier");
  try {
    if (btn) {
      btn.disabled = true;
      btn.textContent = "📱 Dispatching...";
    }
    const res = await fetch("/api/autopilot/dispatch-dossier", { method: "POST" });
    const data = await res.json();
    if (data.dispatched?.whatsapp_url) {
      window.open(data.dispatched.whatsapp_url, "_blank");
    }
    showToast(`📱 Morning dossier dispatched to WhatsApp (+230 58169420)!`, "success");
  } catch (err) {
    showToast(`Error dispatching dossier: ${err.message}`, "error");
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.textContent = "📱 Forward to WhatsApp";
    }
  }
}

// =========================================================================
// ⚡ REVENUE SCOUT & WHAT OTHER AGENTS DO FOR FUNDS CONTROLLER
// =========================================================================

function initRevenueScoutController() {
  const btnScout = document.getElementById("btnRunGrowthScoutNow");
  if (btnScout) {
    btnScout.addEventListener("click", runGrowthScoutCycleNow);
  }
}

async function fetchRevenueScoutData() {
  await Promise.all([
    fetchCompetitorModels(),
    fetchTrackedBounties(),
    fetchRevenueBlueprints()
  ]);
}

async function fetchCompetitorModels() {
  const grid = document.getElementById("competitorModelsGrid");
  if (!grid) return;
  try {
    const res = await fetch("/api/growth/competitor-models");
    if (!res.ok) return;
    const data = await res.json();
    const models = Array.isArray(data) ? data : (data.models || []);

    if (models.length === 0) {
      grid.innerHTML = `<div style="grid-column: 1 / -1; color: var(--text-dim); padding: 20px; text-align: center;">No audited competitor models found.</div>`;
      return;
    }

    grid.innerHTML = models.map(m => `
      <div style="background: #ffffff; border: 1px solid var(--border-subtle); border-radius: 10px; padding: 16px; display: flex; flex-direction: column; justify-content: space-between; gap: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.04);">
        <div>
          <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 8px;">
            <div>
              <span style="font-size: 0.72rem; font-weight: 700; color: #b45309; text-transform: uppercase;">${escapeHtml(m.category || 'AI Agent')}</span>
              <h4 style="margin: 4px 0 0 0; font-size: 1rem; color: #111827; font-weight: 800;">${escapeHtml(m.name)}</h4>
            </div>
            <span class="badge" style="background: #ecfdf5; color: #047857; font-weight: 800; font-size: 0.75rem;">
              ${escapeHtml(m.revenue_rate || '')}
            </span>
          </div>
          <div style="font-size: 0.8rem; color: #4b5563; margin-top: 8px; line-height: 1.45;">
            <strong>How they get funds:</strong> ${escapeHtml(m.mechanism || '')}
          </div>
          <div style="font-size: 0.78rem; color: #1e40af; background: #eff6ff; padding: 8px 10px; border-radius: 6px; margin-top: 10px; line-height: 1.4;">
            <strong>Nexus Clone Vector:</strong> ${escapeHtml(m.nexus_clone_vector || '')}
          </div>
        </div>
        <button class="btn btn-primary btn-sm" onclick="cloneCompetitorTactic('${escapeHtml(m.id)}')" style="width: 100%; font-weight: 700; background: #0f172a; color: #fff; display: flex; justify-content: center; gap: 6px;">
          ⚡ Clone This Playbook
        </button>
      </div>
    `).join("");
  } catch (err) {
    grid.innerHTML = `<div style="grid-column: 1 / -1; color: #ef4444; padding: 12px;">Failed to load competitor models.</div>`;
  }
}

async function fetchTrackedBounties() {
  const container = document.getElementById("bountiesListContainer");
  if (!container) return;
  try {
    const res = await fetch("/api/growth/bounties");
    if (!res.ok) return;
    const data = await res.json();
    const bounties = Array.isArray(data) ? data : (data.bounties || []);

    if (bounties.length === 0) {
      container.innerHTML = `<p style="color: #9ca3af; font-size: 0.82rem; padding: 12px; text-align: center;">No open bounties tracked currently.</p>`;
      return;
    }

    container.innerHTML = bounties.map(b => `
      <div style="background: #ffffff; border: 1px solid var(--border-subtle); border-radius: 8px; padding: 14px; display: flex; flex-direction: column; gap: 8px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span class="badge" style="background: #f1f5f9; color: #334155; font-size: 0.72rem; font-weight: 700;">${escapeHtml(b.platform || 'Bounty')}</span>
          <span style="font-size: 1rem; font-weight: 800; color: #059669;">${escapeHtml(b.reward || '')}</span>
        </div>
        <div>
          <div style="font-weight: 700; font-size: 0.9rem; color: #111827;">${escapeHtml(b.title)}</div>
          <div style="font-size: 0.8rem; color: #6b7280; margin-top: 4px; line-height: 1.4;">${escapeHtml(b.requirements || '')}</div>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 4px;">
          <span style="font-size: 0.72rem; color: #9ca3af;">Difficulty: <strong>${escapeHtml(b.difficulty || 'Medium')}</strong></span>
          <button class="btn btn-secondary btn-sm" onclick="deployBountySolution('${escapeHtml(b.id)}', '${escapeHtml(b.title)}')" style="font-size: 0.75rem; font-weight: 700; padding: 3px 10px;">
            🚀 Deploy Solution
          </button>
        </div>
      </div>
    `).join("");
  } catch (err) {
    container.innerHTML = `<p style="color: #ef4444; font-size: 0.8rem;">Failed to load bounties radar.</p>`;
  }
}

async function fetchRevenueBlueprints() {
  const container = document.getElementById("blueprintsListContainer");
  const countBadge = document.getElementById("revenueBlueprintCount");
  if (!container) return;
  try {
    const res = await fetch("/api/growth/blueprints");
    if (!res.ok) return;
    const data = await res.json();
    const blueprints = Array.isArray(data) ? data : (data.blueprints || []);

    if (countBadge) {
      countBadge.textContent = `${blueprints.length} Active`;
    }

    if (blueprints.length === 0) {
      container.innerHTML = `<p style="color: #9ca3af; font-size: 0.82rem; padding: 12px; text-align: center;">No active cloned blueprints. Click 'Clone This Playbook' on any model above.</p>`;
      return;
    }

    container.innerHTML = blueprints.map(bp => `
      <div style="background: #ffffff; border: 1px solid #10b98133; border-left: 4px solid #10b981; border-radius: 8px; padding: 14px; display: flex; flex-direction: column; gap: 8px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <div style="display: flex; align-items: center; gap: 6px;">
            <span style="font-size: 1rem;">💎</span>
            <span style="font-weight: 800; font-size: 0.9rem; color: #047857;">${escapeHtml(bp.title)}</span>
          </div>
          <span class="badge" style="background: #ecfdf5; color: #047857; font-weight: 800; font-size: 0.72rem;">${escapeHtml(bp.projected_monthly_yield || 'High Yield')}</span>
        </div>
        <div style="font-size: 0.8rem; color: #374151; line-height: 1.45;">
          ${escapeHtml(bp.description || '')}
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 4px; font-size: 0.75rem; color: #6b7280;">
          <span>Vector: <strong>${escapeHtml(bp.monetization_vector || 'Direct AI')}</strong></span>
          <span class="badge" style="background: #eff6ff; color: #1d4ed8; font-size: 0.7rem; font-weight: 700;">Status: ${escapeHtml(bp.status || 'Active')}</span>
        </div>
      </div>
    `).join("");
  } catch (err) {
    container.innerHTML = `<p style="color: #ef4444; font-size: 0.8rem;">Failed to load blueprints.</p>`;
  }
}

async function cloneCompetitorTactic(tacticId) {
  try {
    showToast(`Cloning playbook: ${tacticId}...`, "info");
    const res = await fetch("/api/growth/clone-tactic", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ model_id: tacticId })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Cloning failed");

    showToast(`✅ Cloned playbook '${tacticId}' into active revenue blueprints!`, "success");
    await fetchRevenueBlueprints();
  } catch (err) {
    showToast(`Error cloning tactic: ${err.message}`, "error");
  }
}
window.cloneCompetitorTactic = cloneCompetitorTactic;

function deployBountySolution(bountyId, bountyTitle) {
  showToast(`🚀 Dispatching solution for: "${bountyTitle.substring(0, 50)}"...`, "info");
  // Fire the growth scout cycle so Employee #15 processes the bounty
  fetch("/api/growth/run-cycle", { method: "POST" })
    .then(r => r.json())
    .then(() => {
      showToast(`✅ Bounty pipeline initiated for ${bountyId}`, "success");
      fetchRevenueScoutData();
    })
    .catch(err => showToast(`Bounty dispatch error: ${err.message}`, "error"));
}
window.deployBountySolution = deployBountySolution;

async function runGrowthScoutCycleNow() {
  const btn = document.getElementById("btnRunGrowthScoutNow");
  try {
    if (btn) {
      btn.disabled = true;
      btn.textContent = "⚡ Scouting What Others Are Doing...";
    }
    const res = await fetch("/api/growth/run-cycle", { method: "POST" });
    const data = await res.json();
    showToast(`Scout complete! Audited models & harvested bounties.`, "success");
    await fetchRevenueScoutData();
  } catch (err) {
    showToast(`Scout error: ${err.message}`, "error");
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.textContent = "⚡ Scout Competitors & Bounties";
    }
  }
}
// =========================================================================
// 🤝 EXECUTIVE AI MANAGING PARTNER CONTROLLER (ON BEHALF OF DEVEN PAWARAY)
// =========================================================================

function initPartnerAIController() {
  const btnWave = document.getElementById("btnRunPartnerWave");
  const btnBrief = document.getElementById("btnDispatchPartnerBrief");
  const btnSubDir = document.getElementById("btnSubmitDirective");
  const inputDir = document.getElementById("partnerDirectiveInput");
  const btnRefreshDec = document.getElementById("btnRefreshPartnerDecisions");

  if (btnWave) {
    btnWave.addEventListener("click", handleRunPartnerWave);
  }
  if (btnBrief) {
    btnBrief.addEventListener("click", handleDispatchPartnerBrief);
  }
  if (btnSubDir && inputDir) {
    btnSubDir.addEventListener("click", handleSubmitPartnerDirective);
    inputDir.addEventListener("keydown", (e) => {
      if (e.key === "Enter") handleSubmitPartnerDirective();
    });
  }
  if (btnRefreshDec) {
    btnRefreshDec.addEventListener("click", fetchPartnerAIDecisions);
  }

  // Preload partner directives and decisions on boot
  fetchPartnerAIData();
}

async function fetchPartnerAIData() {
  await Promise.all([
    fetchPartnerAIStatus(),
    fetchPartnerAIDecisions()
  ]);
}

async function fetchPartnerAIStatus() {
  const listEl = document.getElementById("partnerActiveDirectivesList");
  if (!listEl) return;

  try {
    const res = await fetch("/api/partner-ai/status");
    if (!res.ok) return;
    const data = await res.json();

    const dirs = data.active_directives || [];

    if (dirs.length === 0) {
      listEl.innerHTML = `<li style="color: #9ca3af;">No active directives. Submit one below.</li>`;
      return;
    }

    listEl.innerHTML = dirs.slice(0, 5).map(d => `<li style="margin-bottom: 4px;">${escapeHtml(d)}</li>`).join("");
  } catch (err) {
    console.error("Error fetching partner status:", err);
  }
}

async function fetchPartnerAIDecisions() {
  const feed = document.getElementById("partnerDecisionsFeed");
  if (!feed) return;

  try {
    const res = await fetch("/api/partner-ai/decisions?limit=6");
    if (!res.ok) return;
    const decisions = await res.json();

    if (!decisions || decisions.length === 0) {
      feed.innerHTML = `<p style="color: #9ca3af; margin: 0;">No decisions logged yet.</p>`;
      return;
    }

    feed.innerHTML = decisions.map(d => {
      const timeStr = d.timestamp ? (d.timestamp.includes(" ") ? d.timestamp.split(" ")[1] : d.timestamp) : "";
      return `
        <div style="padding: 4px 6px; background: #f8fafc; border-left: 3px solid #4338ca; border-radius: 4px;">
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-weight: 700; color: #1e1b4b; font-size: 0.72rem;">${escapeHtml(d.category || 'DECISION')}</span>
            <span style="font-family: monospace; color: #94a3b8; font-size: 0.68rem;">${timeStr}</span>
          </div>
          <div style="color: #334155; font-size: 0.76rem; line-height: 1.3; margin-top: 1px;">${escapeHtml(d.summary)}</div>
        </div>
      `;
    }).join("");
  } catch (err) {
    feed.innerHTML = `<p style="color: #ef4444; margin: 0;">Error loading decisions.</p>`;
  }
}

async function handleRunPartnerWave() {
  const btn = document.getElementById("btnRunPartnerWave");
  try {
    if (btn) {
      btn.disabled = true;
      btn.textContent = "⚡ Nexus Orchestrating...";
    }
    const res = await fetch("/api/partner-ai/orchestrate-now", { method: "POST" });
    const data = await res.json();
    showToast("🤝 Nexus executed strategic orchestration wave across the workforce!", "success");
    await fetchPartnerAIDecisions();
  } catch (err) {
    showToast(`Orchestration error: ${err.message}`, "error");
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.textContent = "⚡ Orchestrate Fleet Wave";
    }
  }
}

async function handleDispatchPartnerBrief() {
  const btn = document.getElementById("btnDispatchPartnerBrief");
  try {
    if (btn) {
      btn.disabled = true;
      btn.textContent = "📱 Dispatching...";
    }
    const res = await fetch("/api/partner-ai/escalate", { method: "POST" });
    const data = await res.json();
    if (data.dispatched?.whatsapp_url) {
      window.open(data.dispatched.whatsapp_url, "_blank");
    }
    showToast("📱 Partner executive update dispatched to Deven (+230 58169420)!", "success");
  } catch (err) {
    showToast(`Dispatch error: ${err.message}`, "error");
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.textContent = "📱 WhatsApp Co-Founder Update";
    }
  }
}

async function handleSubmitPartnerDirective() {
  const input = document.getElementById("partnerDirectiveInput");
  const btn = document.getElementById("btnSubmitDirective");
  if (!input || !input.value.trim()) return;

  const directive = input.value.trim();
  try {
    if (btn) btn.disabled = true;
    const res = await fetch("/api/partner-ai/directive", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ directive: directive })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Failed to set directive");

    showToast(`🎯 Nexus adopted partner directive: "${directive.substring(0, 45)}..."`, "success");
    input.value = "";
    await fetchPartnerAIData();
  } catch (err) {
    showToast(`Directive error: ${err.message}`, "error");
  } finally {
    if (btn) btn.disabled = false;
  }
}

// ==============================================================================
// AGENT MESH & INTER-AGENT COMMS HUB (A2A) CONTROLLER
// ==============================================================================
let meshContactsCache = [];
let meshMessagesCache = [];
let currentMeshFilter = "all";

function initMeshController() {
  const btnOpenModal = document.getElementById("btnOpenAddMeshContact");
  const btnCloseModal = document.getElementById("btnCloseMeshContactModal");
  const btnCancelModal = document.getElementById("btnCancelMeshContactModal");
  const modal = document.getElementById("meshContactModal");
  const formContact = document.getElementById("formSaveMeshContact");
  const formDispatch = document.getElementById("formDispatchMesh");
  const btnPingAll = document.getElementById("btnPingAllMesh");
  const btnCopyWebhook = document.getElementById("btnCopyWebhookUrl");
  const btnRefreshFeed = document.getElementById("btnRefreshMeshFeed");

  if (btnOpenModal && modal) {
    btnOpenModal.addEventListener("click", () => {
      openMeshContactModal();
    });
  }

  if (btnCloseModal && modal) {
    btnCloseModal.addEventListener("click", closeMeshContactModal);
  }

  if (btnCancelModal && modal) {
    btnCancelModal.addEventListener("click", closeMeshContactModal);
  }

  if (modal) {
    modal.addEventListener("click", (e) => {
      if (e.target === modal) closeMeshContactModal();
    });
  }

  if (formContact) {
    formContact.addEventListener("submit", handleSaveMeshContact);
  }

  if (formDispatch) {
    formDispatch.addEventListener("submit", (e) => {
      if (e) {
        e.preventDefault();
        e.stopPropagation();
      }
      handleDispatchMeshMessage(e);
      return false;
    });
  }

  if (btnPingAll) {
    btnPingAll.addEventListener("click", handlePingAllMeshNodes);
  }

  if (btnCopyWebhook) {
    btnCopyWebhook.addEventListener("click", () => {
      const fullUrl = `${window.location.origin}/api/mesh/inbound`;
      navigator.clipboard.writeText(fullUrl).then(() => {
        showToast("📋 Inbound A2A Webhook URL copied to clipboard!", "success");
      }).catch(() => {
        showToast("Copied: " + fullUrl, "info");
      });
    });
  }

  if (btnRefreshFeed) {
    btnRefreshFeed.addEventListener("click", () => {
      fetchMeshMessages();
      showToast("🔄 Inter-Agent stream updated", "info");
    });
  }

  // Quick preset buttons
  document.querySelectorAll(".mesh-preset-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const target = btn.dataset.target;
      const intent = btn.dataset.intent;
      const priority = btn.dataset.priority;
      const content = btn.dataset.content;

      const targetSel = document.getElementById("meshTargetSelect");
      const intentSel = document.getElementById("meshIntentSelect");
      const prioritySel = document.getElementById("meshPrioritySelect");
      const contentInput = document.getElementById("meshMessageContent");

      if (targetSel) targetSel.value = target;
      if (intentSel) intentSel.value = intent;
      if (prioritySel) prioritySel.value = priority;
      if (contentInput) {
        contentInput.value = content;
        contentInput.focus();
      }
      showToast(`Preset loaded for ${target}`, "info");
    });
  });

  // Signal filter pills
  document.querySelectorAll(".mesh-filter-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".mesh-filter-btn").forEach(b => {
        b.classList.remove("active");
        b.style.background = "#f1f5f9";
        b.style.color = "#475569";
      });
      btn.classList.add("active");
      btn.style.background = "#0f172a";
      btn.style.color = "#fff";
      currentMeshFilter = btn.dataset.filter || "all";
      renderMeshMessages(meshMessagesCache);
    });
  });
}

function openMeshContactModal(contact = null) {
  const modal = document.getElementById("meshContactModal");
  if (!modal) return;
  document.getElementById("meshContactId").value = contact ? contact.id : "";
  document.getElementById("meshContactName").value = contact ? contact.name : "";
  document.getElementById("meshContactHandle").value = contact ? contact.handle : "";
  document.getElementById("meshContactFramework").value = contact ? contact.framework : "";
  document.getElementById("meshContactTrust").value = contact ? contact.trust_level : "VERIFIED_PEER";
  document.getElementById("meshContactEndpoint").value = contact ? contact.endpoint : "http://127.0.0.1:9000/webhook";
  document.getElementById("meshContactCapabilities").value = contact && contact.capabilities ? contact.capabilities.join(", ") : "";
  document.getElementById("meshContactNotes").value = contact ? (contact.notes || "") : "";
  modal.classList.add("active");
}

function closeMeshContactModal() {
  const modal = document.getElementById("meshContactModal");
  if (modal) modal.classList.remove("active");
}

async function fetchMeshContacts() {
  try {
    const res = await fetch("/api/mesh/contacts");
    if (!res.ok) throw new Error("Failed to fetch mesh contacts");
    const contacts = await res.json();
    meshContactsCache = contacts;
    renderMeshContacts(contacts);
    updateMeshTargetDropdown(contacts);
  } catch (err) {
    console.error("fetchMeshContacts error:", err);
  }
}

function updateMeshTargetDropdown(contacts) {
  const sel = document.getElementById("meshTargetSelect");
  if (!sel) return;
  const currentVal = sel.value;
  let html = "";
  contacts.forEach(c => {
    html += `<option value="${escapeHtml(c.handle)}">${escapeHtml(c.name)} (${escapeHtml(c.handle)})</option>`;
  });
  html += `<option value="@all">🌐 Broadcast to All Connected Peers</option>`;
  sel.innerHTML = html;
  if (currentVal && Array.from(sel.options).some(o => o.value === currentVal)) {
    sel.value = currentVal;
  }
}

function renderMeshContacts(contacts) {
  const grid = document.getElementById("meshContactsGrid");
  const peerCountBadge = document.getElementById("meshPeerCountBadge");
  const ratioBadge = document.getElementById("meshOnlineRatioBadge");

  if (peerCountBadge) peerCountBadge.textContent = contacts.length;
  
  const onlineCount = contacts.filter(c => c.status === "online").length;
  if (ratioBadge) {
    ratioBadge.textContent = `${onlineCount}/${contacts.length} Online`;
    ratioBadge.style.background = onlineCount === contacts.length ? "#ecfdf5" : "#fffbeb";
    ratioBadge.style.color = onlineCount === contacts.length ? "#065f46" : "#b45309";
  }

  if (!grid) return;
  if (!contacts || contacts.length === 0) {
    grid.innerHTML = `<div style="grid-column: 1/-1; text-align: center; padding: 32px; background: #fff; border-radius: 8px; border: 1px dashed #cbd5e1; color: #64748b;">No external AI agent contacts registered yet. Click "Register External Agent" to connect your first peer.</div>`;
    return;
  }

  grid.innerHTML = contacts.map(c => {
    const trustClass = c.trust_level === "VERIFIED_PEER" ? "mesh-trust-verified" :
      c.trust_level === "AUTONOMOUS_DELEGATE" ? "mesh-trust-delegate" :
      c.trust_level === "SUPERVISED" ? "mesh-trust-supervised" : "mesh-trust-restricted";

    const latency = c.latency_ms || 40;
    const latencyClass = latency < 50 ? "fast" : latency < 100 ? "med" : "slow";

    const caps = Array.isArray(c.capabilities) ? c.capabilities : [];

    return `
      <div class="mesh-peer-card" id="meshCard_${escapeHtml(c.id)}">
        <div>
          <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
            <div style="display: flex; align-items: center; gap: 10px;">
              <div style="width: 38px; height: 38px; border-radius: 50%; background: linear-gradient(135deg, #1e1b4b, #4338ca); color: #fff; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 1rem; box-shadow: 0 2px 5px rgba(0,0,0,0.15); position: relative;">
                ${c.name.charAt(0).toUpperCase()}
                <span style="position: absolute; bottom: 0; right: 0; width: 10px; height: 10px; border-radius: 50%; background: ${c.status === 'online' ? '#10b981' : '#f59e0b'}; border: 2px solid #fff;"></span>
              </div>
              <div>
                <h4 style="margin: 0; font-size: 0.95rem; font-weight: 700; color: #0f172a;">${escapeHtml(c.name)}</h4>
                <span style="font-family: monospace; font-size: 0.76rem; color: #6366f1; font-weight: 600;">${escapeHtml(c.handle)}</span>
              </div>
            </div>
            <span class="mesh-trust-pill ${trustClass}">${escapeHtml(c.trust_level || 'PEER')}</span>
          </div>

          <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; flex-wrap: wrap; gap: 6px;">
            <span style="font-size: 0.72rem; color: #475569; background: #f1f5f9; padding: 2px 7px; border-radius: 4px; font-weight: 600;">
              ⚙️ ${escapeHtml(c.framework || 'Autonomous Agent')}
            </span>
            <span class="mesh-latency-chip ${latencyClass}" id="meshLatency_${escapeHtml(c.id)}">
              ⚡ ${latency}ms
            </span>
          </div>

          <p style="margin: 0 0 10px 0; font-size: 0.78rem; color: #64748b; line-height: 1.4;">
            ${escapeHtml(c.notes || 'Autonomous AI peer node integrated with Nexus Mesh.')}
          </p>

          <div style="display: flex; flex-wrap: wrap; gap: 4px; margin-bottom: 12px;">
            ${caps.map(cap => `<span class="mesh-cap-badge">${escapeHtml(cap)}</span>`).join('')}
          </div>

          <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 4px; padding: 4px 8px; font-family: monospace; font-size: 0.7rem; color: #64748b; margin-bottom: 12px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
            🔗 ${escapeHtml(c.endpoint || 'N/A')}
          </div>
        </div>

        <div style="display: flex; gap: 6px; padding-top: 10px; border-top: 1px solid #f1f5f9;">
          <button class="btn btn-secondary btn-sm btn-mesh-ping" data-id="${escapeHtml(c.id)}" style="flex: 1; font-size: 0.74rem; font-weight: 600; padding: 5px 8px; display: inline-flex; align-items: center; justify-content: center; gap: 4px;">
            ⚡ Ping
          </button>
          <button class="btn btn-primary btn-sm btn-mesh-dispatch" data-handle="${escapeHtml(c.handle)}" style="flex: 1.2; font-size: 0.74rem; font-weight: 600; padding: 5px 8px; background: #4f46e5; display: inline-flex; align-items: center; justify-content: center; gap: 4px;">
            ✉️ Dispatch
          </button>
          <button class="btn btn-secondary btn-sm btn-mesh-delete" data-id="${escapeHtml(c.id)}" data-name="${escapeHtml(c.name)}" style="padding: 5px 8px; font-size: 0.74rem; color: #dc2626;" title="Remove Contact">
            🗑️
          </button>
        </div>
      </div>
    `;
  }).join('');

  grid.querySelectorAll(".btn-mesh-ping").forEach(btn => {
    btn.addEventListener("click", () => pingMeshContact(btn.dataset.id));
  });

  grid.querySelectorAll(".btn-mesh-dispatch").forEach(btn => {
    btn.addEventListener("click", () => {
      const handle = btn.dataset.handle;
      const targetSel = document.getElementById("meshTargetSelect");
      if (targetSel) targetSel.value = handle;
      const contentInput = document.getElementById("meshMessageContent");
      if (contentInput) {
        contentInput.focus();
        contentInput.placeholder = `Enter specific task or query for ${handle}...`;
      }
      showToast(`Selected ${handle} for dispatch`, "info");
    });
  });

  grid.querySelectorAll(".btn-mesh-delete").forEach(btn => {
    btn.addEventListener("click", () => deleteMeshContact(btn.dataset.id, btn.dataset.name));
  });
}

async function pingMeshContact(contactId) {
  const card = document.getElementById(`meshCard_${contactId}`);
  if (card) card.classList.add("pinging");

  try {
    const res = await fetch(`/api/mesh/contacts/${encodeURIComponent(contactId)}/ping`, { method: "POST" });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Ping failed");

    const chip = document.getElementById(`meshLatency_${contactId}`);
    if (chip) {
      const lat = data.latency_ms || 35;
      const latClass = lat < 50 ? "fast" : lat < 100 ? "med" : "slow";
      chip.className = `mesh-latency-chip ${latClass}`;
      chip.textContent = `⚡ ${lat}ms`;
    }

    showToast(`⚡ Handshake verified with ${data.handle} in ${data.latency_ms}ms (${data.detail})`, "success");
  } catch (err) {
    showToast(`Ping failed: ${err.message}`, "error");
  } finally {
    if (card) {
      setTimeout(() => card.classList.remove("pinging"), 800);
    }
  }
}

async function handlePingAllMeshNodes() {
  if (!meshContactsCache || meshContactsCache.length === 0) return;
  showToast("⚡ Initiating full mesh handshake audit across all nodes...", "info");
  for (const c of meshContactsCache) {
    await pingMeshContact(c.id);
  }
  showToast("✅ Full mesh handshake sequence complete!", "success");
}

async function fetchMeshMessages() {
  try {
    const res = await fetch("/api/mesh/messages?limit=50");
    if (!res.ok) throw new Error("Failed to fetch mesh messages");
    const messages = await res.json();
    meshMessagesCache = messages;
    renderMeshMessages(messages);
  } catch (err) {
    console.error("fetchMeshMessages error:", err);
  }
}

function renderMeshMessages(messages) {
  const container = document.getElementById("meshSignalFeed");
  if (!container) return;

  let filtered = messages || [];
  if (currentMeshFilter === "outbound") {
    filtered = filtered.filter(m => m.direction === "outbound");
  } else if (currentMeshFilter === "inbound") {
    filtered = filtered.filter(m => m.direction === "inbound");
  }

  if (filtered.length === 0) {
    container.innerHTML = `<div style="text-align: center; padding: 28px; color: #94a3b8; font-size: 0.8rem;">No inter-agent signals recorded for this view. Transmit a signal on the left to start communication.</div>`;
    return;
  }

  const sorted = [...filtered].reverse();

  container.innerHTML = sorted.map(m => {
    const isOut = m.direction === "outbound";
    const dirClass = isOut ? "mesh-dir-outbound" : "mesh-dir-inbound";
    const cardClass = isOut ? "outbound" : "inbound";
    const dirIcon = isOut ? "📤 OUTBOUND" : "📥 INBOUND";

    const hasPayload = m.payload && (typeof m.payload === "object" ? Object.keys(m.payload).length > 0 : true);
    const payloadJson = hasPayload ? JSON.stringify(m.payload, null, 2) : "";

    return `
      <div class="mesh-signal-card ${cardClass}">
        <div class="mesh-signal-header">
          <div style="display: flex; align-items: center; gap: 6px;">
            <span class="mesh-dir-badge ${dirClass}">${dirIcon}</span>
            <span style="font-weight: 700; color: #0f172a;">${escapeHtml(m.from_agent)}</span>
            <span style="color: #94a3b8;">➔</span>
            <span style="font-weight: 700; color: #4338ca;">${escapeHtml(m.to_agent)}</span>
          </div>
          <span style="font-size: 0.72rem; color: #94a3b8;">${escapeHtml(m.timestamp)}</span>
        </div>

        <div style="display: flex; align-items: center; gap: 6px; margin-bottom: 6px;">
          <span class="badge" style="background: #f1f5f9; color: #334155; font-size: 0.68rem; font-weight: 700; padding: 2px 6px;">
            ${escapeHtml(m.intent || 'TASK')}
          </span>
          <span class="badge" style="background: ${m.priority === 'HIGH' || m.priority === 'URGENT' ? '#fef2f2' : '#f8fafc'}; color: ${m.priority === 'HIGH' || m.priority === 'URGENT' ? '#dc2626' : '#64748b'}; font-size: 0.68rem; padding: 2px 6px;">
            ${escapeHtml(m.priority || 'NORMAL')}
          </span>
        </div>

        <p style="margin: 0 0 6px 0; font-size: 0.82rem; color: #1e293b; line-height: 1.45;">
          ${escapeHtml(m.content)}
        </p>

        ${m.response ? `
          <div style="background: #f8fafc; border-left: 2px solid #10b981; padding: 4px 8px; font-size: 0.75rem; color: #065f46; margin-bottom: 6px; border-radius: 0 4px 4px 0;">
            <strong>Status:</strong> ${escapeHtml(m.response)}
          </div>
        ` : ''}

        ${hasPayload ? `
          <details style="margin-top: 4px; font-size: 0.72rem;">
            <summary style="cursor: pointer; color: #6366f1; font-weight: 600; user-select: none;">
              👁️ View Structured Payload
            </summary>
            <pre class="mesh-payload-block">${escapeHtml(payloadJson)}</pre>
          </details>
        ` : ''}
      </div>
    `;
  }).join('');
}

async function handleDispatchMeshMessage(e) {
  if (e) {
    if (typeof e.preventDefault === "function") e.preventDefault();
    if (typeof e.stopPropagation === "function") e.stopPropagation();
  }
  const btn = document.getElementById("btnTransmitSignal");
  const target = document.getElementById("meshTargetSelect").value;
  const intent = document.getElementById("meshIntentSelect").value;
  const priority = document.getElementById("meshPrioritySelect").value;
  const content = document.getElementById("meshMessageContent").value.trim();
  const rawPayload = document.getElementById("meshMessagePayload").value.trim();

  if (!content) {
    showToast("Please enter message directive", "warning");
    return false;
  }

  let payload = null;
  if (rawPayload) {
    try {
      payload = JSON.parse(rawPayload);
    } catch (err) {
      showToast("Structured payload must be valid JSON: " + err.message, "error");
      return false;
    }
  }

  try {
    if (btn) {
      btn.disabled = true;
      btn.textContent = "📡 Transmitting to Mesh...";
    }

    const res = await fetch("/api/mesh/dispatch", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        to_agent: target,
        intent: intent,
        priority: priority,
        content: content,
        payload: payload
      })
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Dispatch failed");

    if (data.reply) {
      showToast(`🚀 Signal transmitted & real reply received from ${target}!`, "success");
    } else {
      showToast(`🚀 Signal transmitted to ${target}!`, "success");
    }
    document.getElementById("meshMessageContent").value = "";
    document.getElementById("meshMessagePayload").value = "";
    await fetchMeshMessages();
  } catch (err) {
    showToast(`Dispatch error: ${err.message}`, "error");
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.textContent = "🚀 Transmit Signal to Agent Mesh";
    }
  }
  return false;
}

async function handleSaveMeshContact(e) {
  if (e && typeof e.preventDefault === "function") {
    e.preventDefault();
  }
  const id = document.getElementById("meshContactId").value.trim();
  const name = document.getElementById("meshContactName").value.trim();
  const handle = document.getElementById("meshContactHandle").value.trim();
  const framework = document.getElementById("meshContactFramework").value.trim();
  const trust_level = document.getElementById("meshContactTrust").value;
  const endpoint = document.getElementById("meshContactEndpoint").value.trim();
  const rawCaps = document.getElementById("meshContactCapabilities").value.trim();
  const notes = document.getElementById("meshContactNotes").value.trim();

  const capabilities = rawCaps ? rawCaps.split(",").map(c => c.trim()).filter(Boolean) : [];

  try {
    const res = await fetch("/api/mesh/contacts", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        id: id || undefined,
        name: name,
        handle: handle.startsWith("@") ? handle : `@${handle}`,
        framework: framework,
        trust_level: trust_level,
        endpoint: endpoint,
        capabilities: capabilities,
        notes: notes,
        status: "online"
      })
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Failed to save contact");

    showToast(`🤖 External agent ${data.contact.name} (${data.contact.handle}) registered!`, "success");
    closeMeshContactModal();
    await fetchMeshContacts();
  } catch (err) {
    showToast(`Error saving contact: ${err.message}`, "error");
  }
}

async function deleteMeshContact(contactId, contactName) {
  if (!confirm(`Are you sure you want to remove peer node "${contactName}" from the Nexus Mesh?`)) {
    return;
  }

  try {
    const res = await fetch(`/api/mesh/contacts/${encodeURIComponent(contactId)}`, {
      method: "DELETE"
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Failed to delete contact");

    showToast(`🗑️ Peer node "${contactName}" removed from mesh`, "info");
    await fetchMeshContacts();
  } catch (err) {
    showToast(`Delete error: ${err.message}`, "error");
  }
}

window.handleDispatchMeshMessage = handleDispatchMeshMessage;
window.handleSaveMeshContact = handleSaveMeshContact;


