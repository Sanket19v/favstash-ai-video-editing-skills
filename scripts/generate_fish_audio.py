import requests
import json
import os
import subprocess
import time

API_KEY = "sk-fish-PJ2OwPuOjXeKCRmc4Bpzvzl4dAbrUZUig08hfnbgFNg"
VOICE_IDS = {
    "peter": "b1d36a18f8d84bd59dead30474cbe3d7",
    "stewie": "08311ef33d5243ef9d8cdd87234e5982"
}

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "model": "s2.1-pro-free"
}

with open("script.json", "r", encoding="utf-8") as f:
    script = json.load(f)

os.makedirs("audio/fish_clips", exist_ok=True)

print("Synthesizing authentic Peter & Stewie voices via Fish Audio API...")

for item in script:
    sec = item["second"]
    spk = item["speaker"]
    line = item["line"]
    v_id = VOICE_IDS[spk]
    
    raw_mp3 = f"audio/fish_clips/raw_{sec:02d}.mp3"
    trimmed_wav = f"audio/fish_clips/clip_{sec:02d}.wav"
    pad_wav = f"audio/fish_clips/pad_{sec:02d}.wav"
    
    payload = {
        "text": line,
        "reference_id": v_id,
        "format": "mp3"
    }
    
    # Retry loop in case of transient rate-limits
    for attempt in range(3):
        try:
            resp = requests.post("https://api.fish.audio/v1/tts", headers=HEADERS, json=payload, timeout=20)
            if resp.status_code == 200:
                with open(raw_mp3, "wb") as f_out:
                    f_out.write(resp.content)
                break
            else:
                print(f"Warning: line {sec} returned {resp.status_code}: {resp.text}")
                time.sleep(1)
        except Exception as e:
            print(f"Error for line {sec}: {e}")
            time.sleep(1)
            
    # Silence trim
    cmd_trim = [
        "ffmpeg", "-y", "-i", raw_mp3,
        "-af", "silenceremove=start_periods=1:start_threshold=-35dB,areverse,silenceremove=start_periods=1:start_threshold=-35dB,areverse",
        trimmed_wav
    ]
    subprocess.run(cmd_trim, capture_output=True)
    
    # Measure trimmed duration
    cmd_probe = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", trimmed_wav]
    res = subprocess.run(cmd_probe, capture_output=True, text=True)
    dur = float(res.stdout.strip()) if res.stdout.strip() else 0.5
    
    # If dur > 0.98, atempo slightly to 0.95
    if dur > 0.98:
        speed = dur / 0.95
        cmd_pad = [
            "ffmpeg", "-y", "-i", trimmed_wav,
            "-filter:a", f"atempo={speed:.3f},apad=whole_dur=1.0",
            "-t", "1.0", pad_wav
        ]
        dur = 0.95
    else:
        cmd_pad = [
            "ffmpeg", "-y", "-i", trimmed_wav,
            "-filter:a", "apad=whole_dur=1.0",
            "-t", "1.0", pad_wav
        ]
    subprocess.run(cmd_pad, capture_output=True)
    
    # Calculate word timestamps
    words = item["words"]
    start_t = 0.05
    end_t = min(dur + 0.05, 0.95)
    word_span = (end_t - start_t) / len(words)
    
    caption_words = []
    for w_i, word in enumerate(words):
        w_start = round(start_t + w_i * word_span, 3)
        w_end = round(start_t + (w_i + 1) * word_span, 3)
        caption_words.append({
            "text": word,
            "start": w_start,
            "end": w_end
        })
        
    item["captionWords"] = caption_words
    item["clipDuration"] = dur
    print(f"[{sec:02d}] {dur:.2f}s | {spk:<6} | '{line}'")
    time.sleep(0.1)

# Concat to master audio
concat_list = "audio/fish_concat_list.txt"
with open(concat_list, "w", encoding="utf-8") as f:
    for i in range(30):
        f.write(f"file 'fish_clips/pad_{i:02d}.wav'\n")

master_audio = "audio/master_30s.wav"
cmd_concat = [
    "ffmpeg", "-y", "-f", "concat", "-safe", "0",
    "-i", concat_list,
    "-c:a", "pcm_s16le",
    master_audio
]
subprocess.run(cmd_concat, capture_output=True)

# Probe master audio
cmd_probe = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", master_audio]
res = subprocess.run(cmd_probe, capture_output=True, text=True)
print(f"\nFinal Fish Audio master duration: {res.stdout.strip()}s")

# Save script.json and output/script.json
with open("script.json", "w", encoding="utf-8") as f:
    json.dump(script, f, indent=2)
with open("output/script.json", "w", encoding="utf-8") as f:
    json.dump(script, f, indent=2)
with open("video-engine/script.json", "w", encoding="utf-8") as f:
    json.dump(script, f, indent=2)

# Save output/captions.srt
with open("output/captions.srt", "w", encoding="utf-8") as f:
    for item in script:
        sec = item["second"]
        start_s = f"00:00:{sec:02d},050"
        end_s = f"00:00:{sec:02d},950"
        f.write(f"{sec + 1}\n{start_s} --> {end_s}\n{item['line']}\n\n")

print("All audio files, script.json, and captions.srt updated with authentic Peter & Stewie voices!")
