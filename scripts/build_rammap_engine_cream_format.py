import json
import os

with open("video-engine/aligned_captions.json", "r", encoding="utf-8") as f:
    aligned_data = json.load(f)

with open("output/script.json", "r", encoding="utf-8") as f:
    script_data = json.load(f)

aligned_json_str = json.dumps(aligned_data)
script_json_str = json.dumps(script_data)

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>PC Tips by Ez_peter - RAMMap Memory Optimization</title>
  <style>
    :root {{
      --bg: #f8f4ee;
      --text: #0d0d0d;
      --accent: #1a6cf0;
      --grey-light: #f0ede6;
      --grey-mid: #6b7280;
      --grey-border: #d1d5db;
      --red: #e53935;
      --green: #10b981;
    }}
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-font-smoothing: antialiased;
    }}
    body {{
      background: #222;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      font-family: 'Segoe UI Variable Display', 'Segoe UI', Inter, system-ui, sans-serif;
      overflow: hidden;
    }}
    #stage {{
      position: relative;
      width: 1080px;
      height: 1920px;
      background: var(--bg);
      color: var(--text);
      overflow: hidden;
    }}

    /* TOP BAR & PROGRESS */
    #topArea {{
      position: absolute;
      top: 60px;
      left: 60px;
      width: 960px;
      display: flex;
      flex-direction: column;
      align-items: center;
      z-index: 20;
    }}
    #progressBar {{
      width: 100%;
      height: 8px;
      display: flex;
      gap: 3px;
      margin-bottom: 24px;
    }}
    .prog-seg {{
      flex: 1;
      height: 100%;
      background: rgba(13, 13, 13, 0.12);
      border-radius: 4px;
      overflow: hidden;
    }}
    .prog-fill {{
      height: 100%;
      width: 0%;
      background: var(--accent);
      border-radius: 4px;
    }}
    #pillTag {{
      background: #0d0d0d;
      color: #ffffff;
      font-size: 20px;
      font-weight: 800;
      letter-spacing: 2px;
      padding: 6px 20px;
      border-radius: 20px;
      text-transform: uppercase;
      margin-bottom: 16px;
    }}
    #stepLabel {{
      color: var(--accent);
      font-size: 24px;
      font-weight: 800;
      letter-spacing: 3px;
      text-transform: uppercase;
      margin-bottom: 8px;
      height: 32px;
    }}
    #sceneTitle {{
      font-size: 52px;
      font-weight: 900;
      text-align: center;
      line-height: 1.1;
      margin-bottom: 8px;
      height: 64px;
      color: var(--text);
      letter-spacing: -0.5px;
    }}
    #breadcrumb {{
      font-size: 26px;
      font-weight: 600;
      color: var(--grey-mid);
      text-align: center;
      height: 34px;
    }}

    /* LAPTOP FRAME */
    #laptopContainer {{
      position: absolute;
      top: 300px;
      left: 60px;
      width: 960px;
      height: 590px;
      z-index: 10;
    }}
    #laptopScreenBezel {{
      width: 960px;
      height: 550px;
      background: #18191c;
      border-radius: 20px 20px 4px 4px;
      padding: 14px;
      box-shadow: 0 25px 60px rgba(0, 0, 0, 0.22);
      position: relative;
    }}
    #laptopWebcam {{
      position: absolute;
      top: 6px;
      left: 50%;
      transform: translateX(-50%);
      width: 6px;
      height: 6px;
      background: #2d3035;
      border-radius: 50%;
    }}
    #screen {{
      width: 100%;
      height: 100%;
      background: #ffffff;
      border-radius: 10px;
      overflow: hidden;
      position: relative;
    }}
    #laptopBase {{
      width: 1040px;
      height: 24px;
      background: linear-gradient(to bottom, #d6d9de 0%, #b4b8bf 60%, #9ca0a8 100%);
      border-radius: 4px 4px 28px 28px;
      margin-left: -40px;
      margin-top: 2px;
      position: relative;
      box-shadow: 0 16px 30px rgba(0, 0, 0, 0.18);
    }}
    #laptopNotch {{
      position: absolute;
      top: 0;
      left: 50%;
      transform: translateX(-50%);
      width: 130px;
      height: 8px;
      background: #8b8e96;
      border-radius: 0 0 10px 10px;
    }}

    /* WINDOWS 11 DESKTOP / TASKBAR */
    .win-desktop {{
      position: absolute;
      inset: 0;
      background: radial-gradient(circle at 50% 120%, #dbeafe 0%, #eff6ff 45%, #f8fafc 100%);
      overflow: hidden;
      font-family: 'Segoe UI', system-ui, sans-serif;
    }}
    .win-taskbar {{
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      height: 48px;
      background: rgba(255, 255, 255, 0.88);
      backdrop-filter: blur(20px);
      border-top: 1px solid rgba(0, 0, 0, 0.08);
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 12px;
      z-index: 50;
    }}
    .taskbar-center {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .tb-icon {{
      width: 32px;
      height: 32px;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 6px;
    }}
    .tb-win-logo {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 2px;
      width: 20px;
      height: 20px;
    }}
    .tb-win-logo div {{
      background: #0078d4;
      border-radius: 1px;
    }}
    .tb-search {{
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
    }}
    .tb-clock {{
      position: absolute;
      right: 14px;
      font-size: 13px;
      color: #334155;
      font-weight: 500;
      text-align: right;
      line-height: 1.1;
    }}

    /* REUSABLE WINDOW CONTAINER */
    .win-window {{
      position: absolute;
      background: #ffffff;
      border-radius: 10px;
      box-shadow: 0 16px 36px rgba(0, 0, 0, 0.16), 0 0 0 1px rgba(0, 0, 0, 0.08);
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }}
    .win-titlebar {{
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
    }}
    .win-controls {{
      margin-left: auto;
      display: flex;
      gap: 12px;
      font-size: 13px;
      color: #605e5c;
    }}

    /* CURSOR & CLICK RIPPLE */
    .win-cursor {{
      position: absolute;
      pointer-events: none;
      z-index: 100;
      filter: drop-shadow(0 2px 5px rgba(0, 0, 0, 0.3));
    }}
    .click-ripple {{
      position: absolute;
      width: 32px;
      height: 32px;
      border: 2px solid var(--accent);
      border-radius: 50%;
      transform: translate(-50%, -50%) scale(1);
      animation: ripple 0.4s ease-out forwards;
      pointer-events: none;
      z-index: 99;
    }}

    /* CAPTIONS */
    #captions {{
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
    }}
    .caption-word {{
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
    }}
    .caption-word.word-active {{
      background: #1a6cf0;
      color: #ffffff !important;
      text-shadow: 0 2px 10px rgba(26, 108, 240, 0.4) !important;
      transform: scale(1.08);
      box-shadow: 0 8px 24px rgba(26, 108, 240, 0.35);
    }}

    /* CHARACTERS */
    .char-layer {{
      position: absolute;
      bottom: -150px;
      left: 0;
      width: 1080px;
      height: 1920px;
      pointer-events: none;
      z-index: 15;
      will-change: transform;
    }}
    #peterImg {{
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
    }}
    #stewieImg {{
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
    }}

    /* RAMMap Desktop Window Styles */
    .rammap-app {{
      width: 100%;
      height: 100%;
      background: #ffffff;
      display: flex;
      flex-direction: column;
      font-family: 'Segoe UI', system-ui, sans-serif;
    }}
    .rm-menubar {{
      height: 30px;
      background: #f3f3f3;
      border-bottom: 1px solid #e5e5e5;
      display: flex;
      align-items: center;
      padding: 0 10px;
      gap: 18px;
      font-size: 13px;
      color: #333;
      position: relative;
    }}
    .rm-menu-item {{
      padding: 3px 8px;
      border-radius: 4px;
      cursor: default;
    }}
    .rm-menu-item.active {{
      background: #1a6cf0;
      color: #ffffff;
      font-weight: 700;
    }}
    .rm-dropdown {{
      position: absolute;
      top: 28px;
      left: 45px;
      background: #ffffff;
      border: 1px solid #d1d5db;
      border-radius: 6px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.18);
      width: 250px;
      z-index: 80;
      display: flex;
      flex-direction: column;
      padding: 4px 0;
    }}
    .rm-drop-item {{
      padding: 7px 14px;
      font-size: 13px;
      color: #222;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}
    .rm-drop-item.highlight {{
      background: #e0edfe;
      color: #1a6cf0;
      font-weight: 700;
      border-left: 3px solid #1a6cf0;
    }}
    .rm-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 12px;
    }}
    .rm-table th {{
      background: #f8fafc;
      padding: 6px 10px;
      text-align: left;
      border-bottom: 1px solid #e2e8f0;
      color: #64748b;
      font-weight: 600;
    }}
    .rm-table td {{
      padding: 5px 10px;
      border-bottom: 1px solid #f1f5f9;
      color: #334155;
    }}
  </style>
