import json

with open("video-engine/aligned_captions.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for tr in data["turn_ranges"]:
    print(f"Line {tr['line_index']:02d} | {tr['speaker']:<6} | {tr['start']:5.2f}s -> {tr['end']:5.2f}s")
