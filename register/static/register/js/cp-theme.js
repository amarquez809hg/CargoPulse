(function () {
  var STORAGE_KEY = "cp-theme";
  var root = document.documentElement;

  var ICONS = {
    dark: '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M12 2v2M12 20v2M4.2 4.2l1.4 1.4M18.4 18.4l1.4 1.4M2 12h2M20 12h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>',
    light: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 14.5A7.5 7.5 0 0 1 9.5 4 6 6 0 1 0 20 14.5Z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>',
  };

  function getTheme() {
    return root.getAttribute("data-theme") === "light" ? "light" : "dark";
  }

  function setTheme(theme) {
    var next = theme === "light" ? "light" : "dark";
    root.setAttribute("data-theme", next);
    try {
      localStorage.setItem(STORAGE_KEY, next);
    } catch (e) {}
    updateToggle(next);
  }

  function updateToggle(theme) {
    var btn = document.getElementById("cp-theme-toggle");
    var icon = document.getElementById("cp-theme-icon");
    if (!btn || !icon) return;

    var isLight = theme === "light";
    icon.innerHTML = isLight ? ICONS.light : ICONS.dark;

    var label =
      btn.getAttribute("data-" + (isLight ? "label-dark" : "label-light")) ||
      (isLight ? "Switch to dark mode" : "Switch to light mode");
    var title =
      btn.getAttribute("data-" + (isLight ? "title-dark" : "title-light")) ||
      (isLight ? "Dark mode" : "Light mode");

    btn.setAttribute("aria-label", label);
    btn.setAttribute("title", title);
  }

  function init() {
    updateToggle(getTheme());

    var btn = document.getElementById("cp-theme-toggle");
    if (!btn) return;

    btn.addEventListener("click", function (event) {
      event.preventDefault();
      event.stopPropagation();
      setTheme(getTheme() === "dark" ? "light" : "dark");
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
