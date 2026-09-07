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
      '<div class="pattern-insp-eyebrow">' + n.folder + "/</div>" +
      "<h3>" + esc(n.filename) + "</h3></div>" +
      issuesHtml +
      fieldBlock("Decides", n.decides) +
      fieldBlock("Read at", n.read_at) +
      fieldBlock("Spec", n.spec, true) +
      fieldBlock("Patterns", n.patterns_text) +
      fieldBlock("Examples", n.examples) +
      fieldBlock("Constraints", n.constraints) +
      chipRow("Cites", n.out) +
      chipRow("Cited by", n.incoming);
    Array.prototype.forEach.call(inspectorEl.querySelectorAll(".pattern-chip"), function (c) {
      c.addEventListener("click", function () { selectNode(c.getAttribute("data-id")); });
    });
  }

  function inspectorDefault() {
    var fileCount = Object.keys(DATA.nodes).length;
    var edgeCount = 0;
    Object.keys(DATA.nodes).forEach(function (k) { edgeCount += DATA.nodes[k].out.length; });
    inspectorEl.innerHTML =
      '<p class="hint">Click any file in the columns to the left to see what it decides, ' +
      "what cites it, and what it cites in turn - traced live as you go.</p>" +
      '<p class="hint"><strong>' + fileCount + "</strong> files, <strong>" + edgeCount + "</strong> citations.</p>";
  }

  function selectNode(id) {
    selectedId = id;
    Array.prototype.forEach.call(columnsEl.querySelectorAll(".pattern-card"), function (c) {
      c.classList.toggle("selected", c.getAttribute("data-id") === id);
    });
    renderInspector(id);
    drawEdges(id);
    var card = columnsEl.querySelector('.pattern-card[data-id="' + cssEscape(id) + '"]');
    if (card && card.scrollIntoView) card.scrollIntoView({ block: "nearest", behavior: "smooth" });
  }

  function cssEscape(s) {
    return window.CSS && CSS.escape ? CSS.escape(s) : s.replace(/[^a-zA-Z0-9_-]/g, "\\$&");
  }

  function drawEdges(id) {
    var rect = innerEl.getBoundingClientRect();
    var w = innerEl.scrollWidth, h = innerEl.scrollHeight;
    edgeLayer.setAttribute("width", w);
    edgeLayer.setAttribute("height", h);
    edgeLayer.setAttribute("viewBox", "0 0 " + w + " " + h);
    var defs = '<defs>' +
      '<marker id="pattern-arrow-out" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto-start-reverse">' +
      '<path d="M0,0 L8,4 L0,8 Z" fill="var(--accent)"/></marker>' +
      '<marker id="pattern-arrow-in" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto-start-reverse">' +
      '<path d="M0,0 L8,4 L0,8 Z" fill="var(--ink-soft)"/></marker></defs>';
    var node = columnsEl.querySelector('.pattern-card[data-id="' + cssEscape(id) + '"]');
    if (!node) { edgeLayer.innerHTML = defs; return; }
    var nRect = node.getBoundingClientRect();

    function center(r) { return { x: r.left - rect.left, y: r.top - rect.top + r.height / 2 }; }
    var n0 = center(nRect);

    function pathTo(otherId, mode) {
      var other = columnsEl.querySelector('.pattern-card[data-id="' + cssEscape(otherId) + '"]');
      if (!other) return "";
      var oRect = other.getBoundingClientRect();
      var o = center(oRect);
      var startX = mode === "out" ? n0.x + nRect.width / 2 : n0.x - nRect.width / 2;
      var endX = mode === "out" ? o.x - oRect.width / 2 : o.x + oRect.width / 2;
      var midX = (startX + endX) / 2;
      var d = "M " + startX + " " + n0.y + " C " + midX + " " + n0.y + ", " + midX + " " + o.y + ", " + endX + " " + o.y;
      var stroke = mode === "out" ? "var(--accent)" : "var(--ink-soft)";
      var marker = mode === "out" ? "url(#pattern-arrow-out)" : "url(#pattern-arrow-in)";
      return '<path d="' + d + '" stroke="' + stroke + '" marker-end="' + marker + '" opacity="0.85"/>';
    }

    var n = DATA.nodes[id];
    var paths = n.out.map(function (t) { return pathTo(t, "out"); }).join("") +
      n.incoming.map(function (s) { return pathTo(s, "in"); }).join("");
    edgeLayer.innerHTML = defs + paths;
  }

  window.addEventListener("resize", function () { if (selectedId) drawEdges(selectedId); });

  buildColumns();
  inspectorDefault();
})();
