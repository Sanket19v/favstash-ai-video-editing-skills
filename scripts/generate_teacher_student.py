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

SCRIPT_CONVERSATION = [
    # HOOK
    {"second": 0, "speaker": "peter", "line": "Teach me PC, Stewie!",
     "words": ["Teach", "me", "PC,", "Stewie!"],
     "graphic": "hook_warning", "stepNumber": 0, "title": "PC Masterclass", "breadcrumb": "Student Peter vs Teacher Stewie"},
    {"second": 1, "speaker": "stewie", "line": "Class is in session.",
     "words": ["Class", "is", "in", "session."],
     "graphic": "hook_confused", "stepNumber": 0, "title": "PC Masterclass", "breadcrumb": "Rule #1: Fix Defaults First"},
    {"second": 2, "speaker": "peter", "line": "What setting first?",
     "words": ["What", "setting", "first?"],
     "graphic": "hook_checklist", "stepNumber": 0, "title": "PC Masterclass", "breadcrumb": "4 Essential Lessons"},
     
    # LESSON 1: FILE EXTENSIONS
    {"second": 3, "speaker": "stewie", "line": "Lesson one: File extensions.",
     "words": ["Lesson", "one:", "File", "extensions."],
     "graphic": "step1_title", "stepNumber": 1, "title": "Show File Extensions", "breadcrumb": "File Explorer › View › Show"},
    {"second": 4, "speaker": "peter", "line": "Why? What's wrong?",
     "words": ["Why?", "What's", "wrong?"],
     "graphic": "step1_explorer_closed", "stepNumber": 1, "title": "Show File Extensions", "breadcrumb": "Hidden File Format Danger"},
    {"second": 5, "speaker": "stewie", "line": "Open Explorer, click View.",
     "words": ["Open", "Explorer,", "click", "View."],
     "graphic": "step1_click_view", "stepNumber": 1, "title": "Show File Extensions", "breadcrumb": "Explorer › Toolbar › View"},
    {"second": 6, "speaker": "peter", "line": "Check File extensions?",
     "words": ["Check", "File", "extensions?"],
     "graphic": "step1_dropdown", "stepNumber": 1, "title": "Show File Extensions", "breadcrumb": "View › Show › File name extensions"},
    {"second": 7, "speaker": "stewie", "line": "Yes! That's fake PDF!",
     "words": ["Yes!", "That's", "fake", "PDF!"],
     "graphic": "step1_reveal_exe", "stepNumber": 1, "title": "Show File Extensions", "breadcrumb": "Disguised Malware Detected!"},
    {"second": 8, "speaker": "peter", "line": "It's an EXE malware!",
     "words": ["It's", "an", "EXE", "malware!"],
     "graphic": "step1_success", "stepNumber": 1, "title": "Show File Extensions", "breadcrumb": "Virus Avoided ✓"},
     
    # LESSON 2: CLIPBOARD HISTORY
    {"second": 9, "speaker": "stewie", "line": "Lesson two: Clipboard History.",
     "words": ["Lesson", "two:", "Clipboard", "History."],
     "graphic": "step2_title", "stepNumber": 2, "title": "Clipboard History", "breadcrumb": "Windows Key + V"},
    {"second": 10, "speaker": "peter", "line": "Can I copy multiple?",
     "words": ["Can", "I", "copy", "multiple?"],
     "graphic": "step2_keys_ctrl_c", "stepNumber": 2, "title": "Clipboard History", "breadcrumb": "Forget Single Ctrl + C"},
    {"second": 11, "speaker": "stewie", "line": "Press Windows key V.",
     "words": ["Press", "Windows", "key", "V."],
     "graphic": "step2_keys_win_v", "stepNumber": 2, "title": "Clipboard History", "breadcrumb": "Shortcut: ⊞ Win + V"},
    {"second": 12, "speaker": "peter", "line": "And click Turn On?",
     "words": ["And", "click", "Turn", "On?"],
     "graphic": "step2_turn_on", "stepNumber": 2, "title": "Clipboard History", "breadcrumb": "Click 'Turn on' Button"},
    {"second": 13, "speaker": "stewie", "line": "All your copies save!",
     "words": ["All", "your", "copies", "save!"],
     "graphic": "step2_history_list", "stepNumber": 2, "title": "Clipboard History", "breadcrumb": "Multi-Snippet History"},
    {"second": 14, "speaker": "peter", "line": "Stewie, you're a genius!",
     "words": ["Stewie,", "you're", "a", "genius!"],
     "graphic": "step2_pin_item", "stepNumber": 2, "title": "Clipboard History", "breadcrumb": "Pin Favorite Clips ✓"},
     
    # LESSON 3: STARTUP APPS
    {"second": 15, "speaker": "stewie", "line": "Lesson three: Startup apps.",
     "words": ["Lesson", "three:", "Startup", "apps."],
     "graphic": "step3_title", "stepNumber": 3, "title": "Kill Startup Apps", "breadcrumb": "Settings › Apps › Startup"},
    {"second": 16, "speaker": "peter", "line": "Why boots so slow?",
     "words": ["Why", "boots", "so", "slow?"],
     "graphic": "step3_slow_boot", "stepNumber": 3, "title": "Kill Startup Apps", "breadcrumb": "Boot Lag Problem"},
    {"second": 17, "speaker": "stewie", "line": "Open Settings, Apps, Startup.",
     "words": ["Open", "Settings,", "Apps,", "Startup."],
     "graphic": "step3_settings_page", "stepNumber": 3, "title": "Kill Startup Apps", "breadcrumb": "Settings › Apps › Startup"},
    {"second": 18, "speaker": "peter", "line": "Turn off everything?",
     "words": ["Turn", "off", "everything?"],
     "graphic": "step3_toggle_off", "stepNumber": 3, "title": "Kill Startup Apps", "breadcrumb": "Toggle Background Launchers"},
    {"second": 19, "speaker": "stewie", "line": "Turn off background junk!",
     "words": ["Turn", "off", "background", "junk!"],
     "graphic": "step3_disabled_list", "stepNumber": 3, "title": "Kill Startup Apps", "breadcrumb": "Startup Impact: Low"},
    {"second": 20, "speaker": "peter", "line": "Boots in ten seconds!",
     "words": ["Boots", "in", "ten", "seconds!"],
     "graphic": "step3_fast_boot", "stepNumber": 3, "title": "Kill Startup Apps", "breadcrumb": "10x Boot Acceleration ✓"},
     
    # LESSON 4: STORAGE SENSE
    {"second": 21, "speaker": "stewie", "line": "Lesson four: Storage Sense.",
     "words": ["Lesson", "four:", "Storage", "Sense."],
     "graphic": "step4_title", "stepNumber": 4, "title": "Enable Storage Sense", "breadcrumb": "Settings › System › Storage"},
    {"second": 22, "speaker": "peter", "line": "Is my disk full?",
     "words": ["Is", "my", "disk", "full?"],
     "graphic": "step4_drive_red", "stepNumber": 4, "title": "Enable Storage Sense", "breadcrumb": "C: Drive Out of Space"},
    {"second": 23, "speaker": "stewie", "line": "Go to System, Storage.",
     "words": ["Go", "to", "System,", "Storage."],
     "graphic": "step4_settings_storage", "stepNumber": 4, "title": "Enable Storage Sense", "breadcrumb": "Settings › System › Storage"},
    {"second": 24, "speaker": "peter", "line": "Toggle it On now?",
     "words": ["Toggle", "it", "On", "now?"],
     "graphic": "step4_toggle_storage", "stepNumber": 4, "title": "Enable Storage Sense", "breadcrumb": "Toggle Switch: On"},
    {"second": 25, "speaker": "stewie", "line": "It purges temp junk!",
     "words": ["It", "purges", "temp", "junk!"],
     "graphic": "step4_cleaning_counter", "stepNumber": 4, "title": "Enable Storage Sense", "breadcrumb": "Auto-Cleaner Activated"},
    {"second": 26, "speaker": "peter", "line": "Thirty gigabytes back!",
     "words": ["Thirty", "gigabytes", "back!"],
     "graphic": "step4_drive_green", "stepNumber": 4, "title": "Enable Storage Sense", "breadcrumb": "30 GB Reclaimed ✓"},
     
    # OUTRO
    {"second": 27, "speaker": "peter", "line": "Did I pass, teacher?",
     "words": ["Did", "I", "pass,", "teacher?"],
     "graphic": "outro_speedometer", "stepNumber": 0, "title": "Final Grade: A+", "breadcrumb": "Class Dismissed"},
    {"second": 28, "speaker": "stewie", "line": "You earned an A-plus!",
     "words": ["You", "earned", "an", "A-plus!"],
     "graphic": "outro_summary_cards", "stepNumber": 0, "title": "PC Masterclass", "breadcrumb": "All 4 Lessons Passed"},
    {"second": 29, "speaker": "stewie", "line": "Follow for daily lessons!",
     "words": ["Follow", "for", "daily", "lessons!"],
     "graphic": "outro_follow_card", "stepNumber": 0, "title": "Follow For More!", "breadcrumb": "@DailyPCTips"}
]

