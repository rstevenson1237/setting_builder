(function () {
  "use strict";

  var header = document.querySelector(".site-header");
  function syncHeaderOffset() {
    if (header) {
      var root = document.documentElement.style;
      root.setProperty("--header-offset", (header.offsetHeight + 12) + "px");
      root.setProperty("--header-height", header.offsetHeight + "px");
    }
  }
  syncHeaderOffset();
  window.addEventListener("resize", syncHeaderOffset);
  if (header && window.ResizeObserver) { new ResizeObserver(syncHeaderOffset).observe(header); }

  // The navigation is a sidebar. The header's button collapses it on a wide screen, remembered
  // between pages, and opens it over the page on a narrow one, closed again by a link or Escape.
  var toggle = document.querySelector(".nav-toggle");
  var narrow = window.matchMedia("(max-width: 720px)");
  var NAV_KEY = "setting-nav-collapsed";
  function navShown() {
    return narrow.matches ? document.body.classList.contains("nav-open") : !document.body.classList.contains("nav-collapsed");
  }
  function showNav(on) {
    document.body.classList.toggle(narrow.matches ? "nav-open" : "nav-collapsed", narrow.matches ? on : !on);
    if (toggle) { toggle.setAttribute("aria-expanded", on ? "true" : "false"); }
    if (!narrow.matches) {
      try { localStorage.setItem(NAV_KEY, on ? "" : "1"); } catch (e) { /* storage unavailable - not remembered */ }
    }
    syncHeaderOffset();
  }
  try { if (localStorage.getItem(NAV_KEY) === "1") { document.body.classList.add("nav-collapsed"); } } catch (e) { /* default */ }
  if (toggle) {
    toggle.setAttribute("aria-expanded", navShown() ? "true" : "false");
    toggle.addEventListener("click", function () { showNav(!navShown()); });
    narrow.addEventListener("change", function () { toggle.setAttribute("aria-expanded", navShown() ? "true" : "false"); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && narrow.matches && navShown()) { showNav(false); toggle.focus(); }
    });
    var sideNav = document.querySelector(".site-nav");
    if (sideNav) {
      sideNav.addEventListener("click", function (e) {
        if (narrow.matches && e.target.closest("a")) { showNav(false); }
      });
    }
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

  // The header's dice pill: Roll, the die icons that add to the pool, the pool itself, summed or
  // separate, DL/DH (summed) or ADV/DIS (separate), and a bonus. It is built here; the overlay that
  // throws the dice loads when Roll is first pressed.
  var DICE = [4, 6, 8, 10, 12, 20];
  var MAX_POOL = 6;
  var MAX_BONUS = 20;
  var DICE_KEY = "setting-dice";
  var SHAPES = {
    4: '<polygon points="12,3 22,20 2,20"/>',
    6: '<rect x="4" y="4" width="16" height="16" rx="2"/>',
    8: '<polygon points="12,2 22,12 12,22 2,12"/>',
    10: '<polygon points="12,2 21,10 12,22 3,10"/>',
    12: '<polygon points="12,2 22,9.5 18.5,21 5.5,21 2,9.5"/>',
    20: '<polygon points="12,2 21,7 21,17 12,22 3,17 3,7"/>'
  };
  var pillHost = document.querySelector(".dice-pill");
  if (pillHost) {
    var dice = { pool: { 6: 1 }, sum: true, drop: "", adv: "", bonus: 0 };
    try {
      var saved = JSON.parse(localStorage.getItem(DICE_KEY) || "null");
      if (saved && typeof saved === "object") {
        var pool = {}, held = 0;
        DICE.forEach(function (s) {
          var n = Math.max(0, Math.min(MAX_POOL - held, parseInt(saved.pool && saved.pool[s], 10) || 0));
          if (n) { pool[s] = n; held += n; }
        });
        if (held) { dice.pool = pool; }
        dice.sum = saved.sum !== false;
        dice.drop = saved.drop === "DL" || saved.drop === "DH" ? saved.drop : "";
        dice.adv = saved.adv === "ADV" || saved.adv === "DIS" ? saved.adv : "";
        dice.bonus = Math.max(-MAX_BONUS, Math.min(MAX_BONUS, parseInt(saved.bonus, 10) || 0));
      }
    } catch (e) { /* storage unavailable or unreadable - start from the default roll */ }

    var poolSize = function () {
      return DICE.reduce(function (n, s) { return n + (dice.pool[s] || 0); }, 0);
    };
    var pillButton = function (cls, label, title, onclick) {
      var b = el("button", cls);
      b.type = "button";
      if (label) { b.textContent = label; }
      b.title = title;
      b.setAttribute("aria-label", title);
      b.addEventListener("click", onclick);
      return b;
    };

    var rollBtn = pillButton("dp-roll", "Roll", "Roll the dice", function () {
      var faces = [];
      DICE.forEach(function (s) { for (var i = 0; i < (dice.pool[s] || 0); i++) { faces.push(s); } });
      loadRoller().then(function (r) {
        r.rollSpec({ dice: faces, mode: dice.sum ? "sum" : "sep", drop: dice.sum ? dice.drop : "", adv: dice.sum ? "" : dice.adv, bonus: dice.bonus });
      }).catch(function () {
        alert("The dice roller could not load (it needs WebGL and the three.js CDN).");
      });
    });

    var addGroup = el("span", "dp-add");
    var addBtns = DICE.map(function (s) {
      var b = pillButton("dp-die", "", "Add a d" + s, function () {
        if (poolSize() >= MAX_POOL) { return; }
        dice.pool[s] = (dice.pool[s] || 0) + 1;
        update();
      });
      b.innerHTML = '<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round">' +
        SHAPES[s] + '</g><text x="12" y="' + (s === 4 ? 17 : 15) + '" text-anchor="middle" font-size="' + (s > 9 ? 8 : 9) +
        '" fill="currentColor" font-family="sans-serif" font-weight="bold">' + s + '</text></svg>';
      addGroup.appendChild(b);
      return b;
    });

    var poolGroup = el("span", "dp-pool");
    var modeBtn = pillButton("dp-toggle", "", "", function () { dice.sum = !dice.sum; update(); });
    modeBtn.setAttribute("role", "switch");
    var optGroup = el("span", "dp-opts");
    var opts = [el("button", "dp-opt"), el("button", "dp-opt")];
    opts.forEach(function (b) {
      b.type = "button";
      b.addEventListener("click", function () {
        if (b.getAttribute("aria-disabled") === "true") { return; }
        var field = dice.sum ? "drop" : "adv";
        dice[field] = dice[field] === b.textContent ? "" : b.textContent;
        update();
      });
      optGroup.appendChild(b);
    });
    var bonusGroup = el("span", "dp-bonus");
    var bonusOut = el("span", "dp-bonus-value");
    var minus = pillButton("dp-step", "−", "Subtract 1 from the bonus", function () {
      dice.bonus = Math.max(-MAX_BONUS, dice.bonus - 1);
      update();
    });
    var plus = pillButton("dp-step", "+", "Add 1 to the bonus", function () {
      dice.bonus = Math.min(MAX_BONUS, dice.bonus + 1);
      update();
    });
    bonusOut.addEventListener("click", function () { dice.bonus = 0; update(); });
    bonusOut.title = "Click to reset the bonus";
    bonusGroup.appendChild(minus);
    bonusGroup.appendChild(bonusOut);
    bonusGroup.appendChild(plus);

    var update = function () {
      var full = poolSize() >= MAX_POOL;
      addBtns.forEach(function (b) { b.setAttribute("aria-disabled", full ? "true" : "false"); });
      poolGroup.textContent = "";
      DICE.forEach(function (s) {
        if (!dice.pool[s]) { return; }
        poolGroup.appendChild(pillButton("dp-chip", dice.pool[s] + "d" + s, "Remove a d" + s, function () {
          dice.pool[s]--;
          if (!dice.pool[s]) { delete dice.pool[s]; }
          update();
        }));
      });
      if (!poolSize()) { poolGroup.appendChild(el("span", "dp-empty", "add dice")); }
      rollBtn.disabled = !poolSize();
      modeBtn.textContent = dice.sum ? "Summed" : "Separate";
      modeBtn.setAttribute("aria-checked", dice.sum ? "true" : "false");
      var modeTitle = dice.sum ? "Dice are added together. Click to show them one by one."
        : "Dice are shown one by one. Click to add them together.";
      modeBtn.title = modeTitle;
      modeBtn.setAttribute("aria-label", modeTitle);
      var labels = dice.sum ? ["DL", "DH"] : ["ADV", "DIS"];
      var titles = dice.sum ? ["Drop the lowest die", "Drop the highest die"] : ["Advantage: roll each die twice, keep the higher", "Disadvantage: roll each die twice, keep the lower"];
      var chosen = dice.sum ? dice.drop : dice.adv;
      opts.forEach(function (b, i) {
        b.textContent = labels[i];
        b.title = titles[i];
        b.setAttribute("aria-label", titles[i]);
        b.setAttribute("aria-pressed", chosen === labels[i] ? "true" : "false");
        b.setAttribute("aria-disabled", dice.sum && poolSize() < 2 ? "true" : "false");
      });
      bonusOut.textContent = (dice.bonus > 0 ? "+" : dice.bonus < 0 ? "−" : "") + Math.abs(dice.bonus);
      bonusGroup.title = dice.sum ? "Bonus added to the roll" : "Bonus added to each die";
      try { localStorage.setItem(DICE_KEY, JSON.stringify(dice)); } catch (e) { /* the pill just won't be remembered */ }
    };

    [rollBtn, addGroup, poolGroup, modeBtn, optGroup, bonusGroup].forEach(function (node) { pillHost.appendChild(node); });
    update();
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

  // A pill that rolls one d6 plus the creature's bonus, with the total beside it.
  function dieRoller(who, bonus) {
    var wrap = el("span", "ad-roller");
    var pill = el("button", "ad-roll", "Roll");
    pill.type = "button";
    var sign = bonus ? (bonus > 0 ? "+" : "\u2212") + Math.abs(bonus) : "";
    pill.setAttribute("aria-label", "Roll a d6" + sign + " for " + who);
    var out = el("span", "ad-roll-result");
    out.setAttribute("aria-live", "polite");
    pill.addEventListener("click", function () {
      pill.disabled = true;
      out.textContent = "";
      rollDie(6).then(function (n) {
        out.textContent = n + (bonus || 0);
        out.title = bonus ? n + " " + sign + " = " + (n + bonus) : "";
        pill.disabled = false;
      });
    });
    wrap.appendChild(pill);
    wrap.appendChild(out);
    return wrap;
  }

  function creatureTracker(name, ad, count) {
    var dice = /^(\d+)d6/.exec(ad || "");
    var n = dice ? parseInt(dice[1], 10) : 1;
    var bonus = /d6([+-]\d+)/.exec(ad || "");
    var mod = bonus ? parseInt(bonus[1], 10) : 0;
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
      row.appendChild(dieRoller(name + " " + i, mod));
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
