/**
 * Nexus Morning Daily Triage Engine
 * =================================
 * Orchestrates "First Thing in the Morning: The Daily Triage" & Executive Summary Card:
 * - Executive Summary Snapshot (Overnight Revenue, Run Rate, Critical Alerts, Next Action)
 * - Branch 1 (If YES: How much, Where from, Target pacing, Blockers)
 * - Branch 2 (If NO: System health, Midnight traffic, Queued today, Baseline burn)
 * - Conversational Standup Assistant (Instant Q&A & Voice Synthesis)
 */

window.morningTriageState = {
  currentMode: 'auto',
  activeBranch: 'yes',
  data: null,
  loading: false
};

// --- 1. Load Morning Triage Data from Backend ---
window.loadMorningTriage = async function(mode = null) {
  try {
    const modeParam = mode ? `?mode=${mode}` : '';
    const res = await fetch(`/api/triage/morning${modeParam}`);
    const data = await res.json();
    if (!data.success) {
      console.warn("Failed to load morning triage:", data);
      return;
    }

    window.morningTriageState.data = data;
    window.morningTriageState.activeBranch = data.made_money ? 'yes' : 'no';

    renderExecutiveSummaryCard(data.executive_summary);
    renderTriageBranches(data);
    updateTriageBranchUI(window.morningTriageState.activeBranch);

  } catch (err) {
    console.error("Error loading morning triage:", err);
  }
};

// --- 2. Render Executive Summary Card ---
function renderExecutiveSummaryCard(summary) {
  if (!summary) return;

  // Overnight Revenue
  const revEl = document.getElementById("triageOvernightRev");
  const revMurEl = document.getElementById("triageOvernightMur");
  const revSubEl = document.getElementById("triageOvernightSub");
  if (revEl) revEl.textContent = summary.overnight_revenue;
  if (revMurEl) revMurEl.textContent = summary.overnight_revenue_mur;
  if (revSubEl) revSubEl.textContent = summary.overnight_revenue_sub;

  // Run Rate vs Target
  const runRateBadge = document.getElementById("triageRunRateBadge");
  const runRateSub = document.getElementById("triageRunRateSub");
  const runRateBar = document.getElementById("triageRunRateBar");
  if (runRateBadge) {
    runRateBadge.textContent = summary.run_rate_status;
    if (summary.run_rate_status === "Ahead") {
      runRateBadge.style.background = "#ecfdf5";
      runRateBadge.style.color = "#047857";
      runRateBadge.style.borderColor = "#a7f3d0";
    } else if (summary.run_rate_status === "On Track") {
      runRateBadge.style.background = "#eff6ff";
      runRateBadge.style.color = "#1d4ed8";
      runRateBadge.style.borderColor = "#bfdbfe";
    } else {
      runRateBadge.style.background = "#fffbeb";
      runRateBadge.style.color = "#b45309";
      runRateBadge.style.borderColor = "#fde68a";
    }
  }

  // Critical Alerts
  const alertsBadge = document.getElementById("triageAlertsBadge");
  const alertsSub = document.getElementById("triageAlertsSub");
  if (alertsBadge) {
    alertsBadge.textContent = summary.critical_alerts_text;
    if (summary.critical_alerts_count === 0) {
      alertsBadge.style.background = "#ecfdf5";
      alertsBadge.style.color = "#047857";
      alertsBadge.style.borderColor = "#a7f3d0";
      if (alertsSub) alertsSub.textContent = "Payment gateways & APIs 100% operational";
    } else {
      alertsBadge.style.background = "#fef2f2";
      alertsBadge.style.color = "#b91c1c";
      alertsBadge.style.borderColor = "#fecaca";
      if (alertsSub) alertsSub.textContent = "Requires immediate founder review";
    }
  }

  // Next Action Required
  const nextActionEl = document.getElementById("triageNextAction");
  if (nextActionEl) {
    nextActionEl.textContent = summary.next_action_required;
  }
}

