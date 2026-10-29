// Checks Remix, Twilight Theme's CSS reset (remix/), in Chromium. Three checks:
//
// 1. Parity. pages/elements.html, with every element Remix styles, has the same computed style with
//    remix/remix.css, with remix/remix.min.css, and with Tailwind CSS 4 and remix/remix-tailwind.css: on a
//    desktop screen, a 320 px window, a handheld screen (coarse pointer) and in print.
// 2. Rules. In the same page, sizes, weights and leading are the values of typography/twilight.json for
//    each geometry; no element has outer spacing; placeholders are readable.
// 3. Components. pages/components.html, with daisyUI, Flowbite and utility-class components (the way
//    shadcn/ui and Nuxt UI write them), keeps every style its classes set when Remix is added: spacing,
//    borders, display, colors, decoration, and the size, weight and line height of any element whose
//    own classes set them.
//
//   npm ci && npm test          CHROMIUM_PATH=/path/to/chrome uses that browser; in CI, the runner's Chrome.
import { execFileSync } from "node:child_process";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join, relative } from "node:path";
import { fileURLToPath } from "node:url";
import { inflateSync } from "node:zlib";
import { chromium } from "playwright-core";

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = join(HERE, "..", "..");
const BUILD = join(HERE, ".build");
const T = JSON.parse(readFileSync(join(ROOT, "typography", "twilight.json"), "utf8"));
const failures = [];
const fail = (msg) => failures.push(msg);
mkdirSync(BUILD, { recursive: true });

// Stylesheets ----------------------------------------------------------------------------------
const remix = relative(BUILD, join(ROOT, "remix", "remix-tailwind.css"));
const LIBRARIES = {
  tailwind: [],
  daisyui: ['@plugin "daisyui";'],
  flowbite: ['@import "flowbite/src/themes/default";', '@plugin "flowbite/plugin";'],
};
function compile(name, lines) {
  const input = join(BUILD, `${name}.in.css`);
  writeFileSync(input, lines.join("\n") + `\n@source "../pages";\n`);
  execFileSync(join(HERE, "node_modules", ".bin", "tailwindcss"), ["-i", input, "-o", join(BUILD, `${name}.css`)], {
    cwd: HERE, stdio: "pipe",
  });
}
for (const [lib, extra] of Object.entries(LIBRARIES)) {
  const head = ['@import "tailwindcss";'];
  const imports = extra.filter((l) => l.startsWith("@import")), plugins = extra.filter((l) => !l.startsWith("@import"));
  compile(lib, [...head, ...imports, ...plugins]);
  compile(`${lib}-remix`, [...head, ...imports, `@import "${remix}";`, ...plugins]);
}

function page(name, body, sheets) {
  const links = sheets.map((s) => `<link rel="stylesheet" href="${s}">`).join("");
  const file = join(BUILD, `${name}.html`);
  writeFileSync(file, `<!doctype html><html lang="en"><head><meta charset="utf-8">` +
    `<meta name="viewport" content="width=device-width, initial-scale=1">${links}</head><body>${body}</body></html>`);
  return "file://" + file;
}
const doc = readFileSync(join(HERE, "pages", "elements.html"), "utf8");
const components = readFileSync(join(HERE, "pages", "components.html"), "utf8");
const vanillaDoc = page("elements-vanilla", doc, [relative(BUILD, join(ROOT, "remix", "remix.css"))]);
const minDoc = page("elements-min", doc, [relative(BUILD, join(ROOT, "remix", "remix.min.css"))]);
const tailwindDoc = page("elements-tailwind", doc, ["tailwind-remix.css"]);

