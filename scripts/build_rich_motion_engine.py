import json

with open("video-engine/aligned_captions.json", "r", encoding="utf-8") as f:
    aligned_data = json.load(f)

with open("script.json", "r", encoding="utf-8") as f:
    script_data = json.load(f)

aligned_json_str = json.dumps(aligned_data)
script_json_str = json.dumps(script_data)

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Windows 11 Delivery Optimization - Rich Motion Video Engine</title>
  <style>
    :root {
      --bg: #f8f4ee;
      --text: #0d0d0d;
      --accent: #1a6cf0;
      --grey-light: #f0ede6;
      --grey-mid: #6b7280;
      --grey-border: #d1d5db;
      --red: #e53935;
      --green: #10b981;
    }
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-font-smoothing: antialiased;
    }
    body {
      background: #222;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      font-family: 'Segoe UI Variable Display', 'Segoe UI', Inter, system-ui, sans-serif;
      overflow: hidden;
    }
    #stage {
      position: relative;
      width: 1080px;
      height: 1920px;
      background: var(--bg);
      color: var(--text);
      overflow: hidden;
    }

    /* TOP BAR & PROGRESS */
    #topArea {
      position: absolute;
      top: 60px;
      left: 60px;
      width: 960px;
      display: flex;
      flex-direction: column;
      align-items: center;
      z-index: 20;
    }
    #progressBar {
      width: 100%;
      height: 8px;
      display: flex;
      gap: 3px;
      margin-bottom: 24px;
    }
    .prog-seg {
      flex: 1;
      height: 100%;
      background: rgba(13, 13, 13, 0.12);
      border-radius: 4px;
      overflow: hidden;
    }
    .prog-fill {
      height: 100%;
      width: 0%;
      background: var(--accent);
      border-radius: 4px;
    }
    #pillTag {
      background: #0d0d0d;
      color: #ffffff;
      font-size: 20px;
      font-weight: 800;
      letter-spacing: 2px;
      padding: 6px 20px;
      border-radius: 20px;
      text-transform: uppercase;
      margin-bottom: 16px;
    }
    #stepLabel {
      color: var(--accent);
      font-size: 24px;
      font-weight: 800;
      letter-spacing: 3px;
      text-transform: uppercase;
      margin-bottom: 8px;
      height: 32px;
    }
    #sceneTitle {
      font-size: 50px;
      font-weight: 900;
      text-align: center;
      line-height: 1.1;
      margin-bottom: 8px;
      height: 64px;
      color: var(--text);
      letter-spacing: -0.5px;
    }
    #breadcrumb {
      font-size: 25px;
      font-weight: 600;
      color: var(--grey-mid);
      text-align: center;
      height: 34px;
    }

    /* LAPTOP FRAME */
    #laptopContainer {
      position: absolute;
      top: 300px;
      left: 60px;
      width: 960px;
      height: 590px;
      z-index: 10;
    }
    #laptopScreenBezel {
      width: 960px;
      height: 550px;
      background: #18191c;
      border-radius: 20px 20px 4px 4px;
      padding: 14px;
      box-shadow: 0 25px 60px rgba(0, 0, 0, 0.22);
      position: relative;
    }
    #laptopWebcam {
      position: absolute;
      top: 6px;
      left: 50%;
      transform: translateX(-50%);
      width: 6px;
      height: 6px;
      background: #2d3035;
      border-radius: 50%;
    }
    #screen {
      width: 100%;
      height: 100%;
      background: #ffffff;
      border-radius: 10px;
      overflow: hidden;
      position: relative;
    }
    #laptopBase {
      width: 1040px;
      height: 24px;
      background: linear-gradient(to bottom, #d6d9de 0%, #b4b8bf 60%, #9ca0a8 100%);
      border-radius: 4px 4px 28px 28px;
      margin-left: -40px;
      margin-top: 2px;
      position: relative;
      box-shadow: 0 16px 30px rgba(0, 0, 0, 0.18);
    }
    #laptopNotch {
      position: absolute;
      top: 0;
      left: 50%;
      transform: translateX(-50%);
      width: 130px;
      height: 8px;
      background: #8b8e96;
      border-radius: 0 0 10px 10px;
    }

    /* WINDOWS 11 DESKTOP / TASKBAR */
    .win-desktop {
      position: absolute;
      inset: 0;
      background: radial-gradient(circle at 50% 120%, #dbeafe 0%, #eff6ff 45%, #f8fafc 100%);
      overflow: hidden;
      font-family: 'Segoe UI', system-ui, sans-serif;
    }
    .win-taskbar {
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      height: 48px;
      background: rgba(255, 255, 255, 0.90);
      backdrop-filter: blur(20px);
      border-top: 1px solid rgba(0, 0, 0, 0.08);
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 12px;
      z-index: 50;
    }
    .taskbar-center {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .tb-icon {
      width: 32px;
      height: 32px;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 6px;
    }
    .tb-win-logo {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 2px;
      width: 20px;
      height: 20px;
    }
    .tb-win-logo div {
      background: #0078d4;
      border-radius: 1px;
    }
    .tb-search {
      height: 30px;
      width: 140px;
      background: #f1f3f9;
      border-radius: 15px;
      display: flex;
      align-items: center;
      gap: 6px;
      padding: 0 10px;
      font-size: 13px;
      color: #64748b;
    }
    .tb-clock {
      position: absolute;
      right: 14px;
      font-size: 13px;
      color: #334155;
      font-weight: 500;
      text-align: right;
      line-height: 1.1;
    }

    /* REUSABLE WINDOW CONTAINER */
    .win-window {
      position: absolute;
      background: #ffffff;
      border-radius: 10px;
      box-shadow: 0 16px 36px rgba(0, 0, 0, 0.16), 0 0 0 1px rgba(0, 0, 0, 0.08);
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }
    .win-titlebar {
      height: 38px;
      background: #f8f9fa;
      border-bottom: 1px solid #edebe9;
      display: flex;
      align-items: center;
      padding: 0 12px;
      font-size: 13px;
      font-weight: 600;
      color: #323130;
      user-select: none;
    }
    .win-controls {
      margin-left: auto;
      display: flex;
      gap: 12px;
      font-size: 13px;
      color: #605e5c;
    }

    /* SETTINGS APP STYLING */
    .set-layout {
      display: flex;
      height: calc(100% - 38px);
    }
    .set-sidebar {
      width: 220px;
      background: #f8fafc;
      border-right: 1px solid #e2e8f0;
      padding: 16px 10px;
    }
    .set-side-nav {
      padding: 8px 12px;
      border-radius: 6px;
      font-size: 14px;
      font-weight: 600;
      color: #475569;
      margin-bottom: 4px;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .set-side-nav.active {
      background: #e2e8f0;
      color: var(--accent);
    }
    .set-content {
      flex: 1;
      padding: 20px 24px;
      overflow-y: hidden;
    }
    .set-card {
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 8px;
      padding: 14px 18px;
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .toggle-switch {
      width: 48px;
      height: 24px;
      background: #cbd5e1;
      border-radius: 12px;
      position: relative;
      transition: background 0.2s;
    }
    .toggle-switch.on {
      background: var(--accent);
    }
    .toggle-knob {
      width: 18px;
      height: 18px;
      background: #ffffff;
      border-radius: 50%;
      position: absolute;
      top: 3px;
      left: 3px;
      transition: transform 0.2s;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
    }
    .toggle-switch.on .toggle-knob {
      transform: translateX(24px);
    }

    /* CURSOR & CLICK RIPPLE */
    .win-cursor {
      position: absolute;
      pointer-events: none;
      z-index: 100;
      filter: drop-shadow(0 2px 5px rgba(0, 0, 0, 0.3));
    }
    .click-ripple {
      position: absolute;
      width: 32px;
      height: 32px;
      border: 2px solid var(--accent);
      border-radius: 50%;
      transform: translate(-50%, -50%) scale(1.4);
      pointer-events: none;
      z-index: 99;
    }

    /* CAPTIONS */
    #captions {
      position: absolute;
      top: 925px;
      left: 40px;
      width: 1000px;
      height: 155px;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-wrap: wrap;
      gap: 12px 18px;
      text-align: center;
      z-index: 30;
    }
    .caption-word {
      font-size: 64px;
      font-weight: 900;
      color: #0d0d0d;
      letter-spacing: -1px;
      line-height: 1.1;
      padding: 6px 16px;
      border-radius: 20px;
      display: inline-block;
      text-shadow: 0 2px 8px rgba(255, 255, 255, 0.9);
      transition: transform 0.08s ease;
    }
    .caption-word.word-active {
      background: #1a6cf0;
      color: #ffffff !important;
      text-shadow: 0 2px 10px rgba(26, 108, 240, 0.4) !important;
      transform: scale(1.08);
      box-shadow: 0 8px 24px rgba(26, 108, 240, 0.35);
    }

    /* CHARACTERS */
    .char-layer {
      position: absolute;
      bottom: -150px;
      left: 0;
      width: 1080px;
      height: 1920px;
      pointer-events: none;
      z-index: 15;
      will-change: transform;
    }
    #peterImg {
      position: absolute;
      left: 0;
      bottom: 0;
      width: 1080px;
      height: 1920px;
      object-fit: contain;
      transform: translateX(-1200px);
      filter: drop-shadow(0 25px 35px rgba(0, 0, 0, 0.45)) drop-shadow(0 8px 16px rgba(0, 0, 0, 0.25));
      image-rendering: -webkit-optimize-contrast;
      transform-origin: bottom center;
    }
    #stewieImg {
      position: absolute;
      left: 0;
      bottom: 0;
      width: 1080px;
      height: 1920px;
      object-fit: contain;
      transform: translateX(1200px);
      filter: drop-shadow(0 25px 35px rgba(0, 0, 0, 0.45)) drop-shadow(0 8px 16px rgba(0, 0, 0, 0.25));
      image-rendering: -webkit-optimize-contrast;
      transform-origin: bottom center;
    }
  </style>
</head>
<body>
  <div id="stage">
    <!-- TOP AREA -->
    <div id="topArea">
      <div id="progressBar"></div>
      <div id="pillTag">PC TIPS BY EZ_PETER</div>
      <div id="stepLabel"></div>
      <div id="sceneTitle">Is Windows Using Your PC?</div>
      <div id="breadcrumb">Windows 11 Background Activity</div>
    </div>

    <!-- LAPTOP FRAME -->
    <div id="laptopContainer">
      <div id="laptopScreenBezel">
        <div id="laptopWebcam"></div>
        <div id="screen"></div>
      </div>
      <div id="laptopBase">
        <div id="laptopNotch"></div>
      </div>
    </div>

    <!-- CAPTIONS -->
    <div id="captions"></div>

    <!-- CHARACTERS -->
    <div class="char-layer">
      <img id="peterImg" src="assets/peter.png" alt="Peter">
      <img id="stewieImg" src="assets/stewie.png" alt="Stewie">
    </div>
  </div>

  <script>
    // Global deterministic state
    window.hideCaptions = false;
    window.ALIGNED_CAPTIONS = __ALIGNED_CAPTIONS__;
    let ALIGNED_CAPTIONS = window.ALIGNED_CAPTIONS;
    let SCRIPT = __SCRIPT__;
    window.SCRIPT = SCRIPT;

    // Initialize progress bar segments based on script length
    const progBar = document.getElementById('progressBar');
    progBar.innerHTML = '';
    for (let i = 0; i < SCRIPT.length; i++) {
      const seg = document.createElement('div');
      seg.className = 'prog-seg';
      seg.innerHTML = '<div class="prog-fill"></div>';
      progBar.appendChild(seg);
    }

    // Helper easing functions
    function easeOutCubic(x) { return 1 - Math.pow(1 - x, 3); }
    function easeInOutQuad(x) { return x < 0.5 ? 2 * x * x : 1 - Math.pow(-2 * x + 2, 2) / 2; }
    function clamp(val, min, max) { return Math.max(min, Math.min(max, val)); }

    // Windows 11 Taskbar markup
    const winTaskbarHTML = `
      <div class="win-taskbar">
        <div class="taskbar-center">
          <div class="tb-icon">
            <div class="tb-win-logo"><div></div><div></div><div></div><div></div></div>
          </div>
          <div class="tb-search">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2.5"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
            <span>Search</span>
          </div>
          <div class="tb-icon" style="background:#e0edfe;">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="#0078d4"><path d="M4 4h7v7H4zM13 4h7v7h-7zM4 13h7v7H4zM13 13h7v7h-7z"/></svg>
          </div>
          <div class="tb-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="#d97706"><path d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>
          </div>
          <div class="tb-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="#0284c7"><circle cx="12" cy="12" r="10" stroke="#0284c7" stroke-width="2" fill="none"/></svg>
          </div>
          <div class="tb-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="#475569"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-2 2 2 2 0 01-2-2v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83 0 2 2 0 010-2.83l.06-.06a1.65 1.65 0 00.33-1.82 1.65 1.65 0 00-1.51-1H3a2 2 0 01-2-2 2 2 0 012-2h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 010-2.83 2 2 0 012.83 0l.06.06a1.65 1.65 0 001.82.33H9a1.65 1.65 0 001-1.51V3a2 2 0 012-2 2 2 0 012 2v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 0 2 2 0 010 2.83l-.06.06a1.65 1.65 0 00-.33 1.82V9a1.65 1.65 0 001.51 1H21a2 2 0 012 2 2 2 0 01-2 2h-.09a1.65 1.65 0 00-1.51 1z"/></svg>
          </div>
        </div>
        <div class="tb-clock">10:24 AM<br><span style="font-size:11px;color:#64748b;">11/22/2026</span></div>
      </div>
    `;

    // Cursor SVG markup
    function cursorHTML(x, y, click = false) {
      return `
        <div class="win-cursor" style="left:${x}px; top:${y}px; transform:${click ? 'scale(0.85)' : 'scale(1)'}; transition:transform 0.05s;">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="#000000" stroke="#ffffff" stroke-width="1.5">
            <path d="M3 3l7 18 3-7 7-3L3 3z"/>
          </svg>
        </div>
        ${click ? `<div class="click-ripple" style="left:${x}px; top:${y}px;"></div>` : ''}
      `;
    }

    // REUSABLE SCENE COMPONENT RENDERER (ALL 93 SECOND-BY-SECOND SCENES)
    function renderScreenScene(graphic, tau, t) {
      const eTau = easeOutCubic(tau);
      const pulse = 1 + 0.06 * Math.sin(tau * Math.PI * 4);
      const bob = Math.sin(tau * Math.PI * 2) * 5;

      switch (graphic) {
        // --- 00 to 02: PERMISSION HOOK ---
        case 'sec00_desktop_start':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:rgba(255,255,255,0.96); border-radius:18px; padding:32px 48px; text-align:center; box-shadow:0 15px 35px rgba(0,0,0,0.12); border:1px solid #e2e8f0; transform:scale(${0.92 + 0.08 * eTau});">
                <div style="font-size:52px; margin-bottom:10px;">💻❓</div>
                <div style="font-size:30px; font-weight:900; color:#1e293b; margin-bottom:8px;">Can Windows Use Your PC?</div>
                <div style="font-size:16px; color:#64748b; font-weight:600;">Investigating unauthorized background tasks</div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        case 'sec01_unauthorized_access':
          return `
            <div class="win-desktop">
              <div style="position:absolute; right:24px; bottom:64px; width:360px; background:#ffffff; border-radius:12px; box-shadow:0 15px 35px rgba(0,0,0,0.2); border-left:6px solid #eab308; padding:18px; transform:translateY(${30 * (1 - eTau)}px);">
                <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
                  <span style="font-size:24px;">🔒⚠️</span>
                  <span style="font-weight:800; font-size:15px; color:#1e293b;">Permission Check: BYPASSED</span>
                </div>
                <div style="font-size:14px; color:#475569; line-height:1.4;">Outbound network connection requested by Windows Update without prompt...</div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        case 'sec02_permission_bypassed':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#dc2626; color:#fff; border-radius:18px; padding:32px 48px; text-align:center; box-shadow:0 20px 50px rgba(220,38,38,0.4); transform:scale(${pulse});">
                <div style="font-size:52px; font-weight:900; margin-bottom:10px;">🚫 NO PERMISSION REQUESTED</div>
                <div style="font-size:22px; font-weight:700;">Windows assumes consent automatically!</div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        // --- 03 to 06: ACTIVE SEEDER ---
        case 'sec03_status_seeder_active':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:28px 40px; width:680px; box-shadow:0 15px 40px rgba(0,0,0,0.12); border:2px solid var(--accent); text-align:center;">
                <div style="display:inline-block; background:#dbeafe; color:var(--accent); font-weight:800; font-size:14px; padding:4px 14px; border-radius:20px; margin-bottom:12px;">SYSTEM STATUS</div>
                <div style="font-size:36px; font-weight:900; color:#1e293b; margin-bottom:8px;">It Already Is Using Your PC!</div>
                <div style="font-size:16px; color:#10b981; font-weight:700;">● Active Background Seeder Running</div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        case 'sec04_seeding_updates':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:30px 40px; width:720px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:1px solid #e2e8f0; text-align:center;">
                <div style="font-size:22px; font-weight:800; color:#1e293b; margin-bottom:14px;">📦 Windows Update Cache Seeding</div>
                <div style="display:flex; justify-content:center; gap:16px; margin:16px 0;">
                  <div style="background:#f1f5f9; padding:12px 18px; border-radius:8px; font-weight:700; font-size:13px;">KB5034441 (480 MB) ⬆</div>
                  <div style="background:#f1f5f9; padding:12px 18px; border-radius:8px; font-weight:700; font-size:13px;">Windows 11 Build 22631 ⬆</div>
                </div>
                <div style="font-size:15px; color:var(--accent); font-weight:700;">Uploading chunks from your SSD to outside PCs</div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        case 'sec05_strangers_connecting':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:28px 40px; width:740px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:1px solid #e2e8f0; text-align:center;">
                <div style="font-size:24px; font-weight:900; color:#1e293b; margin-bottom:12px;">🌍 Uploading To Strangers</div>
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; text-align:left; font-size:13px; font-family:monospace; background:#f8fafc; padding:16px; border-radius:10px;">
                  <div style="color:#dc2626;">➔ Peer: 185.220.101.4 (Germany)</div>
                  <div style="color:#dc2626;">➔ Peer: 94.140.8.12 (France)</div>
                  <div style="color:#dc2626;">➔ Peer: 104.244.42.1 (Canada)</div>
                  <div style="color:#dc2626;">➔ Peer: 198.51.100.24 (UK)</div>
                </div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        case 'sec06_since_install_day':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:32px 48px; width:700px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:1px solid #e2e8f0; text-align:center;">
                <div style="font-size:48px; margin-bottom:8px;">🗓️ ⚡</div>
                <div style="font-size:32px; font-weight:900; color:#1e293b; margin-bottom:6px;">Since The Day You Installed It</div>
                <div style="font-size:16px; color:#64748b; font-weight:600;">Active 24/7 in the background from your very first bootup</div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        // --- 07 to 08: EVERYONE'S PC ---
        case 'sec07_everyones_pc':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:32px 48px; width:700px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:1px solid #e2e8f0; text-align:center;">
                <div style="font-size:52px; margin-bottom:8px;">💻 💻 💻 💻</div>
                <div style="font-size:32px; font-weight:900; color:#1e293b; margin-bottom:6px;">Everyone's Computer Is Doing This?</div>
                <div style="font-size:16px; color:#64748b; font-weight:600;">Millions of unsuspecting PC owners worldwide</div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        case 'sec08_global_swarm_mesh':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#1e293b; color:#fff; border-radius:18px; padding:30px 44px; width:720px; box-shadow:0 20px 50px rgba(0,0,0,0.3); text-align:center;">
                <div style="font-size:24px; font-weight:800; color:#38bdf8; margin-bottom:12px;">🌐 1.4 BILLION WINDOWS MACHINES</div>
                <div style="font-size:18px; color:#cbd5e1; margin-bottom:16px;">All wired into Microsoft's decentralized distribution grid</div>
                <div style="background:#334155; border-radius:8px; padding:12px; font-size:14px; color:#a7f3d0; font-weight:700;">
                  Interconnected Peer-To-Peer Mesh Active
                </div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        // --- 09 to 15: WIN 10 & 11 FREE CDN ---
        case 'sec09_win10_affected':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:32px 48px; width:680px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:2px solid #0078d4; text-align:center;">
                <div style="font-size:52px; margin-bottom:8px;">🟦</div>
                <div style="font-size:36px; font-weight:900; color:#1e293b; margin-bottom:6px;">Windows 10</div>
                <div style="background:#fee2e2; color:#dc2626; font-weight:800; font-size:14px; padding:6px 14px; border-radius:20px; display:inline-block;">DELIVERY OPTIMIZATION: ON</div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        case 'sec10_win11_affected':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:32px 48px; width:680px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:2px solid #0078d4; text-align:center;">
                <div style="font-size:52px; margin-bottom:8px;">🪟</div>
                <div style="font-size:36px; font-weight:900; color:#1e293b; margin-bottom:6px;">Windows 11</div>
                <div style="background:#fee2e2; color:#dc2626; font-weight:800; font-size:14px; padding:6px 14px; border-radius:20px; display:inline-block;">DELIVERY OPTIMIZATION: ON</div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        case 'sec11_secret_cdn_part':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:30px 44px; width:720px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:1px solid #e2e8f0; text-align:center;">
                <div style="font-size:24px; font-weight:900; color:#1e293b; margin-bottom:12px;">Part of Microsoft's Free CDN</div>
                <div style="display:flex; justify-content:space-around; align-items:center; margin:16px 0;">
                  <div style="background:#eff6ff; padding:12px 18px; border-radius:10px; font-weight:800; color:#1e3a8a;">Azure Cloud</div>
                  <div style="font-size:24px; color:var(--accent);">➔ Offload ➔</div>
                  <div style="background:#fef2f2; padding:12px 18px; border-radius:10px; font-weight:800; color:#991b1b;">Your Living Room</div>
                </div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        case 'sec12_free_cdn_savings':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:32px 48px; width:700px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:1px solid #e2e8f0; text-align:center;">
                <div style="font-size:44px; margin-bottom:8px;">💰💰💰</div>
                <div style="font-size:32px; font-weight:900; color:#1e293b; margin-bottom:6px;">Microsoft's Free CDN Network</div>
                <div style="font-size:16px; color:#10b981; font-weight:700;">Saves them hundreds of millions in server bandwidth</div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        case 'sec13_you_are_server':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:32px 48px; width:700px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:2px solid var(--red); text-align:center;">
                <div style="font-size:48px; margin-bottom:8px;">🖥️ ➔ ☁️</div>
                <div style="font-size:34px; font-weight:900; color:#dc2626; margin-bottom:6px;">YOU ARE THE SERVER</div>
                <div style="font-size:16px; color:#64748b; font-weight:600;">You bought the PC. Microsoft uses it as cloud infrastructure.</div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        case 'sec14_one_toggle_preview':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:32px 48px; width:680px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:1px solid #e2e8f0; text-align:center;">
                <div style="font-size:44px; margin-bottom:10px;">⚙️ 🔘</div>
                <div style="font-size:32px; font-weight:900; color:#1e293b; margin-bottom:8px;">And One Toggle In Settings...</div>
                <div style="font-size:16px; color:var(--accent); font-weight:700;">One single hidden switch stops all of it!</div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        case 'sec15_turns_it_off_teaser':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:32px 48px; width:680px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:2px solid var(--green); text-align:center;">
                <div style="font-size:48px; margin-bottom:10px;">🛑 ➔ 🟢</div>
                <div style="font-size:32px; font-weight:900; color:var(--green); margin-bottom:8px;">Turns It All Off!</div>
                <div style="font-size:16px; color:#64748b; font-weight:600;">Instant shutdown of background upload traffic</div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        // --- 16 to 17: BITTORRENT SEEDING ---
        case 'sec16_bittorrent_logo':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:32px 48px; width:700px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:1px solid #e2e8f0; text-align:center;">
                <div style="font-size:52px; margin-bottom:8px;">⚡ 🔄</div>
                <div style="font-size:32px; font-weight:900; color:#1e293b; margin-bottom:8px;">Wait, Like BitTorrent Seeding?</div>
                <div style="font-size:16px; color:#64748b; font-weight:600;">Peter makes the exact technical connection</div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        case 'sec17_bittorrent_swarm':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#1e293b; color:#fff; border-radius:18px; padding:28px 40px; width:720px; box-shadow:0 20px 45px rgba(0,0,0,0.3); text-align:center;">
                <div style="font-size:22px; font-weight:800; color:#10b981; margin-bottom:12px;">P2P TORRENT SWARM COMPARISON</div>
                <div style="display:flex; justify-content:space-around; font-size:14px; font-family:monospace; background:#0f172a; padding:14px; border-radius:8px;">
                  <div>SEEDERS: 1 (Your PC)</div>
                  <div>LEECHERS: 34 (Strangers)</div>
                  <div style="color:#ef4444;">RATIO: 4.82 ⬆</div>
                </div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        // --- 18 to 20: NEVER TOLD YOU / DEFAULT ---
        case 'sec18_exactly_confirmed':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:32px 48px; width:680px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:2px solid var(--accent); text-align:center;">
                <div style="font-size:48px; margin-bottom:8px;">🎯</div>
                <div style="font-size:36px; font-weight:900; color:var(--accent); margin-bottom:6px;">EXACTLY.</div>
                <div style="font-size:18px; color:#1e293b; font-weight:700;">It is literal BitTorrent-style protocol for updates</div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        case 'sec19_never_told_you':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:32px 48px; width:700px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:1px solid #e2e8f0; text-align:center;">
                <div style="font-size:48px; margin-bottom:8px;">🤫 ❌</div>
                <div style="font-size:32px; font-weight:900; color:#1e293b; margin-bottom:8px;">Microsoft Never Told You</div>
                <div style="font-size:16px; color:#64748b; font-weight:600;">No popup. No prompt. No notification during setup.</div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        case 'sec20_turned_on_default':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#fef2f2; border:2px solid var(--red); border-radius:18px; padding:32px 48px; width:700px; text-align:center; transform:scale(${pulse});">
                <div style="font-size:44px; margin-bottom:8px;">🚨</div>
                <div style="font-size:34px; font-weight:900; color:#dc2626; margin-bottom:6px;">TURNED ON BY DEFAULT</div>
                <div style="font-size:16px; color:#991b1b; font-weight:700;">Every clean Windows installation seeds immediately</div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        // --- 21 to 22: BANDWIDTH GAUGE ---
        case 'sec21_measuring_bandwidth':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:32px 48px; width:680px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:1px solid #e2e8f0; text-align:center;">
                <div style="font-size:48px; margin-bottom:8px;">📊 ❓</div>
                <div style="font-size:32px; font-weight:900; color:#1e293b; margin-bottom:8px;">How Much Bandwidth?</div>
                <div style="font-size:16px; color:#64748b; font-weight:600;">Measuring the real network consumption...</div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        case 'sec22_gauge_climbing':
          const g1 = Math.floor(20 + 35 * eTau);
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:32px 48px; width:700px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:1px solid #e2e8f0; text-align:center;">
                <div style="font-size:22px; font-weight:800; color:#1e293b; margin-bottom:12px;">Upload Bandwidth Monitor</div>
                <div style="font-size:68px; font-weight:900; color:#d97706; margin-bottom:8px;">${g1}%</div>
                <div style="background:#fef3c7; height:18px; border-radius:9px; overflow:hidden;"><div style="width:${g1}%; height:100%; background:#d97706;"></div></div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        // --- 23 to 28: 80% UPLOAD & ZOOM FREEZE ---
        case 'sec23_user_reports':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:30px 44px; width:720px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:1px solid #e2e8f0; text-align:center;">
                <div style="font-size:24px; font-weight:900; color:#1e293b; margin-bottom:12px;">Users Investigating Speeds</div>
                <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:12px; margin-bottom:8px; font-size:14px; text-align:left;">
                  💬 "Why is my 100 Mbps upload pinned at 80% when idle?"
                </div>
                <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:12px; font-size:14px; text-align:left;">
                  💬 "My wife's laptop is lagging the whole house..."
                </div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        case 'sec24_big_80_percent':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:32px 48px; width:700px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:2px solid var(--red); text-align:center; transform:scale(${pulse});">
                <div style="font-size:24px; font-weight:800; color:#dc2626; margin-bottom:6px;">CRIPPLING CONSUMPTION</div>
                <div style="font-size:88px; font-weight:900; color:#dc2626; line-height:1; margin-bottom:10px;">80%</div>
                <div style="font-size:18px; color:#1e293b; font-weight:700;">Of your entire upload speed consumed</div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        case 'sec25_upload_bar_red':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:32px 48px; width:720px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:1px solid #e2e8f0; text-align:center;">
                <div style="display:flex; justify-content:space-between; font-weight:800; font-size:15px; margin-bottom:6px;">
                  <span>Windows Update Seeding</span><span style="color:var(--red);">80.4 Mbps</span>
                </div>
                <div style="background:#fee2e2; height:24px; border-radius:12px; overflow:hidden; margin-bottom:12px;">
                  <div style="width:80%; height:100%; background:var(--red);"></div>
                </div>
                <div style="font-size:14px; color:#64748b; font-weight:600;">Leaving barely 20% for your own software</div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        case 'sec26_choked_pipe':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:32px 48px; width:700px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:1px solid #e2e8f0; text-align:center;">
                <div style="font-size:44px; margin-bottom:8px;">⚠️ 🚿</div>
                <div style="font-size:30px; font-weight:900; color:#1e293b; margin-bottom:8px;">Your Upload Pipe Is Choked</div>
                <div style="font-size:16px; color:#64748b; line-height:1.5;">Broadband cables have limited upload. When saturated, packets drop immediately.</div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        case 'sec27_ping_spiking':
          const pingVal = Math.floor(60 + 220 * eTau);
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#1e293b; color:#fff; border-radius:18px; padding:32px 48px; width:700px; box-shadow:0 20px 50px rgba(0,0,0,0.3); text-align:center;">
                <div style="font-size:20px; font-weight:800; color:#f87171; margin-bottom:6px;">NETWORK LATENCY SPIKE</div>
                <div style="font-size:78px; font-weight:900; color:#ef4444; margin-bottom:8px;">${pingVal} ms</div>
                <div style="font-size:16px; color:#cbd5e1;">Extreme Packet Loss • Gaming Lag Spikes</div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        case 'sec28_zoom_freeze_alert':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:28px 40px; width:720px; box-shadow:0 20px 45px rgba(0,0,0,0.2); border:2px solid #ef4444; text-align:center;">
                <div style="font-size:36px; margin-bottom:6px;">📹 ❄️</div>
                <div style="font-size:28px; font-weight:900; color:#ef4444; margin-bottom:6px;">Why Your Zoom Calls Freeze!</div>
                <div style="background:#fef2f2; border-radius:8px; padding:10px; font-size:13px; font-family:monospace; color:#991b1b; margin-bottom:8px;">
                  "Your internet connection is unstable"
                </div>
                <div style="font-size:14px; color:#64748b;">Caused by Windows stealing your upstream bandwidth!</div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        // --- 29 to 32: TERMS OF SERVICE ---
        case 'sec29_seems_illegal':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:32px 48px; width:680px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:1px solid #e2e8f0; text-align:center;">
                <div style="font-size:52px; margin-bottom:8px;">⚖️ ❓</div>
                <div style="font-size:34px; font-weight:900; color:#1e293b; margin-bottom:6px;">That Seems Illegal.</div>
                <div style="font-size:16px; color:#64748b; font-weight:600;">Using someone's paid bandwidth without explicit notification?</div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        case 'sec30_buried_in_terms':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:32px 48px; width:700px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:1px solid #e2e8f0; text-align:center;">
                <div style="font-size:48px; margin-bottom:8px;">📜 🔍</div>
                <div style="font-size:32px; font-weight:900; color:#1e293b; margin-bottom:8px;">It's Buried In The Terms</div>
                <div style="font-size:16px; color:#64748b; font-weight:600;">Legalized through the Microsoft Services Agreement</div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        case 'sec31_terms_fine_print':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div class="win-window" style="width:700px; height:410px;">
                <div class="win-titlebar"><span>EULA Agreement - Section 13.b</span><div class="win-controls">─ ▢ ✕</div></div>
                <div style="padding:24px; font-size:13px; color:#334155; line-height:1.6; font-family:Georgia, serif;">
                  <div style="background:#fef3c7; border-left:4px solid #f59e0b; padding:14px; border-radius:4px; font-weight:600;">
                    "...Windows may send parts of previously downloaded updates to other PCs on your local network or on the Internet..."
                  </div>
                  <div style="margin-top:16px; color:#dc2626; font-weight:700; font-family:sans-serif;">You accepted this when setting up Windows!</div>
                </div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        case 'sec32_heres_whats_worse':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#dc2626; color:#fff; border-radius:18px; padding:32px 48px; text-align:center; box-shadow:0 20px 50px rgba(220,38,38,0.4); transform:scale(${pulse});">
                <div style="font-size:48px; font-weight:900; margin-bottom:8px;">👀 BUT HERE'S WHAT'S WORSE:</div>
                <div style="font-size:22px; font-weight:700;">Task Manager disguises the entire process!</div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        // --- 33 to 38: TASK MANAGER DISGUISE ---
        case 'sec33_taskmgr_ctrl_shift_esc':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:32px 48px; width:700px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:1px solid #e2e8f0; text-align:center;">
                <div style="display:flex; justify-content:center; gap:12px; margin-bottom:16px;">
                  <div style="background:#f1f5f9; border:2px solid #cbd5e1; border-radius:8px; padding:12px 20px; font-weight:900; font-size:20px;">Ctrl</div>
                  <div style="background:#f1f5f9; border:2px solid #cbd5e1; border-radius:8px; padding:12px 20px; font-weight:900; font-size:20px;">Shift</div>
                  <div style="background:#f1f5f9; border:2px solid #cbd5e1; border-radius:8px; padding:12px 20px; font-weight:900; font-size:20px;">Esc</div>
                </div>
                <div style="font-size:28px; font-weight:900; color:#1e293b;">Opening Task Manager</div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        case 'sec34_taskmgr_scrolling':
        case 'sec35_service_host_highlight':
        case 'sec36_svchost_85mbps':
          return `
            <div class="win-desktop" style="padding:16px;">
              <div class="win-window" style="width:900px; height:470px;">
                <div class="win-titlebar"><span>Task Manager</span><div class="win-controls">─ ▢ ✕</div></div>
                <table style="width:100%; border-collapse:collapse; font-size:13px; margin-top:8px;">
                  <tr style="background:#f8fafc; color:#64748b; font-weight:700;">
                    <th style="text-align:left; padding:8px 14px;">Process Name</th>
                    <th style="padding:8px 10px;">CPU</th>
                    <th style="padding:8px 10px;">Memory</th>
                    <th style="padding:8px 10px; color:var(--red);">Network</th>
                  </tr>
                  <tr style="background:#fee2e2; border-left:4px solid var(--red); font-weight:800;">
                    <td style="padding:12px 14px; color:#1e293b;">⚙ Service Host: Network Service</td>
                    <td style="text-align:center; padding:12px;">1.4%</td>
                    <td style="text-align:center; padding:12px;">48 MB</td>
                    <td style="text-align:center; padding:12px; color:var(--red); font-weight:900;">85.4 Mbps ⬆</td>
                  </tr>
                  <tr style="color:#64748b;">
                    <td style="padding:8px 14px;">📁 Windows Explorer</td>
                    <td style="text-align:center;">0.1%</td>
                    <td style="text-align:center;">72 MB</td>
                    <td style="text-align:center;">0 Mbps</td>
                  </tr>
                  <tr style="color:#64748b;">
                    <td style="padding:8px 14px;">🌐 Google Chrome</td>
                    <td style="text-align:center;">2.2%</td>
                    <td style="text-align:center;">340 MB</td>
                    <td style="text-align:center;">0.1 Mbps</td>
                  </tr>
                </table>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        case 'sec37_cant_even_see':
        case 'sec38_mask_peeled_back':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:32px 48px; width:720px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:1px solid #e2e8f0; text-align:center;">
                <div style="font-size:44px; margin-bottom:8px;">🎭 ➔ 📦</div>
                <div style="font-size:30px; font-weight:900; color:#1e293b; margin-bottom:8px;">The Mask: svchost.exe</div>
                <div style="font-size:16px; color:#64748b; line-height:1.5;">It hides as "Service Host" so ordinary users never realize Windows is seeding updates to strangers.</div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        // --- 39 to 41: MYSTERY PROCESSES ---
        case 'sec39_mystery_processes':
        case 'sec40_eating_bandwidth':
        case 'sec41_user_frustration':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:32px 48px; width:700px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:2px solid #ef4444; text-align:center;">
                <div style="font-size:48px; margin-bottom:8px;">👻 📶</div>
                <div style="font-size:32px; font-weight:900; color:#dc2626; margin-bottom:8px;">Mystery Processes Eating Bandwidth</div>
                <div style="font-size:16px; color:#1e293b; font-weight:600;">You look at Task Manager and can't figure out who is stealing your upload!</div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        // --- 42 to 44: BLAMING THE ISP ---
        case 'sec42_people_blame_isp':
        case 'sec43_router_innocent':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:32px 48px; width:720px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:1px solid #e2e8f0; text-align:center;">
                <div style="font-size:44px; margin-bottom:8px;">📡 ❌</div>
                <div style="font-size:32px; font-weight:900; color:#1e293b; margin-bottom:8px;">Most People Blame Their ISP</div>
                <div style="font-size:16px; color:#64748b; line-height:1.5;">You call Comcast, AT&T or Verizon complaining about lag, thinking the internet line is broken...</div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        case 'sec44_windows_is_culprit':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:32px 48px; width:720px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:2px solid var(--accent); text-align:center;">
                <div style="display:flex; justify-content:space-around; align-items:center; margin-bottom:14px;">
                  <div><span style="font-size:36px;">📡</span><div style="font-weight:700; color:var(--green);">Router: INNOCENT ✓</div></div>
                  <div style="font-size:28px;">➔</div>
                  <div><span style="font-size:36px;">🪟</span><div style="font-weight:800; color:var(--red);">Windows: CULPRIT! ✗</div></div>
                </div>
                <div style="font-size:15px; color:#64748b; font-weight:600;">Windows is the one quietly eating all your upload!</div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        // --- 45 to 46: WHY MICROSOFT DOES THIS ---
        case 'sec45_why_microsoft_cloud':
        case 'sec46_money_savings_icon':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:32px 48px; width:700px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:1px solid #e2e8f0; text-align:center;">
                <div style="font-size:48px; margin-bottom:8px;">🏢 ❓</div>
                <div style="font-size:32px; font-weight:900; color:#1e293b; margin-bottom:8px;">Why Would Microsoft Do This?</div>
                <div style="font-size:16px; color:#64748b; font-weight:600;">Peter asks the million dollar question...</div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        // --- 47 to 54: 3.5 BILLION UPDATES & COSTS ---
        case 'sec47_stat_3_5_billion_intro':
        case 'sec48_stat_3_5_billion_boxes':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:32px 48px; width:720px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:1px solid #e2e8f0; text-align:center;">
                <div style="font-size:20px; font-weight:800; color:var(--accent); margin-bottom:4px;">GLOBAL UPDATE VOLUME</div>
                <div style="font-size:78px; font-weight:900; color:#1e293b; margin-bottom:8px;">3.5 BILLION</div>
                <div style="font-size:18px; color:#64748b; font-weight:700;">Updates Delivered Every Single Month</div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        case 'sec49_p2p_mesh_flow':
        case 'sec50_offload_server_costs':
        case 'sec51_servers_shut_down':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:30px 44px; width:720px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:1px solid #e2e8f0; text-align:center;">
                <div style="font-size:24px; font-weight:900; color:#1e293b; margin-bottom:12px;">Offloading Cloud Server Costs</div>
                <div style="display:flex; justify-content:space-around; align-items:center; margin:16px 0;">
                  <div style="background:#eff6ff; padding:12px 18px; border-radius:8px; font-weight:800;">Microsoft Azure: $0 Saved</div>
                  <div style="font-size:24px;">➔</div>
                  <div style="background:#fee2e2; padding:12px 18px; border-radius:8px; font-weight:800; color:#dc2626;">Paid By Users!</div>
                </div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        case 'sec52_electricity_spinning':
        case 'sec53_electricity_bill_up':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:32px 48px; width:700px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:1px solid #e2e8f0; text-align:center;">
                <div style="font-size:48px; margin-bottom:8px;">⚡ 💡</div>
                <div style="font-size:32px; font-weight:900; color:#1e293b; margin-bottom:8px;">Your Electricity Bill</div>
                <div style="font-size:16px; color:#64748b; font-weight:600;">Your computer stays awake, fans spin, drawing extra power to upload files.</div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        case 'sec54_internet_plan_cap':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:32px 48px; width:700px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:2px solid var(--red); text-align:center;">
                <div style="font-size:44px; margin-bottom:8px;">📊 💸</div>
                <div style="font-size:32px; font-weight:900; color:#dc2626; margin-bottom:8px;">And Your Internet Plan!</div>
                <div style="font-size:16px; color:#1e293b; font-weight:700;">Eating your ISP's monthly upload data cap!</div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        // --- 55 to 56: LOCAL NETWORK QUESTION ---
        case 'sec55_home_wifi_lan':
        case 'sec56_local_devices_only':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:32px 48px; width:700px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:1px solid #e2e8f0; text-align:center;">
                <div style="font-size:48px; margin-bottom:8px;">🏠 📶</div>
                <div style="font-size:30px; font-weight:900; color:#1e293b; margin-bottom:8px;">Limit To Local Network?</div>
                <div style="font-size:16px; color:#64748b; font-weight:600;">Peter asks: "Do they at least keep it inside your own house?"</div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        // --- 57 to 62: THE MISDIRECTION ---
        case 'sec57_the_misdirection':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#1e293b; color:#fff; border-radius:18px; padding:32px 48px; width:700px; text-align:center; box-shadow:0 20px 50px rgba(0,0,0,0.3);">
                <div style="font-size:48px; margin-bottom:8px;">🎩 ✨</div>
                <div style="font-size:34px; font-weight:900; color:#38bdf8; margin-bottom:8px;">THAT'S THE MISDIRECTION</div>
                <div style="font-size:16px; color:#cbd5e1;">Stewie exposes the subtle UI sleight-of-hand</div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        case 'sec58_two_radio_buttons':
        case 'sec59_radio_local_safe':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:30px 44px; width:740px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:1px solid #e2e8f0;">
                <div style="font-size:20px; font-weight:800; color:#1e293b; margin-bottom:14px;">Allow downloads from:</div>
                <div style="background:#f1f5f9; border-radius:8px; padding:12px 18px; margin-bottom:10px; display:flex; align-items:center; gap:10px;">
                  <span style="font-size:18px;">⚪</span> <span style="font-weight:700; color:#475569;">Devices on my local network</span>
                </div>
                <div style="font-size:13px; color:#10b981; font-weight:700;">(This would be safe... but it is NOT the default!)</div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        case 'sec60_radio_internet_default':
        case 'sec61_default_includes_strangers':
        case 'sec62_worldwide_swarms':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:30px 44px; width:740px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:2px solid var(--red);">
                <div style="font-size:20px; font-weight:800; color:#dc2626; margin-bottom:14px;">The Hidden Default Option:</div>
                <div style="background:#fee2e2; border-radius:8px; padding:14px 18px; display:flex; align-items:center; gap:10px;">
                  <span style="font-size:18px;">🔘</span> <span style="font-weight:900; color:#991b1b;">Devices on the Internet and my local network</span>
                </div>
                <div style="font-size:14px; color:#dc2626; font-weight:800; margin-top:10px;">PRE-SELECTED BY MICROSOFT!</div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        // --- 63 to 65: RANDOM STRANGERS ---
        case 'sec63_strangers_avatars':
        case 'sec64_uploading_across_globe':
        case 'sec65_unencrypted_swarm':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:32px 48px; width:720px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:1px solid #e2e8f0; text-align:center;">
                <div style="font-size:48px; margin-bottom:8px;">🌍 👤 👤 👤</div>
                <div style="font-size:30px; font-weight:900; color:#1e293b; margin-bottom:8px;">Uploading To Random Strangers!</div>
                <div style="font-size:16px; color:#dc2626; font-weight:700;">Anyone in the world downloading Windows updates</div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        // --- 66 to 70: OHIO TO GERMANY EXAMPLE ---
        case 'sec66_yep_confirmed':
        case 'sec67_gaming_laptop_ohio':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:30px 44px; width:720px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:1px solid #e2e8f0; text-align:center;">
                <div style="font-size:44px; margin-bottom:8px;">🎮 🇺🇸</div>
                <div style="font-size:32px; font-weight:900; color:#1e293b; margin-bottom:6px;">Gaming Laptop in Ohio</div>
                <div style="font-size:16px; color:var(--red); font-weight:700;">Uploading Windows CAB files across the globe</div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        case 'sec68_atlantic_data_beam':
        case 'sec69_stranger_germany':
        case 'sec70_stranger_download_done':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:30px 44px; width:740px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:1px solid #e2e8f0; text-align:center;">
                <div style="display:flex; justify-content:space-between; align-items:center; background:#f8fafc; padding:16px; border-radius:12px;">
                  <div><div style="font-size:28px;">🇺🇸 💻</div><div style="font-weight:800; font-size:13px;">Ohio, USA</div></div>
                  <div style="font-size:24px; color:var(--accent);">➔ ➔ ✈ ➔ ➔</div>
                  <div><div style="font-size:28px;">🇩🇪 💻</div><div style="font-weight:800; font-size:13px;">Berlin, Germany</div></div>
                </div>
                <div style="font-size:15px; color:#1e293b; font-weight:700; margin-top:12px;">Downloading from your laptop right now!</div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        // --- 71 to 72: EMERGENCY STOP ---
        case 'sec71_how_to_stop_emergency':
        case 'sec72_5_clicks_teaser':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:32px 48px; width:700px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:2px solid var(--accent); text-align:center;">
                <div style="font-size:48px; margin-bottom:8px;">🛑 5️⃣</div>
                <div style="font-size:32px; font-weight:900; color:#1e293b; margin-bottom:8px;">How To Stop This Immediately</div>
                <div style="font-size:18px; color:var(--accent); font-weight:800;">Follow these 5 clicks right now:</div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        // --- 73 to 80: EXACT 5 CLICKS WALKTHROUGH ---
        case 'sec73_click1_open_settings':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:32px 48px; width:700px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:1px solid #e2e8f0; text-align:center;">
                <div style="font-size:20px; font-weight:800; color:var(--accent); margin-bottom:6px;">CLICK 1 OF 5</div>
                <div style="display:flex; justify-content:center; gap:12px; margin-bottom:14px;">
                  <div style="background:#f1f5f9; border:2px solid #cbd5e1; border-radius:8px; padding:10px 20px; font-weight:900; font-size:22px;">⊞ Win</div>
                  <div style="background:#f1f5f9; border:2px solid #cbd5e1; border-radius:8px; padding:10px 20px; font-weight:900; font-size:22px;">I</div>
                </div>
                <div style="font-size:30px; font-weight:900; color:#1e293b;">Open Windows Settings</div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        case 'sec74_click2_windows_update':
          return `
            <div class="win-desktop" style="padding:16px;">
              <div class="win-window" style="width:900px; height:470px;">
                <div class="win-titlebar"><span>⚙ Settings</span><div class="win-controls">─ ▢ ✕</div></div>
                <div class="set-layout">
                  <div class="set-sidebar">
                    <div class="set-side-nav">🖥 System</div>
                    <div class="set-side-nav">📶 Network & Internet</div>
                    <div class="set-side-nav active" style="border:2px solid var(--accent); background:#dbeafe;">🔄 Windows Update (Click 2)</div>
                  </div>
                  <div class="set-content" style="display:flex; align-items:center; justify-content:center; color:#64748b; font-weight:600;">
                    Select Windows Update in the left navigation
                  </div>
                </div>
              </div>
              ${cursorHTML(180, 260, true)}
              ${winTaskbarHTML}
            </div>
          `;

        case 'sec75_click3_advanced_options':
        case 'sec76_click4_delivery_opt':
          return `
            <div class="win-desktop" style="padding:16px;">
              <div class="win-window" style="width:900px; height:470px;">
                <div class="win-titlebar"><span>⚙ Settings › Windows Update</span><div class="win-controls">─ ▢ ✕</div></div>
                <div class="set-layout">
                  <div class="set-sidebar"><div class="set-side-nav active">🔄 Windows Update</div></div>
                  <div class="set-content">
                    <div style="font-size:20px; font-weight:800; margin-bottom:12px;">More options</div>
                    <div class="set-card" style="border:2px solid var(--accent); background:#eff6ff;">
                      <div><div style="font-weight:800; font-size:15px; color:#1e3a8a;">⚙ Advanced options</div><div style="font-size:12px; color:#64748b;">Delivery optimization, optional updates</div></div>
                      <div style="color:var(--accent); font-weight:800;">➔ CLICK</div>
                    </div>
                  </div>
                </div>
              </div>
              ${cursorHTML(600, 180, true)}
              ${winTaskbarHTML}
            </div>
          `;

        case 'sec77_finding_the_switch':
        case 'sec78_cursor_approaching_switch':
          return `
            <div class="win-desktop" style="padding:16px;">
              <div class="win-window" style="width:900px; height:470px;">
                <div class="win-titlebar"><span>⚙ Settings › Windows Update › Advanced › Delivery Optimization</span><div class="win-controls">─ ▢ ✕</div></div>
                <div class="set-layout">
                  <div class="set-content" style="padding:24px;">
                    <div style="font-size:22px; font-weight:800; color:#1e293b; margin-bottom:14px;">Delivery Optimization</div>
                    <div class="set-card" style="border:2px solid var(--red); background:#fef2f2;">
                      <div>
                        <div style="font-weight:800; font-size:15px; color:#1e293b;">Allow downloads from other PCs</div>
                        <div style="font-size:12px; color:#991b1b; font-weight:600;">Currently Active (Seeding)</div>
                      </div>
                      <div class="toggle-switch on"><div class="toggle-knob"></div></div>
                    </div>
                  </div>
                </div>
              </div>
              ${cursorHTML(680, 160, false)}
              ${winTaskbarHTML}
            </div>
          `;

        case 'sec79_click5_toggle_off':
        case 'sec80_switch_turned_grey_off':
          return `
            <div class="win-desktop" style="padding:16px;">
              <div class="win-window" style="width:900px; height:470px;">
                <div class="win-titlebar"><span>⚙ Settings › Windows Update › Advanced › Delivery Optimization</span><div class="win-controls">─ ▢ ✕</div></div>
                <div class="set-layout">
                  <div class="set-content" style="padding:24px;">
                    <div style="font-size:22px; font-weight:800; color:#1e293b; margin-bottom:14px;">Delivery Optimization</div>
                    <div class="set-card" style="border:2px solid var(--green); background:#f0fdf4;">
                      <div>
                        <div style="font-weight:800; font-size:15px; color:#1e293b;">Allow downloads from other PCs</div>
                        <div style="font-size:12px; color:var(--green); font-weight:700;">TOGGLED OFF ✓</div>
                      </div>
                      <div class="toggle-switch"><div class="toggle-knob"></div></div>
                    </div>
                  </div>
                </div>
              </div>
              ${cursorHTML(710, 160, true)}
              ${winTaskbarHTML}
            </div>
          `;

        // --- 81 to 84: 5 CLICKS COMPLETE & FREEDOM ---
        case 'sec81_thats_it_question':
        case 'sec82_five_clicks_checklist':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:28px 44px; width:700px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:2px solid var(--green); text-align:center;">
                <div style="font-size:22px; font-weight:900; color:var(--green); margin-bottom:10px;">ALL 5 CLICKS COMPLETE!</div>
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; text-align:left; font-size:13px; font-weight:700; color:#1e293b;">
                  <div>1. Settings ✓</div>
                  <div>2. Windows Update ✓</div>
                  <div>3. Advanced Options ✓</div>
                  <div>4. Delivery Opt ✓</div>
                  <div style="grid-column:span 2; color:var(--green);">5. Toggle Switch OFF ✓</div>
                </div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        case 'sec83_no_longer_free_bandwidth':
        case 'sec84_bandwidth_liberated':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:32px 48px; width:700px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:2px solid var(--green); text-align:center;">
                <div style="font-size:52px; margin-bottom:8px;">🚀 🔒</div>
                <div style="font-size:32px; font-weight:900; color:#1e293b; margin-bottom:6px;">No Longer Free Bandwidth!</div>
                <div style="font-size:16px; color:var(--green); font-weight:700;">100% of your upload pipe restored to you</div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        // --- 85 to 88: TASK MANAGER CLEAN 0 MBPS ---
        case 'sec85_taskmgr_lies_question':
        case 'sec86_windows_steals_bandwidth':
        case 'sec87_taskmgr_clean_0mbps':
        case 'sec88_speedtest_100_percent':
          return `
            <div class="win-desktop" style="padding:16px;">
              <div class="win-window" style="width:900px; height:470px;">
                <div class="win-titlebar"><span>Task Manager (Optimized)</span><div class="win-controls">─ ▢ ✕</div></div>
                <table style="width:100%; border-collapse:collapse; font-size:13px; margin-top:8px;">
                  <tr style="background:#f8fafc; color:#64748b; font-weight:700;">
                    <th style="text-align:left; padding:8px 14px;">Process Name</th>
                    <th style="padding:8px 10px;">CPU</th>
                    <th style="padding:8px 10px;">Memory</th>
                    <th style="padding:8px 10px; color:var(--green);">Network</th>
                  </tr>
                  <tr style="background:#f0fdf4; border-left:4px solid var(--green); font-weight:800;">
                    <td style="padding:12px 14px; color:#1e293b;">⚙ Service Host: Network Service</td>
                    <td style="text-align:center; padding:12px;">0.0%</td>
                    <td style="text-align:center; padding:12px;">18 MB</td>
                    <td style="text-align:center; padding:12px; color:var(--green); font-weight:900;">0.0 Mbps (IDLE) ✓</td>
                  </tr>
                </table>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        // --- 89 to 92: OUTRO & FOLLOW ---
        case 'sec89_taskmgr_truth_lens':
        case 'sec90_zoom_smooth_hd':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:32px 48px; width:720px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:2px solid var(--green); text-align:center;">
                <div style="font-size:44px; margin-bottom:8px;">📹 ⚡ ✨</div>
                <div style="font-size:32px; font-weight:900; color:#1e293b; margin-bottom:6px;">Zoom & Gaming Crystal Clear</div>
                <div style="font-size:16px; color:var(--green); font-weight:700;">Zero lag spikes • Zero packet loss</div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;

        case 'sec91_master_pc_tips_card':
        case 'sec92_follow_ez_peter_cta':
        default:
          const pop = easeOutCubic(clamp(tau / 0.4, 0, 1));
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:24px; padding:36px 54px; text-align:center; box-shadow:0 25px 60px rgba(26,108,240,0.25); border:2px solid var(--accent); transform:scale(${0.88 + 0.12 * pop});">
                <div style="font-size:52px; margin-bottom:10px;">🔔</div>
                <div style="font-size:36px; font-weight:900; color:#1e293b; margin-bottom:8px;">PC Tips by Ez_peter</div>
                <div style="font-size:18px; font-weight:600; color:#64748b; margin-bottom:18px;">Follow for more essential Windows secrets!</div>
                <div style="background:var(--accent); color:#fff; font-size:22px; font-weight:800; padding:12px 36px; border-radius:30px; display:inline-block; box-shadow:0 10px 25px rgba(26,108,240,0.35);">
                  Follow @Ez_peter
                </div>
              </div>
              ${winTaskbarHTML}
            </div>
          `;
      }
    }

    // MAIN DETERMINISTIC RENDER FUNCTION: window.renderAt(t)
    window.renderAt = function(t) {
      if (!SCRIPT || SCRIPT.length === 0) return;

      const totalSeconds = SCRIPT.length;
      const clampedT = clamp(t, 0, totalSeconds - 0.001);
      const s = Math.floor(clampedT);
      const tau = clampedT - s;
      const currentItem = SCRIPT[s];

      // 1. UPDATE PROGRESS BAR
      const fills = document.querySelectorAll('.prog-fill');
      fills.forEach((fill, idx) => {
        if (idx < s) {
          fill.style.width = '100%';
        } else if (idx === s) {
          fill.style.width = `${tau * 100}%`;
        } else {
          fill.style.width = '0%';
        }
      });

      // 2. UPDATE TOP TEXT
      const stepLabelEl = document.getElementById('stepLabel');
      const titleEl = document.getElementById('sceneTitle');
      const breadcrumbEl = document.getElementById('breadcrumb');

      if (currentItem.stepNumber > 0) {
        stepLabelEl.textContent = `STEP 0${currentItem.stepNumber}`;
      } else {
        stepLabelEl.textContent = '';
      }
      titleEl.textContent = currentItem.title;
      breadcrumbEl.textContent = currentItem.breadcrumb;

      // 3. RENDER SCENE INSIDE LAPTOP SCREEN
      const screenEl = document.getElementById('screen');
      screenEl.innerHTML = renderScreenScene(currentItem.graphic, tau, clampedT);

      // 4. RENDER CAPTIONS - EXACT ACOUSTIC ALIGNMENT (NEVER DRIFTS)
      const capEl = document.getElementById('captions');
      if (window.hideCaptions) {
        capEl.style.display = 'none';
      } else {
        capEl.style.display = 'flex';
        
        // Find the active caption chunk for time clampedT
        const chunks = ALIGNED_CAPTIONS.chunks;
        let activeChunk = null;
        for (let i = 0; i < chunks.length; i++) {
          if (clampedT >= chunks[i].start && clampedT < chunks[i].display_end) {
            activeChunk = chunks[i];
            break;
          }
        }
        if (!activeChunk && chunks.length > 0) {
          if (clampedT >= chunks[chunks.length - 1].start) {
            activeChunk = chunks[chunks.length - 1];
          } else {
            for (let i = 0; i < chunks.length - 1; i++) {
              if (clampedT >= chunks[i].display_end && clampedT < chunks[i+1].start) {
                activeChunk = chunks[i];
                break;
              }
            }
          }
        }

        if (activeChunk && activeChunk.words.length > 0) {
          let activeWordIdx = 0;
          for (let i = 0; i < activeChunk.words.length; i++) {
            if (clampedT >= activeChunk.words[i].global_start) {
              activeWordIdx = i;
            }
          }

          capEl.innerHTML = activeChunk.words.map((w, idx) => {
            const isActive = idx === activeWordIdx;
            return `<span class="caption-word ${isActive ? 'word-active' : ''}">${w.text}</span>`;
          }).join('');
        }
      }

      // 5. RENDER CHARACTERS (Peter on Left, Stewie on Right)
      // Only ONE on screen at a time! Smooth slide in/out aligned to speaker turns
      const peterEl = document.getElementById('peterImg');
      const stewieEl = document.getElementById('stewieImg');

      const turns = ALIGNED_CAPTIONS.turn_ranges;
      let activeTurn = null;
      for (let i = 0; i < turns.length; i++) {
        if (clampedT >= turns[i].start && clampedT <= turns[i].end) {
          activeTurn = turns[i];
          break;
        }
      }
      if (!activeTurn && turns.length > 0) {
        for (let i = 0; i < turns.length - 1; i++) {
          if (clampedT > turns[i].end && clampedT < turns[i+1].start) {
            const mid = (turns[i].end + turns[i+1].start) / 2;
            if (clampedT < mid) {
              activeTurn = turns[i];
            } else {
              activeTurn = turns[i+1];
            }
            break;
          }
        }
        if (!activeTurn) activeTurn = turns[turns.length - 1];
      }

      const isPeter = activeTurn && activeTurn.speaker === 'peter';
      const isStewie = activeTurn && activeTurn.speaker === 'stewie';

      if (isPeter) {
        const turnElapsed = clampedT - activeTurn.start;
        const turnRemaining = activeTurn.end - clampedT;
        let peterX = 0;
        if (turnElapsed < 0.22) {
          const inFrac = easeOutCubic(clamp(turnElapsed / 0.22, 0, 1));
          peterX = -1200 * (1 - inFrac);
        } else if (turnRemaining < 0.22) {
          const outFrac = easeInOutQuad(clamp((0.22 - turnRemaining) / 0.22, 0, 1));
          peterX = -1200 * outFrac;
        }
        const bobY = Math.sin(clampedT * Math.PI * 4) * 6;
        const breathScale = 1.0 + 0.012 * Math.sin(clampedT * Math.PI * 2);
        peterEl.style.transform = `translateX(${peterX}px) translateY(${bobY}px) scale(${breathScale})`;
        stewieEl.style.transform = `translateX(1200px)`;
      } else if (isStewie) {
        const turnElapsed = clampedT - activeTurn.start;
        const turnRemaining = activeTurn.end - clampedT;
        let stewieX = 0;
        if (turnElapsed < 0.22) {
          const inFrac = easeOutCubic(clamp(turnElapsed / 0.22, 0, 1));
          stewieX = 1200 * (1 - inFrac);
        } else if (turnRemaining < 0.22) {
          const outFrac = easeInOutQuad(clamp((0.22 - turnRemaining) / 0.22, 0, 1));
          stewieX = 1200 * outFrac;
        }
        const bobY = Math.sin(clampedT * Math.PI * 4) * 6;
        const breathScale = 1.0 + 0.012 * Math.sin(clampedT * Math.PI * 2);
        stewieEl.style.transform = `translateX(${stewieX}px) translateY(${bobY}px) scale(${breathScale})`;
        peterEl.style.transform = `translateX(-1200px)`;
      } else {
        peterEl.style.transform = `translateX(-1200px)`;
        stewieEl.style.transform = `translateX(1200px)`;
      }
    };

    // Initial render
    window.renderAt(0);
  </script>
</body>
</html>
"""

final_html = html_template.replace("__ALIGNED_CAPTIONS__", aligned_json_str).replace("__SCRIPT__", script_json_str)

with open("video-engine/index.html", "w", encoding="utf-8") as f:
    f.write(final_html)

print("Successfully written video-engine/index.html with all 93 scenes!")
