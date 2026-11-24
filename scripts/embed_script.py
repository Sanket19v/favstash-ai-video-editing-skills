import json
import re

with open("script.json", "r", encoding="utf-8") as f:
    script_data = json.load(f)

script_json_str = json.dumps(script_data)

with open("video-engine/index.html", "r", encoding="utf-8") as f:
    html = f.read()

pattern = r"let SCRIPT = .*?;\s*window\.SCRIPT = SCRIPT;"
replacement = f"let SCRIPT = {script_json_str};\n    window.SCRIPT = SCRIPT;"

if re.search(pattern, html, flags=re.DOTALL):
    html = re.sub(pattern, lambda m: replacement, html, flags=re.DOTALL)
    with open("video-engine/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Successfully updated SCRIPT in video-engine/index.html")
else:
    print("Regex match not found!")