// PNG: the darkest gray value of an 8-bit RGB or RGBA screenshot -------------------------------
function darkest(png) {
  let pos = 8, width = 0, height = 0, channels = 4;
  const idat = [];
  while (pos < png.length) {
    const len = png.readUInt32BE(pos), type = png.toString("ascii", pos + 4, pos + 8), data = png.subarray(pos + 8, pos + 8 + len);
    if (type === "IHDR") { width = data.readUInt32BE(0); height = data.readUInt32BE(4); channels = data[9] === 6 ? 4 : 3; }
    if (type === "IDAT") idat.push(data);
    pos += 12 + len;
  }
  const raw = inflateSync(Buffer.concat(idat)), stride = width * channels, prev = Buffer.alloc(stride), row = Buffer.alloc(stride);
  let min = 255;
  for (let y = 0; y < height; y++) {
    const f = raw[y * (stride + 1)], line = raw.subarray(y * (stride + 1) + 1, (y + 1) * (stride + 1));
    for (let x = 0; x < stride; x++) {
      const a = x >= channels ? row[x - channels] : 0, b = prev[x], c = x >= channels ? prev[x - channels] : 0;
      const p = a + b - c, pa = Math.abs(p - a), pb = Math.abs(p - b), pc = Math.abs(p - c);
      const pred = [0, a, b, (a + b) >> 1, pa <= pb && pa <= pc ? a : pb <= pc ? b : c][f];
      row[x] = (line[x] + pred) & 255;
    }
    for (let x = 0; x < width; x++) min = Math.min(min, row[x * channels], row[x * channels + 1], row[x * channels + 2]);
    row.copy(prev);
  }
  return min;
}

// Browser --------------------------------------------------------------------------------------
const browser = await chromium.launch(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH }
  : { channel: "chrome" });
const MODES = {
  desktop: { context: { viewport: { width: 1280, height: 900 } }, geometry: "desktop" },
  "narrow desktop": { context: { viewport: { width: 320, height: 900 } }, geometry: "desktop" },
  handheld: { context: { viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 },
    geometry: "handheld" },
  print: { context: { viewport: { width: 1280, height: 900 } }, media: "print", geometry: "page" },
};
const PROPS = ["display", "position", "font-family", "font-size", "font-weight", "font-style", "line-height",
  "letter-spacing", "word-spacing", "text-transform", "text-align", "text-decoration-line", "text-wrap-style",
  "font-variant-numeric", "font-variant-ligatures", "list-style-type", "max-width", "margin-top", "margin-right",
  "margin-bottom", "margin-left", "padding-top", "padding-right", "padding-bottom", "padding-left", "border-top-width",
  "border-right-width", "border-bottom-width", "border-left-width", "border-top-style", "border-left-style",
  "border-bottom-style", "border-top-left-radius", "gap", "color", "background-color", "opacity", "box-sizing",
  "vertical-align", "overflow-x", "resize", "appearance", "min-width", "tab-size", "text-indent", "border-collapse",
  "text-decoration-style", "outline-offset", "max-width", "height"];

async function styles(url, mode) {
  const ctx = await browser.newContext(MODES[mode].context);
  const p = await ctx.newPage();
  if (MODES[mode].media) await p.emulateMedia({ media: MODES[mode].media });
  await p.goto(url);
  const out = await p.evaluate((props) => [...document.querySelectorAll("body *")].map((e, i) => {
    const s = getComputedStyle(e), parent = getComputedStyle(e.parentElement);
    const path = e.tagName.toLowerCase() + (e.className && typeof e.className === "string" ? "." + e.className.trim().split(/\s+/).join(".") : "") + `#${i}`;
    return { path, classed: e.hasAttribute("class"), style: Object.fromEntries(props.map((k) => [k, s.getPropertyValue(k)])),
      parent: Object.fromEntries(props.map((k) => [k, parent.getPropertyValue(k)])), tag: e.tagName.toLowerCase(),
      parentTag: e.parentElement.tagName.toLowerCase(), firstChild: e.parentElement.firstElementChild === e,
      type: e.getAttribute("type") };
  }), PROPS);
  // Placeholders have no computed style to read, so their ink is measured: the darkest pixel of each
  // placeholder, drawn in black on white.
  const placeholders = [];
  for (const el of await p.$$("input[placeholder], textarea[placeholder]")) {
    await el.evaluate((e) => { e.value = ""; e.style.color = "#000"; e.style.backgroundColor = "#fff"; e.style.resize = "none"; });
    placeholders.push(darkest(await el.screenshot()));
  }
  const rootSize = await p.evaluate(() => parseFloat(getComputedStyle(document.documentElement).fontSize));
  const width = await p.evaluate(() => document.documentElement.clientWidth);
  await ctx.close();
  return { els: out, rootSize, width, placeholders };
}

