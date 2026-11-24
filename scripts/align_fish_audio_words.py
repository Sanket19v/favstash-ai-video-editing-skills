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

# The 8 conversational turns
TURNS = [
    {"id": "t1", "speaker": "peter", "text": "Stewie! My new PC is slow, what settings do I change?"},
    {"id": "t2", "speaker": "stewie", "text": "Relax, Peter. Open Explorer and enable extensions so you never open fake viruses."},
    {"id": "t3", "speaker": "peter", "text": "Invoices can be viruses?! How do I copy stuff safely?"},
    {"id": "t4", "speaker": "stewie", "text": "Press Windows V, you idiot! Clipboard History lets you save and pin everything."},
    {"id": "t5", "speaker": "peter", "text": "Awesome! But bootup takes forever and my drive is full!"},
    {"id": "t6", "speaker": "stewie", "text": "Disable startup apps in Settings, and turn Storage Sense On to purge junk!"},
    {"id": "t7", "speaker": "peter", "text": "Holy crap, it is flying! Did I pass the class?"},
    {"id": "t8", "speaker": "stewie", "text": "You passed, fat man. Follow for more PC tips!"}
]

os.makedirs("audio/aligned_turns", exist_ok=True)
print("Querying Fish Audio stream with timestamps for all 8 turns...")

all_results = []
for turn in TURNS:
    tid = turn["id"]
    spk = turn["speaker"]
    text = turn["text"]
    v_id = VOICE_IDS[spk]
    
    payload = {
        "text": text,
        "reference_id": v_id,
        "format": "mp3"
    }
    
    resp = requests.post("https://api.fish.audio/v1/tts/stream/with-timestamp", headers=HEADERS, json=payload, stream=True, timeout=30)
    if resp.status_code != 200:
        print(f"Failed turn {tid}: status {resp.status_code}")
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
        except Exception as e:
            pass
            
    raw_mp3 = f"audio/aligned_turns/{tid}.mp3"
    with open(raw_mp3, "wb") as f:
        f.write(audio_bytes)
        
    # Get mp3 duration with ffprobe
    res = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", raw_mp3], capture_output=True, text=True)
    audio_dur = float(res.stdout.strip())
    
    # Deduplicate segments (Fish Audio sometimes repeats segments in chunks)
    unique_words = []
    seen = set()
    for s in raw_segments:
        key = (s.get("text"), round(s.get("start", 0), 3), round(s.get("end", 0), 3))
        if key not in seen:
            seen.add(key)
            unique_words.append(s)
            
    print(f"[{tid}] {spk:<6} | Audio dur: {audio_dur:.2f}s | Words count: {len(unique_words)}")
    for w in unique_words[:6]:
        print(f"   {w.get('text'):<12} {w.get('start', 0):.2f} -> {w.get('end', 0):.2f}")
    if len(unique_words) > 6:
        print(f"   ... ({len(unique_words) - 6} more words)")
        
    all_results.append({
        "id": tid,
        "speaker": spk,
        "text": text,
        "mp3_path": raw_mp3,
        "duration": audio_dur,
        "words": unique_words
    })

with open("audio/aligned_turns/all_turns_metadata.json", "w") as f:
    json.dump(all_results, f, indent=2)

print("\nDone querying Fish Audio aligned turns!")
