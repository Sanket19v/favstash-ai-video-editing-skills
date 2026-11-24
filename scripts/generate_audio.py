import asyncio
import os
import json
import subprocess
import edge_tts

# 30-second script definition
SCRIPT_LINES = [
    # 00
    {
        "second": 0, "speaker": "stewie", "line": "Stop right there!",
        "words": ["Stop", "right", "there!"],
        "graphic": "hook_warning", "stepNumber": 0, "title": "New Windows PC?", "breadcrumb": "Important First Steps"
    },
    # 01
    {
        "second": 1, "speaker": "peter", "line": "Why? What did I do?",
        "words": ["Why?", "What", "did", "I", "do?"],
        "graphic": "hook_confused", "stepNumber": 0, "title": "New Windows PC?", "breadcrumb": "Don't touch that desktop"
    },
    # 02
    {
        "second": 2, "speaker": "stewie", "line": "Change these four settings first!",
        "words": ["Change", "these", "four", "settings!"],
        "graphic": "hook_checklist", "stepNumber": 0, "title": "New Windows PC?", "breadcrumb": "4 Critical Setup Steps"
    },
    # 03
    {
        "second": 3, "speaker": "stewie", "line": "Step one: File extensions.",
        "words": ["Step", "one:", "File", "extensions."],
        "graphic": "step1_title", "stepNumber": 1, "title": "Show File Extensions", "breadcrumb": "File Explorer › View › Show"
    },
    # 04
    {
        "second": 4, "speaker": "peter", "line": "Extensions? Sounds scary!",
        "words": ["Extensions?", "Sounds", "too", "scary!"],
        "graphic": "step1_explorer_closed", "stepNumber": 1, "title": "Show File Extensions", "breadcrumb": "Hidden Extensions Danger"
    },
    # 05
    {
        "second": 5, "speaker": "stewie", "line": "Open Explorer, click View.",
        "words": ["Open", "Explorer,", "click", "View."],
        "graphic": "step1_click_view", "stepNumber": 1, "title": "Show File Extensions", "breadcrumb": "Explorer › Toolbar › View"
    },
    # 06
    {
        "second": 6, "speaker": "stewie", "line": "Hover Show, check Extensions.",
        "words": ["Hover", "Show,", "check", "Extensions."],
        "graphic": "step1_dropdown", "stepNumber": 1, "title": "Show File Extensions", "breadcrumb": "View › Show › File name extensions"
    },
    # 07
    {
        "second": 7, "speaker": "peter", "line": "Wait! Invoice is an EXE?!",
        "words": ["Wait!", "Invoice", "is", "an", "EXE?!"],
        "graphic": "step1_reveal_exe", "stepNumber": 1, "title": "Show File Extensions", "breadcrumb": "Danger Prevented!"
    },
    # 08
    {
        "second": 8, "speaker": "stewie", "line": "Exactly. You avoided malware.",
        "words": ["Exactly.", "You", "avoided", "malware."],
        "graphic": "step1_success", "stepNumber": 1, "title": "Show File Extensions", "breadcrumb": "System Protected ✓"
    },
    # 09
    {
        "second": 9, "speaker": "stewie", "line": "Step two: Clipboard History.",
        "words": ["Step", "two:", "Clipboard", "History."],
        "graphic": "step2_title", "stepNumber": 2, "title": "Clipboard History", "breadcrumb": "Windows Key + V"
    },
    # 10
    {
        "second": 10, "speaker": "peter", "line": "I only know Control C!",
        "words": ["I", "only", "know", "Control", "C!"],
        "graphic": "step2_keys_ctrl_c", "stepNumber": 2, "title": "Clipboard History", "breadcrumb": "Forget Ctrl + C"
    },
    # 11
    {
        "second": 11, "speaker": "stewie", "line": "Press Windows key plus V.",
        "words": ["Press", "Windows", "plus", "V."],
        "graphic": "step2_keys_win_v", "stepNumber": 2, "title": "Clipboard History", "breadcrumb": "Press ⊞ Win + V"
    },
    # 12
    {
        "second": 12, "speaker": "stewie", "line": "Click Turn On now.",
        "words": ["Click", "Turn", "On", "now."],
        "graphic": "step2_turn_on", "stepNumber": 2, "title": "Clipboard History", "breadcrumb": "Clipboard Popup › Turn on"
    },
    # 13
    {
        "second": 13, "speaker": "peter", "line": "It saved all my copies!",
        "words": ["It", "saved", "all", "my", "copies!"],
        "graphic": "step2_history_list", "stepNumber": 2, "title": "Clipboard History", "breadcrumb": "Multi-item clipboard enabled"
    },
    # 14
    {
        "second": 14, "speaker": "stewie", "line": "Never lose copied text!",
        "words": ["Never", "lose", "copied", "text!"],
        "graphic": "step2_pin_item", "stepNumber": 2, "title": "Clipboard History", "breadcrumb": "Pinned Snippets ✓"
    },
    # 15
    {
        "second": 15, "speaker": "stewie", "line": "Step three: Kill startup apps.",
        "words": ["Step", "three:", "Kill", "startup", "apps."],
        "graphic": "step3_title", "stepNumber": 3, "title": "Kill Startup Apps", "breadcrumb": "Settings › Apps › Startup"
    },
    # 16
    {
        "second": 16, "speaker": "peter", "line": "My boot takes five minutes!",
        "words": ["My", "boot", "takes", "five", "minutes!"],
        "graphic": "step3_slow_boot", "stepNumber": 3, "title": "Kill Startup Apps", "breadcrumb": "Slow Boot Times"
    },
    # 17
    {
        "second": 17, "speaker": "stewie", "line": "Open Settings, Apps, Startup.",
        "words": ["Open", "Settings,", "Apps,", "Startup."],
        "graphic": "step3_settings_page", "stepNumber": 3, "title": "Kill Startup Apps", "breadcrumb": "Settings › Apps › Startup"
    },
    # 18
    {
        "second": 18, "speaker": "stewie", "line": "Turn off high impact junk.",
        "words": ["Turn", "off", "high", "impact", "junk."],
        "graphic": "step3_toggle_off", "stepNumber": 3, "title": "Kill Startup Apps", "breadcrumb": "Disable Background Launchers"
    },
    # 19
    {
        "second": 19, "speaker": "peter", "line": "Background apps disabled!",
        "words": ["Background", "apps", "disabled!"],
        "graphic": "step3_disabled_list", "stepNumber": 3, "title": "Kill Startup Apps", "breadcrumb": "Startup Impact: Low"
    },
    # 20
    {
        "second": 20, "speaker": "stewie", "line": "Your PC boots instantly!",
        "words": ["Your", "PC", "boots", "instantly!"],
        "graphic": "step3_fast_boot", "stepNumber": 3, "title": "Kill Startup Apps", "breadcrumb": "Boot Speed 10x Faster ✓"
    },
    # 21
    {
        "second": 21, "speaker": "stewie", "line": "Step four: Storage Sense.",
        "words": ["Step", "four:", "Storage", "Sense."],
        "graphic": "step4_title", "stepNumber": 4, "title": "Enable Storage Sense", "breadcrumb": "Settings › System › Storage"
    },
    # 22
    {
        "second": 22, "speaker": "peter", "line": "My drive is already full!",
        "words": ["My", "drive", "is", "already", "full!"],
        "graphic": "step4_drive_red", "stepNumber": 4, "title": "Enable Storage Sense", "breadcrumb": "Disk Space Warning"
    },
    # 23
    {
        "second": 23, "speaker": "stewie", "line": "Go to System, then Storage.",
        "words": ["Go", "to", "System,", "then", "Storage."],
        "graphic": "step4_settings_storage", "stepNumber": 4, "title": "Enable Storage Sense", "breadcrumb": "Settings › System › Storage"
    },
    # 24
    {
        "second": 24, "speaker": "stewie", "line": "Toggle Storage Sense On.",
        "words": ["Toggle", "Storage", "Sense", "On."],
        "graphic": "step4_toggle_storage", "stepNumber": 4, "title": "Enable Storage Sense", "breadcrumb": "Storage Sense: On"
    },
    # 25
    {
        "second": 25, "speaker": "peter", "line": "Cleaned thirty gigabytes!",
        "words": ["Cleaned", "thirty", "gigabytes!"],
        "graphic": "step4_cleaning_counter", "stepNumber": 4, "title": "Enable Storage Sense", "breadcrumb": "30 GB Freed Instantly"
    },
    # 26
    {
        "second": 26, "speaker": "stewie", "line": "Cleans temp cache daily.",
        "words": ["Cleans", "temp", "cache", "daily."],
        "graphic": "step4_drive_green", "stepNumber": 4, "title": "Enable Storage Sense", "breadcrumb": "Auto-Cleanup Active ✓"
    },
    # 27
    {
        "second": 27, "speaker": "peter", "line": "My computer runs so fast!",
        "words": ["My", "computer", "runs", "so", "fast!"],
        "graphic": "outro_speedometer", "stepNumber": 0, "title": "All 4 Steps Done!", "breadcrumb": "PC Setup Complete"
    },
    # 28
    {
        "second": 28, "speaker": "stewie", "line": "Of course it does, Peter.",
        "words": ["Of", "course", "it", "does,", "Peter."],
        "graphic": "outro_summary_cards", "stepNumber": 0, "title": "PC Optimized", "breadcrumb": "Save This For Later"
    },
    # 29
    {
        "second": 29, "speaker": "stewie", "line": "Follow for daily PC tips!",
        "words": ["Follow", "for", "daily", "PC", "tips!"],
        "graphic": "outro_follow_card", "stepNumber": 0, "title": "Follow For More!", "breadcrumb": "@DailyPCTips"
    }
]

