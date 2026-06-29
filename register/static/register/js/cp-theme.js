(function () {
  var STORAGE_KEY = "cp-theme";
  var root = document.documentElement;

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
    if (!btn) return;

    var sun = btn.querySelector(".cp-theme-icon--sun");
    var moon = btn.querySelector(".cp-theme-icon--moon");
    var isLight = theme === "light";

    if (sun) sun.hidden = isLight;
    if (moon) moon.hidden = !isLight;

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
