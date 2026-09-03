// WorkSphere Enterprise Interactive Scripts
document.addEventListener('DOMContentLoaded', () => {
  // Theme Toggle
  const themeToggle = document.getElementById('theme-toggle-btn');
  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
      document.documentElement.setAttribute('data-theme', isDark ? 'light' : 'dark');
      fetch('/theme/toggle/', { credentials: 'same-origin' });
    });
  }

  // Auto-dismiss Alerts after 5 seconds
  const alerts = document.querySelectorAll('.alert-dismissible');
  alerts.forEach(alert => {
    setTimeout(() => {
      alert.style.opacity = '0';
      setTimeout(() => alert.remove(), 300);
    }, 5000);
  });

  // Global Search Autocomplete
  const searchInput = document.getElementById('global-search-input');
  const searchResults = document.getElementById('search-dropdown-results');
  if (searchInput && searchResults) {
    let timeout = null;
    searchInput.addEventListener('input', (e) => {
      clearTimeout(timeout);
      const q = e.target.value.trim();
      if (q.length < 2) {
        searchResults.style.display = 'none';
        return;
      }
      timeout = setTimeout(() => {
        fetch(/search/?q=, {
          headers: { 'X-Requested-With': 'XMLHttpRequest' }
        })
        .then(res => res.json())
        .then(data => {
          let html = '';
          if (data.employees && data.employees.length > 0) {
            html += '<div style="padding: 8px 12px; font-weight: bold; font-size: 0.75rem; color: #64748b; background: #f8fafc;">EMPLOYEES</div>';
            data.employees.forEach(emp => {
              html += <a href="/employees//" style="display: block; padding: 8px 12px; border-bottom: 1px solid #f1f5f9; color: #1e293b; text-decoration: none;">
                <div style="font-weight: 600; font-size: 0.85rem;"> <span style="font-size: 0.75rem; color: #64748b;">()</span></div>
                <div style="font-size: 0.75rem; color: #64748b;"> • </div>
              </a>;
            });
          }
          if (data.departments && data.departments.length > 0) {
            html += '<div style="padding: 8px 12px; font-weight: bold; font-size: 0.75rem; color: #64748b; background: #f8fafc;">DEPARTMENTS</div>';
            data.departments.forEach(d => {
              html += <a href="/organizations/departments/" style="display: block; padding: 8px 12px; border-bottom: 1px solid #f1f5f9; color: #1e293b; text-decoration: none;">
                <div style="font-weight: 600; font-size: 0.85rem;"> <span style="font-size: 0.75rem; color: #64748b;">()</span></div>
              </a>;
            });
          }
          if (!html) {
            html = '<div style="padding: 12px; font-size: 0.85rem; color: #64748b;">No matching results found.</div>';
          }
          searchResults.innerHTML = html;
          searchResults.style.display = 'block';
        });
      }, 300);
    });

    document.addEventListener('click', (e) => {
      if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
        searchResults.style.display = 'none';
      }
    });
  }
});
