// Checks the CSS reset of Twilight Theme (css/) in Chromium. Three checks:
//
// 1. Parity. pages/document.html styled by css/twilight.css and by Tailwind CSS 4 with
//    css/twilight-tailwind.css has the same computed style on every element: on a desktop screen,
//    on a narrow desktop window, on a handheld screen (coarse pointer) and in print.
// 2. Rules. In the same page, the computed sizes, weights, line heights and spacing are the values
//    of typography/twilight.json for each geometry.
// 3. Components. pages/components.html, with daisyUI, Flowbite and utility-class components (the way
//    shadcn/ui and Nuxt UI write them), keeps every style its classes set when Twilight's file is
//    added: spacing, borders, display, colors, decoration, and the size, weight and line height of
//    any element whose own classes set them.
//
//   npm ci && npm test          CHROMIUM_PATH=/path/to/chrome uses that browser; in CI, the runner's Chrome.
import { execFileSync } from "node:child_process";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join, relative } from "node:path";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright-core";

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = join(HERE, "..", "..");
const BUILD = join(HERE, ".build");
const T = JSON.parse(readFileSync(join(ROOT, "typography", "twilight.json"), "utf8"));
const failures = [];
const fail = (msg) => failures.push(msg);
mkdirSync(BUILD, { recursive: true });

// Stylesheets ----------------------------------------------------------------------------------
const twilight = relative(BUILD, join(ROOT, "css", "twilight-tailwind.css"));
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
  compile(`${lib}-twilight`, [...head, ...imports, `@import "${twilight}";`, ...plugins]);
}

function page(name, body, sheets) {
  const links = sheets.map((s) => `<link rel="stylesheet" href="${s}">`).join("");
  const file = join(BUILD, `${name}.html`);
  writeFileSync(file, `<!doctype html><html lang="en"><head><meta charset="utf-8">` +
    `<meta name="viewport" content="width=device-width, initial-scale=1">${links}</head><body>${body}</body></html>`);
  return "file://" + file;
}
const doc = readFileSync(join(HERE, "pages", "document.html"), "utf8");
const components = readFileSync(join(HERE, "pages", "components.html"), "utf8");
const vanillaDoc = page("document-vanilla", doc, [relative(BUILD, join(ROOT, "css", "twilight.css"))]);
const minDoc = page("document-min", doc, [relative(BUILD, join(ROOT, "css", "twilight.min.css"))]);
const tailwindDoc = page("document-tailwind", doc, ["tailwind-twilight.css"]);

// Browser --------------------------------------------------------------------------------------
const browser = await chromium.launch(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH }
  : { channel: "chrome" });
const MODES = {
  desktop: { context: { viewport: { width: 1280, height: 900 } }, geometry: "desktop" },
  "narrow desktop": { context: { viewport: { width: 320, height: 900 } }, geometry: "desktop" },
  handheld: { context: { viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 },
    geometry: "handheld" },
  print: { context: { viewport: { width: 1280, height: 900 } }, media: "print", geometry: "documents" },
};
const PROPS = ["display", "position", "font-family", "font-size", "font-weight", "font-style", "line-height",
  "letter-spacing", "word-spacing", "text-transform", "text-align", "text-decoration-line", "text-wrap-style",
  "font-variant-numeric", "font-variant-ligatures", "list-style-type", "max-width", "margin-top", "margin-right",
  "margin-bottom", "margin-left", "padding-top", "padding-right", "padding-bottom", "padding-left", "border-top-width",
  "border-right-width", "border-bottom-width", "border-left-width", "border-top-style", "border-left-style",
  "border-bottom-style", "border-top-left-radius", "gap", "color", "background-color", "opacity", "box-sizing",
  "vertical-align"];

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
      inDocument: !!e.closest(".document"), directInDocument: e.parentElement.classList.contains("document"),
      prevTag: e.previousElementSibling ? e.previousElementSibling.tagName.toLowerCase() : null,
      firstP: e.parentElement.classList.contains("document") && e.tagName === "P" && e === e.parentElement.querySelector(":scope > p") };
  }), PROPS);
  const rootSize = await p.evaluate(() => parseFloat(getComputedStyle(document.documentElement).fontSize));
  const width = await p.evaluate(() => document.documentElement.clientWidth);
  await ctx.close();
  return { els: out, rootSize, width };
}

// 1. Parity -------------------------------------------------------------------------------------
const rendered = {};
for (const mode of Object.keys(MODES)) {
  const [v, m, t] = [await styles(vanillaDoc, mode), await styles(minDoc, mode), await styles(tailwindDoc, mode)];
  rendered[mode] = v;
  for (const [label, other] of [["twilight.min.css", m], ["Tailwind CSS with twilight-tailwind.css", t]]) {
    v.els.forEach((e, i) => {
      for (const k of PROPS) {
        if (e.style[k] !== other.els[i].style[k]) fail(`parity, ${mode}: ${e.path} ${k} is ${e.style[k]} with twilight.css, ${other.els[i].style[k]} with ${label}`);
      }
    });
  }
}

