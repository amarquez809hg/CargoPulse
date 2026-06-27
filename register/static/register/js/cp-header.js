(function () {
  function closeAllDropdowns(except) {
    document.querySelectorAll(".cp-header-dropdown.is-open").forEach(function (el) {
      if (el !== except) {
        el.classList.remove("is-open");
      }
    });
  }

  document.querySelectorAll(".cp-header-dropdown-toggle").forEach(function (btn) {
    btn.addEventListener("click", function (event) {
      event.preventDefault();
      event.stopPropagation();
      var dropdown = btn.closest(".cp-header-dropdown");
      var willOpen = !dropdown.classList.contains("is-open");
      closeAllDropdowns();
      if (willOpen) {
        dropdown.classList.add("is-open");
      }
    });
  });

  document.addEventListener("click", function () {
    closeAllDropdowns();
  });

  document.querySelectorAll(".cp-header-dropdown").forEach(function (dropdown) {
    dropdown.addEventListener("click", function (event) {
      event.stopPropagation();
    });
  });

  var menuBtn = document.querySelector(".cp-header-menu-btn");
  var mobileNav = document.querySelector(".cp-header-nav");
  if (menuBtn && mobileNav) {
    menuBtn.addEventListener("click", function () {
      var open = mobileNav.classList.toggle("is-open");
      menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
      document.body.classList.toggle("cp-nav-open", open);
    });
  }

  var langBtn = document.querySelector(".cp-header-lang-btn");
  var langMenu = document.querySelector(".cp-header-lang-menu");
  if (langBtn && langMenu) {
    langBtn.addEventListener("click", function (event) {
      event.preventDefault();
      event.stopPropagation();
      langMenu.classList.toggle("is-open");
    });
    document.addEventListener("click", function () {
      langMenu.classList.remove("is-open");
    });
  }
})();
