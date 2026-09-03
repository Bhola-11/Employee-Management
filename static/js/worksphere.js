document.addEventListener('DOMContentLoaded', function() {
  // 1. Sidebar Toggle
  const sidebarToggle = document.getElementById('sidebarToggle');
  const sidebar = document.querySelector('.sidebar');
  if (sidebarToggle && sidebar) {
    sidebarToggle.addEventListener('click', () => {
      sidebar.classList.toggle('open');
    });
  }

  // 2. User Menu Dropdown Toggle
  const userMenuBtn = document.getElementById('userMenuBtn');
  const userDropdownMenu = document.getElementById('userDropdownMenu');
  if (userMenuBtn && userDropdownMenu) {
    userMenuBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      userDropdownMenu.classList.toggle('show');
    });
    document.addEventListener('click', () => {
      userDropdownMenu.classList.remove('show');
    });
  }

  // 3. Dark/Light Mode Switcher
  const themeToggle = document.getElementById('themeToggle');
  const currentTheme = localStorage.getItem('theme') || 'light';
  if (currentTheme === 'dark') {
    document.documentElement.setAttribute('data-theme', 'dark');
  }
  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
      const nextTheme = isDark ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', nextTheme);
      localStorage.setItem('theme', nextTheme);
    });
  }

  // 4. Live Digital Clock in Attendance Desk
  const liveClockEl = document.getElementById('liveClock');
  if (liveClockEl) {
    setInterval(() => {
      const now = new Date();
      liveClockEl.textContent = now.toLocaleTimeString();
    }, 1000);
  }

  // 5. Auto dismiss alert toasts
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(alert => {
    setTimeout(() => {
      alert.style.opacity = '0';
      alert.style.transition = 'opacity 0.5s ease';
      setTimeout(() => alert.remove(), 500);
    }, 4500);
  });
});
