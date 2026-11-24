import json

with open("video-engine/aligned_captions.json", "r", encoding="utf-8") as f:
    aligned_data = json.load(f)

with open("script.json", "r", encoding="utf-8") as f:
    script_data = json.load(f)

aligned_json_str = json.dumps(aligned_data)
script_json_str = json.dumps(script_data)

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Windows 11 Delivery Optimization - Video Engine</title>
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

    /* SETTINGS APP STYLING */
    .set-layout {{
      display: flex;
      height: calc(100% - 38px);
    }}
    .set-sidebar {{
      width: 220px;
      background: #f8fafc;
      border-right: 1px solid #e2e8f0;
      padding: 16px 10px;
    }}
    .set-side-nav {{
      padding: 8px 12px;
      border-radius: 6px;
      font-size: 14px;
      font-weight: 600;
      color: #475569;
      margin-bottom: 4px;
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .set-side-nav.active {{
      background: #e2e8f0;
      color: var(--accent);
    }}
    .set-content {{
      flex: 1;
      padding: 20px 24px;
      overflow-y: hidden;
    }}
    .set-card {{
      background: #ffffff;
      border: 1px solid #e2e8f0;
      border-radius: 8px;
      padding: 14px 18px;
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}
    .toggle-switch {{
      width: 48px;
      height: 24px;
      background: #cbd5e1;
      border-radius: 12px;
      position: relative;
      transition: background 0.2s;
    }}
    .toggle-switch.on {{
      background: var(--accent);
    }}
    .toggle-knob {{
      width: 18px;
      height: 18px;
      background: #ffffff;
      border-radius: 50%;
      position: absolute;
      top: 3px;
      left: 3px;
      transition: transform 0.2s;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
    }}
    .toggle-switch.on .toggle-knob {{
      transform: translateX(24px);
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
        <div class="tb-clock">10:24 AM<br><span style="font-size:11px;color:#64748b;">11/22/2026</span></div>
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

    // REUSABLE SCENE COMPONENT RENDERER
    function renderScreenScene(graphic, tau, t) {{
      const eTau = easeOutCubic(tau);
      
      switch (graphic) {{
        // --- 0 to 2: HOOK / DESKTOP / ALERT ---
        case 'win_desktop_normal':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:rgba(255,255,255,0.95); border-radius:18px; padding:32px 48px; text-align:center; box-shadow:0 15px 35px rgba(0,0,0,0.12); border:1px solid #e2e8f0; transform:scale(${{0.92 + 0.08 * eTau}});">
                <div style="font-size:48px; margin-bottom:10px;">💻</div>
                <div style="font-size:28px; font-weight:800; color:#1e293b; margin-bottom:8px;">Brand New Windows 11 PC</div>
                <div style="font-size:16px; color:#64748b; font-weight:600;">Fresh install • Default Out-of-Box Experience</div>
              </div>
              ${{winTaskbarHTML}}
            </div>
          `;

        case 'win_network_spike':
          return `
            <div class="win-desktop">
              <div style="position:absolute; right:24px; bottom:64px; width:360px; background:#ffffff; border-radius:12px; box-shadow:0 15px 35px rgba(0,0,0,0.2); border-left:6px solid var(--accent); padding:18px; transform:translateY(${{40 * (1 - eTau)}}px);">
                <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
                  <span style="font-size:22px;">📶</span>
                  <span style="font-weight:800; font-size:15px; color:#1e293b;">Heavy Background Activity</span>
                </div>
                <div style="font-size:14px; color:#475569; line-height:1.4;">Unexplained outbound upload traffic detected on port 7680...</div>
                <div style="margin-top:10px; font-size:12px; font-weight:700; color:var(--accent);">Windows Update Service (Active)</div>
              </div>
              ${{winTaskbarHTML}}
            </div>
          `;

        case 'warning_bandwidth_alert':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#dc2626; color:#fff; border-radius:18px; padding:32px 48px; text-align:center; box-shadow:0 20px 50px rgba(220,38,38,0.35); transform:scale(${{0.88 + 0.12 * eTau}});">
                <div style="font-size:52px; font-weight:900; margin-bottom:10px;">⚠ SECRET SEEDER DETECTED</div>
                <div style="font-size:22px; font-weight:700; opacity:0.95;">Your computer is uploading without your permission!</div>
              </div>
              ${{winTaskbarHTML}}
            </div>
          `;

        // --- 3 to 8: P2P CDN / SEEDING TO STRANGERS ---
        case 'p2p_seeding_strangers':
        case 'p2p_network_mesh':
        case 'p2p_seeding_counter':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:30px 40px; width:720px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:1px solid #e2e8f0; text-align:center;">
                <div style="font-size:24px; font-weight:900; color:#1e293b; margin-bottom:14px;">🌐 Peer-To-Peer Delivery Swarm</div>
                <div style="display:flex; justify-content:space-around; align-items:center; margin:20px 0;">
                  <div style="background:#eff6ff; border:2px solid var(--accent); border-radius:12px; padding:14px 20px;">
                    <div style="font-size:32px;">💻</div>
                    <div style="font-weight:800; font-size:14px; color:#1e3a8a;">YOUR PC</div>
                    <div style="font-size:11px; color:var(--accent); font-weight:700;">SEEDING (UPLOADING)</div>
                  </div>
                  <div style="font-size:32px; color:var(--accent); transform:translateX(${{Math.sin(tau * Math.PI) * 10}}px);">➔ ➔ ➔</div>
                  <div style="background:#fef2f2; border:2px solid var(--red); border-radius:12px; padding:14px 20px;">
                    <div style="font-size:32px;">🌍</div>
                    <div style="font-weight:800; font-size:14px; color:#991b1b;">STRANGERS</div>
                    <div style="font-size:11px; color:var(--red); font-weight:700;">14 ACTIVE PEERS</div>
                  </div>
                </div>
                <div style="font-size:14px; font-weight:600; color:#64748b;">Protocol: Windows Update Delivery Optimization (WUDO)</div>
              </div>
              ${{winTaskbarHTML}}
            </div>
          `;

        case 'cdn_cloud_offload':
        case 'global_pcs_map':
        case 'global_pcs_mesh':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:32px 48px; width:740px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:1px solid #e2e8f0; text-align:center;">
                <div style="font-size:28px; font-weight:900; color:#1e293b; margin-bottom:12px;">Microsoft's Free CDN Network</div>
                <div style="font-size:16px; color:#475569; margin-bottom:20px;">Every Windows 10 & 11 PC acts as a free server node.</div>
                <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:12px;">
                  <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:8px; padding:12px; font-weight:700; font-size:13px;">🇺🇸 PC #10294<br><span style="color:var(--accent);font-size:11px;">Uploading...</span></div>
                  <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:8px; padding:12px; font-weight:700; font-size:13px;">🇩🇪 PC #48291<br><span style="color:var(--accent);font-size:11px;">Downloading</span></div>
                  <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:8px; padding:12px; font-weight:700; font-size:13px;">🇬🇧 PC #30192<br><span style="color:var(--accent);font-size:11px;">Uploading...</span></div>
                  <div style="background:#eff6ff; border:2px solid var(--accent); border-radius:8px; padding:12px; font-weight:800; font-size:13px; color:var(--accent);">⭐ YOUR PC<br><span style="color:var(--red);font-size:11px;">SEEDING NOW</span></div>
                </div>
              </div>
              ${{winTaskbarHTML}}
            </div>
          `;

        // --- 9 to 15: BITTORRENT COMPARISON & DEFAULT NOTICE ---
        case 'bittorrent_comparison':
        case 'bittorrent_swarm':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:32px 48px; width:700px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:1px solid #e2e8f0; text-align:center;">
                <div style="font-size:42px; margin-bottom:12px;">⚡</div>
                <div style="font-size:28px; font-weight:900; color:#1e293b; margin-bottom:8px;">Just Like BitTorrent Seeding</div>
                <div style="font-size:15px; color:#64748b; line-height:1.5;">You download an update once, and Microsoft turns your PC into a permanent upload seeder for everyone else.</div>
              </div>
              ${{winTaskbarHTML}}
            </div>
          `;

        case 'secret_default_badge':
        case 'secret_terms_doc':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:32px 48px; width:680px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:1px solid #e2e8f0; text-align:center;">
                <div style="display:inline-block; background:#fee2e2; color:#dc2626; font-weight:900; font-size:16px; padding:6px 18px; border-radius:20px; margin-bottom:16px;">ENABLED BY DEFAULT</div>
                <div style="font-size:32px; font-weight:900; color:#1e293b; margin-bottom:10px;">Zero Setup Notifications</div>
                <div style="font-size:16px; color:#64748b;">Windows never asks: "Can we use your bandwidth?" It just turns it on.</div>
              </div>
              ${{winTaskbarHTML}}
            </div>
          `;

        case 'settings_toggle_preview':
        case 'network_toggle_badge':
        case 'bandwidth_question':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:32px 48px; width:700px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:1px solid #e2e8f0; text-align:center;">
                <div style="font-size:44px; margin-bottom:10px;">📶 ➔ ❓</div>
                <div style="font-size:32px; font-weight:900; color:#1e293b; margin-bottom:8px;">How Much Bandwidth?</div>
                <div style="font-size:16px; color:#64748b; font-weight:600;">Let's look at what's actually happening to your speed...</div>
              </div>
              ${{winTaskbarHTML}}
            </div>
          `;

        // --- 16 to 20: 80% UPLOAD & ZOOM FREEZE ---
        case 'upload_gauge_80':
        case 'upload_spike_graph':
          const pct = Math.min(80, Math.floor(40 + 40 * eTau));
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:32px 48px; width:720px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:1px solid #e2e8f0; text-align:center;">
                <div style="font-size:24px; font-weight:800; color:#1e293b; margin-bottom:14px;">Upload Bandwidth Consumption</div>
                <div style="font-size:72px; font-weight:900; color:var(--red); margin-bottom:8px;">${{pct}}%</div>
                <div style="background:#fee2e2; height:20px; border-radius:10px; overflow:hidden; margin-bottom:14px;">
                  <div style="width:${{pct}}%; height:100%; background:var(--red);"></div>
                </div>
                <div style="font-size:15px; font-weight:600; color:#64748b;">Consuming up to 80% of your maximum upstream pipe</div>
              </div>
              ${{winTaskbarHTML}}
            </div>
          `;

        case 'zoom_freeze_warning':
        case 'gaming_lag_alert':
        case 'zoom_lag_details':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#1e293b; color:#fff; border-radius:18px; padding:32px 44px; width:720px; box-shadow:0 20px 50px rgba(0,0,0,0.3); text-align:center; border:2px solid #ef4444;">
                <div style="font-size:36px; margin-bottom:8px;">📹 ⚠️</div>
                <div style="font-size:28px; font-weight:900; color:#f87171; margin-bottom:8px;">Zoom Call Frozen!</div>
                <div style="background:#334155; border-radius:8px; padding:12px; margin-bottom:14px; font-size:14px; font-family:monospace; color:#fca5a5;">
                  "Your internet connection is unstable • High Packet Loss"
                </div>
                <div style="font-size:14px; color:#cbd5e1;">Because Windows is uploading update files at full blast.</div>
              </div>
              ${{winTaskbarHTML}}
            </div>
          `;

        // --- 21 to 28: TERMS & TASK MANAGER HIDING ---
        case 'terms_service_modal':
        case 'terms_small_print':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div class="win-window" style="width:680px; height:400px;">
                <div class="win-titlebar"><span>Microsoft Services Agreement - Section 13(b)</span><div class="win-controls">─ ▢ ✕</div></div>
                <div style="padding:24px; font-size:14px; color:#334155; line-height:1.6; font-family:Georgia, serif;">
                  <div style="font-weight:700; margin-bottom:10px;">13.b Delivery Optimization:</div>
                  <div style="background:#fef3c7; border-left:4px solid #f59e0b; padding:12px; border-radius:4px; font-weight:600;">
                    "Windows may upload previously downloaded updates and apps to other PCs on your local network or on the Internet..."
                  </div>
                  <div style="margin-top:16px; color:#64748b; font-size:13px; font-family:sans-serif;">Buried on page 42 of the terms 99.9% of users never read.</div>
                </div>
              </div>
              ${{winTaskbarHTML}}
            </div>
          `;

        case 'task_manager_opening':
        case 'task_manager_disguise':
        case 'task_manager_svchost':
        case 'task_manager_bandwidth':
          return `
            <div class="win-desktop" style="padding:16px;">
              <div class="win-window" style="width:900px; height:470px;">
                <div class="win-titlebar"><span>Task Manager</span><div class="win-controls">─ ▢ ✕</div></div>
                <div style="padding:10px 16px; border-bottom:1px solid #e2e8f0; display:flex; gap:16px; font-size:13px; font-weight:600; color:#64748b;">
                  <span style="color:var(--accent); border-bottom:2px solid var(--accent); padding-bottom:4px;">Processes</span>
                  <span>Performance</span>
                  <span>App history</span>
                  <span>Startup apps</span>
                </div>
                <table style="width:100%; border-collapse:collapse; font-size:13px;">
                  <tr style="background:#f8fafc; color:#64748b; font-weight:700; border-bottom:1px solid #e2e8f0;">
                    <th style="text-align:left; padding:8px 14px;">Name</th>
                    <th style="padding:8px 10px;">CPU</th>
                    <th style="padding:8px 10px;">Memory</th>
                    <th style="padding:8px 10px; color:var(--red);">Network (Upload)</th>
                  </tr>
                  <tr style="background:#fee2e2; border-left:4px solid var(--red); font-weight:700;">
                    <td style="padding:10px 14px; color:#1e293b;">⚙ Service Host: Network Service</td>
                    <td style="text-align:center; padding:10px;">1.4%</td>
                    <td style="text-align:center; padding:10px;">48 MB</td>
                    <td style="text-align:center; padding:10px; color:var(--red); font-weight:900;">85.4 Mbps ⬆</td>
                  </tr>
                  <tr style="border-bottom:1px solid #f1f5f9; color:#64748b;">
                    <td style="padding:8px 14px;">📁 Windows Explorer</td>
                    <td style="text-align:center; padding:8px;">0.1%</td>
                    <td style="text-align:center; padding:8px;">72 MB</td>
                    <td style="text-align:center; padding:8px;">0 Mbps</td>
                  </tr>
                  <tr style="border-bottom:1px solid #f1f5f9; color:#64748b;">
                    <td style="padding:8px 14px;">🌐 Google Chrome</td>
                    <td style="text-align:center; padding:8px;">2.2%</td>
                    <td style="text-align:center; padding:8px;">340 MB</td>
                    <td style="text-align:center; padding:8px;">0.2 Mbps</td>
                  </tr>
                </table>
              </div>
              ${{winTaskbarHTML}}
            </div>
          `;

        case 'isp_blame_modal':
        case 'isp_router_normal':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:32px 48px; width:700px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:1px solid #e2e8f0; text-align:center;">
                <div style="font-size:42px; margin-bottom:10px;">📡 ❌</div>
                <div style="font-size:28px; font-weight:900; color:#1e293b; margin-bottom:8px;">Blaming Your ISP?</div>
                <div style="font-size:16px; color:#64748b; line-height:1.5;">You call Comcast, AT&T or Verizon complaining about lag... but your router is completely fine. Windows is secretly eating your upload!</div>
              </div>
              ${{winTaskbarHTML}}
            </div>
          `;

        // --- 29 to 34: 3.5 BILLION UPDATES & COSTS ---
        case 'why_microsoft_title':
        case 'stat_3_5_billion':
        case 'stat_server_costs':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:32px 48px; width:720px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:1px solid #e2e8f0; text-align:center;">
                <div style="font-size:22px; font-weight:800; color:var(--accent); margin-bottom:6px;">MICROSOFT SCALE</div>
                <div style="font-size:68px; font-weight:900; color:#1e293b; margin-bottom:10px;">3.5 BILLION</div>
                <div style="font-size:20px; font-weight:700; color:#64748b; margin-bottom:16px;">Updates Delivered Every Single Month</div>
                <div style="background:#eff6ff; color:var(--accent); font-weight:800; font-size:14px; padding:8px 18px; border-radius:20px; display:inline-block;">
                  P2P saves them hundreds of millions in server bandwidth
                </div>
              </div>
              ${{winTaskbarHTML}}
            </div>
          `;

        case 'electricity_bill_card':
        case 'internet_plan_cap':
        case 'datacenter_vs_user':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:32px 48px; width:700px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:1px solid #e2e8f0; text-align:center;">
                <div style="font-size:44px; margin-bottom:10px;">⚡ 💸</div>
                <div style="font-size:28px; font-weight:900; color:#1e293b; margin-bottom:8px;">Paid By Your Electricity & Data Cap</div>
                <div style="font-size:15px; color:#64748b; line-height:1.5;">They offload global cloud hosting costs directly onto your home internet bill and your computer's power draw.</div>
              </div>
              ${{winTaskbarHTML}}
            </div>
          `;

        // --- 35 to 41: OHIO TO GERMANY MAP ---
        case 'local_network_question':
        case 'local_vs_internet_toggle':
        case 'default_radio_internet':
        case 'strangers_worldwide_map':
        case 'ohio_to_germany_map':
        case 'gaming_laptop_uploading':
        case 'berlin_peer_receiving':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:30px 40px; width:740px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:1px solid #e2e8f0; text-align:center;">
                <div style="font-size:22px; font-weight:900; color:#1e293b; margin-bottom:12px;">🌍 Global Seeding In Action</div>
                <div style="display:flex; justify-content:space-between; align-items:center; margin:16px 0; background:#f8fafc; border-radius:12px; padding:16px 24px;">
                  <div style="text-align:left;">
                    <div style="font-size:28px;">🎮 🇺🇸</div>
                    <div style="font-weight:800; font-size:15px; color:#1e293b;">Gaming PC in Ohio</div>
                    <div style="font-size:12px; color:var(--red); font-weight:700;">Uploading Windows CABs</div>
                  </div>
                  <div style="font-size:26px; color:var(--accent);">════ ✈ ════</div>
                  <div style="text-align:right;">
                    <div style="font-size:28px;">🇩🇪 💻</div>
                    <div style="font-weight:800; font-size:15px; color:#1e293b;">Stranger in Germany</div>
                    <div style="font-size:12px; color:var(--green); font-weight:700;">Downloading From You</div>
                  </div>
                </div>
                <div style="font-size:14px; font-weight:600; color:#64748b;">The default setting permits seeding across the entire world.</div>
              </div>
              ${{winTaskbarHTML}}
            </div>
          `;

        // --- 42 to 63: TEASER / LOCAL VS INTERNET ---
        case 'stop_it_immediately':
        case 'stop_overview_card':
        case 'settings_icon_pop':
        case 'cdn_switch_ready':
        case 'bandwidth_lock_free':
        case 'step_intro_graphic':
        case 'step_intro_keycap':
        case 'step_intro_update':
        case 'step_intro_advanced':
        case 'step_intro_delivery':
        case 'step_intro_switch':
        case 'bandwidth_recap_badge':
        case 'zoom_restored_badge':
        case 'local_lan_diagram':
        case 'local_lan_details':
        case 'internet_toggle_risk':
        case 'radio_internet_selected':
        case 'misdirection_badge':
        case 'bandwidth_leak_card':
        case 'global_seeder_stop':
        case 'ohio_laptop_safe':
        case 'germany_disconnected':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:32px 48px; width:700px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:1px solid #e2e8f0; text-align:center;">
                <div style="font-size:44px; margin-bottom:10px;">🛠️</div>
                <div style="font-size:32px; font-weight:900; color:#1e293b; margin-bottom:8px;">How To Stop It Now</div>
                <div style="font-size:16px; color:#64748b; font-weight:600;">5 simple clicks in Windows Settings turns it off forever.</div>
              </div>
              ${{winTaskbarHTML}}
            </div>
          `;

        // --- 64 to 75: SETTINGS WALKTHROUGH & TOGGLE OFF ---
        case 'how_to_fix_title':
        case 'settings_action_open':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:36px 48px; width:680px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:1px solid #e2e8f0; text-align:center;">
                <div style="font-size:48px; margin-bottom:12px;">⌨️</div>
                <div style="font-size:24px; font-weight:800; color:var(--accent); margin-bottom:6px;">CLICK 1 OF 5</div>
                <div style="font-size:36px; font-weight:900; color:#1e293b; margin-bottom:10px;">Press Win + I</div>
                <div style="font-size:16px; color:#64748b;">Instantly opens the Windows Settings App</div>
              </div>
              ${{winTaskbarHTML}}
            </div>
          `;

        case 'settings_action_update':
        case 'settings_action_advanced':
        case 'settings_action_delivery':
        case 'settings_action_found':
        case 'settings_toggle_switch_on':
        case 'settings_cursor_approach':
        case 'settings_toggle_click':
        case 'settings_toggle_switch_off':
        case 'solution_confirmed_badge':
        case 'five_clicks_complete':
          const isOffState = ['settings_toggle_click', 'settings_toggle_switch_off', 'solution_confirmed_badge', 'five_clicks_complete'].includes(graphic);
          const curX = 520 + (740 - 520) * eTau;
          const curY = 180 + (224 - 180) * eTau;
          const isClickAction = graphic === 'settings_toggle_click';
          return `
            <div class="win-desktop" style="padding:16px;">
              <div class="win-window" style="width:900px; height:470px;">
                <div class="win-titlebar"><span>⚙ Settings › Windows Update › Advanced options › Delivery Optimization</span><div class="win-controls">─ ▢ ✕</div></div>
                <div class="set-layout">
                  <div class="set-sidebar">
                    <div class="set-side-nav">🖥 System</div>
                    <div class="set-side-nav">📶 Network & Internet</div>
                    <div class="set-side-nav active">🔄 Windows Update</div>
                  </div>
                  <div class="set-content">
                    <div style="font-size:22px; font-weight:800; color:#1e293b; margin-bottom:12px;">Delivery Optimization</div>
                    <div class="set-card" style="border-left:5px solid ${{isOffState ? 'var(--green)' : 'var(--accent)'}};">
                      <div>
                        <div style="font-weight:700; font-size:15px; color:#1e293b;">Allow downloads from other PCs</div>
                        <div style="font-size:12px; color:#64748b; margin-top:2px;">Send parts of previously downloaded Windows updates to PCs on your local network or the Internet.</div>
                      </div>
                      <div class="toggle-switch ${{isOffState ? '' : 'on'}}"><div class="toggle-knob"></div></div>
                    </div>
                    <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:12px; font-size:13px; color:#64748b; opacity:${{isOffState ? 0.4 : 1}};">
                      <div style="margin-bottom:6px; font-weight:600;">Allow downloads from:</div>
                      <div style="display:flex; align-items:center; gap:8px; margin-bottom:4px;">
                        <input type="radio" disabled> <span>Devices on my local network</span>
                      </div>
                      <div style="display:flex; align-items:center; gap:8px;">
                        <input type="radio" checked disabled> <span style="font-weight:700; color:#1e293b;">Devices on the Internet and my local network (Default)</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              ${{cursorHTML(curX, curY, isClickAction)}}
              ${{winTaskbarHTML}}
            </div>
          `;

        // --- 76 to 83: FREEDOM / SPEED RESTORED ---
        case 'bandwidth_freed_card':
        case 'no_longer_free_cdn':
        case 'speed_restored_gauge':
        case 'zoom_lag_cured':
        case 'ping_drops_card':
        case 'thats_it_confirm':
        case 'free_bandwidth_ended':
        case 'five_clicks_victory':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:32px 48px; width:700px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:2px solid var(--green); text-align:center;">
                <div style="font-size:52px; margin-bottom:10px;">✅ 🚀</div>
                <div style="font-size:32px; font-weight:900; color:var(--green); margin-bottom:8px;">Bandwidth Fully Restored!</div>
                <div style="font-size:16px; color:#1e293b; font-weight:700; margin-bottom:6px;">Delivery Optimization Disabled</div>
                <div style="font-size:14px; color:#64748b;">No more stranger uploads • Zero background seeding • Crisp Zoom calls</div>
              </div>
              ${{winTaskbarHTML}}
            </div>
          `;

        // --- 84 to 88: TASK MANAGER TRUTH ---
        case 'taskmgr_truth_card':
        case 'svchost_exposed':
        case 'windows_steals_bandwidth':
        case 'taskmgr_clean_state':
        case 'microsoft_filter_reveal':
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:18px; padding:32px 48px; width:720px; box-shadow:0 20px 45px rgba(0,0,0,0.15); border:1px solid #e2e8f0; text-align:center;">
                <div style="font-size:44px; margin-bottom:10px;">👁️</div>
                <div style="font-size:28px; font-weight:900; color:#1e293b; margin-bottom:8px;">The Truth About Task Manager</div>
                <div style="font-size:15px; color:#64748b; line-height:1.5;">Task Manager doesn't lie. It just shows you what Microsoft wants you to see. Now your network is 100% yours.</div>
              </div>
              ${{winTaskbarHTML}}
            </div>
          `;

        // --- 89 to 92: OUTRO & FOLLOW ---
        case 'mastery_summary_badge':
        case 'recap_action_card':
        case 'ez_peter_branding_card':
        case 'follow_ez_peter_cta':
        default:
          const pop = easeOutCubic(clamp(tau / 0.4, 0, 1));
          return `
            <div class="win-desktop" style="display:flex; align-items:center; justify-content:center;">
              <div style="background:#ffffff; border-radius:24px; padding:36px 54px; text-align:center; box-shadow:0 25px 60px rgba(26,108,240,0.25); border:2px solid var(--accent); transform:scale(${{0.88 + 0.12 * pop}});">
                <div style="font-size:52px; margin-bottom:10px;">🔔</div>
                <div style="font-size:36px; font-weight:900; color:#1e293b; margin-bottom:8px;">PC Tips by Ez_peter</div>
                <div style="font-size:18px; font-weight:600; color:#64748b; margin-bottom:18px;">Follow for more essential Windows secrets!</div>
                <div style="background:var(--accent); color:#fff; font-size:22px; font-weight:800; padding:12px 36px; border-radius:30px; display:inline-block; box-shadow:0 10px 25px rgba(26,108,240,0.35);">
                  Follow @Ez_peter
                </div>
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

      // 3. RENDER SCENE INSIDE LAPTOP SCREEN
      const screenEl = document.getElementById('screen');
      screenEl.innerHTML = renderScreenScene(currentItem.graphic, tau, clampedT);

      // 4. RENDER CAPTIONS - EXACT ACOUSTIC ALIGNMENT (NEVER DRIFTS)
      const capEl = document.getElementById('captions');
      if (window.hideCaptions) {{
        capEl.style.display = 'none';
      }} else {{
        capEl.style.display = 'flex';
        
        // Find the active caption chunk for time clampedT
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
      // Only ONE on screen at a time! Smooth slide in/out aligned to speaker turns
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

print(f"Successfully generated video-engine/index.html for {len(script_data)} seconds of dialogue!")
