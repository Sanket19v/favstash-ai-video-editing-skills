import json
import subprocess
import os

print("=== Building Frame-Perfect Audio & Caption Sync Pipeline ===")

with open("audio/aligned_turns/all_turns_metadata.json", "r", encoding="utf-8") as f:
    raw_turns = json.load(f)

# 1. TRIM RAW MP3 TO EXACT SPEECH BOUNDS
os.makedirs("audio/trimmed_turns", exist_ok=True)
trimmed_turns = []

for t in raw_turns:
    tid = t["id"]
    spk = t["speaker"]
    raw_mp3 = t["mp3_path"]
    words = t["words"]
    
    first_start = max(0.0, words[0]["start"] - 0.02) if words else 0.0
    last_end = words[-1]["end"] + 0.06 if words else t["duration"]
    trim_dur = last_end - first_start
    
    trimmed_wav = f"audio/trimmed_turns/{tid}_clean.wav"
    subprocess.run([
        "ffmpeg", "-y", "-ss", f"{first_start:.4f}", "-to", f"{last_end:.4f}",
        "-i", raw_mp3, "-ar", "48000", "-ac", "2", trimmed_wav
    ], capture_output=True)
    
    # Offset word timestamps by first_start
    clean_words = []
    for w in words:
        clean_words.append({
            "text": w["text"].strip(),
            "start": round(w["start"] - first_start, 4),
            "end": round(w["end"] - first_start, 4)
        })
        
    trimmed_turns.append({
        "id": tid,
        "speaker": spk,
        "text": t["text"],
        "wav_path": trimmed_wav,
        "duration": trim_dur,
        "words": clean_words
    })

total_clean_dur = sum(t["duration"] for t in trimmed_turns)
print(f"Total trimmed speech duration: {total_clean_dur:.4f}s")

# Target total audio: 30.000s
# Allow 7 natural pauses of ~75ms each between the 8 turns: 7 * 0.075 = 0.525s
target_speech_total = 30.0 - (7 * 0.075) # 29.475s
tempo = total_clean_dur / target_speech_total
print(f"Applying exact uniform tempo factor: {tempo:.5f} (speedup of {(tempo-1)*100:.1f}%)")

# 2. TIME-STRETCH EACH TURN WITH EXACT ATEMPO FILTER
stretched_turns = []
for t in trimmed_turns:
    tid = t["id"]
    in_wav = t["wav_path"]
    out_wav = f"audio/trimmed_turns/{tid}_stretched.wav"
    
    subprocess.run([
        "ffmpeg", "-y", "-i", in_wav,
        "-filter:a", f"atempo={tempo:.6f}",
        "-ar", "48000", "-ac", "2",
        out_wav
    ], capture_output=True)
    
    # Get exact stretched duration
    res = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", out_wav
    ], capture_output=True, text=True)
    stretched_dur = float(res.stdout.strip())
    
    # Scale word timestamps by tempo
    scaled_words = []
    for w in t["words"]:
        scaled_words.append({
            "text": w["text"],
            "start": round(w["start"] / tempo, 4),
            "end": round(w["end"] / tempo, 4)
        })
        
    stretched_turns.append({
        "id": tid,
        "speaker": t["speaker"],
        "text": t["text"],
        "wav_path": out_wav,
        "duration": stretched_dur,
        "words": scaled_words
    })

sum_stretched = sum(t["duration"] for t in stretched_turns)
slack = 30.0 - sum_stretched
pause_exact = slack / 7.0
print(f"Stretched total: {sum_stretched:.4f}s, Slack to 30.0s: {slack:.4f}s, Pause between turns: {pause_exact*1000:.1f}ms")

# 3. BUILD CONCATENATED 30.000000s MASTER AUDIO
pause_wav = "audio/trimmed_turns/exact_pause.wav"
subprocess.run([
    "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
    "-t", f"{pause_exact:.6f}", pause_wav
], capture_output=True)

concat_list_file = "audio/trimmed_turns/concat_list.txt"
with open(concat_list_file, "w") as f:
    for i, t in enumerate(stretched_turns):
        abs_p = os.path.abspath(t["wav_path"]).replace("\\", "/")
        f.write(f"file '{abs_p}'\n")
        if i < len(stretched_turns) - 1:
            abs_sil = os.path.abspath(pause_wav).replace("\\", "/")
            f.write(f"file '{abs_sil}'\n")

master_wav = "audio/master_30s.wav"
subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list_file,
    "-af", "apad=whole_dur=30.0,atrim=0:30.0",
    "-ar", "48000", "-ac", "2",
    master_wav
], capture_output=True)

