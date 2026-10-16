import * as THREE from "three";
import * as CANNON from "cannon";
import { DiceManager, DiceD4, DiceD6, DiceD8, DiceD10, DiceD12, DiceD20 } from "./dice.js";

const DIE_TYPES = { 4: DiceD4, 6: DiceD6, 8: DiceD8, 10: DiceD10, 12: DiceD12, 20: DiceD20 };
const SIZE = 50;            // die size in world units
const CROWDED = 6;          // above this many dice, they are thrown smaller
const HALF_VIEW = 260;      // the shorter half-extent of the floor in view
const FOV = 40;
const GRAVITY = -9.82 * 60;
const SETTLE_FRAMES = 30;   // consecutive still frames before a throw counts as finished
const GIVE_UP_SECONDS = 10; // report whatever the dice show after this long
const STEP = 1 / 60;
const QUICK_HOLD_MS = 1400; // how long a result from the page stays up before the overlay closes

const rand = (min, max) => min + Math.random() * (max - min);
const cssVar = (name) => getComputedStyle(document.documentElement).getPropertyValue(name).trim();

function el(tag, className, attrs) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  Object.assign(node, attrs);
  return node;
}

// The physical dice a roll throws: with advantage or disadvantage every die is thrown twice.
function physicalDice(spec) {
  return spec.mode === "sep" && spec.adv ? spec.dice.flatMap((sides) => [sides, sides]) : spec.dice.slice();
}

// What the values the physical dice show come to under the roll's rules.
function evaluate(spec, values) {
  if (spec.mode === "sum") {
    const parts = spec.dice.map((sides, i) => ({ sides, value: values[i], dropped: false }));
    if (spec.drop && parts.length > 1) {
      const lowest = spec.drop === "DL";
      parts.reduce((pick, p) => ((lowest ? p.value < pick.value : p.value > pick.value) ? p : pick)).dropped = true;
    }
    const total = parts.reduce((sum, p) => sum + (p.dropped ? 0 : p.value), spec.bonus);
    return { mode: "sum", parts, bonus: spec.bonus, total };
  }
  const per = spec.adv ? 2 : 1;
  const items = spec.dice.map((sides, i) => {
    const raw = values.slice(i * per, i * per + per);
    const kept = spec.adv === "ADV" ? Math.max(...raw) : spec.adv === "DIS" ? Math.min(...raw) : raw[0];
    return { sides, raw, kept, total: kept + spec.bonus };
  });
  return { mode: "sep", items, bonus: spec.bonus, total: items.reduce((sum, item) => sum + item.total, 0) };
}

const signed = (n) => (n < 0 ? "− " : "+ ") + Math.abs(n);

function renderOutcome(into, outcome) {
  into.textContent = "";
  if (outcome.mode === "sum") {
    into.append(el("strong", "dice-total", { textContent: String(outcome.total) }));
    if (outcome.parts.length > 1 || outcome.bonus) {
      const parts = el("span", "dice-parts", { textContent: " = " });
      outcome.parts.forEach((p, i) => {
        if (i) parts.append(" + ");
        parts.append(el(p.dropped ? "s" : "span", "", { textContent: String(p.value) }));
      });
      if (outcome.bonus) parts.append(" " + signed(outcome.bonus));
      into.append(parts);
    }
    return;
  }
  const row = el("div", "dice-items");
  for (const item of outcome.items) {
    const detail = el("small", "dice-detail", { textContent: "d" + item.sides + " " });
    const kept = item.raw.indexOf(item.kept);
    item.raw.forEach((v, i) => {
      if (i) detail.append(" ");
      detail.append(el(item.raw.length > 1 && i !== kept ? "s" : "span", "", { textContent: String(v) }));
    });
    if (outcome.bonus) detail.append(" " + signed(outcome.bonus));
    const node = el("span", "dice-item");
    node.append(el("strong", "", { textContent: String(item.total) }), detail);
    row.append(node);
  }
  into.append(row);
}

