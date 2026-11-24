import json

with open("video-engine/aligned_captions.json", "r", encoding="utf-8") as f:
    data = json.load(f)

chunks = data["chunks"]

def format_srt_time(sec):
    hrs = int(sec // 3600)
    mins = int((sec % 3600) // 60)
    secs = int(sec % 60)
    millis = int((sec - int(sec)) * 1000)
    return f"{hrs:02d}:{mins:02d}:{secs:02d},{millis:03d}"

srt_entries = []
for idx, c in enumerate(chunks):
    start_str = format_srt_time(c["start"])
    end_str = format_srt_time(c["display_end"])
    spk_label = "Peter" if c["speaker"] == "peter" else "Stewie"
    text = " ".join(w["text"] for w in c["words"])
    srt_entries.append(f"{idx+1}\n{start_str} --> {end_str}\n[{spk_label}] {text}\n")

with open("output/captions.srt", "w", encoding="utf-8") as f:
    f.write("\n".join(srt_entries))

print(f"Wrote {len(srt_entries)} entries to output/captions.srt")
