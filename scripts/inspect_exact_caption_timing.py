import json

with open("video-engine/aligned_captions.json", "r", encoding="utf-8") as f:
    aligned = json.load(f)

print(f"Total duration: {aligned['total_duration']}s")
for tr in aligned["turn_ranges"]:
    print(f"Turn {tr['line_index']:2d} ({tr['speaker']:6s}) [{tr['start']:5.2f}s - {tr['end']:5.2f}s] (speech_end={tr['speech_end']:5.2f}s)")

print("\n--- First 20 chunks ---")
for c in aligned["chunks"][:20]:
    words_str = " ".join(w["text"] for w in c["words"])
    print(f"[{c['start']:5.2f}s - {c['display_end']:5.2f}s] ({c['speaker']:6s}): {words_str}")
