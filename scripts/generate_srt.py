import json

with open("script.json") as f:
    script = json.load(f)

def format_srt_time(sec):
    hrs = int(sec // 3600)
    mins = int((sec % 3600) // 60)
    secs = int(sec % 60)
    millis = int((sec - int(sec)) * 1000)
    return f"{hrs:02d}:{mins:02d}:{secs:02d},{millis:03d}"

srt_lines = []
for i, item in enumerate(script):
    start_t = float(item["second"])
    end_t = start_t + 1.0
    spk_tag = "Peter" if item["speaker"] == "peter" else "Stewie"
    srt_lines.append(f"{i+1}\n{format_srt_time(start_t)} --> {format_srt_time(end_t)}\n[{spk_tag}] {item['line']}\n")

with open("output/captions.srt", "w", encoding="utf-8") as f:
    f.write("\n".join(srt_lines))

print("Generated output/captions.srt with 30 entries.")
