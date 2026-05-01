import streamlit as st
import numpy as np
from PIL import Image
import time
import os
import gdown

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DeepScan · Deepfake Detector",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700&family=Outfit:wght@300;400;500;600;700;800;900&display=swap');

:root {
    --bg:          #06060e;
    --bg2:         #0a0a16;
    --surface:     #0f0f1e;
    --surface2:    #161628;
    --surface3:    #1d1d35;
    --border:      #232342;
    --border2:     #2d2d55;
    --cyan:        #00f5ff;
    --cyan-dim:    rgba(0,245,255,0.12);
    --cyan-glow:   rgba(0,245,255,0.04);
    --violet:      #8b5cf6;
    --violet-dim:  rgba(139,92,246,0.15);
    --pink:        #f472b6;
    --real:        #10ffb0;
    --real-dim:    rgba(16,255,176,0.12);
    --fake:        #ff4069;
    --fake-dim:    rgba(255,64,105,0.12);
    --text:        #e2e2f0;
    --text2:       #9898b8;
    --text3:       #55556a;
    --mono:        'JetBrains Mono', monospace;
    --sans:        'Outfit', sans-serif;
}

*, *::before, *::after { box-sizing: border-box; }

/* ══ NUCLEAR DARK OVERRIDE — targets every Streamlit layer ══ */
html,
body,
[class*="css"],
[data-testid],
.stApp,
.stApp > *,
.main,
.main > *,
.block-container,
section[data-testid="stSidebar"],
section[data-testid="stSidebar"] > *,
div[data-testid="stAppViewContainer"],
div[data-testid="stAppViewBlockContainer"],
div[data-testid="stVerticalBlock"],
div[data-testid="stHorizontalBlock"],
[class^="st-"],
[class*=" st-"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: var(--sans) !important;
}

/* Light-mode iframe / root resets */
:root, html { color-scheme: dark !important; }
body { background: var(--bg) !important; }

/* ── Hide Streamlit chrome ── */
#MainMenu, footer { visibility: hidden; }
.stDeployButton { display: none !important; }
header[data-testid="stHeader"] {
    background: var(--bg) !important;
    border-bottom: 1px solid var(--border) !important;
}
header[data-testid="stHeader"] * { color: var(--text2) !important; }
.block-container {
    padding: 1.5rem 2rem 3rem !important;
    max-width: 100% !important;
    background: var(--bg) !important;
}

/* ── Main content area ── */
.stApp { background: var(--bg) !important; }
.main .block-container { background: var(--bg) !important; }

/* ══════════════════════════════════════════
   SIDEBAR
══════════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: var(--bg2) !important;
    border-right: 1px solid var(--border) !important;
    min-width: 260px !important;
    max-width: 260px !important;
}
[data-testid="stSidebar"] > div {
    background: var(--bg2) !important;
}
[data-testid="stSidebar"] * {
    background-color: transparent !important;
}
[data-testid="stSidebar"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--cyan), var(--violet), transparent);
    z-index: 10;
}
[data-testid="stSidebarContent"] {
    padding: 0 !important;
    background: var(--bg2) !important;
}

.sb-logo {
    padding: 2rem 1.5rem 1.5rem;
    border-bottom: 1px solid var(--border);
}
.sb-logo-glyph {
    width: 42px; height: 42px;
    border: 1.5px solid var(--cyan);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
    margin-bottom: 0.9rem;
    position: relative;
    box-shadow: 0 0 16px rgba(0,245,255,0.2), inset 0 0 16px rgba(0,245,255,0.05);
    background: rgba(0,245,255,0.05) !important;
}
.sb-logo-name {
    font-size: 1.25rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: #fff !important;
    line-height: 1;
    margin-bottom: 0.2rem;
}
.sb-logo-version {
    font-family: var(--mono);
    font-size: 0.6rem;
    letter-spacing: 0.18em;
    color: var(--text3) !important;
    text-transform: uppercase;
}

/* ── Radio nav overrides ── */
.stRadio { background: transparent !important; }
.stRadio > div { background: transparent !important; }
.stRadio label {
    color: var(--text2) !important;
    font-family: var(--sans) !important;
    font-size: 0.87rem !important;
    font-weight: 500 !important;
    cursor: pointer !important;
    padding: 0.5rem 0.75rem !important;
    border-radius: 6px !important;
    transition: background 0.18s !important;
    display: block !important;
    background: transparent !important;
}
.stRadio label:hover {
    background: var(--surface2) !important;
    color: var(--text) !important;
}
/* selected radio item */
.stRadio [data-baseweb="radio"] input:checked + div {
    background: var(--cyan-dim) !important;
}
div[data-baseweb="radio"] {
    background: transparent !important;
}
div[data-baseweb="radio"] > div {
    background: transparent !important;
}
[data-testid="stMarkdownContainer"] {
    background: transparent !important;
}
[data-testid="stMarkdownContainer"] p {
    color: var(--text) !important;
    background: transparent !important;
}

.sb-status {
    margin: 1.5rem 0.75rem 0.75rem;
    padding: 0.85rem 1rem;
    border-radius: 7px;
    border: 1px solid var(--border);
    background: var(--surface) !important;
}
.sb-status-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-family: var(--mono);
    font-size: 0.62rem;
    letter-spacing: 0.05em;
    color: var(--text3);
    margin-bottom: 0.45rem;
}
.sb-status-row:last-child { margin-bottom: 0; }
.sb-status-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    display: inline-block;
    margin-right: 0.35rem;
}

