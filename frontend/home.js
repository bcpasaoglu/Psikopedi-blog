import { HERO, ILLUSTRATIONS, categoryArt } from './illustrations.js';
import {
  BRAND_MARK, categoryColor, getCategories, getJSON, prefersReducedMotion, renderArticleCard, renderMessage,
} from './app.js';

const $ = sel => document.querySelector(sel);
const state = { category: null, q: '' };

$('[data-brand-mark]').innerHTML = BRAND_MARK;
$('[data-hero-art]').innerHTML = HERO;
$('[data-about-art]').innerHTML = ILLUSTRATIONS.farkindalik;

function renderCategories(categories) {
  const list = $('[data-categories]');
  list.replaceChildren(...categories.map(cat => {
    const li = document.createElement('li');
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'category-card';
    btn.dataset.slug = cat.slug;
    btn.style.background = categoryColor(cat.slug);
    btn.setAttribute('aria-pressed', 'false');
    btn.setAttribute('aria-label', `${cat.name}: ${cat.count} yazı`);
    const count = document.createElement('span');
    count.className = 'count';
    count.textContent = cat.count;
    const name = document.createElement('span');
    name.className = 'name';
    name.textContent = cat.name;
    const art = document.createElement('span');
    art.className = 'art';
    art.setAttribute('aria-hidden', 'true');
    art.innerHTML = categoryArt(cat.slug);
    btn.append(count, name, art);
    btn.addEventListener('click', () => {
      setCategory(state.category === cat.slug ? null : cat.slug, categories);
      $('#yazilar').scrollIntoView({ behavior: prefersReducedMotion() ? 'auto' : 'smooth' });
    });
    li.appendChild(btn);
    return li;
  }));
}

function setCategory(slug, categories) {
  state.category = slug;
  document.querySelectorAll('.category-card').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.slug === slug)));
  const filter = $('[data-active-filter]');
  filter.hidden = !slug;
  if (slug) $('[data-active-filter-label]').textContent = `Kategori: ${categories.find(c => c.slug === slug)?.name ?? slug}`;
  loadArticles(categories);
}

let requestId = 0;
async function loadArticles(categories) {
  const list = $('[data-articles]');
  const params = new URLSearchParams({ limit: '12' });
  if (state.category) params.set('category', state.category);
  if (state.q) params.set('q', state.q);
  const id = ++requestId;
  try {
    const { data, total } = await getJSON(`/api/articles?${params}`);
    if (id !== requestId) return; // a newer search already replaced this one
    $('[data-total]').textContent = total;
    if (!data.length) return renderMessage(list, 'empty', 'Bu aramaya uygun yazı bulunamadı.');
    list.replaceChildren(...data.map(a => renderArticleCard(a, categories)));
    if (window.gsap && !prefersReducedMotion()) {
      gsap.from(list.children, { y: 24, opacity: 0, stagger: 0.06, duration: 0.45, ease: 'power2.out' });
    }
  } catch (err) {
    console.error(err);
    renderMessage(list, 'error', 'Yazılar yüklenemedi. Lütfen biraz sonra tekrar dene.');
  }
}

async function init() {
  let categories = [];
  try {
    categories = await getCategories();
    renderCategories(categories);
  } catch (err) {
    console.error(err);
  }

  $('[data-clear-filter]').addEventListener('click', () => setCategory(null, categories));

  let debounce;
  const input = $('#arama');
  $('[data-search]').addEventListener('submit', e => e.preventDefault());
  input.addEventListener('input', () => {
    clearTimeout(debounce);
    debounce = setTimeout(() => { state.q = input.value.trim(); loadArticles(categories); }, 250);
  });

  $('[data-random-article]').addEventListener('click', async e => {
    e.preventDefault();
    try {
      const { data } = await getJSON('/api/articles?limit=100');
      if (data.length) location.href = `article.html?id=${encodeURIComponent(data[Math.floor(Math.random() * data.length)].slug)}`;
    } catch (err) {
      console.error(err);
    }
  });

  await loadArticles(categories);

  if (window.gsap && !prefersReducedMotion()) {
    gsap.from('.category-grid > li', { y: 18, opacity: 0, stagger: 0.07, duration: 0.45, ease: 'back.out(1.6)' });
    gsap.from('.hero-art svg', { scale: 0.9, opacity: 0, duration: 0.6, ease: 'back.out(1.4)' });
    gsap.to('.hero h1 .wave', { rotate: 18, duration: 0.25, repeat: 5, yoyo: true, ease: 'sine.inOut', delay: 0.4 });
  }
}

// GSAP is loaded with `defer`; module scripts run after deferred classic scripts.
init();
