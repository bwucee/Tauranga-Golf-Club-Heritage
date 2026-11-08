/* Search stays on this static site; no query is transmitted to another service. */
(() => {
  const form = document.getElementById('collection-search');
  const input = document.getElementById('search-input');
  const status = document.getElementById('search-status');
  const results = document.getElementById('search-results');
  let indexPromise;
  let request = 0;
  const normalise = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  async function search() {
    const current = ++request;
    const query = input.value.trim();
    results.replaceChildren();
    if (query.length < 2) { status.textContent = 'Enter at least two characters.'; return; }
    status.textContent = 'Searching…';
    try {
      indexPromise ||= fetch('assets/search-index.json').then(response => {
        if (!response.ok) throw new Error('Search index unavailable');
        return response.json();
      });
      const entries = await indexPromise;
      if (current !== request) return;
      const words = normalise(query).split(/\s+/).filter(Boolean);
      const matches = entries.filter(entry => words.every(word => normalise(entry.title + ' ' + entry.text).includes(word)));
      matches.sort((a,b) => (normalise(b.title).includes(words[0]) ? 1 : 0) - (normalise(a.title).includes(words[0]) ? 1 : 0));
      status.textContent = `${matches.length} result${matches.length === 1 ? '' : 's'} for “${query}”.`;
      if (!matches.length) { status.textContent += ' Try a surname or fewer words.'; return; }
      const fragment = document.createDocumentFragment();
      matches.forEach(entry => {
        const article = document.createElement('article');
        article.className = 'search-result';
        const tag = document.createElement('span'); tag.className = 'eyebrow'; tag.textContent = entry.type;
        const title = document.createElement('h2');
        const link = document.createElement('a'); link.href = entry.url; link.textContent = entry.title; title.append(link);
        const para = document.createElement('p');
        const offset = Math.max(0, normalise(entry.text).indexOf(words[0]) - 85);
        para.textContent = (offset ? '…' : '') + entry.text.slice(offset, offset + 290) + (offset + 290 < entry.text.length ? '…' : '');
        article.append(tag, title, para); fragment.append(article);
      });
      results.append(fragment);
    } catch (error) {
      if (current === request) status.textContent = 'Search could not load. Please try again or browse the book chapters.';
      indexPromise = undefined;
    }
  }
  form.addEventListener('submit', event => { event.preventDefault(); search(); });
  const existing = new URLSearchParams(location.search).get('q');
  if (existing) { input.value = existing; search(); }
})();