res = subprocess.run([
    "ffprobe", "-v", "error", "-show_entries", "format=duration",
    "-of", "default=noprint_wrappers=1:nokey=1", master_wav
], capture_output=True, text=True)
print(f"Verified master audio: {master_wav} -> {float(res.stdout.strip()):.6f}s")

# 4. COMPUTE GLOBAL TIMESTAMPS FOR EVERY SINGLE WORD
current_time = 0.0
all_global_words = []
turn_ranges = []

for i, t in enumerate(stretched_turns):
    turn_start = current_time
    for w in t["words"]:
        g_start = round(turn_start + w["start"], 3)
        g_end = round(turn_start + w["end"], 3)
        all_global_words.append({
            "turn_id": t["id"],
            "speaker": t["speaker"],
            "text": w["text"],
            "global_start": g_start,
            "global_end": g_end
        })
    turn_end = round(turn_start + t["duration"], 3)
    turn_ranges.append({
        "turn_id": t["id"],
        "speaker": t["speaker"],
        "start": turn_start,
        "end": turn_end
    })
    current_time = turn_end + pause_exact

print(f"Mapped {len(all_global_words)} words across timeline from 0.00s to {all_global_words[-1]['global_end']:.2f}s")

# 5. CHUNK WORDS INTO NATURAL 2-4 WORD PHRASES (CAPTION CHUNKS)
chunks = []
# Pre-defined natural phrase breaks per turn to match conversational delivery
# Turn 1: "Stewie! My new PC" | "is slow, what settings" | "do I change?"
# Turn 2: "Relax, Peter." | "Open Explorer and enable extensions" | "so you never open fake viruses."
# Turn 3: "Invoices can be viruses?!" | "How do I copy stuff safely?"
# Turn 4: "Press Windows V, you idiot!" | "Clipboard History lets you save" | "and pin everything."
# Turn 5: "Awesome! But bootup" | "takes forever, and my drive is full!"
# Turn 6: "Disable startup apps in Settings," | "and turn Storage Sense On" | "to purge junk!"
# Turn 7: "Holy crap, it is flying!" | "Did I pass the class?"
# Turn 8: "You passed, fat man." | "Follow for more PC tips!"

# Group words into chunks by turn with max 4 words or on punctuation
curr_chunk = []
curr_turn = None
for w in all_global_words:
    tid = w["turn_id"]
    txt = w["text"]
    if tid != curr_turn or len(curr_chunk) >= 4 or (len(curr_chunk) >= 2 and any(p in curr_chunk[-1]["text"] for p in [",", ".", "!", "?", ":"])):
        if curr_chunk:
            chunks.append({
                "chunk_id": len(chunks),
                "turn_id": curr_chunk[0]["turn_id"],
                "speaker": curr_chunk[0]["speaker"],
                "start": curr_chunk[0]["global_start"],
                "end": curr_chunk[-1]["global_end"],
                "words": curr_chunk
            })
            curr_chunk = []
    curr_turn = tid
    curr_chunk.append(w)

if curr_chunk:
    chunks.append({
        "chunk_id": len(chunks),
        "turn_id": curr_chunk[0]["turn_id"],
        "speaker": curr_chunk[0]["speaker"],
        "start": curr_chunk[0]["global_start"],
        "end": curr_chunk[-1]["global_end"],
        "words": curr_chunk
    })

# Ensure continuous display without blackouts between consecutive chunks of the same speaker
for i in range(len(chunks) - 1):
    c_curr = chunks[i]
    c_next = chunks[i + 1]
    if c_curr["turn_id"] == c_next["turn_id"]:
        # Extend current chunk display until next chunk starts so text doesn't flicker
        c_curr["display_end"] = c_next["start"]
    else:
        c_curr["display_end"] = c_curr["end"] + 0.05
chunks[-1]["display_end"] = 30.0

print(f"Generated {len(chunks)} caption chunks:")
for c in chunks:
    line_str = " ".join(w["text"] for w in c["words"])
    print(f"[{c['chunk_id']:02d}] {c['start']:5.2f}s -> {c['display_end']:5.2f}s ({c['speaker']:<6}): \"{line_str}\"")

# 6. WRITE GLOBAL CHUNKS & WORDS TO JSON
with open("video-engine/aligned_captions.json", "w", encoding="utf-8") as f:
    json.dump({
        "total_duration": 30.0,
        "turn_ranges": turn_ranges,
        "chunks": chunks,
        "all_words": all_global_words
    }, f, indent=2)

print("\nSuccessfully built frame-perfect aligned captions and master 30.0s audio!")
