/* ================================================================
   M/S. SOTOTA MACHINERIES STORE — main.js
   ================================================================ */

// ── MOBILE NAV ────────────────────────────────────────────────────────
function toggleMob() {
  const m = document.getElementById('mobnav');
  const b = document.getElementById('hbtn');
  if (!m) return;
  const open = m.classList.toggle('open');
  if (b) b.setAttribute('aria-expanded', open);
}
function closeMob() {
  const m = document.getElementById('mobnav');
  const b = document.getElementById('hbtn');
  if (m) m.classList.remove('open');
  if (b) b.setAttribute('aria-expanded', 'false');
}

// ── SCROLL REVEAL ─────────────────────────────────────────────────────
function initReveal() {
  const obs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('in-view');
        obs.unobserve(e.target);
      }
    });
  }, { threshold: 0.07 });
  document.querySelectorAll('.reveal').forEach(el => obs.observe(el));
}

// ── SUB-TAB SWITCH ────────────────────────────────────────────────────
function switchTab(btn, panelId) {
  const scope = btn.closest('section') || document;
  scope.querySelectorAll('.sub-tab').forEach(b => b.classList.remove('active'));
  scope.querySelectorAll('.sub-panel').forEach(p => p.classList.remove('active'));
  btn.classList.add('active');
  const panel = document.getElementById(panelId);
  if (panel) panel.classList.add('active');
  setTimeout(initReveal, 80);
}

// ── PRODUCT SEARCH/FILTER ─────────────────────────────────────────────
function filterProducts() {
  const q     = (document.getElementById('srch')?.value || '').toLowerCase();
  const badge = document.getElementById('badge-filter')?.value || '';
  document.querySelectorAll('.prod-card').forEach(card => {
    const name  = (card.dataset.name  || '').toLowerCase();
    const brand = (card.dataset.brand || '').toLowerCase();
    const model = (card.dataset.model || '').toLowerCase();
    const b     = card.dataset.badge || '';
    const matchQ = !q    || name.includes(q) || brand.includes(q) || model.includes(q);
    const matchB = !badge || b === badge;
    card.style.display = (matchQ && matchB) ? '' : 'none';
  });
}

// ── ADMIN: Image preview ──────────────────────────────────────────────
function previewImage(input) {
  const preview = document.getElementById('img-preview');
  if (!preview) return;
  const file = input.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = e => {
      preview.src = e.target.result;
      preview.style.display = 'block';
    };
    reader.readAsDataURL(file);
  }
}

function previewImageUrl() {
  const url     = document.getElementById('image_url')?.value.trim();
  const preview = document.getElementById('img-preview-url');
  if (!preview || !url) return;
  preview.src   = url;
  preview.style.display = 'block';
  preview.onerror = () => { preview.style.display = 'none'; };
}

// ── ADMIN: Toggle product active/inactive via AJAX ────────────────────
function toggleProduct(pid, btn) {
  fetch(`/admin/products/toggle/${pid}`, { method: 'POST' })
    .then(r => r.json())
    .then(data => {
      const label = btn.nextElementSibling;
      if (data.is_active) {
        btn.checked = true;
        if (label) label.textContent = 'Visible';
      } else {
        btn.checked = false;
        if (label) label.textContent = 'Hidden';
      }
    })
    .catch(() => alert('Failed to update. Please try again.'));
}

// ── ADMIN: Confirm delete ─────────────────────────────────────────────
function confirmDelete(name) {
  return confirm(`Delete "${name}"?\n\nThis cannot be undone.`);
}

// ── FLASH MESSAGE AUTO-DISMISS ────────────────────────────────────────
function initFlashDismiss() {
  document.querySelectorAll('.alert').forEach(el => {
    setTimeout(() => {
      el.style.transition = 'opacity .4s';
      el.style.opacity = '0';
      setTimeout(() => el.remove(), 400);
    }, 5000);
  });
}

// ── INIT ──────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  initReveal();
  initFlashDismiss();

  // Close mobile nav when clicking outside
  document.addEventListener('click', e => {
    const mob = document.getElementById('mobnav');
    const btn = document.getElementById('hbtn');
    if (mob && mob.classList.contains('open') && !mob.contains(e.target) && btn && !btn.contains(e.target)) {
      closeMob();
    }
  });
});
