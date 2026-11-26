import { BRAND_MARK, getCategories, getJSON, renderArticleCard, renderChip, renderCover, renderMeta } from './app.js';

const $ = sel => document.querySelector(sel);
$('[data-brand-mark]').innerHTML = BRAND_MARK;

function showError(message) {
  $('[data-title]').textContent = message;
  $('[data-article]').setAttribute('aria-busy', 'false');
}

async function init() {
  const params = new URLSearchParams(location.search);
  const idOrSlug = params.get('id') || params.get('slug');
  if (!idOrSlug) return showError('Yazı bulunamadı.');

  let article;
  let categories = [];
  try {
    [{ data: article }, categories] = await Promise.all([
      getJSON(`/api/articles/${encodeURIComponent(idOrSlug)}`),
      getCategories().catch(() => []),
    ]);
  } catch (err) {
    console.error(err);
    return showError('Bu yazı yüklenemedi ya da artık yayında değil.');
  }

  document.title = `${article.title} | Psikopedi`;
  document.querySelector('meta[name="description"]').content = article.summary || article.title;
  $('[data-chip]').replaceChildren(renderChip(article.category, categories));
  $('[data-title]').textContent = article.title;
  $('[data-meta]').replaceChildren(renderMeta(article));
  $('[data-cover]').replaceWith(renderCover(article, 'article-cover'));

  const body = $('[data-body]');
  if (window.DOMPurify) {
    body.innerHTML = DOMPurify.sanitize(article.content || article.summary);
  } else {
    // Sanitizer failed to load: show plain text rather than unsanitized HTML.
    body.textContent = article.content || article.summary;
  }
  $('[data-article]').setAttribute('aria-busy', 'false');

  try {
    const { data } = await getJSON(`/api/articles?category=${encodeURIComponent(article.category)}&limit=3`);
    const related = data.filter(a => a.id !== article.id).slice(0, 2);
    if (related.length) {
      $('[data-related-list]').replaceChildren(...related.map(a => renderArticleCard(a, categories)));
      $('[data-related]').hidden = false;
    }
  } catch (err) {
    console.error(err);
  }
}

init();
