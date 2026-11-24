import json
import re

print("=== Applying Branding & Label Updates requested by User ===")

# 1. UPDATE script.json
with open("script.json", "r", encoding="utf-8") as f:
    script = json.load(f)

for s in script:
    # Update titles
    if "masterclass" in s.get("title", "").lower():
        s["title"] = "PC Tips by Ez_peter"
    
    # Update breadcrumbs
    if "student peter vs teacher stewie" in s.get("breadcrumb", "").lower():
        s["breadcrumb"] = "Must-Change Windows Settings"
    elif "student passed masterclass" in s.get("breadcrumb", "").lower():
        s["breadcrumb"] = "All 4 Settings Configured"
    elif "@dailypctips" in s.get("breadcrumb", "").lower():
        s["breadcrumb"] = "@Ez_peter"

with open("script.json", "w", encoding="utf-8") as f:
    json.dump(script, f, indent=2)
with open("output/script.json", "w", encoding="utf-8") as f:
    json.dump(script, f, indent=2)

print("Updated script.json and output/script.json.")

# 2. UPDATE video-engine/index.html
with open("video-engine/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace pillTag
html = html.replace('<div id="pillTag">PC MASTERCLASS</div>', '<div id="pillTag">PC TIPS BY EZ_PETER</div>')

# Replace @DailyPCTips
html = html.replace('Follow @DailyPCTips', 'Follow @Ez_peter')

# Replace embedded SCRIPT
pattern_script = r"let SCRIPT = \[.*?\];\s*window\.SCRIPT = SCRIPT;"
replacement_script = f"let SCRIPT = {json.dumps(script)};\n    window.SCRIPT = SCRIPT;"
html = re.sub(pattern_script, lambda m: replacement_script, html, flags=re.DOTALL)

# Remove 'STUDENT & TEACHER' in stepLabel logic
old_step_logic = """      if (currentItem.stepNumber > 0) {
        stepLabelEl.textContent = `LESSON 0${currentItem.stepNumber}`;
      } else {
        stepLabelEl.textContent = 'STUDENT & TEACHER';
      }"""

new_step_logic = """      if (currentItem.stepNumber > 0) {
        stepLabelEl.textContent = `STEP 0${currentItem.stepNumber}`;
      } else {
        stepLabelEl.textContent = '';
      }"""

if old_step_logic in html:
    html = html.replace(old_step_logic, new_step_logic)
    print("Replaced stepLabel logic: removed 'STUDENT & TEACHER', set stepNumber > 0 to 'STEP 0X'.")
else:
    print("Warning: old_step_logic not matched directly, checking regex replacement.")
    html = re.sub(r"stepLabelEl\.textContent\s*=\s*'STUDENT & TEACHER';", "stepLabelEl.textContent = '';", html)

with open("video-engine/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Updated video-engine/index.html successfully.")

# 3. UPDATE output/post.txt
with open("output/post.txt", "r", encoding="utf-8") as f:
    post_txt = f.read()

post_txt = post_txt.replace("@DailyPCTips", "@Ez_peter")
post_txt = post_txt.replace("PC MASTERCLASS (STUDENT & TEACHER EDITION)", "PC TIPS BY EZ_PETER")
post_txt = post_txt.replace("PC Masterclass", "PC Tips by Ez_peter")
post_txt = post_txt.replace("Follow @DailyPCTips", "Follow @Ez_peter")

with open("output/post.txt", "w", encoding="utf-8") as f:
    f.write(post_txt)

print("Updated output/post.txt successfully.")