os.makedirs("audio/qna_clips", exist_ok=True)
print("Synthesizing Teacher & Student Q&A conversation via Fish Audio...")

for item in SCRIPT_CONVERSATION:
    sec = item["second"]
    spk = item["speaker"]
    line = item["line"]
    v_id = VOICE_IDS[spk]
    
    raw_mp3 = f"audio/qna_clips/raw_{sec:02d}.mp3"
    trimmed_wav = f"audio/qna_clips/clip_{sec:02d}.wav"
    pad_wav = f"audio/qna_clips/pad_{sec:02d}.wav"
    
    payload = {
        "text": line,
        "reference_id": v_id,
        "format": "mp3"
    }
    
    for attempt in range(3):
        try:
            resp = requests.post("https://api.fish.audio/v1/tts", headers=HEADERS, json=payload, timeout=20)
            if resp.status_code == 200:
                with open(raw_mp3, "wb") as f_out:
                    f_out.write(resp.content)
                break
            else:
                time.sleep(1)
        except Exception as e:
            time.sleep(1)
            
    # Silence trim
    cmd_trim = [
        "ffmpeg", "-y", "-i", raw_mp3,
        "-af", "silenceremove=start_periods=1:start_threshold=-35dB,areverse,silenceremove=start_periods=1:start_threshold=-35dB,areverse",
        trimmed_wav
    ]
    subprocess.run(cmd_trim, capture_output=True)
    
    cmd_probe = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", trimmed_wav]
    res = subprocess.run(cmd_probe, capture_output=True, text=True)
    dur = float(res.stdout.strip()) if res.stdout.strip() else 0.5
    
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
    
    # Word timestamps
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
    role = "STUDENT" if spk == "peter" else "TEACHER"
    print(f"[{sec:02d}] {dur:.2f}s | {role:<7} ({spk}) | '{line}'")
    time.sleep(0.1)

