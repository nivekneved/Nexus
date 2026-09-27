/**
 * Nexus™ Role-Based Sub-Portals & Sub-Navigation Controller
 * ========================================================
 * Solves UI complexity by organizing all operations into 3 focused Portals:
 * 1. Founder Portal (Executive peace of mind, zero clutter)
 * 2. Workforce Fleet (18 AI agents segmented by 5 departmental sub-tabs)
 * 3. Sovereign Core (Conway Automaton features: Soul, Survival, Heartbeat, Replication, Treasury)
 */

(function () {
  let currentPortal = "founder";
  let currentSovereignSub = "soul";
  let currentWorkforceDept = "all";

  const DEPT_MAP = {
    executive: ["executive_partner", "chief_of_staff", "executive_poster", "regression_sentinel"],
    sales: ["lead_finder", "growth_hacker", "influencer_usher", "social_broadcaster"],
    email: ["email_hygiene", "ghost_unsubscriber"],
    concierge: ["customer_support", "bilingual_concierge", "meeting_assistant", "mobile_dispatcher"],
    infra: ["infra_finance_sentinel", "repo_radar", "spec_auditor", "appstore_sentinel"]
  };

  window.switchPortal = function (portalId) {
    currentPortal = portalId;

    // 1. Update Portal Nav Buttons
    document.querySelectorAll(".portal-tab-btn").forEach((btn) => {
      if (btn.dataset.portal === portalId) {
        btn.classList.add("active");
      } else {
        btn.classList.remove("active");
      }
    });

    // 2. Filter Sidebar Visibility by Role
    const sidebar = document.getElementById("mainNavMenu");
    if (sidebar) {
      const execGroup = document.getElementById("navGroupExec");
      const revGroup = document.getElementById("navGroupRevenue");
      const opsGroup = document.getElementById("navGroupOps");

      if (portalId === "founder") {
        if (execGroup) execGroup.style.display = "block";
        if (revGroup) revGroup.style.display = "none";
        if (opsGroup) opsGroup.style.display = "none";
        window.navigateToPage("ceo-cockpit");
      } else if (portalId === "workforce") {
        if (execGroup) execGroup.style.display = "block";
        if (revGroup) revGroup.style.display = "block";
        if (opsGroup) opsGroup.style.display = "block";
        window.navigateToPage("workforce");
      } else if (portalId === "sovereign") {
        if (execGroup) execGroup.style.display = "block";
        if (revGroup) revGroup.style.display = "none";
        if (opsGroup) opsGroup.style.display = "none";
        window.navigateToPage("sovereign-core");
        window.refreshSovereignData();
      }
    }
  };

  window.switchSovereignSub = function (subId) {
    currentSovereignSub = subId;
    document.querySelectorAll(".sovereign-sub-btn").forEach((btn) => {
      btn.classList.toggle("active", btn.dataset.sub === subId);
    });

    document.querySelectorAll(".sovereign-sub-pane").forEach((pane) => {
      pane.style.display = pane.id === `subpane-${subId}` ? "block" : "none";
    });

    window.refreshSovereignData();
  };

  window.filterWorkforceDept = function (dept) {
    currentWorkforceDept = dept;
    document.querySelectorAll(".dept-filter-chip").forEach((chip) => {
      chip.classList.toggle("active", chip.dataset.dept === dept);
    });

    const agentCards = document.querySelectorAll("#agentsList .agent-card");
    const allowed = DEPT_MAP[dept];

    agentCards.forEach((card) => {
      const agentId = card.dataset.agentId;
      if (dept === "all" || (allowed && allowed.includes(agentId))) {
        card.style.display = "";
      } else {
        card.style.display = "none";
      }
    });
  };

  window.refreshSovereignData = async function () {
    try {
      // 1. Soul Status
      const soulRes = await fetch("/api/sovereignty/soul");
      if (soulRes.ok) {
        const soul = await soulRes.json();
        const soulName = document.getElementById("sovSoulName");
        const soulRev = document.getElementById("sovSoulRev");
        const soulAlign = document.getElementById("sovSoulAlign");
        const soulReflection = document.getElementById("sovSoulLastReflection");
        const soulTier = document.getElementById("sovSoulTier");

        if (soulName) soulName.textContent = soul.name || "Nexus";
        if (soulRev) soulRev.textContent = `Revision ${soul.revision || 1}`;
        if (soulAlign) soulAlign.textContent = `${Math.round((soul.genesis_alignment || 1.0) * 100)}% Alignment`;
        if (soulReflection) soulReflection.textContent = soul.last_reflection || "Inaugural";
        if (soulTier) soulTier.textContent = (soul.sovereignty_tier || "NORMAL").toUpperCase();
      }

      // 2. Survival Status
      const survRes = await fetch("/api/sovereignty/survival");
      if (survRes.ok) {
        const surv = await survRes.json();
        const tierBadge = document.getElementById("sovSurvivalTierBadge");
        const burnRate = document.getElementById("sovSurvivalBurnRate");
        const spendVal = document.getElementById("sovSurvivalSpend");
        const survReason = document.getElementById("sovSurvivalReason");
        const survModel = document.getElementById("sovSurvivalModel");

        if (tierBadge) {
          tierBadge.textContent = surv.tier_display || "NORMAL";
          tierBadge.className = `badge-tier-${surv.tier || 'normal'}`;
        }
        if (burnRate) burnRate.textContent = `${surv.burn_rate_pct}%`;
        if (spendVal) spendVal.textContent = `$${surv.spend_usd.toFixed(2)} / $${surv.budget_usd.toFixed(2)}`;
        if (survReason) survReason.textContent = surv.reason || "";
        if (survModel) survModel.textContent = surv.recommended_model || "gemini-1.5-pro";
      }

      // 3. Heartbeat Status
      const hbRes = await fetch("/api/sovereignty/heartbeat");
      if (hbRes.ok) {
        const hb = await hbRes.json();
        const tickCount = document.getElementById("sovHeartbeatTickCount");
        const hbStatus = document.getElementById("sovHeartbeatStatus");
        const hbContext = document.getElementById("sovHeartbeatContext");

        if (tickCount) tickCount.textContent = `Tick #${hb.total_ticks || 0}`;
        if (hbStatus) hbStatus.textContent = hb.is_running ? "RUNNING (30s)" : "IDLE";
        if (hbContext && hb.last_tick_context) {
          hbContext.textContent = JSON.stringify(hb.last_tick_context, null, 2);
        }
      }

      // 4. Children Lineage
      const repRes = await fetch("/api/sovereignty/replication/children");
      if (repRes.ok) {
        const repData = await repRes.json();
        const listEl = document.getElementById("sovChildrenList");
        if (listEl) {
          const children = repData.children || [];
          if (children.length === 0) {
            listEl.innerHTML = `<div style="text-align:center; padding: 20px; color:#64748b;">No child worker subagents active. Spawn one below!</div>`;
          } else {
            listEl.innerHTML = children.map(c => `
              <div class="child-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                  <strong>${c.name}</strong>
                  <span class="status-pill status-${(c.status || '').toLowerCase()}">${c.status}</span>
                </div>
                <div style="font-size:0.8rem; color:#475569; margin: 4px 0;">Prompt: ${c.genesis_prompt}</div>
                <div style="font-size:0.75rem; color:#94a3b8;">
                  Turns: ${c.turns_executed}/${c.max_turns} | Spent: $${(c.spent_usd || 0).toFixed(2)} / $${(c.allocated_budget_usd || 0).toFixed(2)}
                </div>
              </div>
            `).join("");
          }
        }
      }

      // 5. Crypto Treasury & Guardrails
      const txRes = await fetch("/api/sovereignty/treasury");
      if (txRes.ok) {
        const txData = await txRes.json();
        const addrEl = document.getElementById("sovWalletAddress");
        const usdcEl = document.getElementById("sovBalanceUSDC");
        const ethEl = document.getElementById("sovBalanceETH");
        const guardEl = document.getElementById("sovGuardrailsStatus");
        const scanEl = document.getElementById("sovBasescanLink");

        if (addrEl) addrEl.textContent = txData.address || "0x...";
        if (usdcEl) usdcEl.textContent = `$${(txData.balances?.USDC || 0).toFixed(2)} USDC`;
        if (ethEl) ethEl.textContent = `${(txData.balances?.ETH || 0).toFixed(4)} ETH`;
        if (scanEl && txData.basescan_url) {
          scanEl.href = txData.basescan_url;
          scanEl.style.display = "inline";
        }
        if (guardEl && txData.guardrails) {
          const g = txData.guardrails;
          guardEl.innerHTML = `<strong>Ceilings:</strong> $${g.limits.max_single_tx_usd.toFixed(2)} / tx | <strong>24h Spend:</strong> $${g.spent_last_24h_usd.toFixed(2)} / $${g.limits.daily_limit_usd.toFixed(2)} (Remaining: $${g.remaining_daily_budget_usd.toFixed(2)})`;
        }
      }
    } catch (e) {
      console.warn("[PortalController] Sovereign sync warning:", e);
    }
  };

  // Actions
  window.triggerSoulReflection = async function () {
    const note = prompt("Enter an operational or strategic breakthrough for SOUL.md reflection:", "Routine operational calibration");
    if (note === null) return;
    try {
      const res = await fetch("/api/sovereignty/reflect", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ note })
      });
      const data = await res.json();
      alert(`Soul Reflection Logged! New Revision: ${data.revision} (${Math.round(data.genesis_alignment * 100)}% alignment)`);
      window.refreshSovereignData();
    } catch (e) {
      alert("Failed to trigger reflection: " + e);
    }
  };

  window.setSurvivalOverride = async function (tier) {
    try {
      const res = await fetch("/api/sovereignty/survival/override", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ tier })
      });
      const data = await res.json();
      alert(data.message || "Survival tier updated.");
      window.refreshSovereignData();
    } catch (e) {
      alert("Failed to update survival tier: " + e);
    }
  };

  window.forceHeartbeatTick = async function () {
    try {
      const res = await fetch("/api/sovereignty/heartbeat/tick", { method: "POST" });
      const data = await res.json();
      alert(`Tick evaluated! Tier: ${data.survival_tier.toUpperCase()}, Wake Required: ${data.should_wake_agent}`);
      window.refreshSovereignData();
    } catch (e) {
      alert("Failed to force tick: " + e);
    }
  };

  window.spawnChildWorker = async function () {
    const name = document.getElementById("sovSpawnName")?.value;
    const promptText = document.getElementById("sovSpawnPrompt")?.value;
    const budget = parseFloat(document.getElementById("sovSpawnBudget")?.value || "0.50");

    if (!name || !promptText) {
      alert("Please provide both a worker name and genesis prompt.");
      return;
    }

    try {
      const res = await fetch("/api/sovereignty/replication/spawn", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, genesis_prompt: promptText, budget_usd: budget })
      });
      const data = await res.json();
      alert(`Spawned child worker '${data.name}' (ID: ${data.child_id})!`);
      if (document.getElementById("sovSpawnName")) document.getElementById("sovSpawnName").value = "";
      if (document.getElementById("sovSpawnPrompt")) document.getElementById("sovSpawnPrompt").value = "";
      window.refreshSovereignData();
    } catch (e) {
      alert("Failed to spawn child worker: " + e);
    }
  };

  window.sendCryptoPayment = async function () {
    const to = prompt("Enter 0x Ethereum/Base Recipient Address (42 chars):", "");
    if (!to || !to.trim().startsWith("0x")) {
      alert("Invalid EVM address.");
      return;
    }
    const amt = parseFloat(prompt("Enter amount to spend in Base USDC (Max single tx: $15.00):", "1.00") || "0");
    if (!amt || amt <= 0) return;
    const reason = prompt("Enter operational justification / reason:", "Autonomous tool license") || "Agent expenditure";

    try {
      const res = await fetch("/api/sovereignty/treasury/send", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ recipient_address: to.trim(), amount_usdc: amt, reason })
      });
      const data = await res.json();
      if (data.success) {
        alert(`Payment Dispatched!\nTx Hash: ${data.tx_hash}\nStatus: ${data.status}\nNew Balance: $${data.new_balance_usdc} USDC\nBasescan: ${data.basescan_url}`);
      } else {
        alert(`Payment Blocked: ${data.error || "Policy violation"}`);
      }
      window.refreshSovereignData();
    } catch (e) {
      alert("Payment failed: " + e);
    }
  };

  window.testAutoX402 = async function () {
    try {
      alert("Triggering Coinbase x402 cycle against /api/v1/x402/service...\nNexus will catch HTTP 402, parse the required USDC fee, verify policy guardrails, sign the on-chain payment, and unlock the resource!");
      const res = await fetch("/api/sovereignty/treasury/x402-pay", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ endpoint_url: window.location.origin + "/api/v1/x402/service", max_budget_usdc: 5.0 })
      });
      const data = await res.json();
      if (data.success) {
        alert(`x402 Commerce Success!\nUnlocked: ${JSON.stringify(data.response, null, 2)}\nPayment Tx: ${data.payment_tx_hash}`);
      } else {
        alert(`x402 Failed: ${data.error}`);
      }
      window.refreshSovereignData();
    } catch (e) {
      alert("x402 execution failed: " + e);
    }
  };

  window.settleCryptoToBank = async function () {
    const amt = parseFloat(prompt("Enter amount of Base USDC to off-ramp directly to MCB Bank (000443260370):", "50.00") || "0");
    if (!amt || amt <= 0) return;
    try {
      const res = await fetch("/api/sovereignty/treasury/settle-bank", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ amount_usdc: amt, notes: "Automated Off-ramp from Dashboard" })
      });
      const data = await res.json();
      if (data.success) {
        alert(`Bank Off-ramp Successful!\nDispatched: $${data.amount_usdc} USDC -> Rs ${data.amount_mur} MUR\nBeneficiary: ${data.beneficiary_name} (MCB ${data.beneficiary_account})\nTx: ${data.tx_hash}`);
      } else {
        alert(`Bank Settle Failed: ${data.error}`);
      }
      window.refreshSovereignData();
    } catch (e) {
      alert("Settlement failed: " + e);
    }
  };

  // Wire up when DOM is ready
  document.addEventListener("DOMContentLoaded", () => {
    // Add sovereign-core to page titles map
    const origNav = window.navigateToPage;
    window.navigateToPage = function (targetTab) {
      if (targetTab === "sovereign-core") {
        document.querySelectorAll(".tab-pane").forEach((p) => {
          if (p.id === "pane-sovereign-core") {
            p.classList.add("active");
            p.style.display = "block";
          } else {
            p.classList.remove("active");
            p.style.display = "none";
          }
        });
        const titleEl = document.getElementById("pageTitle");
        if (titleEl) titleEl.textContent = "Sovereign Core & Survival Physics";
        window.refreshSovereignData();
        return;
      }
      if (typeof origNav === "function") {
        origNav(targetTab);
      }
    };
  });
})();