// 1. Parity -------------------------------------------------------------------------------------
const rendered = {};
for (const mode of Object.keys(MODES)) {
  const [v, m, t] = [await styles(vanillaDoc, mode), await styles(minDoc, mode), await styles(tailwindDoc, mode)];
  rendered[mode] = v;
  for (const [label, other] of [["remix.min.css", m], ["Tailwind CSS with remix-tailwind.css", t]]) {
    v.els.forEach((e, i) => {
      for (const k of PROPS) {
        if (e.style[k] !== other.els[i].style[k]) fail(`parity, ${mode}: ${e.path} ${k} is ${e.style[k]} with remix.css, ${other.els[i].style[k]} with ${label}`);
      }
    });
    v.placeholders.forEach((d, i) => {
      if (Math.abs(d - other.placeholders[i]) > 2) fail(`parity, ${mode}: placeholder ${i} ink is ${d} with remix.css, ${other.placeholders[i]} with ${label}`);
    });
  }
}

// 2. Rules --------------------------------------------------------------------------------------
const close = (a, b) => Math.abs(a - b) < 0.02;
const px = (v) => parseFloat(v);
for (const [mode, { els, rootSize, width }] of Object.entries(rendered)) {
  const G = T.geometries[MODES[mode].geometry];
  const unit = G.unit === "pt" ? 4 / 3 : rootSize / 16;           // CSS px per unit of the geometry
  const step = (k) => G.scale[k] * unit;
  const fit = (width - 2 * T.fit.gutter) / T.fit.em;
  const leading = T.leading;
  const check = (cond, msg) => cond || fail(`rules, ${mode}: ${msg}`);
  const body = els.find((e) => e.tag === "main").parent;
  check(close(px(body["font-size"]), step("base")), `body is ${body["font-size"]}, base is ${step("base")}px`);
  check(body["font-family"].startsWith(`"${T.fonts.sans.family}"`), `body font is ${body["font-family"]}`);
  check(body["letter-spacing"] === "normal" || body["letter-spacing"] === "0px", `letter spacing ${body["letter-spacing"]}`);
  for (let i = 1; i <= 6; i++) {
    const L = T.levels[`h${i}`];
    for (const h of els.filter((e) => e.tag === `h${i}`)) {
      const want = Math.min(step(L.size), Math.max(...["desktop", "handheld"].map((g) => T.geometries[g].scale[L.size])) > (T.fit.narrowest - 2 * T.fit.gutter) / T.fit.em ? fit : Infinity);
      check(close(px(h.style["font-size"]), want), `${h.path} is ${h.style["font-size"]}, Heading ${i} is ${want}px`);
      check(h.style["font-weight"] === String(L.weight), `${h.path} weight ${h.style["font-weight"]}`);
      check(close(px(h.style["line-height"]), px(h.style["font-size"]) * leading[L.leading]), `${h.path} line height ${h.style["line-height"]}`);
    }
  }
  for (const e of els.filter((e) => e.tag === "p")) {
    check(close(px(e.style["line-height"]), px(e.style["font-size"]) * leading.default), `${e.path} line height ${e.style["line-height"]}`);
  }
  for (const e of els.filter((e) => ["code", "kbd"].includes(e.tag) && e.parentTag !== "pre")) {
    check(e.style["font-size"] === e.parent["font-size"], `${e.path} is ${e.style["font-size"]} in text of ${e.parent["font-size"]}`);
    check(e.style["font-family"].startsWith(`"${T.fonts.mono.family}"`), `${e.path} font is ${e.style["font-family"]}`);
  }
  for (const e of els.filter((e) => e.tag === "small")) check(close(px(e.style["font-size"]), step(T.levels["body-sm"].size)), `${e.path} is ${e.style["font-size"]}`);
  for (const e of els.filter((e) => e.tag === "table")) check(e.style["font-variant-numeric"] === "tabular-nums", `${e.path} figures`);
  for (const e of els) {
    check(["top", "right", "bottom", "left"].every((s) => e.style[`margin-${s}`] === "0px"), `${e.path} has a margin`);
  }
  for (const e of els.filter((e) => ["ul", "ol", "menu"].includes(e.tag))) check(e.style["list-style-type"] === "none", `${e.path} has markers`);
  for (const e of els.filter((e) => e.tag === "pre")) {
    check(close(px(e.style["line-height"]), px(e.style["font-size"]) * leading[T.levels.code.leading]), `${e.path} line height ${e.style["line-height"]}`);
    check(e.style["overflow-x"] === "auto", `${e.path} overflow ${e.style["overflow-x"]}`);
  }
  // Chromium draws a closed select at its own line height, so selects are left out here.
  const oneLine = (e) => e.tag === "button" || e.tag === "input" && !["checkbox", "radio"].includes(e.type);
  for (const e of els.filter(oneLine)) {
    check(close(px(e.style["line-height"]), px(e.style["font-size"]) * leading[T.levels.ui.leading]), `${e.path} line height ${e.style["line-height"]}`);
  }
  // Black at the placeholder opacity over white: 255 × (1 − opacity), the gray that gives 4.5:1.
  const want = Math.round(255 * (1 - 0.54));
  rendered[mode].placeholders.forEach((d, i) => check(Math.abs(d - want) <= 6, `placeholder ${i} ink is ${d}, want ${want}`));
  for (const e of els.filter((e) => e.tag === "input" && e.type === "search")) check(e.style.appearance === "textfield", `${e.path} appearance`);
}

