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
    {"character": "peter", "sentence": "Can Windows really use my computer without permission?"},
    {"character": "stewie", "sentence": "It already is. You've been seeding Windows updates to strangers since the day you installed it."},
    {"character": "peter", "sentence": "So everyone's computer is doing this?"},
    {"character": "stewie", "sentence": "Every Windows 10 and 11 PC is secretly part of Microsoft's free CDN network, and one toggle in Settings turns it all off."},
    {"character": "peter", "sentence": "Wait, like BitTorrent seeding?"},
    {"character": "stewie", "sentence": "Exactly. But Microsoft never told you this was turned on by default."},
    {"character": "peter", "sentence": "How much bandwidth are we talking?"},
    {"character": "stewie", "sentence": "Therefore, some users report 80% of their upload speed getting consumed, which is why your Zoom calls freeze."},
    {"character": "peter", "sentence": "That seems illegal."},
    {"character": "stewie", "sentence": "It's buried in the terms you didn't read. But here's what's worse: Task Manager hides it as Service Host, Network Service. So you can't even see what's happening."},
    {"character": "peter", "sentence": "Right. You just see mystery processes eating bandwidth."},
    {"character": "stewie", "sentence": "Therefore, most people blame their ISP instead of Windows."},
    {"character": "peter", "sentence": "Why would Microsoft do this?"},
    {"character": "stewie", "sentence": "They deliver 3.5 billion updates monthly. Peer-to-peer means they offload server costs to your electricity bill and internet plan."},
    {"character": "peter", "sentence": "Do they at least limit it to your local network?"},
    {"character": "stewie", "sentence": "That's the misdirection. There's a setting for PCs on my local network. But the default includes PCs on the internet."},
    {"character": "peter", "sentence": "You're uploading to random strangers worldwide."},
    {"character": "stewie", "sentence": "Yep. Your gaming laptop in Ohio might be seeding updates to someone in Germany right now."},
    {"character": "peter", "sentence": "How do I stop this immediately?"},
    {"character": "stewie", "sentence": "Open Windows Settings. Go to Windows Update. Click Advanced Options. Then Delivery Optimization. Toggle Allow Downloads from Other PCs to Off."},
    {"character": "peter", "sentence": "That's it?"},
    {"character": "stewie", "sentence": "That's it. Five clicks and you're no longer Microsoft's free bandwidth."},
    {"character": "peter", "sentence": "So Task Manager lies, and now Windows steals bandwidth."},
    {"character": "stewie", "sentence": "Task Manager doesn't lie. It just shows you what Microsoft wants you to see."}
]

out_dir = "audio/delivery_opt_turns"
os.makedirs(out_dir, exist_ok=True)
print(f"Synthesizing {len(DIALOGUE)} turns with Fish Audio neural timestamps...")

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
