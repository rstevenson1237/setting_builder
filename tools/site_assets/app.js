(function () {
  "use strict";

  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
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
})();
