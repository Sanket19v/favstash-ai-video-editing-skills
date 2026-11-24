import json
import subprocess
import os

with open("audio/aligned_turns/all_turns_metadata.json", "r", encoding="utf-8") as f:
    turns = json.load(f)

print("=== Analyzing Spoken Word Timestamps for All 8 Turns ===")
total_spoken = 0.0
for t in turns:
    tid = t["id"]
    spk = t["speaker"]
    raw_dur = t["duration"]
    words = t["words"]
    last_end = words[-1]["end"] if words else raw_dur
    first_start = words[0]["start"] if words else 0.0
    spoken_len = last_end - first_start
    total_spoken += spoken_len
    print(f"[{tid}] {spk:<6} | Spoken: {first_start:.2f}s -> {last_end:.2f}s ({spoken_len:.2f}s) | Raw file: {raw_dur:.2f}s | Words: {len(words)}")

print(f"\nTotal net spoken duration: {total_spoken:.2f}s (Target: 30.00s)")
