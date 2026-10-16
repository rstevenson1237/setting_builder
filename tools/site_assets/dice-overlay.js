import * as THREE from "three";
import * as CANNON from "cannon";
import { DiceManager, DiceD4, DiceD6, DiceD8, DiceD10, DiceD12, DiceD20 } from "./dice.js";

const DIE_TYPES = { 4: DiceD4, 6: DiceD6, 8: DiceD8, 10: DiceD10, 12: DiceD12, 20: DiceD20 };
const MAX_DICE = 6;
const SIZE = 50;            // die size in world units
const HALF_VIEW = 260;      // the shorter half-extent of the floor in view
const FOV = 40;
const GRAVITY = -9.82 * 60;
const SETTLE_FRAMES = 30;   // consecutive still frames before a throw counts as finished
const GIVE_UP_SECONDS = 8;  // report whatever the dice show after this long
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

export function createRoller() {
  let sides = 6;
  let count = 1;

  const overlay = el("div", "dice-overlay", { hidden: true });
  overlay.setAttribute("role", "dialog");
  overlay.setAttribute("aria-modal", "true");
  overlay.setAttribute("aria-label", "Dice roller");
  const canvas = el("canvas", "dice-canvas");
  const panel = el("div", "dice-panel");
  const result = el("div", "dice-result");
  result.setAttribute("aria-live", "polite");

  const countSelect = el("select");
  for (let n = 1; n <= MAX_DICE; n++) countSelect.add(new Option(n, n));
  const sidesSelect = el("select");
  for (const s of Object.keys(DIE_TYPES)) sidesSelect.add(new Option("d" + s, s));
  sidesSelect.value = String(sides);
  const rollButton = el("button", "dice-roll", { type: "button", textContent: "Roll again" });
  const closeButton = el("button", "dice-close", { type: "button", textContent: "Close" });

  const controls = el("div", "dice-controls");
  controls.append(label("Dice", countSelect), label("Die", sidesSelect), rollButton, closeButton);
  panel.append(result, controls);
  overlay.append(canvas, panel);
  document.body.appendChild(overlay);

  function label(text, control) {
    const node = el("label");
    node.append(text + " ", control);
    return node;
  }

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

  // The camera looks straight down, so the floor maps linearly to the screen and the
  // walls can sit exactly on the edges of the area the panel leaves free.
  function fitView() {
    const w = window.innerWidth;
    const h = window.innerHeight;
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

  function throwDice(bounds) {
    const { halfW, minZ, maxZ } = bounds;
    const centreZ = (minZ + maxZ) / 2;
    const halfZ = (maxZ - minZ) / 2;
    // Throw along the longer side of the free area, from one end.
    const alongX = halfW >= halfZ;
    const reach = (alongX ? halfW : halfZ) * 0.8;
    const side = Math.random() < 0.5 ? -1 : 1;
    const options = { size: SIZE, fontColor: cssVar("--bg") || "#faf6ef", backColor: cssVar("--accent") || "#7a2e1d" };
    for (let i = 0; i < count; i++) {
      const die = new DIE_TYPES[sides](options);
      const body = die.getObject().body;
      const lane = (i - (count - 1) / 2) * SIZE * 1.6;
      const speed = rand(250, 400);
      const spread = rand(-120, 120);
      body.position.set(
        alongX ? -side * reach : THREE.MathUtils.clamp(lane + spread / 4, -halfW * 0.8, halfW * 0.8),
        SIZE * (3 + i),
        alongX ? THREE.MathUtils.clamp(centreZ + lane, minZ + SIZE, maxZ - SIZE) : centreZ - side * reach
      );
      body.linearDamping = 0.2;
      body.angularDamping = 0.3;
      body.quaternion.setFromEuler(rand(0, 6.28), rand(0, 6.28), rand(0, 6.28), "XYZ");
      body.velocity.set(alongX ? side * speed : spread, -100, alongX ? spread : side * speed);
      body.angularVelocity.set(rand(-20, 20), rand(-20, 20), rand(-20, 20));
      scene.add(die.getObject());
      dice.push(die);
    }
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
    return dice.map((die) => (sides === 10 && die.getUpsideValue() === 0 ? 10 : die.getUpsideValue()));
  }

  function finish() {
    rolling = false;
    rollButton.disabled = false;
    const values = readValues();
    const total = values.reduce((sum, v) => sum + v, 0);
    result.textContent = "";
    result.append(el("strong", "dice-total", { textContent: String(total) }));
    if (values.length > 1) result.append(el("span", "dice-parts", { textContent: " = " + values.join(" + ") }));
    if (pending) {
      pending.resolve(pending.convert(total));
      pending = null;
      closeTimer = setTimeout(close, QUICK_HOLD_MS);
    }
  }

  function throwNow(wantedSides, wantedCount) {
    if (rolling) return;
    cancelAnimationFrame(frameId);
    sides = wantedSides;
    count = wantedCount;
    const bounds = fitView();
    buildWalls(bounds);
    clearDice();
    throwDice(bounds);
    rolling = true;
    rollButton.disabled = true;
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

  function roll() {
    throwNow(Number(sidesSelect.value), Number(countSelect.value));
  }

  function show(quick) {
    clearTimeout(closeTimer);
    opener = document.activeElement;
    overlay.classList.toggle("quick", quick);
    overlay.hidden = false;
  }

  // The header button: the overlay with its controls.
  function open() {
    show(false);
    roll();
    rollButton.focus();
  }

  // A roll the page asks for: one die, thrown on its own, resolving to the value it shows.
  // d2 and d3 are read off a d6. Resolves null for any other die, or while a throw is running.
  function rollFor(wanted) {
    const physical = DIE_TYPES[wanted] ? wanted : (6 % wanted === 0 ? 6 : 0);
    if (!physical || rolling) return Promise.resolve(null);
    return new Promise((resolve) => {
      pending = { resolve, convert: (value) => Math.ceil(value * wanted / physical) };
      show(true);
      throwNow(physical, 1);
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

  rollButton.addEventListener("click", roll);
  closeButton.addEventListener("click", close);
  overlay.addEventListener("click", (e) => { if (e.target === canvas) dismiss(); });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape" && !overlay.hidden) dismiss(); });
  window.addEventListener("resize", () => {
    if (overlay.hidden) return;
    fitView();
    if (!rolling) renderer.render(scene, camera);
  });

  return { open, roll: rollFor };
}
