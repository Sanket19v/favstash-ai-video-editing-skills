import re

with open("video-engine/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update caption CSS for ultra-bold, high-visibility, punchy viral style
old_cap_css = """    /* CAPTIONS */
    #captions {
      position: absolute;
      top: 900px;
      left: 60px;
      width: 960px;
      height: 120px;
      display: flex;
      justify-content: center;
      align-items: center;
      flex-wrap: wrap;
      gap: 14px;
      z-index: 30;
    }
    .caption-word {
      font-size: 58px;
      font-weight: 900;
      color: var(--text);
      letter-spacing: -0.5px;
      transition: all 0.1s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .caption-word.word-active {
      background: var(--accent);
      color: #ffffff;
      padding: 4px 24px;
      border-radius: 20px;
      box-shadow: 0 10px 25px rgba(26, 108, 240, 0.35);
      transform: scale(1.08);
    }"""

new_cap_css = """    /* CAPTIONS - High Visibility Viral Style */
    #captions {
      position: absolute;
      top: 915px;
      left: 40px;
      width: 1000px;
      height: 130px;
      display: flex;
      justify-content: center;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
      z-index: 50;
    }
    .caption-word {
      font-size: 64px;
      font-weight: 900;
      color: #0d0d0d;
      letter-spacing: -0.5px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 6px 14px;
      border-radius: 20px;
      transition: all 0.08s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .caption-word.word-active {
      background: #1a6cf0;
      color: #ffffff !important;
      padding: 8px 28px;
      border-radius: 24px;
      box-shadow: 0 12px 30px rgba(26, 108, 240, 0.45);
      transform: scale(1.12);
    }"""

if old_cap_css in html:
    html = html.replace(old_cap_css, new_cap_css)
    print("Updated caption CSS to 64px bold with vibrant blue pill.")
else:
    print("Warning: old_cap_css not matched directly, checking regex replacement.")
    html = re.sub(r'/\* CAPTIONS \*/.*?\.caption-word\.word-active\s*\{[^}]+\}', new_cap_css, html, flags=re.DOTALL)

# 2. Update caption render logic in renderAt: ensure activeWordIdx is ALWAYS >= 0 so pill NEVER vanishes
old_cap_js = """        // Determine active word: word where start <= tau <= end
        let activeWordIdx = -1;
        for (let i = 0; i < words.length; i++) {
          if (tau >= words[i].start && tau <= words[i].end) {
            activeWordIdx = i;
            break;
          }
        }
        // If past the last word end, keep the last word active
        if (activeWordIdx === -1 && words.length > 0 && tau > words[words.length - 1].start) {
          activeWordIdx = words.length - 1;
        }"""

new_cap_js = """        // Determine active word: ALWAYS keep currently spoken word active (never vanish!)
        let activeWordIdx = 0;
        for (let i = 0; i < words.length; i++) {
          if (tau >= words[i].start) {
            activeWordIdx = i;
          }
        }"""

if old_cap_js in html:
    html = html.replace(old_cap_js, new_cap_js)
    print("Updated caption JS: blue active pill is active on every single frame.")
else:
    print("Warning: old_cap_js not matched directly, checking regex replacement.")
    html = re.sub(r'// Determine active word:.*?activeWordIdx = words\.length - 1;\s*\}', new_cap_js, html, flags=re.DOTALL)

with open("video-engine/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("video-engine/index.html updated successfully.")
