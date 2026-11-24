import asyncio
import edge_tts
import subprocess
import json
import os

REFINED_SCRIPT = [
    # 00
    {"second": 0, "speaker": "stewie", "line": "Stop right there!",
     "words": ["Stop", "right", "there!"],
     "graphic": "hook_warning", "stepNumber": 0, "title": "New Windows PC?", "breadcrumb": "Important First Steps"},
    # 01
    {"second": 1, "speaker": "peter", "line": "Why, Stewie?",
     "words": ["Why,", "Stewie?"],
     "graphic": "hook_confused", "stepNumber": 0, "title": "New Windows PC?", "breadcrumb": "Don't touch that desktop"},
    # 02
    {"second": 2, "speaker": "stewie", "line": "Change these four!",
     "words": ["Change", "these", "four!"],
     "graphic": "hook_checklist", "stepNumber": 0, "title": "New Windows PC?", "breadcrumb": "4 Critical Setup Steps"},
    # 03
    {"second": 3, "speaker": "stewie", "line": "Step one.",
     "words": ["Step", "one."],
     "graphic": "step1_title", "stepNumber": 1, "title": "Show File Extensions", "breadcrumb": "File Explorer › View › Show"},
    # 04
    {"second": 4, "speaker": "peter", "line": "What extensions?",
     "words": ["What", "extensions?"],
     "graphic": "step1_explorer_closed", "stepNumber": 1, "title": "Show File Extensions", "breadcrumb": "Hidden Extensions Danger"},
    # 05
    {"second": 5, "speaker": "stewie", "line": "Open File Explorer.",
     "words": ["Open", "File", "Explorer."],
     "graphic": "step1_click_view", "stepNumber": 1, "title": "Show File Extensions", "breadcrumb": "Explorer › Toolbar › View"},
    # 06
    {"second": 6, "speaker": "stewie", "line": "Check Extensions.",
     "words": ["Check", "Extensions."],
     "graphic": "step1_dropdown", "stepNumber": 1, "title": "Show File Extensions", "breadcrumb": "View › Show › File name extensions"},
    # 07
    {"second": 7, "speaker": "peter", "line": "It's an EXE?!",
     "words": ["It's", "an", "EXE?!"],
     "graphic": "step1_reveal_exe", "stepNumber": 1, "title": "Show File Extensions", "breadcrumb": "Danger Prevented!"},
    # 08
    {"second": 8, "speaker": "stewie", "line": "Malware avoided!",
     "words": ["Malware", "avoided!"],
     "graphic": "step1_success", "stepNumber": 1, "title": "Show File Extensions", "breadcrumb": "System Protected ✓"},
    # 09
    {"second": 9, "speaker": "stewie", "line": "Step two.",
     "words": ["Step", "two."],
     "graphic": "step2_title", "stepNumber": 2, "title": "Clipboard History", "breadcrumb": "Windows Key + V"},
    # 10
    {"second": 10, "speaker": "peter", "line": "I love Ctrl C!",
     "words": ["I", "love", "Ctrl", "C!"],
     "graphic": "step2_keys_ctrl_c", "stepNumber": 2, "title": "Clipboard History", "breadcrumb": "Forget Ctrl + C"},
    # 11
    {"second": 11, "speaker": "stewie", "line": "Press Win plus V.",
     "words": ["Press", "Win", "plus", "V."],
     "graphic": "step2_keys_win_v", "stepNumber": 2, "title": "Clipboard History", "breadcrumb": "Press ⊞ Win + V"},
    # 12
    {"second": 12, "speaker": "stewie", "line": "Click Turn On.",
     "words": ["Click", "Turn", "On."],
     "graphic": "step2_turn_on", "stepNumber": 2, "title": "Clipboard History", "breadcrumb": "Clipboard Popup › Turn on"},
    # 13
    {"second": 13, "speaker": "peter", "line": "Saved my copies!",
     "words": ["Saved", "my", "copies!"],
     "graphic": "step2_history_list", "stepNumber": 2, "title": "Clipboard History", "breadcrumb": "Multi-item clipboard enabled"},
    # 14
    {"second": 14, "speaker": "stewie", "line": "Pin your favorites.",
     "words": ["Pin", "your", "favorites."],
     "graphic": "step2_pin_item", "stepNumber": 2, "title": "Clipboard History", "breadcrumb": "Pinned Snippets ✓"},
    # 15
    {"second": 15, "speaker": "stewie", "line": "Step three.",
     "words": ["Step", "three."],
     "graphic": "step3_title", "stepNumber": 3, "title": "Kill Startup Apps", "breadcrumb": "Settings › Apps › Startup"},
    # 16
    {"second": 16, "speaker": "peter", "line": "PC boots slow!",
     "words": ["PC", "boots", "slow!"],
     "graphic": "step3_slow_boot", "stepNumber": 3, "title": "Kill Startup Apps", "breadcrumb": "Slow Boot Times"},
    # 17
    {"second": 17, "speaker": "stewie", "line": "Open Startup apps.",
     "words": ["Open", "Startup", "apps."],
     "graphic": "step3_settings_page", "stepNumber": 3, "title": "Kill Startup Apps", "breadcrumb": "Settings › Apps › Startup"},
    # 18
    {"second": 18, "speaker": "stewie", "line": "Turn off junk.",
     "words": ["Turn", "off", "junk."],
     "graphic": "step3_toggle_off", "stepNumber": 3, "title": "Kill Startup Apps", "breadcrumb": "Disable Background Launchers"},
    # 19
    {"second": 19, "speaker": "peter", "line": "Bloat disabled!",
     "words": ["Bloat", "disabled!"],
     "graphic": "step3_disabled_list", "stepNumber": 3, "title": "Kill Startup Apps", "breadcrumb": "Startup Impact: Low"},
    # 20
    {"second": 20, "speaker": "stewie", "line": "Boots instantly now.",
     "words": ["Boots", "instantly", "now."],
     "graphic": "step3_fast_boot", "stepNumber": 3, "title": "Kill Startup Apps", "breadcrumb": "Boot Speed 10x Faster ✓"},
    # 21
    {"second": 21, "speaker": "stewie", "line": "Step four.",
     "words": ["Step", "four."],
     "graphic": "step4_title", "stepNumber": 4, "title": "Enable Storage Sense", "breadcrumb": "Settings › System › Storage"},
    # 22
    {"second": 22, "speaker": "peter", "line": "My disk is full!",
     "words": ["My", "disk", "is", "full!"],
     "graphic": "step4_drive_red", "stepNumber": 4, "title": "Enable Storage Sense", "breadcrumb": "Disk Space Warning"},
    # 23
    {"second": 23, "speaker": "stewie", "line": "Open Storage settings.",
     "words": ["Open", "Storage", "settings."],
     "graphic": "step4_settings_storage", "stepNumber": 4, "title": "Enable Storage Sense", "breadcrumb": "Settings › System › Storage"},
    # 24
    {"second": 24, "speaker": "stewie", "line": "Turn Storage Sense on.",
     "words": ["Turn", "Storage", "Sense", "on."],
     "graphic": "step4_toggle_storage", "stepNumber": 4, "title": "Enable Storage Sense", "breadcrumb": "Storage Sense: On"},
    # 25
    {"second": 25, "speaker": "peter", "line": "Cleaned thirty gigs!",
     "words": ["Cleaned", "thirty", "gigs!"],
     "graphic": "step4_cleaning_counter", "stepNumber": 4, "title": "Enable Storage Sense", "breadcrumb": "30 GB Freed Instantly"},
    # 26
    {"second": 26, "speaker": "stewie", "line": "Temp cache gone.",
     "words": ["Temp", "cache", "gone."],
     "graphic": "step4_drive_green", "stepNumber": 4, "title": "Enable Storage Sense", "breadcrumb": "Auto-Cleanup Active ✓"},
    # 27
    {"second": 27, "speaker": "peter", "line": "My PC is flying!",
     "words": ["My", "PC", "is", "flying!"],
     "graphic": "outro_speedometer", "stepNumber": 0, "title": "All 4 Steps Done!", "breadcrumb": "PC Setup Complete"},
    # 28
    {"second": 28, "speaker": "stewie", "line": "Save this reel.",
     "words": ["Save", "this", "reel."],
     "graphic": "outro_summary_cards", "stepNumber": 0, "title": "PC Optimized", "breadcrumb": "Save This For Later"},
    # 29
    {"second": 29, "speaker": "stewie", "line": "Follow for daily tips!",
     "words": ["Follow", "for", "daily", "tips!"],
     "graphic": "outro_follow_card", "stepNumber": 0, "title": "Follow For More!", "breadcrumb": "@DailyPCTips"}
]