VOICES = {
    "peter": "en-US-GuyNeural",
    "stewie": "en-GB-RyanNeural"
}

os.makedirs("audio/clips", exist_ok=True)
os.makedirs("output", exist_ok=True)

async def generate_line(item):
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
    
    # Measure trimmed duration
    cmd_probe = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", trimmed_wav]
    res = subprocess.run(cmd_probe, capture_output=True, text=True)
    dur = float(res.stdout.strip())
    
    # Pad to exact 1.000s
    # If dur > 1.0, clamp or atempo to 0.95
    if dur > 0.98:
        print(f"Warning: second {idx} duration is {dur:.2f}s, speeding up slightly to fit...")
        speed_factor = dur / 0.95
        cmd_fit = [
            "ffmpeg", "-y", "-i", trimmed_wav,
            "-filter:a", f"atempo={speed_factor:.3f},apad=whole_dur=1.0",
            "-t", "1.0", pad_wav
        ]
        dur = 0.95
    else:
        cmd_fit = [
            "ffmpeg", "-y", "-i", trimmed_wav,
            "-filter:a", "apad=whole_dur=1.0",
            "-t", "1.0", pad_wav
        ]
    subprocess.run(cmd_fit, capture_output=True)
    
    # Calculate word-level timestamps relative to second
    # Distribute words evenly across [0.05, min(dur + 0.05, 0.95)]
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
    print(f"[{idx:02d}] {dur:.2f}s | {item['speaker']} | {item['line']}")