# Concat to master audio
concat_list = "audio/qna_concat_list.txt"
with open(concat_list, "w", encoding="utf-8") as f:
    for i in range(30):
        f.write(f"file 'qna_clips/pad_{i:02d}.wav'\n")

master_audio = "audio/master_30s.wav"
cmd_concat = [
    "ffmpeg", "-y", "-f", "concat", "-safe", "0",
    "-i", concat_list,
    "-c:a", "pcm_s16le",
    master_audio
]
subprocess.run(cmd_concat, capture_output=True)

# Probe duration
cmd_probe = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", master_audio]
res = subprocess.run(cmd_probe, capture_output=True, text=True)
print(f"\nFinal Q&A Master Duration: {res.stdout.strip()}s")

# Save script.json and output/script.json
with open("script.json", "w", encoding="utf-8") as f:
    json.dump(SCRIPT_CONVERSATION, f, indent=2)
with open("output/script.json", "w", encoding="utf-8") as f:
    json.dump(SCRIPT_CONVERSATION, f, indent=2)
with open("video-engine/script.json", "w", encoding="utf-8") as f:
    json.dump(SCRIPT_CONVERSATION, f, indent=2)

# Save output/captions.srt
with open("output/captions.srt", "w", encoding="utf-8") as f:
    for item in SCRIPT_CONVERSATION:
        sec = item["second"]
        start_s = f"00:00:{sec:02d},050"
        end_s = f"00:00:{sec:02d},950"
        f.write(f"{sec + 1}\n{start_s} --> {end_s}\n{item['line']}\n\n")

print("Q&A conversation script and audio generated successfully!")
