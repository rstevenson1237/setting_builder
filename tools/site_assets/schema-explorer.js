// The Schema Reference: every definition in patterns/*_Schema.md as a node in a graph, and an
// entry for each. The model is read from #schema-data (tools/schema_graph.py); nothing here
// knows a schema's names, only its kinds.
(function () {
  "use strict";

  var host = document.getElementById("schema-explorer");
  var dataEl = document.getElementById("schema-data");
  if (!host || !dataEl) { return; }
  var data = JSON.parse(dataEl.textContent);
  var SVG = "http://www.w3.org/2000/svg";

  // Left to right, a definition is built from those before it.
  var TIERS = ["value", "enum", "table", "node", "folder", "region"];
  var PLURAL = { value: "Types", enum: "Enums", table: "Tables", node: "Nodes", folder: "Folders", region: "Regions" };
  var SINGLE = { value: "type", enum: "enum", table: "table", node: "node", folder: "folder", region: "region" };
  var PALETTE = ["#6b7a8f", "#3f6f9f", "#7a5aa0", "#8a2e2e", "#2f6f4f", "#8a6d1e", "#2f8a8a", "#a0527a"];
  var TITLE = document.title;

  var defs = {}, files = {}, fileIndex = {}, uses = {}, usedBy = {};
  data.files.forEach(function (f, i) { files[f.id] = f; fileIndex[f.id] = i; });
  data.defs.forEach(function (d) { defs[d.id] = d; uses[d.id] = []; usedBy[d.id] = []; });
  data.edges.forEach(function (e) { uses[e.from].push(e.to); usedBy[e.to].push(e.from); });

  function fileDefs(f) { return f.groups.reduce(function (a, g) { return a.concat(g.defs); }, []); }
  function colour(file) { return PALETTE[fileIndex[file] % PALETTE.length]; }
  function clamp(v, lo, hi) { return Math.max(lo, Math.min(hi, v)); }

  function add(el, kids) {
    [].concat(kids == null ? [] : kids).forEach(function (k) {
      if (k != null && k !== false) { el.appendChild(typeof k === "string" ? document.createTextNode(k) : k); }
    });
    return el;
  }
  function h(tag, cls, kids) {
    var el = document.createElement(tag);
    if (cls) { el.className = cls; }
    return add(el, kids);
  }
  function svg(tag, attrs, kids) {
    var el = document.createElementNS(SVG, tag);
    Object.keys(attrs || {}).forEach(function (k) { el.setAttribute(k, attrs[k]); });
    return add(el, kids);
  }
  function prose(text) {
    var out = h("span", "sx-prose");
    text.split("`").forEach(function (part, i) {
      if (part) { out.appendChild(i % 2 ? h("code", "", part) : document.createTextNode(part)); }
    });
    return out;
  }

  // -- routes: "" is the top, "Wild" a schema, "Wild/node/Location" a definition ------------

  function hashOf(route) {
    return route ? "#/" + route.split("/").map(encodeURIComponent).join("/") : "#/";
  }
  function routeOf(hash) {
    var parts = hash.replace(/^#\/?/, "").split("/").filter(Boolean).map(decodeURIComponent);
    return parts.join("/");
  }
  function exists(route) { return !route || !!files[route] || !!defs[route]; }
  function parentOf(route) { return defs[route] ? defs[route].file : files[route] ? "" : null; }

  function link(route, cls, kids) {
    var a = h("a", cls, kids);
    a.href = hashOf(route);
    a.setAttribute("data-ref", route);
    return a;
  }
  function dot(file) {
    var d = h("span", "sx-dot");
    d.style.background = colour(file);
    return d;
  }
  function kindTag(kind) { return h("span", "sx-kind sx-kind-" + kind, SINGLE[kind]); }

  // -- an entry's lines ---------------------------------------------------------------------

  function token(t) {
    if (t.to) { return link(t.to, "sx-tok ref ref-" + defs[t.to].kind, t.t); }
    return h("span", "sx-tok" + (t.flag ? " flag" : ""), t.t);
  }
  function tokens(parts) {
    var out = h("span", "sx-toks");
    parts.forEach(function (t) { out.appendChild(token(t)); out.appendChild(document.createTextNode(" ")); });
    return out;
  }
  function lineRow(l) {
    if (l.heading) { return h("h3", "sx-heading", l.heading); }
    var row = h("div", "sx-line" + (l.to ? " go" : ""), [
      l.label && h("span", "sx-label", l.label), tokens(l.parts), l.comment && h("div", "sx-note", prose(l.comment))]);
    if (l.to) {
      row.setAttribute("data-go", l.to);
      row.tabIndex = 0;
      row.setAttribute("role", "link");
    }
    return row;
  }
  function enumRow(r) {
    var row = h("div", "sx-line sx-enum-row", [r.group && h("span", "sx-label", r.group)]);
    r.items.forEach(function (t) {
      row.appendChild(t.to ? link(t.to, "sx-chip ref ref-" + defs[t.to].kind, t.t) : h("span", "sx-chip", t.t));
    });
    if (r.comment) { row.appendChild(h("div", "sx-note", prose(r.comment))); }
    return row;
  }
  function chip(id, withFile) {
    var d = defs[id];
    return link(id, "sx-chip ref ref-" + d.kind, [dot(d.file), d.name, withFile && h("small", "", d.file)]);
  }

  // -- the panel ----------------------------------------------------------------------------

  function topPanel() {
    var p = h("div", "sx-entry", [
      h("h1", "", "Schema Reference"),
      h("p", "hint", ["Every field, enum and range the setting files and location tables are checked against, " +
        "read from ", h("code", "", "patterns/*_Schema.md"), " at build time. Pick a node in the graph or a name " +
        "below to open its entry; follow any line to the definition it names, and hover a name to see it."])]);
    p.appendChild(h("h2", "", "Schemas"));
    var list = h("div", "sx-files");
    data.files.forEach(function (f) {
      list.appendChild(link(f.id, "sx-file", [dot(f.id), h("strong", "", f.title), h("small", "", fileDefs(f).length + " definitions")]));
    });
    p.appendChild(list);
    TIERS.forEach(function (kind) {
      var mine = data.defs.filter(function (d) { return d.kind === kind; });
      if (!mine.length) { return; }
      p.appendChild(h("h2", "", PLURAL[kind] + " (" + mine.length + ")"));
      var cloud = h("div", "sx-cloud");
      mine.forEach(function (d) { cloud.appendChild(chip(d.id, true)); });
      p.appendChild(cloud);
    });
    return p;
  }

  function filePanel(f) {
    var p = h("div", "sx-entry", [h("h1", "", [dot(f.id), f.title])]);
    f.intro.forEach(function (t) { p.appendChild(h("p", "", prose(t))); });
    f.groups.forEach(function (g) {
      if (g.note) { p.appendChild(h("p", "sx-section", prose(g.note))); }
      var list = h("div", "sx-defs");
      g.defs.forEach(function (id) {
        var d = defs[id];
        list.appendChild(link(id, "sx-def", [kindTag(d.kind), h("strong", "", d.name),
          d.doc && h("span", "sx-note", prose(d.doc))]));
      });
      if (g.defs.length) { p.appendChild(list); }
    });
    return p;
  }

  function defPanel(d) {
    var p = h("div", "sx-entry");
    p.appendChild(h("h1", "", [kindTag(d.kind), d.name]));
    p.appendChild(h("p", "sx-meta", [link(d.file, "", [dot(d.file), d.file + " schema"]),
      " · " + files[d.file].path + ":" + d.line]));
    if (d.doc) { p.appendChild(h("p", "sx-doc", prose(d.doc))); }
    if (d.section) { p.appendChild(h("p", "sx-section", prose(d.section))); }
    if (d.head.length) { p.appendChild(h("div", "sx-decl", [h("span", "sx-label", d.kind), tokens(d.head)])); }
    if (d.rows.length) { p.appendChild(h("div", "sx-lines", d.rows.map(enumRow))); }
    if (d.lines.length) { p.appendChild(h("div", "sx-lines", d.lines.map(lineRow))); }
    var same = data.defs.filter(function (o) { return o.name === d.name && o.kind === d.kind && o.id !== d.id; });
    if (same.length) {
      p.appendChild(h("h2", "", "Also defined in"));
      p.appendChild(h("div", "sx-cloud", same.map(function (o) { return chip(o.id, true); })));
    }
    var by = usedBy[d.id];
    if (by.length) {
      p.appendChild(h("h2", "", "Used by (" + by.length + ")"));
      TIERS.forEach(function (kind) {
        var mine = by.filter(function (id) { return defs[id].kind === kind; });
        if (mine.length) {
          p.appendChild(h("div", "sx-cloud", [h("span", "sx-label", PLURAL[kind])].concat(
            mine.map(function (id) { return chip(id, true); }))));
        }
      });
    }
    return p;
  }

  function lostPanel() {
    return h("div", "sx-entry", [h("h1", "", "Not found"),
      h("p", "", ["No schema or definition is named that. ", link("", "", "Back to the top.")])]);
  }

  // -- the popup a name opens on hover ---------------------------------------------------------

  var pop = h("div", "sx-pop");
  pop.hidden = true;
  document.body.appendChild(pop);

  function plainLine(l) {
    return (l.label ? l.label + "  " : "") + l.parts.map(function (t) { return t.t; }).join(" ");
  }
  function card(d) {
    var c = h("div", "", [h("div", "sx-pop-head", [kindTag(d.kind), h("strong", "", d.name), dot(d.file),
      h("small", "", d.file)])]);
    if (d.doc) { c.appendChild(h("div", "sx-pop-doc", prose(d.doc))); }
    var body = h("div", "sx-pop-body");
    if (d.head.length) { body.appendChild(h("div", "", d.kind + " " + d.head.map(function (t) { return t.t; }).join(" "))); }
    d.rows.forEach(function (r) {
      body.appendChild(h("div", "", (r.group ? r.group + ": " : "") + r.items.map(function (t) { return t.t; }).join(" · ")));
    });
    var lines = d.lines.filter(function (l) { return !l.heading; });
    lines.slice(0, 12).forEach(function (l) { body.appendChild(h("div", "", plainLine(l))); });
    if (lines.length > 12) { body.appendChild(h("div", "sx-pop-more", "+ " + (lines.length - 12) + " more")); }
    c.appendChild(body);
    return c;
  }
  var popTimer = null;
  function hidePop() { clearTimeout(popTimer); pop.hidden = true; }
  function showPop(id, anchor) {
    var d = defs[id];
    if (!d) { return; }
    pop.textContent = "";
    pop.appendChild(card(d));
    pop.hidden = false;
    var r = anchor.getBoundingClientRect();
    var x = clamp(r.left, 8, Math.max(8, window.innerWidth - pop.offsetWidth - 8));
    var y = r.bottom + 8;
    if (y + pop.offsetHeight > window.innerHeight - 8) { y = Math.max(8, r.top - pop.offsetHeight - 8); }
    pop.style.left = x + "px";
    pop.style.top = y + "px";
  }

  // -- the graph ------------------------------------------------------------------------------

  var COLW = 144, GAP = 60, ROWH = 21, PILL = 17, GROUP = 10, TOP = 34, PAD = 20;
  var pos = {}, size = { w: 0, h: 0 };

  function layout() {
    var cols = TIERS.map(function (kind) {
      return data.defs.filter(function (d) { return d.kind === kind; })
        .sort(function (a, b) { return fileIndex[a.file] - fileIndex[b.file] || a.line - b.line; });
    });
    function assign() {
      cols.forEach(function (col, c) {
        var y = TOP, last = null;
        col.forEach(function (d) {
          if (last && last.file !== d.file) { y += GROUP; }
          pos[d.id] = { x: PAD + c * (COLW + GAP), y: y, col: c };
          y += ROWH;
          last = d;
        });
        size.h = Math.max(size.h, y + PAD);
      });
      size.w = PAD * 2 + TIERS.length * COLW + (TIERS.length - 1) * GAP;
    }
    assign();
    // Each file's block of a column is ordered by where its neighbours sit, to untangle the edges.
    for (var pass = 0; pass < 6; pass++) {
      (pass % 2 ? cols.slice().reverse() : cols).forEach(function (col) {
        var rank = function (d) {
          var near = uses[d.id].concat(usedBy[d.id]).filter(function (id) { return d.kind === "value" || defs[id].kind !== "value"; });
          if (!near.length) { return pos[d.id].y; }
          return near.reduce(function (a, id) { return a + pos[id].y; }, 0) / near.length;
        };
        var blocks = [];
        col.forEach(function (d) {
          var b = blocks[blocks.length - 1];
          if (b && b[0].file === d.file) { b.push(d); } else { blocks.push([d]); }
        });
        var keyed = blocks.map(function (b) {
          return b.map(function (d) { return [rank(d), d]; }).sort(function (a, b2) { return a[0] - b2[0]; })
            .map(function (e) { return e[1]; });
        });
        col.length = 0;
        keyed.forEach(function (b) { b.forEach(function (d) { col.push(d); }); });
      });
      assign();
    }
  }

  var els = { svg: null, world: null, nodes: {}, edges: [] };
  var selected = null, selectedFile = null, hovered = null, query = "", hiddenFiles = {};
  var view = { k: 1, x: 0, y: 0 }, touched = false, dragged = false;

  function edgePath(a, b) {
    var pa = pos[a], pb = pos[b], cy = PILL / 2;
    if (pa.col === pb.col) {
      var x = pa.x - 38;
      return "M" + pa.x + "," + (pa.y + cy) + "C" + x + "," + (pa.y + cy) + " " + x + "," + (pb.y + cy) + " " + pb.x + "," + (pb.y + cy);
    }
    var l = pa.col < pb.col ? pa : pb, r = pa.col < pb.col ? pb : pa;
    var x0 = l.x + COLW, x1 = r.x, mid = (x0 + x1) / 2;
    return "M" + x0 + "," + (l.y + cy) + "C" + mid + "," + (l.y + cy) + " " + mid + "," + (r.y + cy) + " " + x1 + "," + (r.y + cy);
  }

  function buildGraph(box) {
    layout();
    var s = svg("svg", { "class": "sx-svg", role: "group", "aria-label": "Schema definition graph" });
    var world = svg("g", { "class": "sx-world" });
    var edgeLayer = svg("g"), nodeLayer = svg("g"), headLayer = svg("g");
    data.edges.forEach(function (e) {
      var p = svg("path", { "class": "sx-edge", d: edgePath(e.from, e.to) });
      edgeLayer.appendChild(p);
      els.edges.push({ el: p, from: e.from, to: e.to });
    });
    data.defs.forEach(function (d) {
      var p = pos[d.id], name = d.name.length > 22 ? d.name.slice(0, 21) + "…" : d.name;
      var g = svg("g", { "class": "sx-node", transform: "translate(" + p.x + "," + p.y + ")", tabindex: 0, role: "link",
        "data-ref": d.id, "aria-label": SINGLE[d.kind] + " " + d.name + ", " + d.file }, [
        svg("rect", { width: COLW, height: PILL, rx: 4 }), svg("text", { x: 8, y: PILL / 2 + 4 })]);
      g.style.setProperty("--fc", colour(d.file));
      g.lastChild.textContent = name;
      nodeLayer.appendChild(g);
      els.nodes[d.id] = g;
    });
    TIERS.forEach(function (kind, c) {
      var n = data.defs.filter(function (d) { return d.kind === kind; }).length;
      var t = svg("text", { "class": "sx-colhead", x: PAD + c * (COLW + GAP), y: 22 });
      t.textContent = PLURAL[kind] + " · " + n;
      headLayer.appendChild(t);
    });
    add(world, [edgeLayer, nodeLayer, headLayer]);
    s.appendChild(world);
    els.svg = s;
    els.world = world;
    box.appendChild(s);
    interactions(s);
  }

  function paint() {
    var focus = hovered || selected;
    var near = {};
    if (focus) {
      near[focus] = 1;
      uses[focus].concat(usedBy[focus]).forEach(function (id) { near[id] = 1; });
    }
    var q = query.trim().toLowerCase();
    var matches = {};
    if (q && !focus) {
      data.defs.forEach(function (d) {
        if (d.name.toLowerCase().indexOf(q) >= 0 || SINGLE[d.kind] === q) { matches[d.id] = 1; }
      });
    }
    data.defs.forEach(function (d) {
      var c = els.nodes[d.id].classList;
      c.toggle("off", !!hiddenFiles[d.file]);
      c.toggle("sel", d.id === selected);
      c.toggle("nb", !!focus && !!near[d.id] && d.id !== selected);
      c.toggle("dim", (!!focus && !near[d.id]) || (!!q && !focus && !matches[d.id]) ||
        (!!selectedFile && !focus && d.file !== selectedFile));
    });
    els.edges.forEach(function (e) {
      var c = e.el.classList;
      var touch = focus && (e.from === focus || e.to === focus);
      var gone = hiddenFiles[defs[e.from].file] || hiddenFiles[defs[e.to].file] ||
        (defs[e.to].kind === "value" && !touch);
      c.toggle("gone", !!gone);
      c.toggle("hot", !!touch);
      c.toggle("uses", !!touch && e.from === focus);
      c.toggle("usedby", !!touch && e.to === focus);
      if (touch) { e.el.parentNode.appendChild(e.el); }
    });
  }

  function apply(animate) {
    els.world.style.transition = animate ? "transform .35s ease" : "none";
    els.world.style.transform = "translate(" + view.x + "px," + view.y + "px) scale(" + view.k + ")";
  }
  // Frame the selection and what it touches, or the whole graph. Types are left out of the
  // frame: nearly everything uses them, and they sit at the far left.
  function frame(animate, whole) {
    var r = els.svg.getBoundingClientRect();
    if (!r.width || !r.height) { return; }
    var ids = whole ? null : selected ? [selected].concat(uses[selected], usedBy[selected]).filter(function (id) {
      return id === selected || defs[id].kind !== "value";
    }) : selectedFile ? fileDefs(files[selectedFile]) : null;
    var x0 = 0, y0 = 0, x1 = size.w, y1 = size.h;
    if (ids) {
      x0 = y0 = Infinity; x1 = y1 = -Infinity;
      ids.forEach(function (id) {
        x0 = Math.min(x0, pos[id].x); x1 = Math.max(x1, pos[id].x + COLW);
        y0 = Math.min(y0, pos[id].y); y1 = Math.max(y1, pos[id].y + PILL);
      });
      x0 -= 30; x1 += 30; y0 -= 40; y1 += 30;
    }
    var k = clamp(Math.min(r.width / (x1 - x0), r.height / (y1 - y0)), ids ? 0.45 : 0.2, ids ? 1.1 : 1);
    view.k = k;
    view.x = (r.width - (x1 - x0) * k) / 2 - x0 * k;
    view.y = (r.height - (y1 - y0) * k) / 2 - y0 * k;
    touched = false;
    apply(animate);
  }
  function zoomAt(px, py, f) {
    var k = clamp(view.k * f, 0.2, 3);
    f = k / view.k;
    view.x = px - (px - view.x) * f;
    view.y = py - (py - view.y) * f;
    view.k = k;
    touched = true;
    apply(false);
  }

  function interactions(s) {
    s.addEventListener("wheel", function (e) {
      e.preventDefault();
      var r = s.getBoundingClientRect();
      zoomAt(e.clientX - r.left, e.clientY - r.top, Math.exp(-e.deltaY * 0.0015));
    }, { passive: false });
    var start = null;
    s.addEventListener("pointerdown", function (e) {
      if (e.button) { return; }
      start = { x: e.clientX, y: e.clientY, vx: view.x, vy: view.y, id: e.pointerId, moving: false };
    });
    s.addEventListener("pointermove", function (e) {
      if (!start || e.pointerId !== start.id) { return; }
      var dx = e.clientX - start.x, dy = e.clientY - start.y;
      if (!start.moving && Math.hypot(dx, dy) < 5) { return; }
      if (!start.moving) { start.moving = true; s.setPointerCapture(e.pointerId); s.classList.add("panning"); hidePop(); }
      view.x = start.vx + dx;
      view.y = start.vy + dy;
      touched = true;
      apply(false);
    });
    function end() {
      if (start && start.moving) { dragged = true; setTimeout(function () { dragged = false; }, 0); }
      start = null;
      s.classList.remove("panning");
    }
    s.addEventListener("pointerup", end);
    s.addEventListener("pointercancel", end);
  }

  // -- the page -----------------------------------------------------------------------------

  var ui = {};
  var idx = 0, furthest = 0;

  function build() {
    host.textContent = "";
    ui.back = h("button", "sx-btn", "←");
    ui.fwd = h("button", "sx-btn", "→");
    ui.up = h("button", "sx-btn", "↑");
    ui.back.title = "Back"; ui.fwd.title = "Forward"; ui.up.title = "Up one level";
    ui.back.setAttribute("aria-label", "Back"); ui.fwd.setAttribute("aria-label", "Forward");
    ui.up.setAttribute("aria-label", "Up one level");
    ui.crumbs = h("nav", "sx-crumbs");
    ui.crumbs.setAttribute("aria-label", "Breadcrumb");
    ui.search = h("input", "sx-search");
    ui.search.type = "search";
    ui.search.placeholder = "Find a definition…";
    ui.search.setAttribute("aria-label", "Find a definition");
    ui.search.autocomplete = "off";
    ui.results = h("ul", "sx-results");
    ui.results.hidden = true;
    ui.graph = h("div", "sx-graph");
    ui.panel = h("div", "sx-panel");
    ui.panel.tabIndex = -1;

    var legend = h("div", "sx-legend");
    data.files.forEach(function (f) {
      var b = h("button", "sx-key", [dot(f.id), f.id]);
      b.title = "Show or hide the " + f.id + " schema's definitions";
      b.setAttribute("aria-pressed", "true");
      b.addEventListener("click", function () {
        hiddenFiles[f.id] = !hiddenFiles[f.id];
        b.setAttribute("aria-pressed", hiddenFiles[f.id] ? "false" : "true");
        paint();
      });
      legend.appendChild(b);
    });
    var zoom = h("div", "sx-zoom", [h("button", "sx-btn", "+"), h("button", "sx-btn", "−"), h("button", "sx-btn", "Fit")]);
    zoom.children[0].title = "Zoom in"; zoom.children[1].title = "Zoom out"; zoom.children[2].title = "Show the whole graph";
    zoom.children[0].addEventListener("click", function () { var r = els.svg.getBoundingClientRect(); zoomAt(r.width / 2, r.height / 2, 1.3); });
    zoom.children[1].addEventListener("click", function () { var r = els.svg.getBoundingClientRect(); zoomAt(r.width / 2, r.height / 2, 1 / 1.3); });
    zoom.children[2].addEventListener("click", function () { frame(true, true); });
    add(ui.graph, [legend, zoom]);
    buildGraph(ui.graph);

    add(host, [
      h("div", "sx-bar", [ui.back, ui.fwd, ui.up, ui.crumbs, h("div", "sx-find", [ui.search, ui.results])]),
      h("div", "sx-split", [ui.graph, ui.panel])]);

    ui.back.addEventListener("click", function () { history.back(); });
    ui.fwd.addEventListener("click", function () { history.forward(); });
    ui.up.addEventListener("click", function () { var p = parentOf(current); if (p != null) { navigate(p); } });
    search();
  }

  function search() {
    function show() {
      var q = ui.search.value.trim().toLowerCase();
      query = q;
      ui.results.textContent = "";
      var hits = q ? data.defs.filter(function (d) { return d.name.toLowerCase().indexOf(q) >= 0; }) : [];
      hits.sort(function (a, b) { return (a.name.toLowerCase().indexOf(q) > 0) - (b.name.toLowerCase().indexOf(q) > 0) || TIERS.indexOf(a.kind) - TIERS.indexOf(b.kind); });
      hits.slice(0, 12).forEach(function (d) {
        ui.results.appendChild(h("li", "", link(d.id, "sx-hit", [kindTag(d.kind), d.name, h("small", "", d.file)])));
      });
      ui.results.hidden = !hits.length;
      paint();
    }
    ui.search.addEventListener("input", show);
    ui.search.addEventListener("keydown", function (e) {
      if (e.key === "Escape") { ui.search.value = ""; show(); }
      if (e.key === "Enter") {
        var first = ui.results.querySelector("a");
        if (first) { e.preventDefault(); ui.search.value = ""; navigate(first.getAttribute("data-ref")); show(); }
      }
    });
    document.addEventListener("click", function (e) {
      if (!e.target.closest(".sx-find")) { ui.results.hidden = true; }
    });
    ui.search.addEventListener("focus", function () { if (ui.results.children.length) { ui.results.hidden = false; } });
  }

  var current = null;
  function crumbs(route) {
    ui.crumbs.textContent = "";
    var trail = [["", "Schema Reference"]];
    if (defs[route]) { trail.push([defs[route].file, defs[route].file], [route, defs[route].name]); }
    else if (files[route]) { trail.push([route, route]); }
    trail.forEach(function (t, i) {
      if (i) { ui.crumbs.appendChild(h("span", "sx-sep", "›")); }
      ui.crumbs.appendChild(i === trail.length - 1 ? h("span", "sx-here", t[1]) : link(t[0], "", t[1]));
    });
  }

  function render() {
    hidePop();
    anchor = null;
    current = routeOf(location.hash);
    var panel = !exists(current) ? lostPanel() : !current ? topPanel() : files[current] ? filePanel(files[current]) : defPanel(defs[current]);
    ui.panel.textContent = "";
    ui.panel.appendChild(panel);
    ui.panel.scrollTop = 0;
    crumbs(current);
    ui.back.disabled = idx <= 0;
    ui.fwd.disabled = idx >= furthest;
    ui.up.disabled = parentOf(current) == null;
    selected = defs[current] ? current : null;
    selectedFile = files[current] ? current : null;
    hovered = null;
    paint();
    frame(true);
    var name = defs[current] ? defs[current].name : files[current] ? files[current].title : "";
    document.title = name ? name + " — " + TITLE : TITLE;
  }

  function navigate(route) {
    if (route === current) { return; }
    idx += 1;
    furthest = idx;
    history.pushState({ sx: idx }, "", hashOf(route));
    render();
  }

  // -- events -------------------------------------------------------------------------------

  function target(el) { return el.closest ? el.closest("[data-ref],[data-go]") : null; }

  host.addEventListener("click", function (e) {
    var t = target(e.target);
    if (!t || dragged) { return; }
    if (e.button || e.ctrlKey || e.metaKey || e.shiftKey || e.altKey) { return; }
    if (String(window.getSelection()).trim() && !t.matches("a, .sx-node")) { return; }
    e.preventDefault();
    if (t.closest(".sx-results")) { ui.search.value = ""; ui.results.hidden = true; query = ""; }
    navigate(t.getAttribute("data-ref") || t.getAttribute("data-go"));
  });
  host.addEventListener("keydown", function (e) {
    var t = target(e.target);
    if (t && t === e.target && (e.key === "Enter" || e.key === " ") && !t.matches("a")) {
      e.preventDefault();
      navigate(t.getAttribute("data-ref") || t.getAttribute("data-go"));
    }
  });

  var anchor = null;
  function over(el) {
    var t = el && el.closest ? el.closest("[data-ref]") : null;
    var id = t && defs[t.getAttribute("data-ref")] ? t.getAttribute("data-ref") : null;
    var node = t && t.matches(".sx-node") ? id : null;
    if (node !== hovered) { hovered = node; paint(); }
    if (t === anchor) { return; }
    anchor = t;
    hidePop();
    if (id) { popTimer = setTimeout(function () { showPop(id, t); }, 120); }
  }
  host.addEventListener("mouseover", function (e) { over(e.target); });
  host.addEventListener("mouseleave", function () { over(null); });
  host.addEventListener("focusin", function (e) { over(e.target); });
  host.addEventListener("focusout", function () { over(null); });
  document.addEventListener("scroll", hidePop, true);

  window.addEventListener("popstate", function (e) {
    idx = (e.state && e.state.sx) || 0;
    furthest = Math.max(furthest, idx);
    render();
  });
  var resizeTimer = null;
  function resized() {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(function () { if (!touched) { frame(false); } }, 100);
  }

  idx = (history.state && history.state.sx) || 0;
  furthest = idx;
  history.replaceState({ sx: idx }, "");
  build();
  render();
  if (window.ResizeObserver) { new ResizeObserver(resized).observe(ui.graph); }
  else { window.addEventListener("resize", resized); }
})();