// --- 3. Render Triage Decision Tree Branches ---
function renderTriageBranches(data) {
  const yes = data.yes_breakdown;
  const no = data.no_breakdown;

  // Render YES Branch
  if (yes) {
    // 1. How Much
    const hm = yes.how_much;
    const howMuchVal = document.getElementById("triageHowMuchValue");
    const howMuchSub = document.getElementById("triageHowMuchSub");
    if (howMuchVal) howMuchVal.textContent = hm.display_revenue;
    if (howMuchSub) howMuchSub.textContent = `${hm.unit_sales} unit sale(s) • ${hm.window}`;

    // 2. Where From (Top Sources)
    const sourcesContainer = document.getElementById("triageSourcesList");
    if (sourcesContainer && yes.where_from) {
      sourcesContainer.innerHTML = yes.where_from.map(s => `
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 10px; background: rgba(255,255,255,0.7); border: 1px solid rgba(226,232,240,0.8); border-radius: 8px; margin-bottom: 6px;">
          <div style="display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 1.1rem;">${s.icon || '📦'}</span>
            <div>
              <div style="font-size: 0.82rem; font-weight: 700; color: #0f172a;">${escapeHtml(s.product)}</div>
              <div style="font-size: 0.7rem; color: #64748b;">${escapeHtml(s.client_channel)}</div>
            </div>
          </div>
          <div style="text-align: right;">
            <div style="font-size: 0.85rem; font-weight: 800; color: #10b981;">${s.amount}</div>
            <div style="font-size: 0.65rem; color: #94a3b8;">${s.share_pct}% share</div>
          </div>
        </div>
      `).join('');
    }

    // 3. How far from target
    const targetMsg = document.getElementById("triageTargetMessage");
    const targetDailyBar = document.getElementById("triageTargetDailyBar");
    const targetDailyText = document.getElementById("triageTargetDailyText");
    if (targetMsg) targetMsg.textContent = yes.target_pacing.pacing_message;
    if (targetDailyBar) targetDailyBar.style.width = `${Math.min(100, yes.target_pacing.daily_pct)}%`;
    if (targetDailyText) targetDailyText.textContent = `${yes.target_pacing.daily_pct}% of daily target (Rs ${yes.target_pacing.daily_target_mur.toLocaleString()})`;

    // 4. Blockers
    const blockersContainer = document.getElementById("triageBlockersList");
    if (blockersContainer && yes.blockers) {
      blockersContainer.innerHTML = yes.blockers.map(b => {
        const isLow = b.urgency === 'LOW';
        const badgeColor = isLow ? '#047857' : (b.urgency === 'HIGH' ? '#b91c1c' : '#b45309');
        const badgeBg = isLow ? '#ecfdf5' : (b.urgency === 'HIGH' ? '#fef2f2' : '#fffbeb');
        return `
          <div style="padding: 10px; background: rgba(255,255,255,0.7); border: 1px solid rgba(226,232,240,0.8); border-left: 3px solid ${badgeColor}; border-radius: 8px; margin-bottom: 6px;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 4px;">
              <strong style="font-size: 0.82rem; color: #0f172a;">${escapeHtml(b.title)}</strong>
              <span class="badge" style="background: ${badgeBg}; color: ${badgeColor}; font-size: 0.65rem;">${b.urgency}</span>
            </div>
            <p style="margin: 0 0 6px 0; font-size: 0.74rem; color: #64748b;">${escapeHtml(b.description)}</p>
            ${b.action_cmd !== 'noop' ? `<button class="btn btn-secondary btn-sm" style="font-size: 0.68rem; padding: 2px 8px;" onclick="window.handleTriageAction('${b.action_cmd}')">⚡ ${escapeHtml(b.action_label)}</button>` : ''}
          </div>
        `;
      }).join('');
    }
  }

  // Render NO Branch
  if (no) {
    // 1. Is Anything Broken
    const healthContainer = document.getElementById("triageHealthChecksList");
    if (healthContainer && no.is_broken.checks) {
      healthContainer.innerHTML = no.is_broken.checks.map(c => `
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 10px; background: rgba(255,255,255,0.7); border: 1px solid rgba(226,232,240,0.8); border-radius: 8px; margin-bottom: 6px;">
          <div>
            <div style="font-size: 0.8rem; font-weight: 700; color: #0f172a;">${escapeHtml(c.name)}</div>
            <div style="font-size: 0.68rem; color: #64748b;">${escapeHtml(c.detail)}</div>
          </div>
          <div style="text-align: right;">
            <span class="badge" style="background: #ecfdf5; color: #047857; font-size: 0.68rem; font-weight: 800;">● ${c.badge}</span>
            <div style="font-size: 0.65rem; color: #94a3b8; margin-top: 2px;">${c.latency}</div>
          </div>
        </div>
      `).join('');
    }

    // 2. Did Traffic Show Up
    const tr = no.traffic_activity;
    const trafficSessions = document.getElementById("triageTrafficSessions");
    const trafficDropoff = document.getElementById("triageTrafficDropoff");
    const trafficSummary = document.getElementById("triageTrafficSummary");
    if (trafficSessions) trafficSessions.textContent = tr.overnight_sessions;
    if (trafficDropoff) trafficDropoff.textContent = tr.dropoff_rate;
    if (trafficSummary) trafficSummary.textContent = `${tr.midnight_pageviews} midnight pageviews • Primary: ${tr.top_landing_page}`;

    // 3. What is Queued Today
    const queuedContainer = document.getElementById("triageQueuedList");
    if (queuedContainer && no.queued_today) {
      queuedContainer.innerHTML = no.queued_today.map(q => `
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 10px; background: rgba(255,255,255,0.7); border: 1px solid rgba(226,232,240,0.8); border-radius: 8px; margin-bottom: 6px;">
          <div>
            <div style="display: flex; align-items: center; gap: 6px;">
              <span style="font-size: 0.7rem; font-weight: 800; background: #e0f2fe; color: #0369a1; padding: 2px 6px; border-radius: 4px;">${q.time}</span>
              <strong style="font-size: 0.8rem; color: #0f172a;">${escapeHtml(q.title)}</strong>
            </div>
            <div style="font-size: 0.7rem; color: #64748b; margin-top: 2px;">${escapeHtml(q.detail)}</div>
          </div>
          <span class="badge" style="background: #eff6ff; color: #1d4ed8; font-size: 0.65rem; font-weight: 700;">${q.status}</span>
        </div>
      `).join('');
    }

    // 4. What's the Burn
    const burn = no.overnight_burn;
    const burnVal = document.getElementById("triageBurnValue");
    const burnSub = document.getElementById("triageBurnSub");
    const burnList = document.getElementById("triageBurnItemized");
    if (burnVal) burnVal.textContent = `$${burn.overnight_burn_usd.toFixed(2)} USD`;
    if (burnSub) burnSub.textContent = `~Rs ${burn.overnight_burn_mur.toFixed(0)} MUR (Baseline 8h night operating cost)`;

    if (burnList && burn.itemized) {
      burnList.innerHTML = burn.itemized.map(it => `
        <div style="display: flex; justify-content: space-between; font-size: 0.72rem; padding: 3px 0; border-bottom: 1px dashed rgba(226,232,240,0.6);">
          <span style="color: #475569;">${escapeHtml(it.service)}</span>
          <strong style="color: #0f172a;">$${it.overnight_usd.toFixed(2)}/night</strong>
        </div>
      `).join('');
    }
  }
}

