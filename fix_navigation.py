with open('static/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

navigation_code = """
// --- Robust Global Navigation Controller ---
window.navigateToPage = function(targetTab) {
  document.querySelectorAll('.tab-pane').forEach(pane => {
    pane.classList.remove('active');
    pane.style.display = 'none';
  });

  let targetPane = document.getElementById('pane-' + targetTab) || document.getElementById(targetTab);
  if (targetPane) {
    targetPane.classList.add('active');
    targetPane.style.display = 'block';
  }

  document.querySelectorAll('.nav-item').forEach(item => {
    if (item.dataset.tab === targetTab) {
      item.classList.add('active');
    } else {
      item.classList.remove('active');
    }
  });

  const titleEl = document.getElementById('pageTitle');
  if (titleEl) {
    const titles = {
      'ceo-cockpit': 'Solo Founder Dashboard',
      'domain-comms': 'CRM & Communications',
      'domain-operations': 'Operations & Lead Generation',
      'domain-commerce': 'Treasury & Markets',
      'workforce': 'Agent Workforce & Operations',
      'sovereign-core': 'Sovereign Core & Survival Physics'
    };
    if (titles[targetTab]) {
      titleEl.textContent = titles[targetTab];
    }
  }
};

document.addEventListener('click', (e) => {
  const navItem = e.target.closest('.nav-item');
  if (navItem && navItem.dataset.tab) {
    e.preventDefault();
    const tabId = navItem.dataset.tab;
    window.navigateToPage(tabId);
  }
});
// ------------------------------------------
"""

code = navigation_code + "\n" + code

with open('static/app.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("Navigation controller successfully injected into static/app.js!")
