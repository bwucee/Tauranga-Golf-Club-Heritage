// Open a targeted group or period when a reader follows a permanent fragment link.
(() => {
  function revealTarget() {
    if (!location.hash) return;
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    const target = document.getElementById(id);
    if (!target) return;
    if (target.matches('details')) target.open = true;
    let parent = target.parentElement;
    while (parent) { if (parent.matches('details')) parent.open = true; parent = parent.parentElement; }
  }
  revealTarget();
  addEventListener('hashchange', revealTarget);
})();