export function createRoller() {
  const overlay = el("div", "dice-overlay", { hidden: true });
  overlay.setAttribute("role", "dialog");
  overlay.setAttribute("aria-label", "Dice roller");
  const canvas = el("canvas", "dice-canvas");
  const panel = el("div", "dice-panel");
  const result = el("div", "dice-result");
  result.setAttribute("aria-live", "polite");
  const closeButton = el("button", "dice-close", { type: "button", textContent: "Close" });
  panel.append(result, closeButton);
  overlay.append(canvas, panel);
  document.body.appendChild(overlay);
  const header = document.querySelector(".site-header");

  const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(FOV, 1, 10, 5000);
  scene.add(new THREE.AmbientLight(0xffffff, 0.7));
  const sun = new THREE.DirectionalLight(0xffffff, 0.6);
  sun.position.set(-150, 400, 200);
  scene.add(sun);

  const world = new CANNON.World();
  world.gravity.set(0, GRAVITY, 0);
  world.broadphase = new CANNON.NaiveBroadphase();
  world.solver.iterations = 16;
  DiceManager.setWorld(world);
  const floorContact = world.getContactMaterial(DiceManager.floorBodyMaterial, DiceManager.diceBodyMaterial);
  floorContact.friction = 0.3;
  floorContact.restitution = 0.4;

  addPlane(DiceManager.floorBodyMaterial, [0, 0, 0], "x", -Math.PI / 2);
  let walls = [];
  let dice = [];
  let spec = null;          // the roll in flight, or last thrown
  let frameId = 0;
  let lastTime = 0;
  let elapsed = 0;
  let stillFrames = 0;
  let rolling = false;
  let opener = null;
  let pending = null;       // a roll asked for by the page: { resolve, convert }
  let closeTimer = 0;

  function addPlane(material, position, axis, angle) {
    const body = new CANNON.Body({ mass: 0, shape: new CANNON.Plane(), material });
    body.quaternion.setFromAxisAngle(new CANNON.Vec3(axis === "x" ? 1 : 0, axis === "y" ? 1 : 0, 0), angle);
    body.position.set(...position);
    world.add(body);
    return body;
  }

  // The overlay sits under the header so the header's roll controls stay in reach.
  // The camera looks straight down, so the floor maps linearly to the screen and the
  // walls can sit exactly on the edges of the area the panel leaves free.
  function fitView() {
    overlay.style.top = header ? header.getBoundingClientRect().bottom + "px" : "0";
    const w = overlay.clientWidth;
    const h = overlay.clientHeight;
    renderer.setPixelRatio(window.devicePixelRatio || 1);
    renderer.setSize(w, h, false);
    const aspect = w / h;
    camera.aspect = aspect;
    camera.position.set(0, HALF_VIEW / (Math.tan(THREE.MathUtils.degToRad(FOV / 2)) * Math.min(1, aspect)), 0);
    camera.up.set(0, 0, -1);
    camera.lookAt(0, 0, 0);
    camera.updateProjectionMatrix();
    const halfD = camera.position.y * Math.tan(THREE.MathUtils.degToRad(FOV / 2));
    const panelShare = Math.min(0.5, (panel.offsetHeight + 16) / h);
    // Perspective pushes a die's top toward the screen edge, so keep the walls inside it.
    const inset = 0.88;
    return { halfW: halfD * aspect * inset, minZ: -halfD * inset, maxZ: halfD * inset - 2 * halfD * panelShare };
  }

  function buildWalls(bounds) {
    walls.forEach((wall) => world.remove(wall));
    const { halfW, minZ, maxZ } = bounds;
    const ceiling = SIZE * 8;
    walls = [
      addPlane(DiceManager.barrierBodyMaterial, [halfW, 0, 0], "y", -Math.PI / 2),
      addPlane(DiceManager.barrierBodyMaterial, [-halfW, 0, 0], "y", Math.PI / 2),
      addPlane(DiceManager.barrierBodyMaterial, [0, 0, maxZ], "y", Math.PI),
      addPlane(DiceManager.barrierBodyMaterial, [0, 0, minZ], "y", 0),
      addPlane(DiceManager.barrierBodyMaterial, [0, ceiling, 0], "x", Math.PI / 2),
    ];
  }

  function clearDice() {
    for (const die of dice) {
      const mesh = die.getObject();
      scene.remove(mesh);
      world.remove(mesh.body);
      mesh.geometry.dispose();
      for (const material of mesh.material) {
        material.map.dispose();
        material.dispose();
      }
    }
    dice = [];
  }

  // Dice are thrown from one end of the free area along its longer side, in rows across it.
  function throwDice(plan, bounds) {
    const { halfW, minZ, maxZ } = bounds;
    const halfZ = (maxZ - minZ) / 2;
    const alongX = halfW >= halfZ;
    const size = plan.length > CROWDED ? SIZE * 0.8 : SIZE;
    const gap = size * 2.6;
    const crossHalf = alongX ? halfZ : halfW;
    const perRow = Math.max(1, Math.floor((crossHalf * 2) / gap));
    const side = Math.random() < 0.5 ? -1 : 1;
    const options = { size, fontColor: cssVar("--bg") || "#faf6ef", backColor: cssVar("--accent") || "#7a2e1d" };
    plan.forEach((faces, i) => {
      const die = new DIE_TYPES[faces](options);
      const body = die.getObject().body;
      const row = Math.floor(i / perRow);
      const inRow = Math.min(perRow, plan.length - row * perRow);
      const cross = (i % perRow - (inRow - 1) / 2) * gap;
      const along = -side * ((alongX ? halfW : halfZ) - size * 1.6 - row * gap);
      const speed = rand(250, 400);
      const spread = rand(-120, 120);
      const y = size * 2.5 + rand(0, size);
      if (alongX) {
        body.position.set(along, y, (minZ + maxZ) / 2 + cross);
        body.velocity.set(side * speed, -100, spread);
      } else {
        body.position.set(cross, y, (minZ + maxZ) / 2 + along);
        body.velocity.set(spread, -100, side * speed);
      }
      body.linearDamping = 0.2;
      body.angularDamping = 0.3;
      body.quaternion.setFromEuler(rand(0, 6.28), rand(0, 6.28), rand(0, 6.28), "XYZ");
      body.angularVelocity.set(rand(-20, 20), rand(-20, 20), rand(-20, 20));
      scene.add(die.getObject());
      dice.push(die);
    });
  }

  function advance(seconds) {
    world.step(STEP, seconds, 5);
    dice.forEach((die) => die.updateMeshFromBody());
    elapsed += seconds;
    stillFrames = dice.every((die) => die.isFinished()) ? stillFrames + 1 : 0;
    return stillFrames >= SETTLE_FRAMES || elapsed > GIVE_UP_SECONDS;
  }

  function frame(now) {
    const seconds = Math.min((now - lastTime) / 1000, 0.1);
    lastTime = now;
    const done = advance(seconds);
    renderer.render(scene, camera);
    if (done) finish();
    else frameId = requestAnimationFrame(frame);
  }

  function readValues() {
    // A d10 shows 0 where the ten is.
    return dice.map((die) => (die.values === 10 && die.getUpsideValue() === 0 ? 10 : die.getUpsideValue()));
  }

  function finish() {
    rolling = false;
    const outcome = evaluate(spec, readValues());
    renderOutcome(result, outcome);
    if (pending) {
      pending.resolve(pending.convert(outcome.total));
      pending = null;
      closeTimer = setTimeout(close, QUICK_HOLD_MS);
    }
  }

  function throwNow(rollSpec) {
    if (rolling) return;
    cancelAnimationFrame(frameId);
    spec = rollSpec;
    const bounds = fitView();
    buildWalls(bounds);
    clearDice();
    throwDice(physicalDice(spec), bounds);
    rolling = true;
    elapsed = 0;
    stillFrames = 0;
    result.textContent = "Rolling…";
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      while (!advance(STEP));
      renderer.render(scene, camera);
      finish();
      return;
    }
    lastTime = performance.now();
    frameId = requestAnimationFrame(frame);
  }

  function show(quick) {
    clearTimeout(closeTimer);
    opener = document.activeElement;
    overlay.classList.toggle("quick", quick);
    overlay.hidden = false;
  }

  // The header pill's roll: { dice: [faces], mode: "sum" | "sep", drop, adv, bonus }.
  function rollSpec(rollSpecification) {
    if (rolling) return;
    show(false);
    throwNow(rollSpecification);
  }

  // A roll the page asks for: one die, thrown on its own, resolving to the value it shows.
  // d2 and d3 are read off a d6. Resolves null for any other die, or while a throw is running.
  function rollFor(wanted) {
    const physical = DIE_TYPES[wanted] ? wanted : (6 % wanted === 0 ? 6 : 0);
    if (!physical || rolling) return Promise.resolve(null);
    return new Promise((resolve) => {
      pending = { resolve, convert: (value) => Math.ceil(value * wanted / physical) };
      show(true);
      throwNow({ dice: [physical], mode: "sum", drop: "", adv: "", bonus: 0 });
    });
  }

  function close() {
    clearTimeout(closeTimer);
    cancelAnimationFrame(frameId);
    rolling = false;
    pending = null;
    overlay.hidden = true;
    if (opener && opener.focus) opener.focus();
  }

  // Closing during a roll the page is waiting on lets the dice finish at once, so it gets its value.
  function dismiss() {
    if (pending && rolling) {
      cancelAnimationFrame(frameId);
      while (!advance(STEP));
      renderer.render(scene, camera);
      finish();
    } else {
      close();
    }
  }

  function relayout() {
    if (overlay.hidden) return;
    fitView();
    if (!rolling) renderer.render(scene, camera);
  }

  closeButton.addEventListener("click", close);
  overlay.addEventListener("click", (e) => { if (e.target === canvas) dismiss(); });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape" && !overlay.hidden) dismiss(); });
  window.addEventListener("resize", relayout);
  if (header && window.ResizeObserver) new ResizeObserver(relayout).observe(header);

  return { rollSpec, roll: rollFor };
}
