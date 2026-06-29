/**
 * Cargo Pulse theme helper (no UI toggle).
 * Light mode is the site default. Dark mode styles remain in cp-theme.css
 * and can be enabled by setting data-theme="dark" on <html>.
 */
(function () {
  var root = document.documentElement;
  if (!root.getAttribute("data-theme")) {
    root.setAttribute("data-theme", "light");
  }
})();