// --- 4. Switch Between YES and NO Triage Views ---
window.switchTriageBranch = function(branch) {
  window.morningTriageState.activeBranch = branch;
  updateTriageBranchUI(branch);
};

function updateTriageBranchUI(branch) {
  const btnYes = document.getElementById("btnTriageTabYes");
  const btnNo = document.getElementById("btnTriageTabNo");
  const yesPanel = document.getElementById("triageBranchYes");
  const noPanel = document.getElementById("triageBranchNo");

  if (branch === 'yes') {
    if (btnYes) {
      btnYes.style.background = "#10b981";
      btnYes.style.color = "#ffffff";
      btnYes.style.borderColor = "#059669";
    }
    if (btnNo) {
      btnNo.style.background = "#ffffff";
      btnNo.style.color = "#64748b";
      btnNo.style.borderColor = "#cbd5e1";
    }
    if (yesPanel) yesPanel.style.display = "grid";
    if (noPanel) noPanel.style.display = "none";
  } else {
    if (btnYes) {
      btnYes.style.background = "#ffffff";
      btnYes.style.color = "#64748b";
      btnYes.style.borderColor = "#cbd5e1";
    }
    if (btnNo) {
      btnNo.style.background = "#0284c7";
      btnNo.style.color = "#ffffff";
      btnNo.style.borderColor = "#0369a1";
    }
    if (yesPanel) yesPanel.style.display = "none";
    if (noPanel) noPanel.style.display = "grid";
  }
}

