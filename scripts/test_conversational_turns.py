import requests
import json
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

TURNS = [
    {
        "id": "t1", "speaker": "peter", "target_dur": 3.0,
        "text": "Stewie, look at my new PC! It's so slow, what settings should I change first?"
    },
    {
        "id": "t2", "speaker": "stewie", "target_dur": 5.5,
        "text": "Relax, Peter! First, open File Explorer and turn on file extensions so you don't run fake PDF viruses."
    },
    {
        "id": "t3", "speaker": "peter", "target_dur": 3.5,
        "text": "Holy crap, that invoice was an EXE?! How do I copy all my files without losing them?"
    },
    {
        "id": "t4", "speaker": "stewie", "target_dur": 5.5,
        "text": "Press Windows key V, you fool! Turn on Clipboard History and you can save and pin every single copy."
    },
    {
        "id": "t5", "speaker": "peter", "target_dur": 4.0,
        "text": "That's awesome! But why does my boot take so long, and my hard drive is completely packed?"
    },
    {
        "id": "t6", "speaker": "stewie", "target_dur": 5.5,
        "text": "Disable background startup apps in Settings, and toggle Storage Sense On to purge thirty gigs of junk automatically!"
    },
    {
        "id": "t7", "speaker": "peter", "target_dur": 1.7,
        "text": "My PC is flying! Did I pass the class, Stewie?"
    },
    {
        "id": "t8", "speaker": "stewie", "target_dur": 1.3,
        "text": "You earned an A-plus! Follow for more tips!"
    }
]

os.makedirs("audio/turns", exist_ok=True)
print("Testing full conversational turns synthesis via Fish Audio...")

total_raw_dur = 0.0
for turn in TURNS:
    t_id = turn["id"]
    spk = turn["speaker"]
    text = turn["text"]
    v_id = VOICE_IDS[spk]
    
    raw_mp3 = f"audio/turns/{t_id}.mp3"
    trimmed_wav = f"audio/turns/{t_id}_trimmed.wav"
    
    payload = {"text": text, "reference_id": v_id, "format": "mp3"}
    resp = requests.post("https://api.fish.audio/v1/tts", headers=HEADERS, json=payload, timeout=20)
    with open(raw_mp3, "wb") as f:
        f.write(resp.content)
        
    cmd_trim = [
        "ffmpeg", "-y", "-i", raw_mp3,
        "-af", "silenceremove=start_periods=1:start_threshold=-35dB,areverse,silenceremove=start_periods=1:start_threshold=-35dB,areverse",
        trimmed_wav
    ]
    subprocess.run(cmd_trim, capture_output=True)
    
    cmd_probe = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", trimmed_wav]
    res = subprocess.run(cmd_probe, capture_output=True, text=True)
    dur = float(res.stdout.strip())
    total_raw_dur += dur
    print(f"[{t_id}] {dur:.2f}s (target ~{turn['target_dur']:.1f}s) | {spk:<6} | '{text}'")

print(f"\nTotal raw conversation duration: {total_raw_dur:.2f}s (Target: exactly 30.00s)")
