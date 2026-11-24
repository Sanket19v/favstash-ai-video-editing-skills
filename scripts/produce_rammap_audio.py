import requests
import json
import base64
import subprocess
import os

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

DIALOGUE = [
    {"character": "peter", "sentence": "Stewie, my PC is running slow, my FPS isn't great, and my RAM usage is insanely high even when I barely have anything open."},
    {"character": "stewie", "sentence": "And RAM isn't exactly cheap, right? This can help you find out what's eating all that memory."},
    {"character": "peter", "sentence": "Okay, what do I need?"},
    {"character": "stewie", "sentence": "Just type RAMMap and go to the first site."},
    {"character": "peter", "sentence": "But before someone in the comments says it's a virus, is this actually safe?"},
    {"character": "stewie", "sentence": "It's a Microsoft site, okay?"},
    {"character": "peter", "sentence": "Alright, what do I click?"},
    {"character": "stewie", "sentence": "Click this option, then choose where you want to download it."},
    {"character": "peter", "sentence": "And here's the file. Now what?"},
    {"character": "stewie", "sentence": "Click it and run it as administrator. Then just wait a few seconds for it to load all the memory processes."},
    {"character": "peter", "sentence": "So I can actually see what's happening in real time?"},
    {"character": "stewie", "sentence": "Exactly. You can see how your memory is being used in real time. Here, 45% of the memory is being used."},
    {"character": "peter", "sentence": "Okay, where do I go next?"},
    {"character": "stewie", "sentence": "Come to this second option, click the first one, Working Sets."},
    {"character": "peter", "sentence": "And it's already going down."},
    {"character": "stewie", "sentence": "Yep. You can already see the memory usage lowering."},
    {"character": "peter", "sentence": "Can we free up even more?"},
    {"character": "stewie", "sentence": "Go back to the second option and then select the Standby List option."},
    {"character": "peter", "sentence": "What's on the Standby List?"},
    {"character": "stewie", "sentence": "Those are programs you've already closed but are still eating up memory."},
    {"character": "peter", "sentence": "And look at that. Over 10 gigs are available now."},
    {"character": "stewie", "sentence": "Exactly. That's over 10 gigs you can now have available to play your games smoothly or run any other heavy task on your PC."},
    {"character": "peter", "sentence": "Okay, now I want the whole PC optimized."},
    {"character": "stewie", "sentence": "I should fully optimize your PC, Windows, BIOS, and games. Do follow."}
]

out_dir = "audio/rammap_turns"
os.makedirs(out_dir, exist_ok=True)
print(f"Synthesizing {len(DIALOGUE)} turns for RAMMap with Fish Audio neural timestamps...")

results = []
for idx, d in enumerate(DIALOGUE):
    tid = f"line_{idx:02d}"
    spk = d["character"]
    text = d["sentence"]
    v_id = VOICE_IDS[spk]
    
    payload = {
        "text": text,
        "reference_id": v_id,
        "format": "mp3"
    }
    
    resp = requests.post("https://api.fish.audio/v1/tts/stream/with-timestamp", headers=HEADERS, json=payload, stream=True, timeout=30)
    if resp.status_code != 200:
        print(f"Error {resp.status_code} on line {idx}: {resp.text[:100]}")
        continue
        
    audio_bytes = bytearray()
    raw_segments = []
    for raw_line in resp.iter_lines(decode_unicode=True):
        if not raw_line or not raw_line.startswith("data:"):
            continue
        payload_str = raw_line[len("data:"):].strip()
        if payload_str == "[DONE]":
            break
        try:
            event = json.loads(payload_str)
            if "audio_base64" in event:
                audio_bytes.extend(base64.b64decode(event["audio_base64"]))
            if "alignment" in event and event["alignment"]:
                for seg in event["alignment"].get("segments", []):
                    raw_segments.append(seg)
        except Exception:
            pass
            
    mp3_file = f"{out_dir}/{tid}.mp3"
    with open(mp3_file, "wb") as f:
        f.write(audio_bytes)
        
    # Deduplicate segments
    unique_words = []
    seen = set()
    for s in raw_segments:
        key = (s.get("text"), round(s.get("start", 0), 3), round(s.get("end", 0), 3))
        if key not in seen:
            seen.add(key)
            unique_words.append(s)
            
    # Probe duration
    res = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", mp3_file], capture_output=True, text=True)
    dur = float(res.stdout.strip())
    
    print(f"[{tid}] {spk:<6} | dur: {dur:.2f}s | words: {len(unique_words):2d} | \"{text[:45]}...\"")
    results.append({
        "line_index": idx,
        "id": tid,
        "speaker": spk,
        "text": text,
        "mp3_path": mp3_file,
        "duration": dur,
        "words": unique_words
    })

meta_path = f"{out_dir}/turns_metadata.json"
with open(meta_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

total_raw = sum(r["duration"] for r in results)
print(f"\nCompleted! Total raw audio duration: {total_raw:.2f}s ({total_raw/60:.1f} mins) across {len(results)} lines.")
