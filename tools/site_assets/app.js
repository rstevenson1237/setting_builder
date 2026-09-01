(function () {
  "use strict";

  var header = document.querySelector(".site-header");
  function syncHeaderOffset() {
    if (header) {
      document.documentElement.style.setProperty("--header-offset", (header.offsetHeight + 12) + "px");
    }
  }
  syncHeaderOffset();
  window.addEventListener("resize", syncHeaderOffset);

  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      syncHeaderOffset();
    });
  }

  var dropdown = document.querySelector(".nav-dropdown");
  var dropdownToggle = document.querySelector(".dropdown-toggle");
  if (dropdown && dropdownToggle) {
    dropdownToggle.addEventListener("click", function (e) {
      e.stopPropagation();
      var open = dropdown.classList.toggle("open");
      dropdownToggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    document.addEventListener("click", function (e) {
      if (!dropdown.contains(e.target)) {
        dropdown.classList.remove("open");
        dropdownToggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  if (window.mermaid) {
    var isDark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
    mermaid.initialize({ startOnLoad: true, theme: isDark ? "dark" : "default", securityLevel: "loose" });
  }

  var searchInput = document.getElementById("site-search");
  var resultsBox = document.getElementById("search-results");
  if (searchInput && resultsBox) {
    var indexUrl = searchInput.getAttribute("data-index");
    var indexData = null;
    var loadPromise = null;

    function ensureIndex() {
      if (!loadPromise) {
        loadPromise = fetch(indexUrl).then(function (r) { return r.json(); }).then(function (data) {
          indexData = data;
          return data;
        }).catch(function () { indexData = []; return []; });
      }
      return loadPromise;
    }

    function render(items) {
      resultsBox.innerHTML = "";
      if (!items.length) {
        resultsBox.hidden = true;
        return;
      }
      items.slice(0, 12).forEach(function (item) {
        var li = document.createElement("li");
        var a = document.createElement("a");
        a.href = item.url;
        var title = document.createElement("span");
        title.textContent = item.title;
        var type = document.createElement("span");
        type.className = "result-type";
        type.textContent = item.type;
        a.appendChild(title);
        a.appendChild(type);
        li.appendChild(a);
        resultsBox.appendChild(li);
      });
      resultsBox.hidden = false;
    }

    searchInput.addEventListener("input", function () {
      var q = searchInput.value.trim().toLowerCase();
      if (!q) {
        resultsBox.hidden = true;
        return;
      }
      ensureIndex().then(function (data) {
        var matches = data.filter(function (item) {
          return item.title.toLowerCase().indexOf(q) !== -1;
        });
        render(matches);
      });
    });

    searchInput.addEventListener("focus", ensureIndex);

    document.addEventListener("click", function (e) {
      if (e.target !== searchInput && !resultsBox.contains(e.target)) {
        resultsBox.hidden = true;
      }
    });
  }

  var checklistBoxes = document.querySelectorAll("[data-checklist-id]");
  if (checklistBoxes.length) {
    var CHECKLIST_PREFIX = "setting-checklist:";
    checklistBoxes.forEach(function (box) {
      var key = CHECKLIST_PREFIX + box.getAttribute("data-checklist-id");
      try {
        box.checked = localStorage.getItem(key) === "1";
      } catch (e) { /* storage unavailable - leave unchecked */ }
      box.addEventListener("change", function () {
        try {
          localStorage.setItem(key, box.checked ? "1" : "0");
        } catch (e) { /* storage unavailable - state just won't persist */ }
      });
    });
  }
})();
