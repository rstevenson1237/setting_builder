// dice.js imports 'cannon' as an ES module; cannon 0.6.2 only ships a UMD build that sets window.CANNON.
await new Promise((resolve, reject) => {
  const script = document.createElement("script");
  script.src = "https://cdn.jsdelivr.net/npm/cannon@0.6.2/build/cannon.min.js";
  script.onload = resolve;
  script.onerror = () => reject(new Error("cannon failed to load"));
  document.head.appendChild(script);
});

export const {
  World, NaiveBroadphase, Body, Plane, Vec3, Quaternion, Mat3,
  Material, ContactMaterial, ConvexPolyhedron,
} = window.CANNON;
