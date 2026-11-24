import json
import subprocess
import os
import re

with open("audio/delivery_opt_turns/turns_metadata.json", "r", encoding="utf-8") as f:
    turns = json.load(f)

print(f"Loaded {len(turns)} turns.")

for t in turns:
    tid = t["id"]
    spk = t["speaker"]
    text = t["text"]
    words = t["words"]
    dur = t["duration"]
    first_w = words[0] if words else None
    last_w = words[-1] if words else None
    print(f"[{tid}] {spk:6s} | dur={dur:5.2f}s | words={len(words):2d} | 1st: {first_w['text'] if first_w else ''} ({first_w['start'] if first_w else 0:.2f}s) | last: {last_w['text'] if last_w else ''} ({last_w['end'] if last_w else 0:.2f}s)")
