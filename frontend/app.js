// Shared helpers for the home and article pages. Every value that comes from
// the API is written with textContent or element properties, never as HTML.
import { categoryArt } from './illustrations.js';

export const BRAND_MARK = `<svg viewBox="0 0 64 64" aria-hidden="true"><path d="M32 50c-14-9-20-16-20-23 0-6 5-11 11-11 4 0 7 2 9 6 2-4 5-6 9-6 6 0 11 5 11 11 0 7-6 14-20 23z" fill="#d9381e" stroke="#1f1b2e" stroke-width="4.5" stroke-linejoin="round"/></svg>`;

const dateFormat = new Intl.DateTimeFormat('tr-TR', { day: 'numeric', month: 'long', year: 'numeric' });

export const formatDate = iso => {
  const d = new Date(iso);
  return Number.isNaN(d.getTime()) ? '' : dateFormat.format(d);
};

export async function getJSON(url) {
  const res = await fetch(url, { headers: { Accept: 'application/json' } });
  if (!res.ok) throw new Error(`${url} -> ${res.status}`);
  return { data: await res.json(), total: Number(res.headers.get('X-Total-Count') ?? 0) };
}

let categoriesPromise;
export function getCategories() {
  categoriesPromise ??= getJSON('/api/categories').then(r => r.data);
  return categoriesPromise;
}

const el = (tag, className, text) => {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text != null) node.textContent = text;
  return node;
};

export const categoryColor = slug => `var(--c-${slug}, #fff)`;

/** Cover for an article: its image when set, otherwise the category illustration. */
export function renderCover(article, className) {
  const cover = el('div', className);
  cover.style.background = categoryColor(article.category);
  if (article.image_url) {
    const img = el('img');
    img.src = article.image_url;
    img.alt = '';
    img.loading = 'lazy';
    cover.appendChild(img);
  } else {
    cover.innerHTML = categoryArt(article.category); // static, trusted SVG
  }
  return cover;
}

export function renderChip(slug, categories) {
  const cat = categories.find(c => c.slug === slug);
  const chip = el('span', 'chip', cat ? cat.name : slug);
  chip.style.background = categoryColor(slug);
  return chip;
}

export function renderMeta(article) {
  const meta = el('p', 'meta');
  const time = el('time', null, formatDate(article.date));
  time.dateTime = article.date;
  meta.append(time, el('span', null, '·'), el('span', null, `${article.reading_minutes} dk okuma`));
  return meta;
}

export function renderArticleCard(article, categories) {
  const li = el('li');
  const link = el('a', 'article-card');
  link.href = `article.html?id=${encodeURIComponent(article.slug)}`;
  const body = el('div', 'card-body');
  body.append(renderChip(article.category, categories), el('h3', null, article.title), el('p', null, article.summary), renderMeta(article));
  link.append(renderCover(article, 'cover'), body);
  li.appendChild(link);
  return li;
}

export function renderMessage(list, className, text) {
  list.replaceChildren(el('li', className, text));
}

export const prefersReducedMotion = () => window.matchMedia('(prefers-reduced-motion: reduce)').matches;