VOICES = {
    "peter": "en-US-GuyNeural",
    "stewie": "en-GB-RyanNeural"
}

os.makedirs("audio/clips", exist_ok=True)
os.makedirs("output", exist_ok=True)

async def generate_refined():
    print("Testing natural duration for all 30 lines (target: <= 0.95s naturally)...")
    over_limit = []
    
    for item in REFINED_SCRIPT:
        idx = item["second"]
        voice = VOICES[item["speaker"]]
        raw_mp3 = f"audio/clips/raw_{idx:02d}.mp3"
        trimmed_wav = f"audio/clips/clip_{idx:02d}.wav"
        pad_wav = f"audio/clips/pad_{idx:02d}.wav"
        
        comm = edge_tts.Communicate(item["line"], voice)
        await comm.save(raw_mp3)
        
        # Silence trim
        cmd = [
            "ffmpeg", "-y", "-i", raw_mp3,
            "-af", "silenceremove=start_periods=1:start_threshold=-40dB,areverse,silenceremove=start_periods=1:start_threshold=-40dB,areverse",
            trimmed_wav
        ]
        subprocess.run(cmd, capture_output=True)
        
        cmd_probe = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", trimmed_wav]
        res = subprocess.run(cmd_probe, capture_output=True, text=True)
        dur = float(res.stdout.strip()) if res.stdout.strip() else 0.0
        
        if dur > 0.95:
            over_limit.append((idx, dur, item["line"]))
            
        # Pad to exactly 1.000s without any pitch or speed distortion
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
        print(f"[{idx:02d}] {dur:.2f}s | {item['speaker']:<6} | {item['line']}")
        
    print(f"\nLines exceeding 0.95s: {len(over_limit)}")
    if over_limit:
        for idx, dur, line in over_limit:
            print(f"  Sec {idx}: {dur:.2f}s -> '{line}'")
    else:
        print("ALL 30 lines naturally fit within 0.95s!")
        
    # Concatenate to master 30.000s
    concat_list_file = "audio/concat_list.txt"
    with open(concat_list_file, "w", encoding="utf-8") as f:
        for i in range(30):
            f.write(f"file 'clips/pad_{i:02d}.wav'\n")
            
    master_audio = "audio/master_30s.wav"
    cmd_concat = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", concat_list_file,
        "-c:a", "pcm_s16le",
        master_audio
    ]
    subprocess.run(cmd_concat, capture_output=True)
    
    cmd_probe = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", master_audio]
    res = subprocess.run(cmd_probe, capture_output=True, text=True)
    print(f"Master audio duration: {res.stdout.strip()}s")
    
    # Save script.json and output/script.json
    with open("script.json", "w", encoding="utf-8") as f:
        json.dump(REFINED_SCRIPT, f, indent=2)
    with open("output/script.json", "w", encoding="utf-8") as f:
        json.dump(REFINED_SCRIPT, f, indent=2)
        
    # Save captions.srt
    with open("output/captions.srt", "w", encoding="utf-8") as f:
        for item in REFINED_SCRIPT:
            sec = item["second"]
            start_s = f"00:00:{sec:02d},050"
            end_s = f"00:00:{sec:02d},950"
            f.write(f"{sec + 1}\n{start_s} --> {end_s}\n{item['line']}\n\n")

if __name__ == "__main__":
    asyncio.run(generate_refined())