/* ══════════════════════════════════════════
   FILE UPLOADER
══════════════════════════════════════════ */
[data-testid="stFileUploader"] {
    background: transparent !important;
}
[data-testid="stFileUploader"] > div {
    background: var(--surface) !important;
    border: 1.5px dashed var(--border2) !important;
    border-radius: 8px !important;
    padding: 1.75rem !important;
    transition: border-color 0.2s !important;
}
[data-testid="stFileUploader"] > div:hover {
    border-color: var(--cyan) !important;
}
[data-testid="stFileUploader"] label,
[data-testid="stFileUploader"] [data-testid="stMarkdownContainer"] p,
[data-testid="stFileUploader"] span,
[data-testid="stFileUploader"] small {
    color: var(--text3) !important;
    font-family: var(--mono) !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.1em !important;
}
/* The drag-and-drop zone inner */
[data-testid="stFileUploaderDropzone"] {
    background: var(--surface2) !important;
    border: 1px dashed var(--border2) !important;
    border-radius: 6px !important;
}
[data-testid="stFileUploaderDropzone"] * {
    color: var(--text3) !important;
    background: transparent !important;
}
/* Browse files button inside uploader */
[data-testid="stFileUploaderDropzone"] button,
[data-testid="stFileUploaderDropzone"] button * {
    background: var(--surface3) !important;
    color: var(--cyan) !important;
    border: 1px solid var(--border2) !important;
    border-radius: 4px !important;
}

/* ══════════════════════════════════════════
   BUTTONS
══════════════════════════════════════════ */
.stButton > button {
    background: linear-gradient(135deg, #1a0e3a 0%, #0d2a3a 100%) !important;
    color: var(--cyan) !important;
    font-family: var(--mono) !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    border: 1px solid rgba(0,245,255,0.3) !important;
    border-radius: 5px !important;
    padding: 0.7rem 2rem !important;
    font-weight: 700 !important;
    width: 100% !important;
    transition: all 0.2s !important;
    box-shadow: 0 0 18px rgba(0,245,255,0.07) !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #220f4d 0%, #103340 100%) !important;
    border-color: rgba(0,245,255,0.6) !important;
    box-shadow: 0 0 28px rgba(0,245,255,0.18) !important;
    color: #fff !important;
}
.stButton > button:disabled {
    opacity: 0.35 !important;
    cursor: not-allowed !important;
}

/* ══════════════════════════════════════════
   PROGRESS BAR
══════════════════════════════════════════ */
.stProgress {
    background: transparent !important;
}
.stProgress > div {
    background: var(--surface2) !important;
    border-radius: 4px !important;
    border: 1px solid var(--border) !important;
}
.stProgress > div > div {
    background: transparent !important;
}
.stProgress > div > div > div {
    background: transparent !important;
}
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, var(--violet), var(--cyan)) !important;
    border-radius: 4px !important;
}

/* ══════════════════════════════════════════
   SPINNER
══════════════════════════════════════════ */
.stSpinner > div {
    border-color: var(--border) !important;
    border-top-color: var(--cyan) !important;
}

/* ══════════════════════════════════════════
   IMAGES
══════════════════════════════════════════ */
div[data-testid="stImage"] {
    background: transparent !important;
}
div[data-testid="stImage"] img {
    border-radius: 8px !important;
}

/* ══════════════════════════════════════════
   ALERTS / WARNINGS
══════════════════════════════════════════ */
.stAlert {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    color: var(--text) !important;
}
.stAlert * { color: var(--text) !important; }

/* ══════════════════════════════════════════
   COLUMNS
══════════════════════════════════════════ */
[data-testid="column"] {
    background: transparent !important;
}

/* ══════════════════════════════════════════
   SCROLLBAR
══════════════════════════════════════════ */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: var(--violet); }

/* ══════════════════════════════════════════
   PAGE — ABOUT
══════════════════════════════════════════ */
.page-hero {
    position: relative;
    padding: 3rem 0 2.5rem;
    overflow: hidden;
}
.page-hero::before {
    content: '';
    position: absolute;
    top: -120px; right: -200px;
    width: 600px; height: 500px;
    background: radial-gradient(ellipse, rgba(0,245,255,0.055) 0%, transparent 65%);
    pointer-events: none;
}
.page-hero::after {
    content: '';
    position: absolute;
    bottom: -150px; left: -100px;
    width: 500px; height: 400px;
    background: radial-gradient(ellipse, rgba(139,92,246,0.04) 0%, transparent 65%);
    pointer-events: none;
}
.eyebrow {
    font-family: var(--mono);
    font-size: 0.65rem;
    letter-spacing: 0.3em;
    color: var(--cyan);
    text-transform: uppercase;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}
