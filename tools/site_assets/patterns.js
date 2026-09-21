(function () {
  "use strict";

  var dataEl = document.getElementById("pattern-data");
  if (!dataEl) return;
  var DATA = JSON.parse(dataEl.textContent);

  var FOLDER_LABEL = { setting: "Setting", region: "Region", safe: "Safe", wild: "Wild", dangerous: "Dangerous" };
  var FOLDER_VAR = { setting: "--pattern-setting", region: "--pattern-region", safe: "--safe", wild: "--wild", dangerous: "--dangerous" };

  var columnsEl = document.getElementById("pattern-columns");
  var inspectorEl = document.getElementById("pattern-inspector");
  var innerEl = document.getElementById("pattern-diagram-inner");
  var edgeLayer = document.getElementById("pattern-edge-layer");
  if (!columnsEl || !inspectorEl || !innerEl || !edgeLayer) return;

  var selectedId = null;

  function esc(s) {
    return (s || "").replace(/[&<>]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]; });
  }

  function buildColumns() {
    var html = "";
    DATA.folder_order.forEach(function (f) {
      var ids = DATA.folder_nodes[f] || [];
      var cards = ids.map(nodeCardHtml).join("");
      html += '<div class="pattern-col" style="--pattern-col-color:var(' + FOLDER_VAR[f] + ')">' +
        '<div class="pattern-col-head" style="--pattern-col-color:var(' + FOLDER_VAR[f] + ')">' +
        "<h3>" + FOLDER_LABEL[f] + "</h3><span class=\"n\">" + ids.length + "</span></div>" +
        '<div class="pattern-col-list">' + cards + "</div></div>";
    });
    columnsEl.innerHTML = html;
    Array.prototype.forEach.call(columnsEl.querySelectorAll(".pattern-card"), function (btn) {
      btn.addEventListener("click", function () { selectNode(btn.getAttribute("data-id")); });
    });
  }

  function nodeCardHtml(id) {
    var n = DATA.nodes[id];
    var warn = (n.issues && n.issues.length)
      ? ' <span title="' + esc(n.issues.join("; ")) + '" style="color:var(--dangerous)">&#9650;</span>' : "";
    var shortTitle = n.title.replace(/^.*?-\s*/, "");
    return '<button type="button" class="pattern-card" data-id="' + id + '" style="--pattern-col-color:var(' + FOLDER_VAR[n.folder] + ')">' +
      '<span class="fname">' + esc(n.filename) + warn + "</span>" +
      '<span class="ftitle">' + esc(shortTitle) + "</span></button>";
  }

  function fieldBlock(label, value, mono) {
    if (!value) return "";
    var tag = mono ? "pre" : "p";
    return '<div class="pattern-insp-block"><h4>' + label + "</h4><" + tag + ">" + esc(value) + "</" + tag + "></div>";
  }

  function chipRow(label, ids) {
    if (!ids || !ids.length) {
      return '<div class="pattern-insp-block"><h4>' + label + " (0)</h4><p style=\"color:var(--ink-soft)\">none</p></div>";
    }
    var chips = ids.map(function (id) {
      return '<button type="button" class="pattern-chip" data-id="' + id + '">' + esc(id) + "</button>";
    }).join("");
    return '<div class="pattern-insp-block"><h4>' + label + " (" + ids.length + ")</h4><div class=\"pattern-chip-row\">" + chips + "</div></div>";
  }

  function renderInspector(id) {
    var n = DATA.nodes[id];
    var issuesHtml = (n.issues && n.issues.length)
      ? '<div class="pattern-insp-block"><h4>Issues</h4><p style="color:var(--dangerous)">' + esc(n.issues.join("; ")) + "</p></div>" : "";
    inspectorEl.innerHTML =
      '<div class="pattern-insp-head" style="--pattern-col-color:var(' + FOLDER_VAR[n.folder] + ')">' +
      '<div class="pattern-insp-eyebrow">' + n.folder + "/" +
      ((n.modes && n.modes.length) ? " &middot; " + n.modes.join(", ") : "") +
      ((n.out && n.out.length) ? " &middot; classifier" : " &middot; leaf") + "</div>" +
      "<h3>" + esc(n.filename) + "</h3></div>" +
      issuesHtml +
      fieldBlock("Provides", n.provides) +
      fieldBlock("Read at", n.read_at) +
      fieldBlock("Spec", n.spec, true) +
      fieldBlock("Constraints", n.constraints) +
      chipRow("Draws", n.out) +
      chipRow("Drawn by", n.incoming) +
      chipRow("Mentions", n.mentions || []);
    Array.prototype.forEach.call(inspectorEl.querySelectorAll(".pattern-chip"), function (c) {
      c.addEventListener("click", function () { selectNode(c.getAttribute("data-id")); });
    });
  }

  function inspectorDefault() {
    var fileCount = Object.keys(DATA.nodes).length;
    var edgeCount = 0;
    Object.keys(DATA.nodes).forEach(function (k) { edgeCount += DATA.nodes[k].out.length; });
    inspectorEl.innerHTML =
      '<p class="hint">Click any file in the columns to the left to see what it provides, ' +
      "what cites it, and what it cites in turn - traced live as you go.</p>" +
      '<p class="hint"><strong>' + fileCount + "</strong> files, <strong>" + edgeCount + "</strong> citations.</p>";
  }

  function selectNode(id) {
    selectedId = id;
    Array.prototype.forEach.call(columnsEl.querySelectorAll(".pattern-card"), function (c) {
      c.classList.toggle("selected", c.getAttribute("data-id") === id);
    });
    renderInspector(id);
    var card = columnsEl.querySelector('.pattern-card[data-id="' + cssEscape(id) + '"]');
    if (card && card.scrollIntoView) card.scrollIntoView({ block: "nearest", behavior: "smooth" });
    // Draw after the scroll, not before it: scrollIntoView is smooth and
    // asynchronous, so edges computed first are stale by the time it settles.
    drawEdges(id);
    requestAnimationFrame(redraw);
    setTimeout(redraw, 400);
  }

  function cssEscape(s) {
    return window.CSS && CSS.escape ? CSS.escape(s) : s.replace(/[^a-zA-Z0-9_-]/g, "\\$&");
  }

  function drawEdges(id) {
    // The overlay is a 1:1 layer over .pattern-diagram-inner. It must NOT also
    // carry width/height/viewBox attributes: CSS `inset: 0` already sizes it,
    // so a viewBox would be re-fitted into a different box (uniform scale plus
    // a centring offset) while these coordinates stay in unscaled pixels, and
    // every path would land somewhere other than where it was computed.
    var rect = innerEl.getBoundingClientRect();
    var defs = '<defs>' +
      '<marker id="pattern-arrow-out" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto">' +
      '<path d="M0,0 L8,4 L0,8 Z" fill="var(--accent)"/></marker>' +
      '<marker id="pattern-arrow-in" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto">' +
      '<path d="M0,0 L8,4 L0,8 Z" fill="var(--ink-soft)"/></marker></defs>';
    var node = columnsEl.querySelector('.pattern-card[data-id="' + cssEscape(id) + '"]');
    if (!node) { edgeLayer.innerHTML = defs; return; }
    var nRect = node.getBoundingClientRect();

    // Real box edges, relative to the overlay's own origin. The previous
    // version returned the card's LEFT edge as `x` and then treated it as the
    // centre, so every line began inside the source card and ended a half-card
    // outside the target - and, in the leftmost column, at a negative x.
    function box(r) {
      return {
        left: r.left - rect.left,
        right: r.right - rect.left,
        y: r.top - rect.top + r.height / 2
      };
    }
    var n0 = box(nRect);

    function pathBetween(fromBox, toBox) {
      // Leave from whichever side faces the target, and arrive on the facing
      // side of the target, so the line runs through the gutter rather than
      // under either card.
      var leftToRight = toBox.left >= fromBox.right;
      var startX = leftToRight ? fromBox.right : fromBox.left;
      var endX = leftToRight ? toBox.left : toBox.right;
      var midX = (startX + endX) / 2;
      return "M " + startX + " " + fromBox.y +
        " C " + midX + " " + fromBox.y + ", " + midX + " " + toBox.y +
        ", " + endX + " " + toBox.y;
    }

    function pathTo(otherId, mode) {
      var other = columnsEl.querySelector('.pattern-card[data-id="' + cssEscape(otherId) + '"]');
      if (!other) return "";
      var o = box(other.getBoundingClientRect());
      // An outgoing edge points at what this file draws; an incoming edge
      // points at this file. Both arrowheads therefore sit at the end of a
      // path drawn in the citation's own direction.
      var d = mode === "out" ? pathBetween(n0, o) : pathBetween(o, n0);
      var stroke = mode === "out" ? "var(--accent)" : "var(--ink-soft)";
      var marker = mode === "out" ? "url(#pattern-arrow-out)" : "url(#pattern-arrow-in)";
      return '<path d="' + d + '" stroke="' + stroke + '" marker-end="' + marker + '" opacity="0.9"/>';
    }

    var n = DATA.nodes[id];
    var paths = n.out.map(function (t) { return pathTo(t, "out"); }).join("") +
      n.incoming.map(function (s) { return pathTo(s, "in"); }).join("");
    edgeLayer.innerHTML = defs + paths;
  }

  function redraw() { if (selectedId) drawEdges(selectedId); }

  window.addEventListener("resize", redraw);
  // The columns live in a scrollable box, so anything that moves them moves
  // the endpoints with them.
  var scrollEl = document.querySelector(".pattern-diagram-scroll");
  if (scrollEl) scrollEl.addEventListener("scroll", redraw, { passive: true });

  buildColumns();
  inspectorDefault();
})();
