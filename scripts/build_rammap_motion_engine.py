import json
import os

with open("video-engine/aligned_captions.json", "r", encoding="utf-8") as f:
    aligned_json = f.read()

with open("output/script.json", "r", encoding="utf-8") as f:
    script_json = f.read()

engine_html = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>PC Tips by Ez_peter - RAMMap Memory Optimization</title>
  <style>
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      user-select: none;
    }
    body {
      width: 1080px;
      height: 1920px;
      background: radial-gradient(circle at 50% 35%, #1a2236 0%, #0a0e17 70%, #04060a 100%);
      font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
      overflow: hidden;
      color: #ffffff;
      position: relative;
    }

    /* Ambient background grid */
    .bg-grid {
      position: absolute;
      top: 0; left: 0; width: 100%; height: 100%;
      background-image: 
        linear-gradient(to right, rgba(255, 255, 255, 0.03) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
      background-size: 60px 60px;
      pointer-events: none;
    }

    /* Radial glow highlights */
    .glow-sphere {
      position: absolute;
      width: 700px;
      height: 700px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(0, 120, 212, 0.15) 0%, rgba(0,0,0,0) 70%);
      top: 300px;
      left: 190px;
      pointer-events: none;
    }

    /* TOP BRANDING BAR */
    .header-bar {
      position: absolute;
      top: 60px;
      left: 60px;
      right: 60px;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 16px;
      z-index: 50;
    }

    .top-tag {
      background: rgba(0, 120, 212, 0.2);
      border: 1px solid rgba(0, 120, 212, 0.6);
      color: #60cdff;
      padding: 8px 24px;
      border-radius: 30px;
      font-size: 24px;
      font-weight: 700;
      letter-spacing: 2px;
      text-transform: uppercase;
      box-shadow: 0 0 20px rgba(0, 120, 212, 0.3);
    }

    .title-box {
      text-align: center;
      max-width: 900px;
    }

    .scene-title {
      font-size: 42px;
      font-weight: 800;
      color: #ffffff;
      line-height: 1.2;
      text-shadow: 0 4px 12px rgba(0,0,0,0.6);
      margin-bottom: 6px;
    }

    .breadcrumb {
      font-size: 24px;
      font-weight: 600;
      color: #9bb7d4;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
    }

    /* PROGRESS BAR */
    .progress-bar-container {
      width: 100%;
      height: 8px;
      background: rgba(255, 255, 255, 0.1);
      border-radius: 4px;
      overflow: hidden;
      display: flex;
      gap: 2px;
      margin-top: 10px;
    }

    .prog-seg {
      flex: 1;
      height: 100%;
      background: rgba(255, 255, 255, 0.15);
      position: relative;
    }

    .prog-fill {
      height: 100%;
      background: #0078d4;
      width: 0%;
    }

    /* CENTRAL DISPLAY (Laptop / Windows 11 UI frame) */
    .screen-stage {
      position: absolute;
      top: 310px;
      left: 80px;
      width: 920px;
      height: 600px;
      z-index: 30;
      perspective: 1000px;
    }

    .laptop-frame {
      width: 100%;
      height: 100%;
      background: #0f141c;
      border: 3px solid rgba(255, 255, 255, 0.12);
      border-radius: 20px;
      box-shadow: 0 30px 80px rgba(0, 0, 0, 0.8), 0 0 40px rgba(0, 120, 212, 0.25);
      overflow: hidden;
      display: flex;
      flex-direction: column;
      position: relative;
    }

    /* Windows 11 Title Bar */
    .win-titlebar {
      height: 48px;
      background: rgba(255, 255, 255, 0.05);
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 20px;
    }

    .win-title-left {
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 20px;
      font-weight: 600;
      color: #e0e6ed;
    }

    .win-logo {
      width: 22px;
      height: 22px;
    }

    .win-controls {
      display: flex;
      gap: 14px;
    }

    .win-btn {
      width: 14px;
      height: 14px;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.2);
    }
    .win-btn.close { background: #ff5f56; }
    .win-btn.min { background: #ffbd2e; }
    .win-btn.max { background: #27c93f; }

    /* Screen Inner Content */
    .screen-content {
      flex: 1;
      padding: 24px;
      position: relative;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      background: #090d14;
      overflow: hidden;
    }

    /* CHARACTERS */
    .character-container {
      position: absolute;
      bottom: 220px;
      width: 480px;
      height: 520px;
      z-index: 40;
      pointer-events: none;
      transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.25s ease;
    }

    .char-peter {
      left: 30px;
      transform-origin: bottom left;
    }

    .char-stewie {
      right: 30px;
      transform-origin: bottom right;
    }

    .character-img {
      width: 100%;
      height: 100%;
      object-fit: contain;
      filter: drop-shadow(0 15px 30px rgba(0, 0, 0, 0.8));
    }

    /* CAPTIONS AREA */
    .caption-container {
      position: absolute;
      bottom: 90px;
      left: 60px;
      right: 60px;
      display: flex;
      justify-content: center;
      align-items: center;
      z-index: 60;
      min-height: 120px;
    }

    .caption-box {
      background: rgba(10, 14, 22, 0.85);
      backdrop-filter: blur(20px);
      border: 1px solid rgba(255, 255, 255, 0.12);
      padding: 16px 36px;
      border-radius: 60px;
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 14px 18px;
      max-width: 960px;
      box-shadow: 0 10px 40px rgba(0,0,0,0.6);
    }

    .caption-word {
      font-size: 58px;
      font-weight: 800;
      color: #8b9bb4;
      transition: all 0.12s ease;
      padding: 2px 10px;
      border-radius: 12px;
      line-height: 1.1;
    }

    .caption-word.active {
      color: #ffffff;
      background: #1a6cf0;
      transform: scale(1.08);
      box-shadow: 0 4px 20px rgba(26, 108, 240, 0.6);
    }

    /* DYNAMIC MOTION GRAPHIC STYLES */
    .meter-card {
      width: 100%;
      height: 100%;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      gap: 20px;
      text-align: center;
    }

    .big-value {
      font-size: 86px;
      font-weight: 900;
      letter-spacing: -1px;
    }
    .text-red { color: #ff4757; }
    .text-green { color: #2ed573; }
    .text-blue { color: #1e90ff; }
    .text-gold { color: #ffa502; }

    .sub-badge {
      font-size: 26px;
      font-weight: 700;
      padding: 10px 24px;
      border-radius: 40px;
      display: inline-flex;
      align-items: center;
      gap: 12px;
    }

    .badge-red { background: rgba(255, 71, 87, 0.2); border: 2px solid #ff4757; color: #ff6b81; }
    .badge-green { background: rgba(46, 213, 115, 0.2); border: 2px solid #2ed573; color: #2ed573; }
    .badge-blue { background: rgba(30, 144, 255, 0.2); border: 2px solid #1e90ff; color: #70a1ff; }

    /* Animated cursor */
    .mouse-cursor {
      position: absolute;
      width: 32px;
      height: 32px;
      z-index: 100;
      pointer-events: none;
      filter: drop-shadow(0 4px 8px rgba(0,0,0,0.6));
      transition: transform 0.15s ease;
    }

    /* RAMMap Table Mock */
    .rammap-window {
      width: 100%;
      height: 100%;
      background: #1e1e1e;
      border-radius: 8px;
      display: flex;
      flex-direction: column;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      font-size: 18px;
      color: #cccccc;
      overflow: hidden;
      border: 1px solid #333333;
    }

    .rammap-menubar {
      display: flex;
      background: #2d2d2d;
      padding: 4px 10px;
      gap: 20px;
      border-bottom: 1px solid #3d3d3d;
      font-size: 18px;
      position: relative;
    }

    .rammap-menu-item {
      padding: 4px 12px;
      border-radius: 4px;
      cursor: default;
    }
    .rammap-menu-item.active {
      background: #0078d4;
      color: #ffffff;
      font-weight: 700;
      box-shadow: 0 0 10px rgba(0, 120, 212, 0.8);
    }

    .rammap-dropdown {
      position: absolute;
      top: 36px;
      left: 70px;
      background: #252526;
      border: 1px solid #454545;
      border-radius: 4px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.8);
      display: flex;
      flex-direction: column;
      width: 280px;
      z-index: 120;
    }

    .rammap-drop-option {
      padding: 10px 16px;
      display: flex;
      align-items: center;
      gap: 12px;
      color: #ffffff;
      font-size: 17px;
    }
    .rammap-drop-option.highlight {
      background: #094771;
      font-weight: 700;
      border-left: 4px solid #0078d4;
    }

    .rammap-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 16px;
    }
    .rammap-table th {
      background: #252526;
      padding: 8px 12px;
      text-align: left;
      border-bottom: 1px solid #333;
      color: #888;
    }
    .rammap-table td {
      padding: 7px 12px;
      border-bottom: 1px solid #2a2a2a;
    }

    .bar-fill-red { background: #e81123; height: 18px; border-radius: 3px; }
    .bar-fill-orange { background: #ff8c00; height: 18px; border-radius: 3px; }
    .bar-fill-blue { background: #0078d4; height: 18px; border-radius: 3px; }
    .bar-fill-green { background: #107c41; height: 18px; border-radius: 3px; }
  </style>
</head>
<body>
  <div class="bg-grid"></div>
  <div class="glow-sphere"></div>

  <!-- HEADER BRANDING -->
  <div class="header-bar">
    <div class="top-tag" id="stepTag">PC TIPS BY EZ_PETER</div>
    <div class="title-box">
      <div class="scene-title" id="sceneTitle">PC Running Extremely Slow</div>
      <div class="breadcrumb" id="breadcrumb">System Stuttering & Lag Detected</div>
    </div>
    <div class="progress-bar-container" id="progressBar"></div>
  </div>

  <!-- CENTRAL SCREEN STAGE -->
  <div class="screen-stage">
    <div class="laptop-frame">
      <div class="win-titlebar">
        <div class="win-title-left">
          <svg class="win-logo" viewBox="0 0 88 88" fill="none">
            <path d="M0 12.5L35.8 7.6V41.7H0V12.5ZM0 46.3H35.8V80.4L0 75.5V46.3ZM40.1 7.0L88 0V41.7H40.1V7.0ZM88 88L40.1 81.0V46.3H88V88Z" fill="#0078D4"/>
          </svg>
          <span id="winTitleText">Windows Memory Diagnostics</span>
        </div>
        <div class="win-controls">
          <div class="win-btn min"></div>
          <div class="win-btn max"></div>
          <div class="win-btn close"></div>
        </div>
      </div>
      <div class="screen-content" id="screenContent">
        <!-- Rendered by window.renderAt(t) -->
      </div>
    </div>
  </div>

  <!-- CHARACTERS -->
  <div class="character-container char-peter" id="peterChar">
    <img src="../assets/peter.png" class="character-img" alt="Peter Griffin">
  </div>
  <div class="character-container char-stewie" id="stewieChar">
    <img src="../assets/stewie.png" class="character-img" alt="Stewie Griffin">
  </div>

  <!-- CAPTIONS -->
  <div class="caption-container" id="captionContainer">
    <div class="caption-box" id="captionBox">
      <!-- Word spans rendered by renderAt -->
    </div>
  </div>

  <script>
    window.ALIGNED_CAPTIONS = __ALIGNED_CAPTIONS__;
    window.SCRIPT = __SCRIPT__;

    // Build progress bar segments
    const progBar = document.getElementById('progressBar');
    progBar.innerHTML = '';
    for (let i = 0; i < window.SCRIPT.length; i++) {
      const seg = document.createElement('div');
      seg.className = 'prog-seg';
      seg.innerHTML = '<div class="prog-fill"></div>';
      progBar.appendChild(seg);
    }

    function clamp(val, min, max) {
      return Math.max(min, Math.min(max, val));
    }

    // RENDER SCREEN SCENE DYNAMICALLY
    function renderScreenScene(graphic, tau, t) {
      const el = document.getElementById('screenContent');
      const winTitle = document.getElementById('winTitleText');

      // 1. PC SLOW & HIGH RAM
      if (graphic === 'sec00_pc_slow_alert') {
        winTitle.textContent = 'System Alert - High Latency';
        el.innerHTML = `
          <div class="meter-card">
            <div class="sub-badge badge-red">🚨 CRITICAL SYSTEM WARNING</div>
            <div class="big-value text-red">PC SLOW & LAGGING</div>
            <div style="font-size: 28px; color: #9bb7d4;">High Memory Latency • System Micro-Stutters</div>
          </div>
        `;
      } else if (graphic === 'sec01_low_fps_counter') {
        winTitle.textContent = 'Game Performance Monitor';
        const fps = Math.round(22 + Math.sin(tau * Math.PI * 4) * 3);
        el.innerHTML = `
          <div class="meter-card">
            <div class="sub-badge badge-red">🎮 IN-GAME FRAME RATE</div>
            <div class="big-value text-red">${fps} FPS</div>
            <div style="width: 80%; height: 16px; background: rgba(255,255,255,0.1); border-radius: 8px; overflow: hidden;">
              <div style="width: 25%; height: 100%; background: #ff4757;"></div>
            </div>
            <div style="font-size: 26px; color: #ff6b81; font-weight: 700;">Severe Frame Drop Detected</div>
          </div>
        `;
      } else if (graphic === 'sec02_ram_usage_94_percent') {
        winTitle.textContent = 'Task Manager - Performance';
        const pct = (94.2 + tau * 0.4).toFixed(1);
        el.innerHTML = `
          <div class="meter-card">
            <div class="sub-badge badge-red">⚠️ MEMORY CONSUMPTION</div>
            <div class="big-value text-red">${pct}%</div>
            <div style="font-size: 32px; font-weight: 700; color: #ffffff;">15.1 GB / 16.0 GB In Use</div>
            <div style="width: 85%; height: 24px; background: #222; border-radius: 12px; overflow: hidden; border: 1px solid #ff4757;">
              <div style="width: ${pct}%; height: 100%; background: linear-gradient(90deg, #ff6b81, #ff4757);"></div>
            </div>
          </div>
        `;
      } else if (graphic === 'sec03_task_mgr_memory_red') {
        winTitle.textContent = 'Task Manager (Processes)';
        el.innerHTML = `
          <div class="rammap-window" style="padding: 16px; gap: 12px;">
            <div style="display: flex; justify-content: space-between; font-weight: 700; color: #fff;">
              <span>Memory Usage</span>
              <span style="color: #ff4757;">94% (Redlined)</span>
            </div>
            <div style="width: 100%; height: 18px; background: #333; border-radius: 9px; overflow: hidden;">
              <div style="width: 94%; height: 100%; background: #ff4757;"></div>
            </div>
            <table class="rammap-table" style="margin-top: 10px;">
              <tr><th>Process</th><th>Memory</th><th>Status</th></tr>
              <tr><td>Desktop Window Manager</td><td>840 MB</td><td style="color:#ffa502;">High</td></tr>
              <tr><td>System & Compressed Memory</td><td>2,450 MB</td><td style="color:#ff4757;">Critical</td></tr>
              <tr><td>System Standby Cache</td><td>8,920 MB</td><td style="color:#ff4757;">Hidden Leak</td></tr>
            </table>
          </div>
        `;
      } else if (graphic === 'sec04_idle_desktop_leak' || graphic === 'sec05_barely_anything_open' || graphic === 'sec06_system_bottleneck' || graphic === 'sec07_peter_seeking_solution') {
        winTitle.textContent = 'Windows Memory Leak';
        el.innerHTML = `
          <div class="meter-card">
            <div class="sub-badge badge-red">DESKTOP IDLE</div>
            <div class="big-value text-gold">NO APPS OPEN</div>
            <div style="font-size: 28px; color: #ffffff;">Yet 15 GB of RAM is completely locked!</div>
            <div class="sub-badge badge-blue" style="margin-top: 10px;">Mystery Windows Cache Leak</div>
          </div>
        `;
      }

      // 2. STEWIE REVEAL & RAM EXPENSIVE
      else if (graphic === 'sec08_ram_expensive_price' || graphic === 'sec09_memory_detective_radar') {
        winTitle.textContent = 'Hardware Upgrades vs Software Fix';
        el.innerHTML = `
          <div class="meter-card">
            <div class="sub-badge badge-blue">DDR5 / DDR4 RAM UPGRADE</div>
            <div class="big-value text-gold">$120 - $250+</div>
            <div style="font-size: 28px; color: #2ed573; font-weight: 700;">Don't Buy More RAM! Fix The Cache For FREE!</div>
          </div>
        `;
      } else if (graphic === 'sec10_sysinternals_tool_teaser' || graphic === 'sec11_free_solution_reveal' || graphic === 'sec12_transition_to_steps' || graphic === 'sec13_what_do_i_need') {
        winTitle.textContent = 'Microsoft Sysinternals Utility';
        el.innerHTML = `
          <div class="meter-card">
            <div class="sub-badge badge-green">OFFICIAL MICROSOFT TOOL</div>
            <div class="big-value text-blue">RAMMap</div>
            <div style="font-size: 28px; color: #ffffff;">Advanced Physical Memory Map Analyzer</div>
          </div>
        `;
      }

      // 3. STEP 1: SEARCH RAMMAP
      else if (graphic === 'sec14_google_search_rammap') {
        winTitle.textContent = 'Edge Browser - Google Search';
        const typed = "RAMMap".substring(0, Math.floor(tau * 6) + 1);
        el.innerHTML = `
          <div class="meter-card" style="gap: 16px;">
            <div style="font-size: 40px; font-weight: 700; color: #fff;">Google Search</div>
            <div style="width: 80%; background: #202124; border: 2px solid #5f6368; border-radius: 30px; padding: 14px 28px; display: flex; align-items: center; justify-content: space-between; font-size: 28px; color: #fff;">
              <span>${typed}<span style="color:#1a6cf0;">|</span></span>
              <span>🔍</span>
            </div>
            <div class="sub-badge badge-blue">Step 1: Type "RAMMap"</div>
          </div>
        `;
      } else if (graphic === 'sec15_first_search_result' || graphic === 'sec16_click_first_link') {
        winTitle.textContent = 'Google Search Results';
        const cursorX = 350 + tau * 40;
        const cursorY = 220 + tau * 20;
        el.innerHTML = `
          <div style="width: 100%; height: 100%; padding: 20px; display: flex; flex-direction: column; gap: 14px; position: relative;">
            <div style="color: #9aa0a6; font-size: 18px;">https://learn.microsoft.com > sysinternals > rammap</div>
            <div style="color: #8ab4f8; font-size: 32px; font-weight: 700; text-decoration: underline;">RAMMap - Sysinternals | Microsoft Learn</div>
            <div style="color: #bdc1c6; font-size: 20px; line-height: 1.4;">RAMMap is an advanced physical memory usage analysis utility for Windows. Free download from official Microsoft site.</div>
            <div class="sub-badge badge-green" style="align-self: flex-start; margin-top: 10px;">Verified Official Microsoft Domain</div>
            <!-- Animated cursor clicking link -->
            <svg class="mouse-cursor" style="left: ${cursorX}px; top: ${cursorY}px;" viewBox="0 0 24 24" fill="#ffffff">
              <path d="M4 0l16 12.279-6.951 1.17 4.325 8.817-3.596 1.734-4.35-8.879-5.428 5.139v-20.26z"/>
            </svg>
          </div>
        `;
      }

      // 4. SAFETY & VIRUS CHECK
      else if (graphic === 'sec17_comments_virus_concern' || graphic === 'sec18_safety_security_check' || graphic === 'sec19_virus_scanner_shield') {
        winTitle.textContent = 'Security Verification';
        el.innerHTML = `
          <div class="meter-card">
            <div class="sub-badge badge-red">💬 COMMENTS CONCERN</div>
            <div class="big-value text-gold">"Is It A Virus?"</div>
            <div style="font-size: 28px; color: #ffffff;">100% Safe • Zero Third-Party Malware</div>
          </div>
        `;
      } else if (graphic === 'sec20_microsoft_official_shield' || graphic === 'sec21_microsoft_learn_verified') {
        winTitle.textContent = 'Microsoft Security Certified';
        el.innerHTML = `
          <div class="meter-card">
            <div class="sub-badge badge-green">🛡️ OFFICIAL MICROSOFT SITE</div>
            <div class="big-value text-green">100% SAFE</div>
            <div style="font-size: 28px; color: #60cdff; font-weight: 700;">learn.microsoft.com/sysinternals</div>
            <div style="font-size: 22px; color: #ccc;">Published directly by Microsoft Sysinternals</div>
          </div>
        `;
      }

      // 5. STEP 2: DOWNLOAD RAMMAP
      else if (graphic === 'sec22_page_download_section' || graphic === 'sec23_cursor_hover_download' || graphic === 'sec24_click_download_button') {
        winTitle.textContent = 'Microsoft Learn - RAMMap';
        const isClick = graphic === 'sec24_click_download_button';
        el.innerHTML = `
          <div class="meter-card">
            <div style="font-size: 32px; font-weight: 700; color: #fff;">Download RAMMap</div>
            <div style="background: ${isClick ? '#005a9e' : '#0078d4'}; border: 2px solid #60cdff; border-radius: 12px; padding: 20px 48px; font-size: 32px; font-weight: 800; color: #fff; box-shadow: 0 0 30px rgba(0,120,212,0.6); transform: ${isClick ? 'scale(0.96)' : 'scale(1)'};">
              ⬇️ Download RAMMap (671 KB)
            </div>
            <div class="sub-badge badge-blue">Lightweight Official Microsoft Zip</div>
          </div>
        `;
      } else if (graphic === 'sec25_choose_download_location') {
        winTitle.textContent = 'Save As Dialog';
        el.innerHTML = `
          <div class="meter-card">
            <div class="sub-badge badge-blue">CHOOSE DOWNLOAD FOLDER</div>
            <div style="background: #252526; border: 1px solid #454545; padding: 20px 30px; border-radius: 8px; width: 80%; text-align: left;">
              <div style="color: #888; font-size: 18px;">File name:</div>
              <div style="color: #fff; font-size: 24px; font-weight: 700;">RAMMap.zip</div>
              <div style="color: #2ed573; font-size: 18px; margin-top: 10px;">Save location: Downloads / Desktop</div>
            </div>
          </div>
        `;
      }

      // 6. STEP 3: RUN AS ADMINISTRATOR
      else if (graphic === 'sec26_rammap_zip_downloaded' || graphic === 'sec27_unzip_rammap64') {
        winTitle.textContent = 'File Explorer - Downloads';
        el.innerHTML = `
          <div class="meter-card">
            <div style="font-size: 70px;">📁</div>
            <div class="big-value text-blue">RAMMap.zip</div>
            <div class="sub-badge badge-green">Extracting: RAMMap64.exe</div>
          </div>
        `;
      } else if (graphic === 'sec28_right_click_context_menu' || graphic === 'sec29_click_run_as_admin') {
        winTitle.textContent = 'Context Menu - RAMMap64.exe';
        const isRun = graphic === 'sec29_click_run_as_admin';
        el.innerHTML = `
          <div style="width: 100%; height: 100%; display: flex; justify-content: center; align-items: center; position: relative;">
            <div style="background: #2b2b2b; border: 1px solid #454545; border-radius: 8px; width: 340px; box-shadow: 0 10px 30px rgba(0,0,0,0.8); overflow: hidden;">
              <div style="padding: 12px 18px; color: #fff; font-size: 20px; font-weight: 700; border-bottom: 1px solid #3d3d3d;">RAMMap64.exe</div>
              <div style="padding: 14px 18px; background: ${isRun ? '#0078d4' : '#333'}; color: #fff; font-size: 20px; font-weight: 700; display: flex; align-items: center; gap: 12px;">
                <span>🛡️</span>
                <span>Run as administrator</span>
              </div>
              <div style="padding: 10px 18px; color: #888; font-size: 16px;">Open</div>
              <div style="padding: 10px 18px; color: #888; font-size: 16px;">Properties</div>
            </div>
          </div>
        `;
      } else if (graphic === 'sec30_uac_approved_loading' || graphic === 'sec31_loading_memory_processes' || graphic === 'sec32_rammap_window_opened') {
        winTitle.textContent = 'RAMMap v1.61 - Initializing';
        el.innerHTML = `
          <div class="meter-card">
            <div style="font-size: 60px;">⏳</div>
            <div class="big-value text-blue">Loading Memory...</div>
            <div style="font-size: 26px; color: #ccc;">Scanning all active physical RAM pages</div>
          </div>
        `;
      }

      // 7. REAL TIME MEMORY VIEW & 45% / 90% BREAKDOWN
      else if (graphic === 'sec33_real_time_dashboard' || graphic === 'sec34_use_counts_table' || graphic === 'sec35_live_tracking_active' || graphic === 'sec36_physical_memory_breakdown' || graphic === 'sec37_active_memory_highlight') {
        winTitle.textContent = 'RAMMap - Use Counts (Real-Time)';
        el.innerHTML = `
          <div class="rammap-window">
            <div class="rammap-menubar">
              <span class="rammap-menu-item">File</span>
              <span class="rammap-menu-item">Empty</span>
              <span class="rammap-menu-item">Configure</span>
              <span class="rammap-menu-item">Help</span>
            </div>
            <table class="rammap-table">
              <tr><th>Use Type</th><th>Active</th><th>Standby</th><th>Total</th></tr>
              <tr><td>Process Private</td><td>4,210 MB</td><td>-</td><td>4,210 MB</td></tr>
              <tr><td>Mapped File</td><td>1,120 MB</td><td>4,810 MB</td><td>5,930 MB</td></tr>
              <tr><td>Paged Pool</td><td>680 MB</td><td>-</td><td>680 MB</td></tr>
              <tr><td>Driver Locked</td><td>1,210 MB</td><td>-</td><td>1,210 MB</td></tr>
              <tr style="background: rgba(0,120,212,0.2); font-weight: 700; color: #60cdff;">
                <td>Total Physical</td><td>7,220 MB</td><td>8,450 MB</td><td>16,000 MB</td>
              </tr>
            </table>
          </div>
        `;
      } else if (graphic === 'sec38_memory_meter_45_percent' || graphic === 'sec39_standby_cache_leak_meter' || graphic === 'sec40_why_pc_slow_explained' || graphic === 'sec41_ready_to_empty' || graphic === 'sec42_transition_to_empty_menu') {
        winTitle.textContent = 'Memory Usage Breakdown';
        el.innerHTML = `
          <div class="meter-card">
            <div class="sub-badge badge-blue">REAL-TIME MEMORY MONITOR</div>
            <div class="big-value text-blue">45% ACTIVE</div>
            <div style="font-size: 28px; color: #ff6b81; font-weight: 700;">+ 50% LOCKED IN STANDBY CACHE!</div>
            <div class="sub-badge badge-red" style="margin-top: 10px;">Why Your Games Stutter</div>
          </div>
        `;
      }

      // 8. STEP 4: CLICK EMPTY WORKING SETS
      else if (graphic === 'sec43_where_do_i_go_next' || graphic === 'sec44_focus_empty_menu') {
        winTitle.textContent = 'RAMMap - Menu Navigation';
        el.innerHTML = `
          <div class="meter-card">
            <div class="sub-badge badge-blue">STEP 4: LOCATE "EMPTY"</div>
            <div class="big-value text-gold">Top Menu Bar</div>
            <div style="font-size: 28px; color: #fff;">File \u2022 <b style="color:#60cdff; text-decoration: underline;">Empty</b> \u2022 Configure \u2022 Help</div>
          </div>
        `;
      } else if (graphic === 'sec45_click_empty_menu_open' || graphic === 'sec46_highlight_empty_working_sets' || graphic === 'sec47_click_empty_working_sets') {
        winTitle.textContent = 'RAMMap - [Empty Menu]';
        const isClick = graphic === 'sec47_click_empty_working_sets';
        el.innerHTML = `
          <div class="rammap-window" style="position: relative;">
            <div class="rammap-menubar">
              <span class="rammap-menu-item">File</span>
              <span class="rammap-menu-item active">Empty</span>
              <span class="rammap-menu-item">Configure</span>
              <span class="rammap-menu-item">Help</span>
            </div>
            <div class="rammap-dropdown">
              <div class="rammap-drop-option highlight">
                <span>⚡</span>
                <span style="color: ${isClick ? '#60cdff' : '#ffffff'}; font-weight: 800;">Empty Working Sets</span>
              </div>
              <div class="rammap-drop-option">Empty System Working Set</div>
              <div class="rammap-drop-option">Empty Modified Page List</div>
              <div class="rammap-drop-option">Empty Standby List</div>
              <div class="rammap-drop-option">Empty Priority 0 Standby List</div>
            </div>
            <div style="padding: 40px; text-align: center; color: #777;">
              Clicking "Empty Working Sets" flushes unneeded process memory
            </div>
          </div>
        `;
      }

      // 9. WORKING SETS LOWERING
      else if (graphic === 'sec48_memory_meter_plunging' || graphic === 'sec49_usage_down_to_32_percent' || graphic === 'sec50_instant_responsiveness' || graphic === 'sec51_but_wait_theres_more') {
        winTitle.textContent = 'Working Sets Flushed';
        const pct = Math.max(28, Math.round(45 - tau * 15));
        el.innerHTML = `
          <div class="meter-card">
            <div class="sub-badge badge-green">WORKING SETS EMPTIED! ⚡</div>
            <div class="big-value text-green">${pct}%</div>
            <div style="font-size: 28px; color: #ffffff;">Memory Usage Plunging In Real Time</div>
            <div class="sub-badge badge-blue">Now Let's Free Up The Standby List!</div>
          </div>
        `;
      }

      // 10. STEP 5: EMPTY STANDBY LIST
      else if (graphic === 'sec52_can_we_free_even_more' || graphic === 'sec53_turbo_optimization_icon' || graphic === 'sec54_reopen_empty_menu') {
        winTitle.textContent = 'Target: 10+ GB Free Memory';
        el.innerHTML = `
          <div class="meter-card">
            <div class="sub-badge badge-gold">WANT EVEN MORE SPEED?</div>
            <div class="big-value text-blue">Standby List</div>
            <div style="font-size: 28px; color: #fff;">Clear closed background program caches!</div>
          </div>
        `;
      } else if (graphic === 'sec55_highlight_empty_standby_list' || graphic === 'sec56_click_empty_standby_list') {
        winTitle.textContent = 'RAMMap - [Empty Standby List]';
        const isClick = graphic === 'sec56_click_empty_standby_list';
        el.innerHTML = `
          <div class="rammap-window" style="position: relative;">
            <div class="rammap-menubar">
              <span class="rammap-menu-item">File</span>
              <span class="rammap-menu-item active">Empty</span>
              <span class="rammap-menu-item">Configure</span>
              <span class="rammap-menu-item">Help</span>
            </div>
            <div class="rammap-dropdown">
              <div class="rammap-drop-option">Empty Working Sets</div>
              <div class="rammap-drop-option">Empty System Working Set</div>
              <div class="rammap-drop-option">Empty Modified Page List</div>
              <div class="rammap-drop-option highlight">
                <span>🔥</span>
                <span style="color: ${isClick ? '#2ed573' : '#ffffff'}; font-weight: 800;">Empty Standby List</span>
              </div>
              <div class="rammap-drop-option">Empty Priority 0 Standby List</div>
            </div>
          </div>
        `;
      }

      // 11. WHAT IS STANDBY LIST (CLOSED APPS STILL IN RAM)
      else if (graphic === 'sec57_what_is_standby_list' || graphic === 'sec58_questioning_the_cache' || graphic === 'sec59_closed_apps_ghost_icons' || graphic === 'sec60_ghost_memory_leak_graphic') {
        winTitle.textContent = 'What Is The Standby List?';
        el.innerHTML = `
          <div class="meter-card">
            <div class="sub-badge badge-red">GHOST MEMORY CACHE</div>
            <div style="font-size: 48px; font-weight: 800; color: #fff;">CLOSED APPS STILL IN RAM</div>
            <div style="font-size: 26px; color: #9bb7d4; max-width: 80%;">Chrome, Discord & Games you closed hours ago are still hoarding your memory!</div>
          </div>
        `;
      }

      // 12. OVER 10 GIGS AVAILABLE NOW
      else if (graphic === 'sec61_standby_flushed_to_zero' || graphic === 'sec62_peter_eyes_wide_shock' || graphic === 'sec63_ten_gigs_available_counter' || graphic === 'sec64_total_memory_restored') {
        winTitle.textContent = 'Memory Liberated Successfully';
        const gigs = (10.2 + tau * 0.4).toFixed(1);
        el.innerHTML = `
          <div class="meter-card">
            <div class="sub-badge badge-green">🚀 MASSIVE MEMORY FREED</div>
            <div class="big-value text-green">+${gigs} GB FREE</div>
            <div style="font-size: 32px; font-weight: 800; color: #ffffff;">Available Memory: 13.5 GB / 16 GB</div>
            <div class="sub-badge badge-blue">Zero Standby Cache Bloat</div>
          </div>
        `;
      }

      // 13. SMOOTH GAMING & 144 FPS
      else if (graphic === 'sec65_smooth_gaming_readiness' || graphic === 'sec66_fps_boost_144_counter' || graphic === 'sec67_heavy_task_smooth_graphic' || graphic === 'sec68_pc_running_like_brand_new' || graphic === 'sec69_rammap_master_success') {
        winTitle.textContent = 'Ultra-Smooth Gaming Performance';
        const fps = Math.round(144 + Math.sin(tau * Math.PI * 2) * 2);
        el.innerHTML = `
          <div class="meter-card">
            <div class="sub-badge badge-green">🎮 GAMING BENCHMARK RESTORED</div>
            <div class="big-value text-green">${fps} FPS SOLID</div>
            <div style="font-size: 28px; color: #fff;">Zero Stutters • Butter Smooth Frame Times</div>
            <div class="sub-badge badge-blue" style="margin-top: 10px;">Heavy Tasks & Editing Run Flawlessly</div>
          </div>
        `;
      }

      // 14. OUTRO & FULL PC OPTIMIZATION
      else {
        winTitle.textContent = 'Full System Tuning by Ez_peter';
        el.innerHTML = `
          <div class="meter-card" style="gap: 16px;">
            <div class="sub-badge badge-blue">PC • WINDOWS • BIOS • GAMES</div>
            <div class="big-value text-blue" style="font-size: 72px;">PC Tips by Ez_peter</div>
            <div style="font-size: 36px; font-weight: 800; color: #2ed573;">Follow @Ez_peter 🚀</div>
            <div style="font-size: 24px; color: #9bb7d4;">Save & Share For Maximum PC Performance!</div>
          </div>
        `;
      }
    }

    // MAIN DETERMINISTIC RENDER FUNCTION
    window.renderAt = function(t) {
      if (!window.SCRIPT || window.SCRIPT.length === 0) return;

      const totalSeconds = window.SCRIPT.length;
      const clampedT = clamp(t, 0, totalSeconds - 0.001);
      const s = Math.floor(clampedT);
      const tau = clampedT - s;
      const currentItem = window.SCRIPT[s];

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

      // 2. UPDATE TOP HEADINGS
      const titleEl = document.getElementById('sceneTitle');
      const breadcrumbEl = document.getElementById('breadcrumb');
      const tagEl = document.getElementById('stepTag');

      if (currentItem.stepNumber > 0) {
        tagEl.textContent = `STEP 0${currentItem.stepNumber} • PC TIPS BY EZ_PETER`;
      } else {
        tagEl.textContent = 'PC TIPS BY EZ_PETER';
      }
      titleEl.textContent = currentItem.title;
      breadcrumbEl.textContent = currentItem.breadcrumb;

      // 3. UPDATE CHARACTERS (PETER VS STEWIE)
      const peterEl = document.getElementById('peterChar');
      const stewieEl = document.getElementById('stewieChar');

      if (currentItem.speaker === 'peter') {
        peterEl.style.transform = `translateX(0px) scale(${1.0 + Math.sin(tau * Math.PI * 4) * 0.015})`;
        peterEl.style.opacity = '1.0';
        stewieEl.style.transform = 'translateX(200px) scale(0.9)';
        stewieEl.style.opacity = '0.0';
      } else {
        stewieEl.style.transform = `translateX(0px) scale(${1.0 + Math.sin(tau * Math.PI * 4) * 0.015})`;
        stewieEl.style.opacity = '1.0';
        peterEl.style.transform = 'translateX(-200px) scale(0.9)';
        peterEl.style.opacity = '0.0';
      }

      // 4. RENDER CENTRAL DISPLAY SCENE
      renderScreenScene(currentItem.graphic, tau, clampedT);

      // 5. RENDER CAPTIONS
      const capContainer = document.getElementById('captionContainer');
      const capBox = document.getElementById('captionBox');

      if (window.hideCaptions) {
        capContainer.style.display = 'none';
        return;
      }
      capContainer.style.display = 'flex';

      const chunks = window.ALIGNED_CAPTIONS.chunks;
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

      if (activeChunk) {
        let html = '';
        activeChunk.words.forEach(w => {
          const isActive = (clampedT >= w.global_start && clampedT < w.global_end);
          html += `<span class="caption-word ${isActive ? 'active' : ''}">${w.text}</span>`;
        });
        capBox.innerHTML = html;
      } else {
        capBox.innerHTML = '';
      }
    };
  </script>
</body>
</html>
"""

# Replace placeholders
final_html = engine_html.replace("__ALIGNED_CAPTIONS__", aligned_json).replace("__SCRIPT__", script_json)

with open("video-engine/index.html", "w", encoding="utf-8") as f:
    f.write(final_html)

print("Successfully written video-engine/index.html with all 78 RAMMap scenes!")