.eyebrow-line {
    display: inline-block;
    width: 32px; height: 1px;
    background: linear-gradient(90deg, var(--cyan), transparent);
}
.hero-title {
    font-size: clamp(2.8rem, 5vw, 4.5rem);
    font-weight: 900;
    letter-spacing: -0.04em;
    line-height: 1.0;
    margin: 0 0 1.25rem;
    background: linear-gradient(135deg, #ffffff 0%, rgba(0,245,255,0.9) 60%, var(--violet) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-desc {
    color: var(--text2);
    font-size: 1.05rem;
    font-weight: 300;
    line-height: 1.75;
    max-width: 580px;
}
.tag-row {
    display: flex;
    gap: 0.5rem;
    margin-top: 2rem;
    flex-wrap: wrap;
}
.chip {
    font-family: var(--mono);
    font-size: 0.58rem;
    letter-spacing: 0.12em;
    padding: 0.28rem 0.7rem;
    border-radius: 3px;
    border: 1px solid var(--border2);
    color: var(--text3);
    background: var(--surface) !important;
    text-transform: uppercase;
    transition: border-color 0.2s, color 0.2s;
    display: inline-block;
}
.chip:hover {
    border-color: var(--cyan);
    color: var(--cyan);
}

/* Feature cards */
.feat-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin: 2.5rem 0;
}
.feat-card {
    background: var(--surface) !important;
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.5rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.25s, transform 0.25s;
}
.feat-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--cyan), var(--violet));
    opacity: 0;
    transition: opacity 0.25s;
}
.feat-card:hover {
    border-color: var(--border2);
    transform: translateY(-2px);
}
.feat-card:hover::before { opacity: 1; }
.feat-icon {
    font-size: 1.6rem;
    margin-bottom: 1rem;
    display: block;
}
.feat-title {
    font-size: 0.95rem;
    font-weight: 700;
    color: #fff !important;
    margin-bottom: 0.4rem;
    letter-spacing: -0.01em;
}
.feat-desc {
    font-size: 0.82rem;
    color: var(--text2) !important;
    line-height: 1.6;
}

/* Architecture diagram */
.arch-section {
    background: var(--surface) !important;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 2rem;
    margin: 1.5rem 0;
}
.arch-title {
    font-family: var(--mono);
    font-size: 0.62rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--cyan);
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.arch-title::before { content: '//'; color: var(--border2); }
.arch-flow {
    display: flex;
    align-items: center;
    gap: 0;
    flex-wrap: wrap;
    justify-content: center;
}
.arch-node {
    background: var(--surface2) !important;
    border: 1px solid var(--border2);
    border-radius: 6px;
    padding: 0.65rem 1rem;
    text-align: center;
    flex-shrink: 0;
}
.arch-node-label {
    font-family: var(--mono);
    font-size: 0.6rem;
    letter-spacing: 0.1em;
    color: var(--text3) !important;
    text-transform: uppercase;
    margin-bottom: 0.2rem;
}
.arch-node-val {
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--text) !important;
}
.arch-arrow {
    color: var(--border2);
    font-size: 0.9rem;
    padding: 0 0.3rem;
    flex-shrink: 0;
}

/* Stats bar */
.stats-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin: 2rem 0;
}
.stat-card {
    background: var(--surface) !important;
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.25rem 1.5rem;
    text-align: center;
}
.stat-num {
    font-size: 2rem;
    font-weight: 900;
    letter-spacing: -0.04em;
    background: linear-gradient(135deg, var(--cyan), var(--violet));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
}
.stat-lbl {
    font-family: var(--mono);
    font-size: 0.58rem;
    letter-spacing: 0.12em;
    color: var(--text3) !important;
    text-transform: uppercase;
    margin-top: 0.4rem;
}

/* ══════════════════════════════════════════
   PAGE — DETECTION
══════════════════════════════════════════ */
.detect-header {
    padding: 2rem 0 1.5rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2rem;
}
.detect-title {
    font-size: 1.9rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: #fff !important;
    margin-bottom: 0.3rem;
}
.detect-sub {
    font-size: 0.88rem;
    color: var(--text2) !important;
    font-weight: 300;
}

/* Upload panel */
.panel {
    background: var(--surface) !important;
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.75rem;
    height: 100%;
}
.panel-title {
    font-family: var(--mono);
    font-size: 0.6rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--cyan) !important;
    margin-bottom: 1.25rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.panel-title::before { content: '//'; color: var(--border2); font-family: var(--mono); }

/* Scan animation */
@keyframes scanline {
    0% { top: 0%; opacity: 1; }
    100% { top: 100%; opacity: 0; }
}
@keyframes glow-pulse {
    0%, 100% { box-shadow: 0 0 12px rgba(0,245,255,0.2); }
    50% { box-shadow: 0 0 28px rgba(0,245,255,0.45), 0 0 50px rgba(0,245,255,0.15); }
}

.img-frame {
    position: relative;
    border-radius: 8px;
    overflow: hidden;
    border: 1px solid var(--border);
    animation: glow-pulse 2.5s ease-in-out infinite;
    background: transparent !important;
}
.scanline-overlay {
    position: absolute;
    left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, transparent 0%, var(--cyan) 40%, rgba(0,245,255,0.6) 50%, var(--cyan) 60%, transparent 100%);
    animation: scanline 1.8s ease-in-out infinite;
    z-index: 10;
    filter: blur(1px);
    box-shadow: 0 0 12px var(--cyan);
}
.img-corner {
    position: absolute;
    width: 14px; height: 14px;
    border-color: var(--cyan);
    border-style: solid;
    opacity: 0.8;
}
.img-corner.tl { top: 6px; left: 6px; border-width: 2px 0 0 2px; }
.img-corner.tr { top: 6px; right: 6px; border-width: 2px 2px 0 0; }
.img-corner.bl { bottom: 6px; left: 6px; border-width: 0 0 2px 2px; }
.img-corner.br { bottom: 6px; right: 6px; border-width: 0 2px 2px 0; }

