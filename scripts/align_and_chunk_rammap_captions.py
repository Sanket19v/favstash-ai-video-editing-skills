import json
import re
import os
import subprocess

def clean_word(w):
    return re.sub(r'^[^\w\']+|[^\w\']+$', '', w)

with open("audio/rammap_turns/turns_metadata.json", "r", encoding="utf-8") as f:
    turns = json.load(f)

trimmed_dir = "audio/rammap_trimmed"
os.makedirs(trimmed_dir, exist_ok=True)

current_time = 0.0
INTER_TURN_GAP = 0.08  # 80ms snappy gap

master_chunks = []
turn_ranges = []
concat_files = []

for idx, t in enumerate(turns):
    tid = t["id"]
    spk = t["speaker"]
    sentence = t["text"]
    raw_words = t["words"]
    raw_dur = t["duration"]
    mp3_path = t["mp3_path"]
    
    last_word_end = raw_words[-1]["end"] if raw_words else raw_dur
    keep_dur = min(raw_dur, last_word_end + 0.10)
    
    trimmed_wav = f"{trimmed_dir}/{tid}.wav"
    subprocess.run([
        "ffmpeg", "-y", "-i", mp3_path,
        "-t", f"{keep_dur:.3f}",
        "-af", f"apad=pad_dur={INTER_TURN_GAP}",
        "-ar", "44100", "-ac", "2",
        trimmed_wav
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    
    p = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", trimmed_wav
    ], capture_output=True, text=True, check=True)
    turn_full_dur = float(p.stdout.strip())
    
    turn_start_time = current_time
    turn_speech_end_time = turn_start_time + keep_dur
    turn_end_time = turn_start_time + turn_full_dur
    
    turn_ranges.append({
        "line_index": idx,
        "speaker": spk,
        "start": round(turn_start_time, 3),
        "speech_end": round(turn_speech_end_time, 3),
        "end": round(turn_end_time, 3)
    })
    concat_files.append(trimmed_wav)
    
    sentence_tokens = sentence.split()
    aligned_words = []
    rw_idx = 0
    
    for s_i, tok in enumerate(sentence_tokens):
        w_clean = clean_word(tok)
        best_w = None
        for search_i in range(rw_idx, min(rw_idx + 4, len(raw_words))):
            cand_clean = clean_word(raw_words[search_i]["text"])
            if cand_clean.lower() == w_clean.lower():
                best_w = raw_words[search_i]
                rw_idx = search_i + 1
                break
                
        if best_w is None:
            prev_end = aligned_words[-1]["local_end"] if aligned_words else 0.0
            next_start = keep_dur
            if rw_idx < len(raw_words):
                next_start = raw_words[rw_idx]["start"]
            interpolated_dur = max(0.12, (next_start - prev_end) / max(1, len(sentence_tokens) - s_i))
            w_start = prev_end
            w_end = min(keep_dur, prev_end + interpolated_dur)
        else:
            w_start = best_w["start"]
            w_end = max(w_start + 0.10, best_w["end"])
            
        aligned_words.append({
            "text": tok,
            "local_start": round(w_start, 3),
            "local_end": round(w_end, 3),
            "global_start": round(turn_start_time + w_start, 3),
            "global_end": round(turn_start_time + w_end, 3)
        })
        
    chunks_in_turn = []
    chunk_buffer = []
    for w_idx, w in enumerate(aligned_words):
        chunk_buffer.append(w)
        has_punct = bool(re.search(r'[,.?!;:]$', w["text"]))
        if len(chunk_buffer) >= 3 or (has_punct and len(chunk_buffer) >= 2) or w_idx == len(aligned_words) - 1:
            c_start = chunk_buffer[0]["global_start"]
            c_end = chunk_buffer[-1]["global_end"]
            chunks_in_turn.append({
                "chunk_index": len(master_chunks) + len(chunks_in_turn),
                "turn_index": idx,
                "speaker": spk,
                "start": round(c_start, 3),
                "end": round(c_end, 3),
                "words": chunk_buffer
            })
            chunk_buffer = []
            
    for c_i in range(len(chunks_in_turn)):
        if c_i < len(chunks_in_turn) - 1:
            chunks_in_turn[c_i]["display_end"] = chunks_in_turn[c_i+1]["start"]
        else:
            chunks_in_turn[c_i]["display_end"] = round(turn_end_time, 3)
            
    master_chunks.extend(chunks_in_turn)
    current_time = turn_end_time

print(f"Total video duration: {current_time:.2f}s ({current_time/60:.2f} mins)")
print(f"Total caption chunks: {len(master_chunks)}")

concat_list_file = "audio/master_rammap_concat.txt"
with open(concat_list_file, "w", encoding="utf-8") as f:
    for cw in concat_files:
        f.write(f"file '{os.path.abspath(cw).replace('\\', '/')}'\n")

master_wav = "audio/master_rammap.wav"
subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0",
    "-i", concat_list_file,
    "-c:a", "pcm_s16le",
    master_wav
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

p = subprocess.run([
    "ffprobe", "-v", "error", "-show_entries", "format=duration",
    "-of", "default=noprint_wrappers=1:nokey=1", master_wav
], capture_output=True, text=True, check=True)
final_audio_dur = float(p.stdout.strip())
print(f"Master audio created at {master_wav}: {final_audio_dur:.2f}s")

aligned_output = {
    "total_duration": round(final_audio_dur, 3),
    "turn_ranges": turn_ranges,
    "chunks": master_chunks
}

os.makedirs("video-engine", exist_ok=True)
with open("video-engine/aligned_captions.json", "w", encoding="utf-8") as f:
    json.dump(aligned_output, f, indent=2)

print("Saved video-engine/aligned_captions.json successfully.")

# Also generate output/captions.srt
def format_srt_time(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    ms = int(round((sec - int(sec)) * 1000))
    if ms >= 1000:
        s += 1
        ms -= 1000
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

os.makedirs("video-engine", exist_ok=True)
srt_file = "video-engine/captions.srt"
with open(srt_file, "w", encoding="utf-8") as f:
    for c_idx, ch in enumerate(master_chunks):
        f.write(f"{c_idx + 1}\n")
        f.write(f"{format_srt_time(ch['start'])} --> {format_srt_time(ch['display_end'])}\n")
        words_txt = " ".join(w["text"] for w in ch["words"])
        f.write(f"{words_txt}\n\n")

print(f"Saved {srt_file} successfully.")
