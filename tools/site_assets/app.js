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

  // The dice overlay loads on first use. Table and creature rolls go through rollDie, which
  // falls back to a plain random number when the overlay cannot load or cannot throw that die.
  var assetBase = document.currentScript.src.replace(/[^\/]*$/, "");
  var rollerLoad = null;
  function loadRoller() {
    if (!rollerLoad) {
      rollerLoad = import(assetBase + "dice-overlay.js").then(function (m) { return m.createRoller(); })
        .catch(function (e) { rollerLoad = null; throw e; });
    }
    return rollerLoad;
  }
  var inFlight = {};
  function rollDie(sides) {
    if (!inFlight[sides]) {
      inFlight[sides] = loadRoller().then(function (r) { return r.roll(sides); }).catch(function () { return null; })
        .then(function (n) { inFlight[sides] = null; return n || between(1, sides); });
    }
    return inFlight[sides];
  }

  var diceButton = document.querySelector(".dice-button");
  if (diceButton) {
    diceButton.addEventListener("click", function () {
      loadRoller().then(function (r) { r.open(); }).catch(function () {
        diceButton.title = "The dice roller could not load (it needs WebGL and the three.js CDN).";
        alert(diceButton.title);
      });
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
  // A citation opens a box below the line holding it: the entry itself, a random row of a
  // roll table, or a creature with a row of circles per creature to mark Attack Dice lost.
  // The link stays a plain link for anyone without scripts.
  var citesUrl = document.body.getAttribute("data-cites");
  var citesLoad = null;
  function loadCites() {
    if (!citesLoad) {
      citesLoad = fetch(citesUrl).then(function (r) { return r.json(); });
    }
    return citesLoad;
  }
  function fromRoot(html) {
    var prefix = citesUrl.replace(/cites\.json$/, "");
    return html.replace(/href="(?![a-z]+:|#)/g, 'href="' + prefix);
  }
  function el(tag, cls, text) {
    var node = document.createElement(tag);
    if (cls) { node.className = cls; }
    if (text !== undefined) { node.textContent = text; }
    return node;
  }
  function button(label, title, onclick) {
    var b = el("button", "cite-btn", label);
    b.type = "button";
    b.title = title;
    b.addEventListener("click", onclick);
    return b;
  }
  function between(lo, hi) { return lo + Math.floor(Math.random() * (hi - lo + 1)); }

  // A pill that rolls one d6, with the result beside it.
  function dieRoller(who) {
    var wrap = el("span", "ad-roller");
    var pill = el("button", "ad-roll", "Roll");
    pill.type = "button";
    pill.setAttribute("aria-label", "Roll a d6 for " + who);
    var out = el("span", "ad-roll-result");
    out.setAttribute("aria-live", "polite");
    pill.addEventListener("click", function () {
      pill.disabled = true;
      out.textContent = "";
      rollDie(6).then(function (n) { out.textContent = n; pill.disabled = false; });
    });
    wrap.appendChild(pill);
    wrap.appendChild(out);
    return wrap;
  }

  function creatureTracker(name, ad, count) {
    var dice = /^(\d+)d6/.exec(ad || "");
    var n = dice ? parseInt(dice[1], 10) : 1;
    var bonus = /d6([+-]\d+)/.exec(ad || "");
    var wrap = el("div", "ad-track");
    for (var i = 1; i <= count; i++) {
      var row = el("div", "ad-row");
      row.appendChild(el("span", "ad-name", name + " " + i));
      var dots = el("span", "ad-dots");
      for (var d = 1; d <= n; d++) {
        var dot = el("button", "ad-dot");
        dot.type = "button";
        dot.setAttribute("aria-pressed", "false");
        dot.setAttribute("aria-label", name + " " + i + ", Attack Die " + d + " of " + n + " lost");
        dot.addEventListener("click", function () {
          this.setAttribute("aria-pressed", this.getAttribute("aria-pressed") === "true" ? "false" : "true");
        });
        dots.appendChild(dot);
      }
      row.appendChild(dots);
      if (bonus) { row.appendChild(el("span", "ad-bonus", bonus[1])); }
      row.appendChild(dieRoller(name + " " + i));
      wrap.appendChild(row);
    }
    return wrap;
  }

  // A procedure that is a table: roll its Results list and show the row it lands on.
  function addRoller(body, actions) {
    var th = Array.prototype.find.call(body.querySelectorAll("th"), function (t) {
      return t.textContent === "Results";
    });
    var rows = th ? th.parentNode.querySelectorAll("li") : [];
    if (!rows.length) { return; }
    var result = el("div", "cite-roll-result");
    body.insertBefore(result, body.firstChild);
    var show = function (n) {
      Array.prototype.forEach.call(rows, function (li, i) { li.classList.toggle("rolled", i === n - 1); });
      result.innerHTML = "<strong>Rolled " + n + " on d" + rows.length + ":</strong> " +
        rows[n - 1].innerHTML.replace(/^\d+\.\s*/, "");
    };
    var roll = function () { rollDie(rows.length).then(show); };
    actions.insertBefore(button("Roll d" + rows.length, "Roll the table", roll), actions.firstChild);
  }

  function buildBox(a, data) {
    var kind = a.getAttribute("data-cite");
    var table = a.getAttribute("data-table");
    var title = a.getAttribute("data-title");
    var box = el("div", "cite-box");
    box.setAttribute("role", "group");
    var head = el("div", "cite-box-head");
    var label = el("strong", "cite-box-title");
    var actions = el("span", "cite-box-actions");
    var body = el("div", "cite-box-body");
    head.appendChild(label);
    head.appendChild(actions);
    box.appendChild(head);
    box.appendChild(body);

    if (kind === "roll") {
      var rows = data.roll[table] || {};
      var keys = Object.keys(rows);
      var die = parseInt(a.getAttribute("data-die"), 10) || keys.length;
      var show = function (n) {
        var row = rows[String(n)] || rows[keys[(n - 1) % keys.length]];
        label.textContent = table + " - rolled " + n + " on d" + die;
        body.innerHTML = fromRoot(row || "");
      };
      actions.appendChild(button("Roll again", "Roll again", function () { rollDie(die).then(show); }));
      show(between(1, die));
    } else {
      var card = (data.entry[table] || {})[title];
      if (!card) { return null; }
      var render = function () {
        body.innerHTML = fromRoot(card.html);
        if (kind === "creature") {
          var spec = a.getAttribute("data-count") || "1";
          var range = /^(\d+)-(\d+)$/.exec(spec);
          var count = range ? between(+range[1], +range[2]) : parseInt(spec, 10) || 1;
          label.textContent = title + " x" + count + (range ? " (rolled from " + spec + ")" : "");
          body.appendChild(creatureTracker(title, card.ad, count));
        } else {
          label.textContent = table + ": " + title;
        }
      };
      render();
      if (card.roll) { addRoller(body, actions); }
      if (kind === "creature") {
        var again = button("Reset", "Clear every circle", render);
        actions.appendChild(again);
      }
    }
    var open = el("a", "cite-btn", "Open page");
    open.href = a.href;
    actions.appendChild(open);
    actions.appendChild(button("\u00d7", "Close", function () {
      box.hidden = true;
      a.setAttribute("aria-expanded", "false");
    }));
    return box;
  }

  function placeBox(a, box) {
    var host = a.closest("td, th, li, p, .cite-box-body");
    if (!host) { a.parentNode.appendChild(box); }
    else if (host.matches("p")) { host.after(box); }
    else { host.appendChild(box); }
  }

  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("a.cite");
    if (!a || !citesUrl || e.button || e.ctrlKey || e.metaKey || e.shiftKey || e.altKey) { return; }
    e.preventDefault();
    if (a._box) {
      a._box.hidden = !a._box.hidden;
      a.setAttribute("aria-expanded", a._box.hidden ? "false" : "true");
      return;
    }
    loadCites().then(function (data) {
      var box = buildBox(a, data);
      if (!box) { window.location.href = a.href; return; }
      a._box = box;
      placeBox(a, box);
      a.setAttribute("aria-expanded", "true");
    }).catch(function () { window.location.href = a.href; });
  });

})();
