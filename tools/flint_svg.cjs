#!/usr/bin/env node
/**
 * flint_svg.cjs — Flint chart spec -> static, themed SVG (seek-safe for HyperFrames).
 *
 * Compiles a compact Flint ChartAssemblyInput into an ECharts option, applies a
 * house theme (dark by default), then renders a STATIC SVG via ECharts SSR (no
 * browser, animation off). Drop the SVG into a composition and animate the
 * *reveal* with GSAP — see styles/elements/animations/flint-chart-drawon.md.
 *
 * Usage:
 *   node tools/flint_svg.cjs <spec.json> <out.svg> [width] [height]
 *
 * Extra (non-Flint) keys honoured on the spec root:
 *   "style":   "dark" (default) | "light"   -> axis/label/grid colours for the theme
 *   "accent":  "#RRGGBB"                     -> primary series colour (default #6EA8FF)
 *   "palette": ["#..", ..]                   -> full series colour cycle
 *   "area":    true|false                    -> gradient area fill under line charts (default true)
 *
 * The data series render with the ECharts SVG class `.zrN-cls-2` (series index),
 * which the draw-on pattern targets for strokeDashoffset line-draw.
 */
const fs = require("fs");
const path = require("path");
const { assembleECharts } = require("flint-chart");
const echarts = require("echarts");

function die(m) { console.error("flint_svg: " + m); process.exit(1); }

function hexA(hex, a) {
  const h = String(hex).replace("#", "");
  const n = h.length === 3 ? h.split("").map((c) => c + c).join("") : h;
  const r = parseInt(n.slice(0, 2), 16), g = parseInt(n.slice(2, 4), 16), b = parseInt(n.slice(4, 6), 16);
  return `rgba(${r},${g},${b},${a})`;
}

const [specPath, outPath, wArg, hArg] = process.argv.slice(2);
if (!specPath || !outPath) die("usage: node tools/flint_svg.cjs <spec.json> <out.svg> [width] [height]");
if (!fs.existsSync(specPath)) die("spec not found: " + specPath);

let input;
try { input = JSON.parse(fs.readFileSync(specPath, "utf8")); }
catch (e) { die("bad JSON in " + specPath + ": " + e.message); }

const base = (input.chart_spec && input.chart_spec.baseSize) || {};
const width = parseInt(wArg || base.width || 900, 10);
const height = parseInt(hArg || base.height || 300, 10);

const style = (input.style || "dark").toLowerCase();
const dark = style !== "light";
const accent = input.accent || (dark ? "#6EA8FF" : "#2563EB");
const palette = input.palette || [accent, "#34D399", "#FBBF24", "#F472B6", "#A78BFA", "#22D3EE"];
const wantArea = input.area !== false;

const ink = dark ? "rgba(255,255,255,0.78)" : "rgba(17,17,17,0.82)";
const faint = dark ? "rgba(255,255,255,0.42)" : "rgba(17,17,17,0.5)";
const grid = dark ? "rgba(255,255,255,0.12)" : "rgba(17,17,17,0.1)";

let option;
try { option = assembleECharts(input); }
catch (e) { die("assembleECharts failed: " + e.message); }

// ---- house theme ----
option.animation = false;
option.backgroundColor = input.backgroundColor || "transparent";
option.color = palette;
option.textStyle = Object.assign({ fontFamily: "Inter, Arial, sans-serif", color: ink }, option.textStyle);
delete option.tooltip; // static render

function themeAxis(ax) {
  if (!ax) return ax;
  if (Array.isArray(ax)) return ax.map(themeAxis);
  ax.axisLine = { show: true, lineStyle: { color: faint } };
  ax.axisTick = { show: false };
  ax.axisLabel = Object.assign({ fontSize: 22, rotate: 0 }, ax.axisLabel || {}, { color: ink });
  ax.nameTextStyle = Object.assign({ fontSize: 22 }, ax.nameTextStyle || {}, { color: faint });
  ax.splitLine = { show: ax.type !== "category", lineStyle: { color: grid } };
  return ax;
}
option.xAxis = themeAxis(option.xAxis);
option.yAxis = themeAxis(option.yAxis);

(option.series || []).forEach((s, i) => {
  const col = palette[i % palette.length];
  if (s.type === "line") {
    s.smooth = s.smooth != null ? s.smooth : true;
    s.symbol = "circle"; s.symbolSize = 10; s.showSymbol = true;
    s.lineStyle = Object.assign({ cap: "round", join: "round" }, s.lineStyle, { width: 5, color: col });
    s.itemStyle = Object.assign({}, s.itemStyle, { color: col });
    if (wantArea) {
      s.areaStyle = {
        opacity: 1,
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: hexA(col, dark ? 0.42 : 0.3) },
          { offset: 1, color: hexA(col, 0.0) },
        ]),
      };
    }
  } else if (s.type === "bar") {
    s.itemStyle = Object.assign({}, s.itemStyle, { color: col, borderRadius: [10, 10, 0, 0] });
    s.barMaxWidth = s.barMaxWidth || 64;
  } else if (s.type === "pie") {
    s.itemStyle = Object.assign({}, s.itemStyle, { borderColor: dark ? "#0b1020" : "#fff", borderWidth: 4 });
    s.label = Object.assign({}, s.label, { color: ink, fontSize: 24 });
  }
});

const chart = echarts.init(null, null, { renderer: "svg", ssr: true, width, height });
chart.setOption(option);
let svg = chart.renderToSVGString();
chart.dispose();

// Tag the data line (unique stroke-width:5, fill:none) and the area path so the
// HyperFrames draw-on can target [data-flint-line] / [data-flint-area] regardless
// of ECharts' internal class numbering.
svg = svg
  .replace(/(<path\b(?=[^>]*\bfill="none")(?=[^>]*\bstroke-width="5")[^>]*?)>/, '$1 data-flint-line="1">')
  .replace(/(<path\b(?=[^>]*\bfill="url\()[^>]*?)>/, '$1 data-flint-area="1">');

fs.mkdirSync(path.dirname(path.resolve(outPath)), { recursive: true });
fs.writeFileSync(outPath, svg, "utf8");
console.log("OK wrote " + outPath + " (" + width + "x" + height + ", " + style + ", " + svg.length + " bytes)");
