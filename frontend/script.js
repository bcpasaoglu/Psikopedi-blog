



// Core interactions: menu, theme toggle, smooth scrolling, and simple form validation
document.addEventListener('DOMContentLoaded', () => {
  // Mobile menu toggle (add data-menu-btn to the button)
  const menuBtn = document.querySelector('[data-menu-btn]');
  const nav = document.querySelector('nav');
  if (menuBtn && nav) menuBtn.addEventListener('click', () => nav.classList.toggle('open'));

  // Theme switcher (add data-theme-toggle to the button)
  const themeBtn = document.querySelector('[data-theme-toggle]');
  const root = document.documentElement;
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme) root.setAttribute('data-theme', savedTheme);
  if (themeBtn) themeBtn.addEventListener('click', () => {
    const next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
  });

  // Smooth scrolling for in-page anchor links
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', (e) => {
      const target = document.querySelector(a.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });

  // Simple form validation for id="contact-form"
  const form = document.getElementById('contact-form');
  if (form) {
    form.addEventListener('submit', (e) => {
      const email = form.querySelector('input[name="email"]');
      if (email && !/^\S+@\S+\.\S+$/.test(email.value)) {
        e.preventDefault();
        alert('Please enter a valid email address.');
        email.focus();
      }
    });
  }

  // GSAP animations: loading screen, nav and content entrances
  if (window.gsap) {
    const $loader = document.querySelector('.loader-wrapper');
    const $loaderText = document.querySelector('.loader-text');
    const $loaderLine = document.querySelector('.loader-line');
    const $comic = document.querySelectorAll('.comic-effects > *');

    const tl = gsap.timeline({ defaults: { ease: 'power2.out' } });

    if ($loaderText) tl.fromTo($loaderText, { y: 20, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6 });
    if ($loaderLine) tl.fromTo($loaderLine, { scaleX: 0 }, { scaleX: 1, transformOrigin: 'left center', duration: 0.6 }, '-=0.4');
    if ($comic.length) tl.from($comic, { scale: 0, opacity: 0, stagger: 0.08, duration: 0.35 }, '-=0.3');

    // Remove loader and reveal main content
    tl.to($loader || {}, { yPercent: -100, duration: 0.7, delay: 0.35, onComplete: () => {
      if ($loader && $loader.parentNode) $loader.parentNode.removeChild($loader);
    }});

    // Navbar, featured section and footer animations
    tl.from('nav', { y: -10, opacity: 0, duration: 0.6 }, '-=0.2');
    tl.from('.featured-section', { y: 20, opacity: 0, duration: 0.6 }, '-=0.3');
    tl.from('.blog-list > *', { y: 20, opacity: 0, stagger: 0.08, duration: 0.45 }, '-=0.45');
    tl.from('footer', { y: 10, opacity: 0, duration: 0.5 }, '-=0.4');

    // Subtle micro-interaction: social icon hover effects
    document.querySelectorAll('.social-links a').forEach(a => {
      a.addEventListener('mouseenter', () => gsap.to(a, { scale: 1.08, duration: 0.15 }));
      a.addEventListener('mouseleave', () => gsap.to(a, { scale: 1, duration: 0.15 }));
    });
  }
  // Fallback: if GSAP fails to load, clean up loader and show nav
  setTimeout(() => {
    const loader = document.querySelector('.loader-wrapper');
    if (loader) {
      if (loader.parentNode) loader.parentNode.removeChild(loader);
    }
    const navEl = document.querySelector('nav');
    if (navEl) {
      navEl.style.transform = 'none';
      navEl.style.opacity = '1';
    }
  }, 1500);

  // Backend article integration: fetches from /api/articles and renders cards into .blog-list
  (function loadArticlesFromBackend() {
    // Only run on pages that have a .blog-list (skip article detail pages)
    if (!document.querySelector('.blog-list')) return;

    const endpoint = '/api/articles';

    // Disable cache for development so we always get fresh data
    fetch(endpoint, { cache: 'no-store' })
      .then(res => {
        if (!res.ok) throw new Error('Network error: ' + res.status);
        return res.json();
      })
      .then(data => {
        if (!Array.isArray(data)) return;

        const blogList = document.querySelector('.blog-list');
        if (!blogList) return;

        blogList.innerHTML = '';
        data.forEach((m, i) => {
          const id = m.id ?? m.slug ?? `local-${i}`;
          // Store full content if present
          try { if (m.content) localStorage.setItem('article_' + id, m.content); } catch (e) {}

          const link = document.createElement('a');
          link.className = 'blog-card';
          link.href = `article.html?id=${encodeURIComponent(id)}`;

          const imgWrap = document.createElement('div');
          imgWrap.className = 'card-image';
          const img = document.createElement('img');
          img.src = m.image_url || `https://picsum.photos/600/400?random=${i+20}`;
          img.alt = m.title || 'Article image';
          imgWrap.appendChild(img);

          const content = document.createElement('div');
          content.className = 'card-content';
          const date = document.createElement('div');
          date.className = 'date';
          date.textContent = new Date(m.date || Date.now()).toLocaleDateString('tr-TR');
          const h3 = document.createElement('h3');
          h3.textContent = m.title || 'Untitled article';
          const p = document.createElement('p');
          p.textContent = m.summary || '';

          content.appendChild(date);
          content.appendChild(h3);
          content.appendChild(p);

          link.appendChild(imgWrap);
          link.appendChild(content);
          blogList.appendChild(link);
        });
      })
      .catch(err => console.warn('Failed to load articles:', err));
  })();
});