</head>
<body>
  <div id="stage">
    <!-- TOP AREA -->
    <div id="topArea">
      <div id="progressBar"></div>
      <div id="pillTag">PC TIPS BY EZ_PETER</div>
      <div id="stepLabel"></div>
      <div id="sceneTitle">PC Running Extremely Slow</div>
      <div id="breadcrumb">System Stuttering & Lag Detected</div>
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
    window.ALIGNED_CAPTIONS = {aligned_json_str};
    let ALIGNED_CAPTIONS = window.ALIGNED_CAPTIONS;
    let SCRIPT = {script_json_str};
    window.SCRIPT = SCRIPT;

    // Initialize progress bar segments based on script length
    const progBar = document.getElementById('progressBar');
    progBar.innerHTML = '';
    for (let i = 0; i < SCRIPT.length; i++) {{
      const seg = document.createElement('div');
      seg.className = 'prog-seg';
      seg.innerHTML = '<div class="prog-fill"></div>';
      progBar.appendChild(seg);
    }}

    // Helper easing functions
    function easeOutCubic(x) {{ return 1 - Math.pow(1 - x, 3); }}
    function easeInOutQuad(x) {{ return x < 0.5 ? 2 * x * x : 1 - Math.pow(-2 * x + 2, 2) / 2; }}
    function clamp(val, min, max) {{ return Math.max(min, Math.min(max, val)); }}

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
        <div class="tb-clock">10:24 AM<br><span style="font-size:11px;color:#64748b;">11/23/2026</span></div>
      </div>
    `;

    // Cursor SVG markup
    function cursorHTML(x, y, click = false) {{
      return `
        <div class="win-cursor" style="left:${{x}}px; top:${{y}}px; transform:${{click ? 'scale(0.85)' : 'scale(1)'}};">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="#000000" stroke="#ffffff" stroke-width="1.5">
            <path d="M3 3l7 18 3-7 7-3L3 3z"/>
          </svg>
        </div>
        ${{click ? `<div class="click-ripple" style="left:${{x}}px; top:${{y}}px;"></div>` : ''}}
      `;
    }}

    // REUSABLE SCENE COMPONENT RENDERER (78 Dynamic RAMMap Scenes)
    function renderScreenScene(graphic, tau, t) {{
      const eTau = easeOutCubic(tau);

      // 1. PC SLOW & HIGH RAM
      if (graphic.startsWith('sec00') || graphic.startsWith('sec01')) {{
        const fps = Math.round(22 + Math.sin(tau * Math.PI * 4) * 3);
        return `
          <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
            <div style="background:rgba(255,255,255,0.95); border-radius:18px; padding:28px 44px; text-align:center; box-shadow:0 15px 35px rgba(0,0,0,0.12); border:1px solid #fed7d7; width:680px;">
              <div style="display:inline-block; background:#fee2e2; color:#dc2626; padding:6px 18px; border-radius:20px; font-weight:800; font-size:15px; margin-bottom:12px;">🚨 CRITICAL PERFORMANCE ALERT</div>
              <div style="font-size:36px; font-weight:900; color:#991b1b; margin-bottom:6px;">PC Slow & Micro-Stuttering</div>
              <div style="font-size:52px; font-weight:900; color:#dc2626; margin:8px 0;">${{fps}} FPS</div>
              <div style="font-size:16px; color:#64748b; font-weight:600;">Severe Frame Drop Detected In Games</div>
            </div>
            ${{winTaskbarHTML}}
          </div>
        `;
      }} else if (graphic.startsWith('sec02') || graphic.startsWith('sec03')) {{
        const pct = (94.2 + tau * 0.4).toFixed(1);
        return `
          <div class="win-desktop" style="padding:24px;">
            <div class="win-window" style="width:100%; height:calc(100% - 60px);">
              <div class="win-titlebar">
                <span>Task Manager - Performance</span>
                <div class="win-controls"><span>─</span><span>□</span><span>✕</span></div>
              </div>
              <div style="padding:20px; display:flex; flex-direction:column; gap:14px;">
                <div style="display:flex; justify-content:space-between; font-weight:800; font-size:18px;">
                  <span>Memory (RAM)</span>
                  <span style="color:#dc2626;">${{pct}}% Consumed</span>
                </div>
                <div style="width:100%; height:24px; background:#f1f5f9; border-radius:12px; overflow:hidden; border:1px solid #fca5a5;">
                  <div style="width:${{pct}}%; height:100%; background:linear-gradient(90deg, #f87171, #dc2626);"></div>
                </div>
                <div style="font-size:16px; font-weight:700; color:#1e293b;">15.1 GB of 16.0 GB In Use (94%)</div>
                <div style="background:#fef2f2; border:1px solid #fecaca; border-radius:8px; padding:10px 14px; font-size:14px; color:#991b1b; font-weight:600;">
                  ⚠️ Standby cache leak hoards 8.8 GB even when idle!
                </div>
              </div>
            </div>
            ${{winTaskbarHTML}}
          </div>
        `;
      }} else if (graphic.startsWith('sec04') || graphic.startsWith('sec05') || graphic.startsWith('sec06') || graphic.startsWith('sec07')) {{
        return `
          <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
            <div style="background:rgba(255,255,255,0.95); border-radius:18px; padding:28px 44px; text-align:center; box-shadow:0 15px 35px rgba(0,0,0,0.12); border:1px solid #e2e8f0; width:680px;">
              <div style="font-size:42px; margin-bottom:8px;">💻</div>
              <div style="font-size:26px; font-weight:900; color:#0f172a; margin-bottom:4px;">Desktop Completely Idle</div>
              <div style="font-size:18px; color:#dc2626; font-weight:800; margin-bottom:10px;">Barely Anything Open... Yet 15 GB Locked!</div>
              <div style="font-size:15px; color:#64748b;">Hidden Windows Cache Hoarding Memory</div>
            </div>
            ${{winTaskbarHTML}}
          </div>
        `;
      }}

      // 2. RAM EXPENSIVE & SOLUTION
      else if (graphic.startsWith('sec08') || graphic.startsWith('sec09')) {{
        return `
          <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
            <div style="background:rgba(255,255,255,0.95); border-radius:18px; padding:28px 44px; text-align:center; box-shadow:0 15px 35px rgba(0,0,0,0.12); border:1px solid #cbd5e1; width:680px;">
              <div style="font-size:20px; font-weight:800; color:#d97706; text-transform:uppercase; margin-bottom:6px;">DDR4 / DDR5 RAM Prices</div>
              <div style="font-size:48px; font-weight:900; color:#0f172a; margin-bottom:8px;">$120 — $250+</div>
              <div style="font-size:18px; color:#16a34a; font-weight:800;">Don't Buy More RAM! Fix It For Free!</div>
            </div>
            ${{winTaskbarHTML}}
          </div>
        `;
      }} else if (graphic.startsWith('sec10') || graphic.startsWith('sec11') || graphic.startsWith('sec12') || graphic.startsWith('sec13')) {{
        return `
          <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
            <div style="background:rgba(255,255,255,0.95); border-radius:18px; padding:28px 44px; text-align:center; box-shadow:0 15px 35px rgba(0,0,0,0.12); border:1px solid #bfdbfe; width:680px;">
              <div style="display:inline-block; background:#dbeafe; color:#1a6cf0; padding:6px 18px; border-radius:20px; font-weight:800; font-size:15px; margin-bottom:8px;">OFFICIAL MICROSOFT UTILITY</div>
              <div style="font-size:44px; font-weight:900; color:#1a6cf0; margin-bottom:6px;">RAMMap</div>
              <div style="font-size:16px; color:#64748b; font-weight:600;">Advanced Physical Memory Visualizer</div>
            </div>
            ${{winTaskbarHTML}}
          </div>
        `;
      }}

      // 3. STEP 1: SEARCH RAMMAP
      else if (graphic.startsWith('sec14')) {{
        const typed = "RAMMap".substring(0, Math.floor(tau * 6) + 1);
        return `
          <div class="win-desktop" style="padding:20px;">
            <div class="win-window" style="width:100%; height:calc(100% - 50px);">
              <div class="win-titlebar">
                <span>Google Search - Microsoft Edge</span>
                <div class="win-controls"><span>─</span><span>□</span><span>✕</span></div>
              </div>
              <div style="padding:30px; display:flex; flex-direction:column; align-items:center; gap:20px;">
                <div style="font-size:36px; font-weight:900; color:#1e293b;">Google</div>
                <div style="width:80%; background:#f8fafc; border:2px solid #cbd5e1; border-radius:24px; padding:12px 24px; font-size:22px; color:#0f172a; display:flex; justify-content:space-between; align-items:center;">
                  <span>${{typed}}<span style="color:#1a6cf0;">|</span></span>
                  <span>🔍</span>
                </div>
                <div style="font-size:15px; color:#64748b; font-weight:600;">Step 1: Type "RAMMap" in search</div>
              </div>
            </div>
            ${{winTaskbarHTML}}
          </div>
        `;
      }} else if (graphic.startsWith('sec15') || graphic.startsWith('sec16')) {{
        const cx = 380 + tau * 40;
        const cy = 180 + tau * 15;
        return `
          <div class="win-desktop" style="padding:20px;">
            <div class="win-window" style="width:100%; height:calc(100% - 50px);">
              <div class="win-titlebar">
                <span>RAMMap Search Results - Microsoft Edge</span>
                <div class="win-controls"><span>─</span><span>□</span><span>✕</span></div>
              </div>
              <div style="padding:24px; display:flex; flex-direction:column; gap:8px;">
                <div style="font-size:14px; color:#64748b;">https://learn.microsoft.com › sysinternals › rammap</div>
                <div style="font-size:24px; font-weight:800; color:#1a6cf0; text-decoration:underline;">RAMMap - Sysinternals | Microsoft Learn</div>
                <div style="font-size:14px; color:#334155; line-height:1.4;">RAMMap is an advanced physical memory usage analysis utility for Windows. Free download from official Microsoft site.</div>
                <div style="margin-top:10px; display:inline-block; background:#dcfce7; color:#16a34a; padding:6px 14px; border-radius:14px; font-size:13px; font-weight:700;">
                  ✓ Verified Official Microsoft Domain
                </div>
              </div>
            </div>
            ${{cursorHTML(cx, cy, graphic.startsWith('sec16'))}}
            ${{winTaskbarHTML}}
          </div>
        `;
      }}

      // 4. VIRUS CHECK & MICROSOFT VERIFIED
      else if (graphic.startsWith('sec17') || graphic.startsWith('sec18') || graphic.startsWith('sec19')) {{
        return `
          <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
            <div style="background:rgba(255,255,255,0.95); border-radius:18px; padding:28px 44px; text-align:center; box-shadow:0 15px 35px rgba(0,0,0,0.12); border:1px solid #fecaca; width:680px;">
              <div style="font-size:20px; font-weight:800; color:#dc2626; margin-bottom:8px;">💬 COMMENTS CONCERN</div>
              <div style="font-size:38px; font-weight:900; color:#1e293b; margin-bottom:8px;">"Is It Actually Safe?"</div>
              <div style="font-size:16px; color:#64748b;">Zero third-party bloat • 100% Genuine System Tool</div>
            </div>
            ${{winTaskbarHTML}}
          </div>
        `;
      }} else if (graphic.startsWith('sec20') || graphic.startsWith('sec21')) {{
        return `
          <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
            <div style="background:rgba(255,255,255,0.95); border-radius:18px; padding:28px 44px; text-align:center; box-shadow:0 15px 35px rgba(0,0,0,0.12); border:1px solid #bbf7d0; width:680px;">
              <div style="font-size:48px; margin-bottom:8px;">🛡️</div>
              <div style="font-size:36px; font-weight:900; color:#16a34a; margin-bottom:6px;">100% Official Microsoft Site</div>
              <div style="font-size:18px; font-weight:700; color:#1a6cf0; margin-bottom:8px;">learn.microsoft.com/sysinternals</div>
              <div style="font-size:14px; color:#64748b;">Created by Microsoft CTO Mark Russinovich</div>
            </div>
            ${{winTaskbarHTML}}
          </div>
        `;
      }}

      // 5. STEP 2: DOWNLOAD RAMMAP
      else if (graphic.startsWith('sec22') || graphic.startsWith('sec23') || graphic.startsWith('sec24')) {{
        const isClick = graphic.startsWith('sec24');
        return `
          <div class="win-desktop" style="padding:20px;">
            <div class="win-window" style="width:100%; height:calc(100% - 50px);">
              <div class="win-titlebar">
                <span>Microsoft Learn - RAMMap Download</span>
                <div class="win-controls"><span>─</span><span>□</span><span>✕</span></div>
              </div>
              <div style="padding:32px; display:flex; flex-direction:column; align-items:center; gap:16px;">
                <div style="font-size:24px; font-weight:800; color:#0f172a;">Download RAMMap</div>
                <div style="background:${{isClick ? '#1657c7' : '#1a6cf0'}}; color:#fff; padding:16px 36px; border-radius:10px; font-size:22px; font-weight:800; box-shadow:0 8px 24px rgba(26,108,240,0.3); transform:${{isClick ? 'scale(0.96)' : 'scale(1)'}};">
                  ⬇️ Download RAMMap (671 KB)
                </div>
                <div style="font-size:14px; color:#64748b; font-weight:600;">Runs on Windows 10 & Windows 11 (64-bit / 32-bit)</div>
              </div>
            </div>
            ${{cursorHTML(480, 200, isClick)}}
            ${{winTaskbarHTML}}
          </div>
        `;
      }} else if (graphic.startsWith('sec25')) {{
        return `
          <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
            <div style="background:rgba(255,255,255,0.98); border-radius:12px; padding:24px 36px; box-shadow:0 20px 45px rgba(0,0,0,0.18); border:1px solid #cbd5e1; width:640px;">
              <div style="font-size:18px; font-weight:800; color:#1e293b; margin-bottom:12px;">Save As...</div>
              <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:6px; padding:10px 14px; font-size:16px; font-weight:600; color:#0f172a; margin-bottom:14px;">
                File: RAMMap.zip (671 KB)
              </div>
              <div style="font-size:14px; color:#16a34a; font-weight:700;">✓ Saved to Downloads Folder</div>
            </div>
            ${{winTaskbarHTML}}
          </div>
        `;
      }}

      // 6. STEP 3: RUN AS ADMINISTRATOR
      else if (graphic.startsWith('sec26') || graphic.startsWith('sec27')) {{
        return `
          <div class="win-desktop" style="padding:20px;">
            <div class="win-window" style="width:100%; height:calc(100% - 50px);">
              <div class="win-titlebar">
                <span>File Explorer - Downloads</span>
                <div class="win-controls"><span>─</span><span>□</span><span>✕</span></div>
              </div>
              <div style="padding:24px; display:flex; gap:20px; align-items:center;">
                <div style="font-size:52px;">📁</div>
                <div>
                  <div style="font-size:20px; font-weight:800; color:#0f172a;">RAMMap64.exe</div>
                  <div style="font-size:14px; color:#64748b;">Sysinternals Memory Tool • Application</div>
                </div>
              </div>
            </div>
            ${{winTaskbarHTML}}
          </div>
        `;
      }} else if (graphic.startsWith('sec28') || graphic.startsWith('sec29')) {{
        const isRun = graphic.startsWith('sec29');
        return `
          <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
            <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:8px; width:320px; box-shadow:0 15px 35px rgba(0,0,0,0.18); overflow:hidden;">
              <div style="padding:10px 16px; font-size:15px; font-weight:700; color:#334155; border-bottom:1px solid #f1f5f9;">RAMMap64.exe</div>
              <div style="padding:12px 16px; background:${{isRun ? '#1a6cf0' : '#f8fafc'}}; color:${{isRun ? '#ffffff' : '#0f172a'}}; font-size:15px; font-weight:700; display:flex; align-items:center; gap:10px;">
                <span>🛡️</span>
                <span>Run as administrator</span>
              </div>
              <div style="padding:8px 16px; font-size:14px; color:#64748b;">Open</div>
              <div style="padding:8px 16px; font-size:14px; color:#64748b;">Properties</div>
            </div>
            ${{cursorHTML(540, 260, isRun)}}
            ${{winTaskbarHTML}}
          </div>
        `;
      }} else if (graphic.startsWith('sec30') || graphic.startsWith('sec31') || graphic.startsWith('sec32')) {{
        return `
          <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
            <div style="background:rgba(255,255,255,0.95); border-radius:18px; padding:28px 44px; text-align:center; box-shadow:0 15px 35px rgba(0,0,0,0.12); border:1px solid #bfdbfe; width:680px;">
              <div style="font-size:44px; margin-bottom:8px;">⏳</div>
              <div style="font-size:32px; font-weight:900; color:#1a6cf0; margin-bottom:6px;">Loading Memory Processes...</div>
              <div style="font-size:15px; color:#64748b;">Scanning all active physical RAM pages</div>
            </div>
            ${{winTaskbarHTML}}
          </div>
        `;
      }}

      // 7. REAL-TIME RAMMAP DASHBOARD & 45% BREAKDOWN
      else if (graphic.startsWith('sec33') || graphic.startsWith('sec34') || graphic.startsWith('sec35') || graphic.startsWith('sec36') || graphic.startsWith('sec37')) {{
        return `
          <div class="win-desktop" style="padding:16px;">
            <div class="win-window" style="width:100%; height:calc(100% - 50px);">
              <div class="win-titlebar">
                <span>RAMMap v1.61 - Sysinternals: www.sysinternals.com</span>
                <div class="win-controls"><span>─</span><span>□</span><span>✕</span></div>
              </div>
              <div class="rammap-app">
                <div class="rm-menubar">
                  <span class="rm-menu-item">File</span>
                  <span class="rm-menu-item">Empty</span>
                  <span class="rm-menu-item">Configure</span>
                  <span class="rm-menu-item">Help</span>
                </div>
                <div style="padding:12px;">
                  <table class="rm-table">
                    <tr><th>Use Type</th><th>Active</th><th>Standby</th><th>Total</th></tr>
                    <tr><td>Process Private</td><td>4,210 MB</td><td>-</td><td>4,210 MB</td></tr>
                    <tr><td>Mapped File</td><td>1,120 MB</td><td>4,810 MB</td><td>5,930 MB</td></tr>
                    <tr><td>Paged Pool</td><td>680 MB</td><td>-</td><td>680 MB</td></tr>
                    <tr><td>Driver Locked</td><td>1,210 MB</td><td>-</td><td>1,210 MB</td></tr>
                    <tr style="background:#e0edfe; font-weight:700; color:#1a6cf0;">
                      <td>Total Physical</td><td>7,220 MB (45%)</td><td>8,450 MB (Standby)</td><td>16,000 MB</td>
                    </tr>
                  </table>
                </div>
              </div>
            </div>
            ${{winTaskbarHTML}}
          </div>
        `;
      }} else if (graphic.startsWith('sec38') || graphic.startsWith('sec39') || graphic.startsWith('sec40') || graphic.startsWith('sec41') || graphic.startsWith('sec42')) {{
        return `
          <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
            <div style="background:rgba(255,255,255,0.95); border-radius:18px; padding:28px 44px; text-align:center; box-shadow:0 15px 35px rgba(0,0,0,0.12); border:1px solid #cbd5e1; width:680px;">
              <div style="display:inline-block; background:#dbeafe; color:#1a6cf0; padding:6px 16px; border-radius:20px; font-weight:800; font-size:15px; margin-bottom:8px;">REAL-TIME RAM TELEMETRY</div>
              <div style="font-size:46px; font-weight:900; color:#1e293b; margin-bottom:6px;">45% In Active Use</div>
              <div style="font-size:22px; font-weight:800; color:#dc2626; margin-bottom:6px;">+ 50% Trapped in Standby Cache!</div>
              <div style="font-size:15px; color:#64748b;">No memory left for games ➔ Stutters & lag!</div>
            </div>
            ${{winTaskbarHTML}}
          </div>
        `;
      }}

      // 8. STEP 4: CLICK EMPTY WORKING SETS
      else if (graphic.startsWith('sec43') || graphic.startsWith('sec44')) {{
        return `
          <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
            <div style="background:rgba(255,255,255,0.95); border-radius:18px; padding:28px 44px; text-align:center; box-shadow:0 15px 35px rgba(0,0,0,0.12); border:1px solid #bfdbfe; width:680px;">
              <div style="font-size:20px; font-weight:800; color:#1a6cf0; margin-bottom:8px;">STEP 4: EMPTY MENU</div>
              <div style="font-size:36px; font-weight:900; color:#1e293b; margin-bottom:8px;">Top Menu Bar: "Empty"</div>
              <div style="font-size:16px; color:#64748b;">File • <b style="color:#1a6cf0; text-decoration:underline;">Empty</b> • Configure • Help</div>
            </div>
            ${{winTaskbarHTML}}
          </div>
        `;
      }} else if (graphic.startsWith('sec45') || graphic.startsWith('sec46') || graphic.startsWith('sec47')) {{
        const isClick = graphic.startsWith('sec47');
        return `
          <div class="win-desktop" style="padding:16px;">
            <div class="win-window" style="width:100%; height:calc(100% - 50px);">
              <div class="win-titlebar">
                <span>RAMMap v1.61 - [Empty Menu]</span>
                <div class="win-controls"><span>─</span><span>□</span><span>✕</span></div>
              </div>
              <div class="rammap-app" style="position:relative;">
                <div class="rm-menubar">
                  <span class="rm-menu-item">File</span>
                  <span class="rm-menu-item active">Empty</span>
                  <span class="rm-menu-item">Configure</span>
                  <span class="rm-menu-item">Help</span>
                </div>
                <div class="rm-dropdown">
                  <div class="rm-drop-item highlight">
                    <span>⚡ Empty Working Sets</span>
                    <span>✓</span>
                  </div>
                  <div class="rm-drop-item">Empty System Working Set</div>
                  <div class="rm-drop-item">Empty Modified Page List</div>
                  <div class="rm-drop-item">Empty Standby List</div>
                  <div class="rm-drop-item">Empty Priority 0 Standby List</div>
                </div>
                <div style="padding:40px; text-align:center; color:#94a3b8; font-size:16px;">
                  Clicking "Empty Working Sets" flushes unneeded process RAM
                </div>
              </div>
            </div>
            ${{cursorHTML(170, 75, isClick)}}
            ${{winTaskbarHTML}}
          </div>
        `;
      }}

      // 9. WORKING SETS LOWERING
      else if (graphic.startsWith('sec48') || graphic.startsWith('sec49') || graphic.startsWith('sec50') || graphic.startsWith('sec51')) {{
        const pct = Math.max(28, Math.round(45 - tau * 15));
        return `
          <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
            <div style="background:rgba(255,255,255,0.95); border-radius:18px; padding:28px 44px; text-align:center; box-shadow:0 15px 35px rgba(0,0,0,0.12); border:1px solid #bbf7d0; width:680px;">
              <div style="display:inline-block; background:#dcfce7; color:#16a34a; padding:6px 18px; border-radius:20px; font-weight:800; font-size:15px; margin-bottom:8px;">WORKING SETS FLUSHED! ⚡</div>
              <div style="font-size:52px; font-weight:900; color:#16a34a; margin-bottom:6px;">${{pct}}%</div>
              <div style="font-size:18px; font-weight:700; color:#1e293b; margin-bottom:4px;">Memory Usage Plunging In Real Time</div>
              <div style="font-size:14px; color:#64748b;">Now let's free up the Standby List!</div>
            </div>
            ${{winTaskbarHTML}}
          </div>
        `;
      }}

      // 10. STEP 5: EMPTY STANDBY LIST
      else if (graphic.startsWith('sec52') || graphic.startsWith('sec53') || graphic.startsWith('sec54')) {{
        return `
          <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
            <div style="background:rgba(255,255,255,0.95); border-radius:18px; padding:28px 44px; text-align:center; box-shadow:0 15px 35px rgba(0,0,0,0.12); border:1px solid #bfdbfe; width:680px;">
              <div style="font-size:20px; font-weight:800; color:#1a6cf0; margin-bottom:8px;">STEP 5: EMPTY STANDBY LIST</div>
              <div style="font-size:36px; font-weight:900; color:#1e293b; margin-bottom:8px;">Reclaim Ghost Memory</div>
              <div style="font-size:16px; color:#64748b;">Flushes cached data from closed programs</div>
            </div>
            ${{winTaskbarHTML}}
          </div>
        `;
      }} else if (graphic.startsWith('sec55') || graphic.startsWith('sec56')) {{
        const isClick = graphic.startsWith('sec56');
        return `
          <div class="win-desktop" style="padding:16px;">
            <div class="win-window" style="width:100%; height:calc(100% - 50px);">
              <div class="win-titlebar">
                <span>RAMMap v1.61 - [Empty Standby List]</span>
                <div class="win-controls"><span>─</span><span>□</span><span>✕</span></div>
              </div>
              <div class="rammap-app" style="position:relative;">
                <div class="rm-menubar">
                  <span class="rm-menu-item">File</span>
                  <span class="rm-menu-item active">Empty</span>
                  <span class="rm-menu-item">Configure</span>
                  <span class="rm-menu-item">Help</span>
                </div>
                <div class="rm-dropdown">
                  <div class="rm-drop-item">Empty Working Sets</div>
                  <div class="rm-drop-item">Empty System Working Set</div>
                  <div class="rm-drop-item">Empty Modified Page List</div>
                  <div class="rm-drop-item highlight">
                    <span>🔥 Empty Standby List</span>
                    <span>✓</span>
                  </div>
                  <div class="rm-drop-item">Empty Priority 0 Standby List</div>
                </div>
              </div>
            </div>
            ${{cursorHTML(170, 140, isClick)}}
            ${{winTaskbarHTML}}
          </div>
        `;
      }}

      // 11. WHAT IS STANDBY LIST (CLOSED APPS STILL IN RAM)
      else if (graphic.startsWith('sec57') || graphic.startsWith('sec58') || graphic.startsWith('sec59') || graphic.startsWith('sec60')) {{
        return `
          <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
            <div style="background:rgba(255,255,255,0.95); border-radius:18px; padding:28px 44px; text-align:center; box-shadow:0 15px 35px rgba(0,0,0,0.12); border:1px solid #cbd5e1; width:680px;">
              <div style="display:inline-block; background:#fee2e2; color:#dc2626; padding:6px 16px; border-radius:20px; font-weight:800; font-size:15px; margin-bottom:8px;">GHOST MEMORY CACHE</div>
              <div style="font-size:32px; font-weight:900; color:#0f172a; margin-bottom:6px;">Closed Apps Still In RAM!</div>
              <div style="font-size:16px; color:#64748b; line-height:1.4;">Chrome tabs, Discord & games you closed hours ago are still hoarding your memory.</div>
            </div>
            ${{winTaskbarHTML}}
          </div>
        `;
      }}

      // 12. OVER 10 GIGS AVAILABLE NOW
      else if (graphic.startsWith('sec61') || graphic.startsWith('sec62') || graphic.startsWith('sec63') || graphic.startsWith('sec64')) {{
        const gigs = (10.2 + tau * 0.4).toFixed(1);
        return `
          <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
            <div style="background:rgba(255,255,255,0.95); border-radius:18px; padding:28px 44px; text-align:center; box-shadow:0 15px 35px rgba(0,0,0,0.12); border:1px solid #bbf7d0; width:680px;">
              <div style="display:inline-block; background:#dcfce7; color:#16a34a; padding:6px 18px; border-radius:20px; font-weight:800; font-size:16px; margin-bottom:8px;">MASSIVE RAM RESTORED! 🚀</div>
              <div style="font-size:52px; font-weight:900; color:#16a34a; margin-bottom:6px;">+${{gigs}} GB FREE</div>
              <div style="font-size:18px; font-weight:800; color:#1e293b;">Available Memory: 13.5 GB / 16 GB</div>
            </div>
            ${{winTaskbarHTML}}
          </div>
        `;
      }}

      // 13. 144 FPS GAMING & SMOOTH HEAVY TASKS
      else if (graphic.startsWith('sec65') || graphic.startsWith('sec66') || graphic.startsWith('sec67') || graphic.startsWith('sec68') || graphic.startsWith('sec69') || graphic.startsWith('sec70')) {{
        const fps = Math.round(144 + Math.sin(tau * Math.PI * 2) * 2);
        return `
          <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
            <div style="background:rgba(255,255,255,0.95); border-radius:18px; padding:28px 44px; text-align:center; box-shadow:0 15px 35px rgba(0,0,0,0.12); border:1px solid #bbf7d0; width:680px;">
              <div style="display:inline-block; background:#dcfce7; color:#16a34a; padding:6px 18px; border-radius:20px; font-weight:800; font-size:15px; margin-bottom:8px;">🎮 GAMING BENCHMARK RESTORED</div>
              <div style="font-size:54px; font-weight:900; color:#16a34a; margin-bottom:6px;">${{fps}} FPS SOLID</div>
              <div style="font-size:18px; font-weight:800; color:#0f172a; margin-bottom:4px;">Zero Stutters • Butter Smooth Frame Times</div>
              <div style="font-size:14px; color:#64748b;">Heavy Tasks & Editing Run Flawlessly</div>
            </div>
            ${{winTaskbarHTML}}
          </div>
        `;
      }}

      // 14. OUTRO & FULL PC OPTIMIZATION
      else {{
        return `
          <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
            <div style="background:rgba(255,255,255,0.95); border-radius:18px; padding:28px 44px; text-align:center; box-shadow:0 15px 35px rgba(0,0,0,0.12); border:1px solid #bfdbfe; width:680px;">
              <div style="display:inline-block; background:#dbeafe; color:#1a6cf0; padding:6px 18px; border-radius:20px; font-weight:800; font-size:15px; margin-bottom:8px;">PC • WINDOWS • BIOS • GAMES</div>
              <div style="font-size:42px; font-weight:900; color:#1a6cf0; margin-bottom:6px;">PC Tips by Ez_peter</div>
              <div style="font-size:26px; font-weight:800; color:#16a34a; margin-bottom:8px;">Follow @Ez_peter 🚀</div>
              <div style="font-size:14px; color:#64748b;">Save & Share For Daily Windows Hacks!</div>
            </div>
            ${{winTaskbarHTML}}
          </div>
        `;
      }}
    }}

    // MAIN DETERMINISTIC RENDER FUNCTION: window.renderAt(t)
    window.renderAt = function(t) {{
      if (!SCRIPT || SCRIPT.length === 0) return;

      const totalSeconds = SCRIPT.length;
      const clampedT = clamp(t, 0, totalSeconds - 0.001);
      const s = Math.floor(clampedT);
      const tau = clampedT - s;
      const currentItem = SCRIPT[s];

      // 1. UPDATE PROGRESS BAR
      const fills = document.querySelectorAll('.prog-fill');
      fills.forEach((fill, idx) => {{
        if (idx < s) {{
          fill.style.width = '100%';
        }} else if (idx === s) {{
          fill.style.width = `${{tau * 100}}%`;
        }} else {{
          fill.style.width = '0%';
        }}
      }});

      // 2. UPDATE TOP TEXT
      const stepLabelEl = document.getElementById('stepLabel');
      const titleEl = document.getElementById('sceneTitle');
      const breadcrumbEl = document.getElementById('breadcrumb');

      if (currentItem.stepNumber > 0) {{
        stepLabelEl.textContent = `STEP 0${{currentItem.stepNumber}}`;
      }} else {{
        stepLabelEl.textContent = '';
      }}
      titleEl.textContent = currentItem.title;
      breadcrumbEl.textContent = currentItem.breadcrumb;

      // 3. RENDER SCREEN SCENE
      const screenEl = document.getElementById('screen');
      screenEl.innerHTML = renderScreenScene(currentItem.graphic, tau, clampedT);

      // 4. RENDER CAPTIONS
      const capEl = document.getElementById('captions');
      if (window.hideCaptions) {{
        capEl.style.display = 'none';
      }} else {{
        capEl.style.display = 'flex';

        const chunks = ALIGNED_CAPTIONS.chunks;
        let activeChunk = null;
        for (let i = 0; i < chunks.length; i++) {{
          if (clampedT >= chunks[i].start && clampedT < chunks[i].display_end) {{
            activeChunk = chunks[i];
            break;
          }}
        }}
        if (!activeChunk && chunks.length > 0) {{
          if (clampedT >= chunks[chunks.length - 1].start) {{
            activeChunk = chunks[chunks.length - 1];
          }} else {{
            for (let i = 0; i < chunks.length - 1; i++) {{
              if (clampedT >= chunks[i].display_end && clampedT < chunks[i+1].start) {{
                activeChunk = chunks[i];
                break;
              }}
            }}
          }}
        }}

        if (activeChunk && activeChunk.words.length > 0) {{
          let activeWordIdx = 0;
          for (let i = 0; i < activeChunk.words.length; i++) {{
            if (clampedT >= activeChunk.words[i].global_start) {{
              activeWordIdx = i;
            }}
          }}

          capEl.innerHTML = activeChunk.words.map((w, idx) => {{
            const isActive = idx === activeWordIdx;
            return `<span class="caption-word ${{isActive ? 'word-active' : ''}}">${{w.text}}</span>`;
          }}).join('');
        }}
      }}

      // 5. RENDER CHARACTERS (Peter on Left, Stewie on Right)
      const peterEl = document.getElementById('peterImg');
      const stewieEl = document.getElementById('stewieImg');

      const turns = ALIGNED_CAPTIONS.turn_ranges;
      let activeTurn = null;
      for (let i = 0; i < turns.length; i++) {{
        if (clampedT >= turns[i].start && clampedT <= turns[i].end) {{
          activeTurn = turns[i];
          break;
        }}
      }}
      if (!activeTurn && turns.length > 0) {{
        for (let i = 0; i < turns.length - 1; i++) {{
          if (clampedT > turns[i].end && clampedT < turns[i+1].start) {{
            const mid = (turns[i].end + turns[i+1].start) / 2;
            if (clampedT < mid) {{
              activeTurn = turns[i];
            }} else {{
              activeTurn = turns[i+1];
            }}
            break;
          }}
        }}
        if (!activeTurn) activeTurn = turns[turns.length - 1];
      }}

      const isPeter = activeTurn && activeTurn.speaker === 'peter';
      const isStewie = activeTurn && activeTurn.speaker === 'stewie';

      if (isPeter) {{
        const turnElapsed = clampedT - activeTurn.start;
        const turnRemaining = activeTurn.end - clampedT;
        let peterX = 0;
        if (turnElapsed < 0.22) {{
          const inFrac = easeOutCubic(clamp(turnElapsed / 0.22, 0, 1));
          peterX = -1200 * (1 - inFrac);
        }} else if (turnRemaining < 0.22) {{
          const outFrac = easeInOutQuad(clamp((0.22 - turnRemaining) / 0.22, 0, 1));
          peterX = -1200 * outFrac;
        }}
        const bobY = Math.sin(clampedT * Math.PI * 4) * 6;
        const breathScale = 1.0 + 0.012 * Math.sin(clampedT * Math.PI * 2);
        peterEl.style.transform = `translateX(${{peterX}}px) translateY(${{bobY}}px) scale(${{breathScale}})`;
        stewieEl.style.transform = `translateX(1200px)`;
      }} else if (isStewie) {{
        const turnElapsed = clampedT - activeTurn.start;
        const turnRemaining = activeTurn.end - clampedT;
        let stewieX = 0;
        if (turnElapsed < 0.22) {{
          const inFrac = easeOutCubic(clamp(turnElapsed / 0.22, 0, 1));
          stewieX = 1200 * (1 - inFrac);
        }} else if (turnRemaining < 0.22) {{
          const outFrac = easeInOutQuad(clamp((0.22 - turnRemaining) / 0.22, 0, 1));
          stewieX = 1200 * outFrac;
        }}
        const bobY = Math.sin(clampedT * Math.PI * 4) * 6;
        const breathScale = 1.0 + 0.012 * Math.sin(clampedT * Math.PI * 2);
        stewieEl.style.transform = `translateX(${{stewieX}}px) translateY(${{bobY}}px) scale(${{breathScale}})`;
        peterEl.style.transform = `translateX(-1200px)`;
      }} else {{
        peterEl.style.transform = `translateX(-1200px)`;
        stewieEl.style.transform = `translateX(1200px)`;
      }}
    }};

    // Initial render
    window.renderAt(0);
  </script>
</body>
</html>
"""

with open("video-engine/index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Successfully generated video-engine/index.html with exact cream format for RAMMap!")