/* Result display */
.verdict-box-real {
    background: var(--real-dim) !important;
    border: 1px solid rgba(16,255,176,0.3);
    border-radius: 10px;
    padding: 2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.verdict-box-real::before {
    content: '';
    position: absolute;
    top: -60px; left: 50%;
    transform: translateX(-50%);
    width: 200px; height: 120px;
    background: radial-gradient(ellipse, rgba(16,255,176,0.15), transparent);
}
.verdict-box-fake {
    background: var(--fake-dim) !important;
    border: 1px solid rgba(255,64,105,0.3);
    border-radius: 10px;
    padding: 2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.verdict-box-fake::before {
    content: '';
    position: absolute;
    top: -60px; left: 50%;
    transform: translateX(-50%);
    width: 200px; height: 120px;
    background: radial-gradient(ellipse, rgba(255,64,105,0.15), transparent);
}
.verdict-tag {
    font-family: var(--mono);
    font-size: 0.58rem;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}
.verdict-text {
    font-size: 3rem;
    font-weight: 900;
    letter-spacing: -0.04em;
    line-height: 1;
}
.verdict-conf {
    font-family: var(--mono);
    font-size: 0.72rem;
    color: var(--text2) !important;
    margin-top: 0.5rem;
}

/* Meter */
.meter-wrap { margin: 1.25rem 0; }
.meter-labels {
    display: flex;
    justify-content: space-between;
    font-family: var(--mono);
    font-size: 0.6rem;
    letter-spacing: 0.08em;
    color: var(--text3) !important;
    margin-bottom: 0.5rem;
}
.meter-track {
    background: var(--surface2) !important;
    border-radius: 4px;
    height: 8px;
    overflow: hidden;
    border: 1px solid var(--border);
    position: relative;
}
.meter-track::after {
    content: '';
    position: absolute;
    left: 50%; top: 0; bottom: 0;
    width: 1px;
    background: var(--border2);
}
.meter-fill-real {
    height: 100%;
    background: linear-gradient(90deg, #06b669, var(--real));
    border-radius: 4px;
    box-shadow: 0 0 8px rgba(16,255,176,0.4);
    transition: width 0.9s cubic-bezier(0.4,0,0.2,1);
}
.meter-fill-fake {
    height: 100%;
    background: linear-gradient(90deg, #991133, var(--fake));
    border-radius: 4px;
    box-shadow: 0 0 8px rgba(255,64,105,0.4);
    transition: width 0.9s cubic-bezier(0.4,0,0.2,1);
}

/* Probability rows */
.prob-bar-row { margin-bottom: 0.8rem; }
.prob-bar-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.3rem;
}
.prob-bar-label {
    font-family: var(--mono);
    font-size: 0.62rem;
    letter-spacing: 0.08em;
    color: var(--text2) !important;
}
.prob-bar-pct {
    font-family: var(--mono);
    font-size: 0.65rem;
    font-weight: 700;
}
.prob-track {
    background: var(--surface2) !important;
    border-radius: 3px;
    height: 5px;
    overflow: hidden;
}
.prob-fill { height: 100%; border-radius: 3px; }

/* Info table */
.info-table { width: 100%; }
.info-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.65rem 0;
    border-bottom: 1px solid var(--border);
}
.info-row:last-child { border-bottom: none; }
.info-k {
    font-family: var(--mono);
    font-size: 0.62rem;
    letter-spacing: 0.06em;
    color: var(--text3) !important;
}
.info-v {
    font-size: 0.82rem;
    font-weight: 600;
    color: var(--text) !important;
}

/* Empty state */
.empty-state {
    background: var(--surface) !important;
    border: 1.5px dashed var(--border2);
    border-radius: 10px;
    padding: 4rem 2rem;
    text-align: center;
}
.empty-glyph {
    font-size: 3rem;
    opacity: 0.15;
    margin-bottom: 1rem;
    display: block;
}
.empty-text {
    font-family: var(--mono);
    font-size: 0.68rem;
    letter-spacing: 0.18em;
    color: var(--text3) !important;
    text-transform: uppercase;
}
</style>
""", unsafe_allow_html=True)


# ─── Model loader ──────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    model_paths = [
        'deepfake_mobilenet_model.h5',
        'deepfake_mobilenet_updated.h5',
    ]
    model_urls = [
        "https://drive.google.com/uc?id=1wcCdLdQXjqlovtvkBDsznMVZi9_Sxcjs",
        "https://drive.google.com/uc?id=1fRln-iCgZm_KPtot3xy7eshvfTw5DN37",
    ]

    import tensorflow as tf
    import h5py, json

    for p, url in zip(model_paths, model_urls):
        # Remove corrupted files (< 1MB)
        if os.path.exists(p) and os.path.getsize(p) < 1_000_000:
            os.remove(p)

        if not os.path.exists(p):
            try:
                with st.spinner(f"Downloading {p}..."):
                    gdown.download(url, p, quiet=False, fuzzy=True)
            except Exception as e:
                st.warning(f"Download failed for {p}: {e}")
                continue

        if not os.path.exists(p):
            continue

        # ── Attempt 1: standard load ──────────────────────────────
        try:
            model = tf.keras.models.load_model(p, compile=False)
            return model, p
        except Exception as e1:
            pass

        # ── Attempt 2: patch batch_shape in the h5 config ─────────
        try:
            with h5py.File(p, 'r+') as f:
                if 'model_config' in f.attrs:
                    cfg = f.attrs['model_config']
                    if isinstance(cfg, bytes):
                        cfg = cfg.decode('utf-8')
                    cfg = cfg.replace('"batch_shape"', '"shape"') \
                             .replace("'batch_shape'", "'shape'")
                    f.attrs['model_config'] = cfg.encode('utf-8')

            model = tf.keras.models.load_model(p, compile=False)
            return model, p
        except Exception as e2:
            st.warning(f"Could not load {p}: {e2}")

    return None, None

def preprocess_image(img: Image.Image, size=(128, 128)) -> np.ndarray:
    img = img.convert("RGB").resize(size, Image.LANCZOS)
    arr = np.array(img, dtype=np.float32) / 255.0
    return np.expand_dims(arr, axis=0)


def run_prediction(model, img_array):
    score = float(model.predict(img_array, verbose=0)[0][0])
    is_real = score > 0.5
    confidence = score if is_real else 1.0 - score
    return is_real, confidence, score


# ─── Load model ───────────────────────────────────────────────────────────────
model, model_path = load_model()
model_loaded = model is not None


# ══════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════
with st.sidebar:

    st.markdown("""
    <div class="sb-logo">
        <div class="sb-logo-glyph">🔬</div>
        <div class="sb-logo-name">DeepScan</div>
        <div class="sb-logo-version">v2.1 · MobileNetV2</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="padding:1rem 0.75rem 0.4rem;font-family:'JetBrains Mono',monospace;
                font-size:0.55rem;letter-spacing:0.25em;color:#55556a;text-transform:uppercase">
        Navigation
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        label="nav",
        options=["🏠  About the Project", "🔍  Detection"],
        label_visibility="collapsed",
        key="nav_radio"
    )

    status_color  = "#10ffb0" if model_loaded else "#ff4069"
    status_text   = "ONLINE"  if model_loaded else "OFFLINE"
    status_dot_bg = status_color

    st.markdown(f"""
    <div class="sb-status">
        <div class="sb-status-row">
            <span>Model Engine</span>
            <span style="color:{status_color}">
                <span class="sb-status-dot" style="background:{status_dot_bg};
                      box-shadow:0 0 6px {status_dot_bg}"></span>{status_text}
            </span>
        </div>
        <div class="sb-status-row">
            <span>Architecture</span>
            <span style="color:#9898b8">MobileNetV2</span>
        </div>
        <div class="sb-status-row">
            <span>Input Shape</span>
            <span style="color:#9898b8">128×128×3</span>
        </div>
        <div class="sb-status-row">
            <span>Mode</span>
            <span style="color:{'#9898b8' if model_loaded else '#ff4069'}">
                {'Inference' if model_loaded else 'Demo'}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="padding:0 0.75rem 1.5rem;font-family:'JetBrains Mono',monospace;
                font-size:0.55rem;letter-spacing:0.08em;color:#2d2d55;line-height:1.7;
                text-align:center">
        FOR RESEARCH &amp; EDUCATIONAL USE ONLY<br>
        © 2024 DEEPSCAN PROJECT
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  PAGE: ABOUT
# ══════════════════════════════════════════════════════════════
if page == "🏠  About the Project":

    st.markdown("""
    <div class="page-hero">
        <div class="eyebrow">
            <span class="eyebrow-line"></span>
            Neural Deepfake Detection System
        </div>
        <div class="hero-title">DeepScan</div>
        <div class="hero-desc">
            A state-of-the-art deepfake detection system powered by transfer-learned
            MobileNetV2. Upload any face image and receive an instantaneous authenticity
            verdict with confidence scoring.
        </div>
        <div class="tag-row">
            <span class="chip">MobileNetV2</span>
            <span class="chip">Transfer Learning</span>
            <span class="chip">Fine-tuned</span>
            <span class="chip">128×128 px</span>
            <span class="chip">Binary CE Loss</span>
            <span class="chip">ImageNet Weights</span>
            <span class="chip">Real-time</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="stats-row">
        <div class="stat-card">
            <div class="stat-num">~93%</div>
            <div class="stat-lbl">Val Accuracy</div>
        </div>
        <div class="stat-card">
            <div class="stat-num">128px</div>
            <div class="stat-lbl">Input Size</div>
        </div>
        <div class="stat-card">
            <div class="stat-num">13</div>
            <div class="stat-lbl">Total Epochs</div>
        </div>
        <div class="stat-card">
            <div class="stat-num">&lt;50ms</div>
            <div class="stat-lbl">Inference Time</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="feat-grid">
        <div class="feat-card">
            <span class="feat-icon">⚡</span>
            <div class="feat-title">Lightning Fast</div>
            <div class="feat-desc">Sub-50ms inference using optimised MobileNetV2. Engineered for real-time deepfake screening at scale.</div>
        </div>
        <div class="feat-card">
            <span class="feat-icon">🧠</span>
            <div class="feat-title">Transfer Learning</div>
            <div class="feat-desc">ImageNet-pretrained backbone fine-tuned on curated real/fake face datasets for superior generalisation.</div>
        </div>
        <div class="feat-card">
            <span class="feat-icon">📊</span>
            <div class="feat-title">Confidence Scoring</div>
            <div class="feat-desc">Outputs a continuous authenticity score alongside a binary verdict, giving nuanced probability insight.</div>
        </div>
        <div class="feat-card">
            <span class="feat-icon">🔁</span>
            <div class="feat-title">Augmentation</div>
            <div class="feat-desc">Trained with rotation, zoom, and horizontal flip augmentation to improve robustness against varied inputs.</div>
        </div>
        <div class="feat-card">
            <span class="feat-icon">🛡️</span>
            <div class="feat-title">Robust Architecture</div>
            <div class="feat-desc">GAP → BatchNorm → Dense(64) → Sigmoid head with 0.3 dropout for regularisation and stability.</div>
        </div>
        <div class="feat-card">
            <span class="feat-icon">🎯</span>
            <div class="feat-title">Fine-tuned Layers</div>
            <div class="feat-desc">Last 20 layers of MobileNetV2 fine-tuned at a reduced 1e-5 learning rate for precision feature adaptation.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="arch-section">
        <div class="arch-title">Model Architecture Pipeline</div>
        <div class="arch-flow">
            <div class="arch-node">
                <div class="arch-node-label">Input</div>
                <div class="arch-node-val">128×128×3</div>
            </div>
            <div class="arch-arrow">→</div>
            <div class="arch-node">
                <div class="arch-node-label">Backbone</div>
                <div class="arch-node-val">MobileNetV2</div>
            </div>
            <div class="arch-arrow">→</div>
            <div class="arch-node">
                <div class="arch-node-label">Pooling</div>
                <div class="arch-node-val">Global Avg</div>
            </div>
            <div class="arch-arrow">→</div>
            <div class="arch-node">
                <div class="arch-node-label">Norm</div>
                <div class="arch-node-val">BatchNorm</div>
            </div>
            <div class="arch-arrow">→</div>
            <div class="arch-node">
                <div class="arch-node-label">Dense</div>
                <div class="arch-node-val">64 + Drop(0.3)</div>
            </div>
            <div class="arch-arrow">→</div>
            <div class="arch-node">
                <div class="arch-node-label">Output</div>
                <div class="arch-node-val">Sigmoid (1)</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        st.markdown("""
        <div class="panel">
            <div class="panel-title">Training Configuration</div>
            <div class="info-table">
                <div class="info-row"><span class="info-k">Phase 1 Epochs</span><span class="info-v">10</span></div>
                <div class="info-row"><span class="info-k">Phase 2 (Fine-tune)</span><span class="info-v">3</span></div>
                <div class="info-row"><span class="info-k">Batch Size</span><span class="info-v">8</span></div>
                <div class="info-row"><span class="info-k">Steps / Epoch</span><span class="info-v">300</span></div>
                <div class="info-row"><span class="info-k">Val Steps</span><span class="info-v">100</span></div>
                <div class="info-row"><span class="info-k">Val Split</span><span class="info-v">15%</span></div>
                <div class="info-row"><span class="info-k">Loss</span><span class="info-v">Binary Cross-Entropy</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="panel">
            <div class="panel-title">Optimiser & Regularisation</div>
            <div class="info-table">
                <div class="info-row"><span class="info-k">Optimiser</span><span class="info-v">Adam</span></div>
                <div class="info-row"><span class="info-k">LR Phase 1</span><span class="info-v">1e-4</span></div>
                <div class="info-row"><span class="info-k">LR Phase 2</span><span class="info-v">1e-5</span></div>
                <div class="info-row"><span class="info-k">Dropout</span><span class="info-v">0.3</span></div>
                <div class="info-row"><span class="info-k">Fine-tune Layers</span><span class="info-v">Last 20</span></div>
                <div class="info-row"><span class="info-k">Augmentation</span><span class="info-v">Rot · Zoom · Flip</span></div>
                <div class="info-row"><span class="info-k">Pretrained On</span><span class="info-v">ImageNet</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  PAGE: DETECTION
# ══════════════════════════════════════════════════════════════
elif page == "🔍  Detection":

    st.markdown("""
    <div class="detect-header">
        <div class="detect-title">Deepfake Detection</div>
        <div class="detect-sub">Upload a face image — the neural network will classify it in milliseconds.</div>
    </div>
    """, unsafe_allow_html=True)

    if not model_loaded:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#1a0d10,#100d1a);border:1px solid #3a1530;
                    border-radius:8px;padding:1rem 1.25rem;margin-bottom:1.5rem;display:flex;
                    align-items:center;gap:1rem">
            <span style="font-size:1.2rem">⚠️</span>
            <div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:0.6rem;
                            letter-spacing:0.2em;color:#ff4069;text-transform:uppercase;
                            margin-bottom:0.2rem">Model Not Found — Demo Mode Active</div>
                <div style="font-size:0.8rem;color:#7a5565">
                    Place <code style="color:#ff8caa;background:#1a0d10;padding:0.1em 0.3em;
                    border-radius:3px">deepfake_mobilenet_model.h5</code> in the working 
                    directory and relaunch for real inference. Results below are simulated.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.warning("Demo Mode: Model inference is simulated.")

    col_upload, col_result, col_specs = st.columns([1, 1.2, 0.9], gap="large")

    if "result" not in st.session_state:
        st.session_state.result = None
    if "last_file" not in st.session_state:
        st.session_state.last_file = None

    # ── LEFT: Upload ──
    with col_upload:
        st.markdown('<div class="panel-title">Upload Image</div>', unsafe_allow_html=True)

        uploaded = st.file_uploader(
            label="Drop a face image",
            type=["jpg", "jpeg", "png", "webp"],
            label_visibility="collapsed",
            key="file_uploader"
        )

        if uploaded and uploaded.name != st.session_state.last_file:
            st.session_state.result = None
            st.session_state.last_file = uploaded.name

        st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)

        if uploaded:
            img = Image.open(uploaded)
            scanning = st.session_state.result is None

            if scanning:
                st.markdown('<div class="img-frame"><div class="scanline-overlay"></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="img-frame">', unsafe_allow_html=True)

            st.image(img, use_container_width=True)

            st.markdown("""
                <div class="img-corner tl"></div>
                <div class="img-corner tr"></div>
                <div class="img-corner bl"></div>
                <div class="img-corner br"></div>
            </div>""", unsafe_allow_html=True)

            w, h = img.size
            size_kb = uploaded.size / 1024
            st.markdown(f"""
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.6rem;margin-top:1rem">
                <div style="background:var(--surface2);border:1px solid var(--border);
                            border-radius:6px;padding:0.75rem 1rem">
                    <div style="font-family:'JetBrains Mono',monospace;font-size:0.55rem;
                                letter-spacing:0.12em;color:var(--text3);text-transform:uppercase;
                                margin-bottom:0.3rem">Resolution</div>
                    <div style="font-size:0.9rem;font-weight:700;color:var(--text)">{w}×{h}</div>
                </div>
                <div style="background:var(--surface2);border:1px solid var(--border);
                            border-radius:6px;padding:0.75rem 1rem">
                    <div style="font-family:'JetBrains Mono',monospace;font-size:0.55rem;
                                letter-spacing:0.12em;color:var(--text3);text-transform:uppercase;
                                margin-bottom:0.3rem">File Size</div>
                    <div style="font-size:0.9rem;font-weight:700;color:var(--text)">{size_kb:.1f} KB</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="empty-state">
                <span class="empty-glyph">◈</span>
                <div class="empty-text">No Image Loaded</div>
                <div style="font-size:0.75rem;color:var(--text3);margin-top:0.5rem;font-weight:300">
                    JPG · PNG · WEBP supported
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        run_btn = st.button(
            "⬡  Run DeepScan Analysis",
            disabled=(uploaded is None),
            key="run_btn"
        )

    # ── MIDDLE: Result ──
    with col_result:
        st.markdown('<div class="panel-title">Analysis Result</div>', unsafe_allow_html=True)

        if run_btn and uploaded:
            img_to_analyse = Image.open(uploaded)
            arr = preprocess_image(img_to_analyse)

            with st.spinner(""):
                prog = st.progress(0)
                steps = list(range(0, 86, 14)) + list(range(86, 101, 5))
                for i in steps:
                    time.sleep(0.06)
                    prog.progress(i)

                if model_loaded:
                    is_real, confidence, raw_score = run_prediction(model, arr)
                else:
                    mean_val = float(np.mean(arr))
                    is_real = mean_val > 0.45
                    confidence = min(0.72 + abs(mean_val - 0.5) * 0.6, 0.97)
                    raw_score = confidence if is_real else 1.0 - confidence

                prog.progress(100)

            prog.empty()
            st.session_state.result = {
                "is_real": is_real,
                "confidence": confidence,
                "raw_score": raw_score,
            }

        if st.session_state.result:
            r = st.session_state.result
            is_real    = r["is_real"]
            confidence = r["confidence"]
            raw_score  = r["raw_score"]

            verdict      = "AUTHENTIC" if is_real else "DEEPFAKE"
            vbox_cls     = "verdict-box-real" if is_real else "verdict-box-fake"
            verdict_clr  = "#10ffb0" if is_real else "#ff4069"
            fill_cls     = "meter-fill-real" if is_real else "meter-fill-fake"
            icon         = "✦" if is_real else "⚠"
            pct          = int(confidence * 100)

            st.markdown(f"""
            <div class="{vbox_cls}" style="margin-bottom:1.5rem">
                <div class="verdict-tag" style="color:{verdict_clr}">{icon} Verdict</div>
                <div class="verdict-text" style="color:{verdict_clr}">{verdict}</div>
                <div class="verdict-conf">Confidence · {pct}%</div>
            </div>
            """, unsafe_allow_html=True)

            raw_pct = int(raw_score * 100)
            st.markdown(f"""
            <div class="meter-wrap">
                <div class="meter-labels">
                    <span>◀ FAKE (0.0)</span>
                    <span style="font-family:'JetBrains Mono',monospace;font-size:0.6rem;
                                 color:var(--cyan)">Score: {raw_score:.4f}</span>
                    <span>REAL (1.0) ▶</span>
                </div>
                <div class="meter-track">
                    <div class="{fill_cls}" style="width:{raw_pct}%"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            real_pct = raw_pct
            fake_pct = 100 - real_pct

            st.markdown("""
            <div style="margin-top:1.5rem;margin-bottom:0.6rem;font-family:'JetBrains Mono',
                         monospace;font-size:0.58rem;letter-spacing:0.18em;
                         text-transform:uppercase;color:var(--text3)">
                Class Probabilities
            </div>
            """, unsafe_allow_html=True)

            for lbl, val, clr in [("REAL", real_pct, "#10ffb0"), ("FAKE", fake_pct, "#ff4069")]:
                st.markdown(f"""
                <div class="prob-bar-row">
                    <div class="prob-bar-header">
                        <span class="prob-bar-label">{lbl}</span>
                        <span class="prob-bar-pct" style="color:{clr}">{val}%</span>
                    </div>
                    <div class="prob-track">
                        <div class="prob-fill" style="width:{val}%;background:{clr};
                             box-shadow:0 0 6px {clr}44"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            risk     = "Low" if (is_real and confidence > 0.8) else ("High" if (not is_real and confidence > 0.8) else "Medium")
            risk_clr = "#10ffb0" if risk == "Low" else ("#ff4069" if risk == "High" else "#f59e0b")
            st.markdown(f"""
            <div style="margin-top:1.5rem;background:var(--surface2);border:1px solid var(--border);
                        border-radius:7px;padding:1rem 1.25rem;display:flex;
                        justify-content:space-between;align-items:center">
                <div>
                    <div style="font-family:'JetBrains Mono',monospace;font-size:0.58rem;
                                letter-spacing:0.12em;color:var(--text3);
                                text-transform:uppercase;margin-bottom:0.2rem">Risk Level</div>
                    <div style="font-size:1.1rem;font-weight:700;color:{risk_clr}">{risk}</div>
                </div>
                <div>
                    <div style="font-family:'JetBrains Mono',monospace;font-size:0.58rem;
                                letter-spacing:0.12em;color:var(--text3);
                                text-transform:uppercase;margin-bottom:0.2rem">Raw Score</div>
                    <div style="font-size:1.1rem;font-weight:700;color:var(--text)">{raw_score:.6f}</div>
                </div>
                <div>
                    <div style="font-family:'JetBrains Mono',monospace;font-size:0.58rem;
                                letter-spacing:0.12em;color:var(--text3);
                                text-transform:uppercase;margin-bottom:0.2rem">Threshold</div>
                    <div style="font-size:1.1rem;font-weight:700;color:var(--text)">0.5000</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        else:
            st.markdown("""
            <div class="empty-state" style="min-height:340px;display:flex;flex-direction:column;
                         align-items:center;justify-content:center">
                <span class="empty-glyph">◈</span>
                <div class="empty-text">Awaiting Analysis</div>
                <div style="font-size:0.78rem;color:var(--text3);margin-top:0.5rem;font-weight:300">
                    Upload an image and press Run
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── RIGHT: Model Specs ──
    with col_specs:
        st.markdown('<div class="panel-title">Model Specs</div>', unsafe_allow_html=True)

        model_name   = os.path.basename(model_path) if model_path else "Not Found"
        status_color = "#10ffb0" if model_loaded else "#ff4069"
        status_text  = "LOADED"  if model_loaded else "NOT FOUND"

        st.markdown(f"""
        <div style="background:var(--surface);border:1px solid var(--border);
                    border-radius:10px;padding:1.5rem;margin-bottom:1rem">
            <div class="info-table">
                <div class="info-row"><span class="info-k">Architecture</span><span class="info-v">MobileNetV2</span></div>
                <div class="info-row"><span class="info-k">Input Shape</span><span class="info-v">128×128×3</span></div>
                <div class="info-row"><span class="info-k">Head</span><span class="info-v" style="font-size:0.75rem">GAP→BN→Dense64→Sigmoid</span></div>
                <div class="info-row"><span class="info-k">Fine-tune Layers</span><span class="info-v">Last 20</span></div>
                <div class="info-row"><span class="info-k">Loss</span><span class="info-v">Binary CE</span></div>
                <div class="info-row"><span class="info-k">Optimiser</span><span class="info-v">Adam</span></div>
                <div class="info-row"><span class="info-k">Weights</span><span class="info-v">ImageNet→FT</span></div>
                <div class="info-row">
                    <span class="info-k">Status</span>
                    <span class="info-v" style="color:{status_color};font-family:'JetBrains Mono',monospace;
                          font-size:0.68rem;letter-spacing:0.1em">{status_text}</span>
                </div>
                <div class="info-row">
                    <span class="info-k">Model File</span>
                    <span class="info-v" style="font-family:'JetBrains Mono',monospace;
                          font-size:0.65rem;color:var(--text2)">{model_name}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="panel-title" style="margin-top:1.25rem">How To Use</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="background:var(--surface);border:1px solid var(--border);
                    border-radius:10px;padding:1.5rem">
            <div style="display:flex;flex-direction:column;gap:0.9rem">
                <div style="display:flex;align-items:flex-start;gap:0.75rem">
                    <span style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;
                                 color:var(--cyan);flex-shrink:0;margin-top:0.1rem">01</span>
                    <span style="font-size:0.82rem;color:var(--text2);line-height:1.5">
                        Upload a face image (JPG, PNG, or WEBP)
                    </span>
                </div>
                <div style="display:flex;align-items:flex-start;gap:0.75rem">
                    <span style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;
                                 color:var(--cyan);flex-shrink:0;margin-top:0.1rem">02</span>
                    <span style="font-size:0.82rem;color:var(--text2);line-height:1.5">
                        Click <strong style="color:var(--text)">Run DeepScan Analysis</strong>
                    </span>
                </div>
                <div style="display:flex;align-items:flex-start;gap:0.75rem">
                    <span style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;
                                 color:var(--cyan);flex-shrink:0;margin-top:0.1rem">03</span>
                    <span style="font-size:0.82rem;color:var(--text2);line-height:1.5">
                        Review the verdict and confidence score
                    </span>
                </div>
                <div style="height:1px;background:var(--border);margin:0.2rem 0"></div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:0.62rem;
                             color:var(--text3);line-height:1.7">
                    Score &gt; 0.5 → REAL<br>
                    Score ≤ 0.5 → FAKE<br>
                    Higher % = more confident
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)