// 2. Rules --------------------------------------------------------------------------------------
const close = (a, b) => Math.abs(a - b) < 0.02;
const px = (v) => parseFloat(v);
for (const [mode, { els, rootSize, width }] of Object.entries(rendered)) {
  const G = T.geometries[MODES[mode].geometry];
  const unit = G.unit === "pt" ? 4 / 3 : rootSize / 16;           // CSS px per unit of the geometry
  const step = (k) => G.steps[String(k)] * unit;
  const fit = (width - 2 * T.fit.gutter) / T.fit.em;
  const lines = T["line height"];
  const check = (cond, msg) => cond || fail(`rules, ${mode}: ${msg}`);
  const body = els.find((e) => e.tag === "main").parent;
  check(close(px(body["font-size"]), step(0)), `body is ${body["font-size"]}, step 0 is ${step(0)}px`);
  check(body["font-family"].startsWith(`"${T.families.text}"`), `body font is ${body["font-family"]}`);
  check(body["letter-spacing"] === "normal" || body["letter-spacing"] === "0px", `letter spacing ${body["letter-spacing"]}`);
  for (let i = 1; i <= 6; i++) {
    const L = T.levels[`heading-${i}`];
    for (const h of els.filter((e) => e.tag === `h${i}`)) {
      const want = Math.min(step(L.step), Math.max(...["desktop", "handheld"].map((g) => T.geometries[g].steps[String(L.step)])) > (320 - 2 * T.fit.gutter) / T.fit.em ? fit : Infinity);
      check(close(px(h.style["font-size"]), want), `${h.path} is ${h.style["font-size"]}, Heading ${i} is ${want}px`);
      check(h.style["font-weight"] === String(L.weight), `${h.path} weight ${h.style["font-weight"]}`);
      check(close(px(h.style["line-height"]), px(h.style["font-size"]) * L["line height"]), `${h.path} line height ${h.style["line-height"]}`);
    }
  }
  for (const e of els.filter((e) => e.tag === "p" && !e.firstP)) {
    check(close(px(e.style["line-height"]), px(e.style["font-size"]) * lines.running), `${e.path} line height ${e.style["line-height"]}`);
  }
  for (const e of els.filter((e) => ["code", "kbd"].includes(e.tag) && e.parentTag !== "pre")) {
    check(e.style["font-size"] === e.parent["font-size"], `${e.path} is ${e.style["font-size"]} in text of ${e.parent["font-size"]}`);
    check(e.style["font-family"].startsWith(`"${T.families.literal}"`), `${e.path} font is ${e.style["font-family"]}`);
  }
  for (const e of els.filter((e) => e.tag === "small")) check(close(px(e.style["font-size"]), step(-1)), `${e.path} is ${e.style["font-size"]}`);
  for (const e of els.filter((e) => e.tag === "table")) check(e.style["font-variant-numeric"] === "tabular-nums", `${e.path} figures`);
  const space = step(0) * lines.running;
  const doc = els.find((e) => e.classed && e.path.startsWith("article.document"));
  check(close(px(doc.style["max-width"]), T.measure.em * step(0)), `measure is ${doc.style["max-width"]}`);
  for (const e of els.filter((e) => e.directInDocument && !e.firstChild)) {
    const heading = /^h[1-6]$/.test(e.tag), afterHeading = /^h[1-6]$/.test(e.prevTag || "");
    const want = space * (afterHeading ? T.spacing["after-heading"] : heading ? T.spacing["before-heading"] : T.spacing.paragraph);
    check(close(px(e.style["margin-top"]), want), `${e.path} margin ${e.style["margin-top"]}, want ${want}px`);
  }
  const lead = els.find((e) => e.firstP);
  check(close(px(lead.style["font-size"]), step(T.levels.lead.step)), `lead is ${lead.style["font-size"]}`);
  for (const e of els.filter((e) => !e.inDocument && ["p", "ul", "h2"].includes(e.tag))) {
    check(e.style["margin-top"] === "0px" && e.style["margin-bottom"] === "0px", `${e.path} outside .document has a margin`);
  }
}

// 3. Components ---------------------------------------------------------------------------------
const STRICT = PROPS.filter((k) => !["font-family", "font-size", "font-weight", "line-height", "font-variant-ligatures",
  "text-wrap-style", "font-variant-numeric", "max-width"].includes(k));
for (const lib of Object.keys(LIBRARIES)) {
  const base = await styles(page(`components-${lib}`, components, [`${lib}.css`]), "desktop");
  const withT = await styles(page(`components-${lib}-twilight`, components, [`${lib}-twilight.css`]), "desktop");
  base.els.forEach((e, i) => {
    const o = withT.els[i];
    for (const k of STRICT) {
      if (e.style[k] !== o.style[k]) fail(`components, ${lib}: ${e.path} ${k} is ${e.style[k]}, ${o.style[k]} with Twilight`);
    }
    // Size, weight and line height are kept wherever the element's own styles set them. Line height is
    // compared as a ratio to the size, since a size inherited from Twilight scales it.
    const ratio = (s) => s["line-height"] === "normal" ? "normal" : (px(s["line-height"]) / px(s["font-size"])).toFixed(3);
    for (const k of ["font-size", "font-weight"]) {
      if (e.classed && e.style[k] !== e.parent[k] && e.style[k] !== o.style[k]) {
        fail(`components, ${lib}: ${e.path} ${k} is ${e.style[k]}, ${o.style[k]} with Twilight`);
      }
    }
    if (e.classed && ratio(e.style) !== ratio(e.parent) && ratio(e.style) !== ratio(o.style)) {
      fail(`components, ${lib}: ${e.path} line height is ${ratio(e.style)} × size, ${ratio(o.style)} with Twilight`);
    }
  });
}

await browser.close();
const unique = [...new Set(failures)];
console.log(unique.length ? unique.join("\n") : "CSS reset: parity, rules and components pass");
console.log(`${Object.keys(MODES).length} modes, ${rendered.desktop.els.length} document elements, ${Object.keys(LIBRARIES).length} component sets`);
process.exit(unique.length ? 1 : 0);
