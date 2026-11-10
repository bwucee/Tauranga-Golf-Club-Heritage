/* Open the current original-book page as linked web text. */
(() => {
  const file = new URLSearchParams(location.search).get('file') || '';
  if (file.split('/').pop() !== 'pars-from-the-past.pdf') return;
  const link = document.getElementById('linked-book-page');
  const update = page => {
    const n = Number(page);
    if (!Number.isInteger(n) || n < 1 || n > 305) return;
    link.href = `../../book-page-${String(n).padStart(3, '0')}.html`;
    link.hidden = false;
  };
  const hashPage = () => update(new URLSearchParams(location.hash.slice(1)).get('page') || 1);
  hashPage();
  window.addEventListener('hashchange', hashPage);
  const connect = () => {
    const app = window.PDFViewerApplication;
    if (!app) return;
    app.initializedPromise.then(() => {
      app.eventBus.on('pagechanging', event => update(event.pageNumber));
      if (app.pdfDocument) update(app.page);
    });
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', connect, {once: true});
  else connect();
})();