async def main():
    print("Generating speech clips...")
    for item in SCRIPT_LINES:
        await generate_line(item)
        
    # Concatenate all 30 clips into master 30.000s audio
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
    
    # Check master audio duration
    cmd_probe = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", master_audio]
    res = subprocess.run(cmd_probe, capture_output=True, text=True)
    print(f"\nMaster audio total duration: {res.stdout.strip()} seconds")
    
    # Write script.json
    script_path = "script.json"
    with open(script_path, "w", encoding="utf-8") as f:
        json.dump(SCRIPT_LINES, f, indent=2)
        
    with open("output/script.json", "w", encoding="utf-8") as f:
        json.dump(SCRIPT_LINES, f, indent=2)
        
    print(f"Saved script.json and output/script.json (30 seconds)")
    
    # Write captions.srt
    srt_path = "output/captions.srt"
    with open(srt_path, "w", encoding="utf-8") as f:
        for item in SCRIPT_LINES:
            sec = item["second"]
            start_s = f"00:00:{sec:02d},050"
            end_s = f"00:00:{sec:02d},950"
            f.write(f"{sec + 1}\n{start_s} --> {end_s}\n{item['line']}\n\n")
    print(f"Saved output/captions.srt")

if __name__ == "__main__":
    asyncio.run(main())