// --- 5. Conversational Standup Assistant ---
window.askTriageAssistant = async function(prefilledQuery = null) {
  const inputEl = document.getElementById("triageAssistantInput");
  const answerEl = document.getElementById("triageAssistantAnswer");
  const query = prefilledQuery || (inputEl ? inputEl.value : "");

  if (!query || !query.trim()) return;

  if (answerEl) {
    answerEl.style.display = "block";
    answerEl.innerHTML = `<span style="color: #64748b;">Consulting executive memory & live telemetry...</span>`;
  }

  try {
    const res = await fetch("/api/triage/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: query.trim() })
    });
    const data = await res.json();

    if (answerEl) {
      const formatted = (data.answer || "")
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/\n/g, '<br>');

      answerEl.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
          <div style="font-weight: 800; font-size: 0.85rem; color: #1e1b4b;">🤖 Standup Assistant: "${escapeHtml(query)}"</div>
          <button class="btn btn-secondary btn-sm" style="font-size: 0.65rem; padding: 2px 6px;" onclick="window.speakTriageText()">🔊 Read Aloud</button>
        </div>
        <div id="triageFormattedSpeech" style="font-size: 0.82rem; line-height: 1.5; color: #334155;">${formatted}</div>
      `;
      window.lastTriageSpeechText = data.answer || "";
    }
    if (inputEl) inputEl.value = "";
  } catch (err) {
    if (answerEl) answerEl.innerHTML = `<span style="color: #ef4444;">Error: ${err.message}</span>`;
  }
};

// --- 6. Voice Read Aloud ---
window.speakTriageText = function() {
  const rawText = window.lastTriageSpeechText;
  if (!rawText) return;
  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
    const cleanText = rawText.replace(/[*#•_-]/g, ' ');
    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.rate = 1.05;
    utterance.pitch = 1.0;
    window.speechSynthesis.speak(utterance);
  } else {
    alert("Speech Synthesis not supported by this browser.");
  }
};

// --- 7. Dispatch Morning Triage to WhatsApp ---
window.dispatchTriageWhatsApp = async function() {
  try {
    const res = await fetch("/api/triage/dispatch-whatsapp", { method: "POST" });
    const data = await res.json();
    if (data.success) {
      alert("✅ Morning Daily Triage dispatched to Deven's WhatsApp (+230 58169420)!");
    } else {
      alert("⚠️ WhatsApp dispatch response: " + (data.note || "Check gateway connection"));
    }
  } catch (e) {
    alert("Error dispatching WhatsApp: " + e.message);
  }
};

// --- 8. Handle Triage Action Triggers ---
window.handleTriageAction = function(actionCmd) {
  if (actionCmd === 'check_stripe_logs') {
    alert("Navigating to Treasury Engine & Security Shield log auditor.");
    if (typeof window.navigateToPage === 'function') window.navigateToPage('domain-commerce');
  } else if (actionCmd.startsWith('remind_')) {
    const invId = actionCmd.replace('remind_', '');
    alert(`Dispatching 1-Click payment reminder for ${invId} via WhatsApp & Email.`);
  } else if (actionCmd === 'fulfill_pending') {
    alert("Triggering automated digital vending license generator and customer email delivery.");
  } else {
    alert(`Executing action: ${actionCmd}`);
  }
};

// Helper: Escape HTML
function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

// Auto-initialize when DOM is ready
document.addEventListener("DOMContentLoaded", () => {
  window.loadMorningTriage();
});