// 3. Components ---------------------------------------------------------------------------------
const STRICT = PROPS.filter((k) => !["font-family", "font-size", "font-weight", "line-height", "font-variant-ligatures",
  "text-wrap-style", "font-variant-numeric", "max-width", "height"].includes(k));
for (const lib of Object.keys(LIBRARIES)) {
  const base = await styles(page(`components-${lib}`, components, [`${lib}.css`]), "desktop");
  const withT = await styles(page(`components-${lib}-remix`, components, [`${lib}-remix.css`]), "desktop");
  base.els.forEach((e, i) => {
    const o = withT.els[i];
    for (const k of STRICT) {
      if (e.style[k] !== o.style[k]) fail(`components, ${lib}: ${e.path} ${k} is ${e.style[k]}, ${o.style[k]} with Remix`);
    }
    // Size, weight and line height are kept wherever the element's own styles set them. Line height is
    // compared as a ratio to the size, since a size inherited from Remix scales it.
    const ratio = (s) => s["line-height"] === "normal" ? "normal" : (px(s["line-height"]) / px(s["font-size"])).toFixed(3);
    for (const k of ["font-size", "font-weight"]) {
      if (e.classed && e.style[k] !== e.parent[k] && e.style[k] !== o.style[k]) {
        fail(`components, ${lib}: ${e.path} ${k} is ${e.style[k]}, ${o.style[k]} with Remix`);
      }
    }
    if (e.classed && ratio(e.style) !== ratio(e.parent) && ratio(e.style) !== ratio(o.style)) {
      fail(`components, ${lib}: ${e.path} line height is ${ratio(e.style)} × size, ${ratio(o.style)} with Remix`);
    }
  });
}

await browser.close();
const unique = [...new Set(failures)];
console.log(unique.length ? unique.join("\n") : "Remix: parity, rules and components pass");
console.log(`${Object.keys(MODES).length} modes, ${rendered.desktop.els.length} elements, ${Object.keys(LIBRARIES).length} component sets`);
process.exit(unique.length ? 1 : 0);
