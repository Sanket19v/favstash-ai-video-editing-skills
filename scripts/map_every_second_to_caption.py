import json

with open("video-engine/aligned_captions.json", "r", encoding="utf-8") as f:
    aligned = json.load(f)

chunks = aligned["chunks"]
total_seconds = int(aligned["total_duration"]) # 93

for s in range(total_seconds):
    t_start = s
    t_end = s + 1
    t_mid = s + 0.5
    
    # Find all words spoken in this second
    words_in_sec = []
    active_chunk = None
    for c in chunks:
        if c["start"] <= t_mid < c["display_end"] or (c["start"] <= t_start and c["display_end"] >= t_end):
            active_chunk = c
        for w in c["words"]:
            if (w["global_start"] >= t_start and w["global_start"] < t_end) or \
               (w["global_end"] > t_start and w["global_end"] <= t_end) or \
               (w["global_start"] <= t_start and w["global_end"] >= t_end):
                words_in_sec.append(w["text"])
                
    spoken_phrase = " ".join(words_in_sec) if words_in_sec else (" ".join(w["text"] for w in active_chunk["words"]) if active_chunk else "")
    spk = active_chunk["speaker"] if active_chunk else "unknown"
    print(f"Second {s:02d} [{s:02d}s - {s+1:02d}s] ({spk:6s}): \"{spoken_phrase}\"")
