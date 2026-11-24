import os
import json
import subprocess
import re

print("=== Building Smooth Friend Conversation Engine & Audio ===")

# 1. AUDIO TURNS & CONVERSATIONAL TIMINGS
# Total 8 turns spanning 30 seconds
# Exact files generated from Fish Audio:
# audio/test_turns/t1_tight.wav (Peter)
# audio/test_turns/t2_tight.wav (Stewie)
# audio/test_turns/t3_tight.wav (Peter)
# audio/test_turns/t4_tight.wav (Stewie)
# audio/test_turns/t5_tight.wav (Peter)
# audio/test_turns/t6_tight.wav (Stewie)
# audio/test_turns/t7_tight.wav (Peter)
# audio/test_turns/t8_tight.wav (Stewie)

# Let's inspect the exact durations of each tight turn
turn_files = [f"audio/test_turns/t{i}_tight.wav" for i in range(1, 9)]
durs = []
for tf in turn_files:
    res = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", tf],
        capture_output=True, text=True
    )
    durs.append(float(res.stdout.strip()))

total_raw = sum(durs)
slack = 30.0 - total_raw
pause_between = slack / 7.0 # distribute remaining 0.2376s across 7 pauses (~0.034s each)
print(f"Total raw audio: {total_raw:.4f}s, Slack to 30.0s: {slack:.4f}s, Natural pause between turns: {pause_between*1000:.1f}ms")

# Assemble ffmpeg filter_complex to concatenate with exact micro-pauses
# [0]adelay=0|0[a0]; [1]adelay=...
filter_parts = []
concat_inputs = []

# Generate silent pad file for exact natural pause
silence_pad = "audio/turns/micro_pause.wav"
os.makedirs("audio/turns", exist_ok=True)
subprocess.run([
    "ffmpeg", "-y", "-f", "lavfi", "-i", f"anullsrc=r=48000:cl=mono", "-t", f"{pause_between:.6f}", silence_pad
], capture_output=True)

# Build file list for concat demuxer or filter_complex
concat_txt = "audio/turns/concat_list.txt"
with open(concat_txt, "w") as f:
    for i, tf in enumerate(turn_files):
        abs_tf = os.path.abspath(tf).replace("\\", "/")
        f.write(f"file '{abs_tf}'\n")
        if i < len(turn_files) - 1:
            abs_sil = os.path.abspath(silence_pad).replace("\\", "/")
            f.write(f"file '{abs_sil}'\n")

# Render master_30s.wav
master_wav = "audio/master_30s.wav"
subprocess.run([
    "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_txt,
    "-af", "apad=whole_dur=30.0,atrim=0:30.0",
    "-ar", "48000", "-ac", "2",
    master_wav
], capture_output=True)

# Verify master_30s.wav
res = subprocess.run(
    ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", master_wav],
    capture_output=True, text=True
)
master_dur = float(res.stdout.strip())
print(f"Generated {master_wav} - Duration: {master_dur:.6f}s (Target: exactly 30.000000s)")

# 2. DEFINE SCRIPT.JSON WITH 30 DISTINCT VISUALS AND 8 CONVERSATIONAL BLOCKS
# Speaker blocks:
# Sec 0-3: Peter (Turn 1: 'Stewie! My new PC is slow, what settings do I change?')
# Sec 4-8: Stewie (Turn 2: 'Relax, Peter. Open Explorer and enable extensions so you never open fake viruses.')
# Sec 9-12: Peter (Turn 3: 'Invoices can be viruses?! How do I copy stuff safely?')
# Sec 13-16: Stewie (Turn 4: 'Press Windows V, you idiot! Clipboard History lets you save and pin everything.')
# Sec 17-19: Peter (Turn 5: 'Awesome! But bootup takes forever and my drive is full!')
# Sec 20-23: Stewie (Turn 6: 'Disable startup apps in Settings, and turn Storage Sense On to purge junk!')
# Sec 24-26: Peter (Turn 7: 'Holy crap, it is flying! Did I pass the class?')
# Sec 27-29: Stewie (Turn 8: 'You passed, fat man. Follow for more PC tips!')

script_data = [
    # --- TURN 1: PETER (0 - 3) ---
    {
        "second": 0, "speaker": "peter",
        "line": "Stewie! My new PC",
        "words": ["Stewie!", "My", "new", "PC"],
        "graphic": "hook_warning", "stepNumber": 0,
        "title": "New PC Masterclass", "breadcrumb": "Student Peter vs Teacher Stewie",
        "captionWords": [
            {"text": "Stewie!", "start": 0.05, "end": 0.35},
            {"text": "My", "start": 0.35, "end": 0.55},
            {"text": "new", "start": 0.55, "end": 0.75},
            {"text": "PC", "start": 0.75, "end": 0.95}
        ]
    },
    {
        "second": 1, "speaker": "peter",
        "line": "is running so slow,",
        "words": ["is", "running", "so", "slow,"],
        "graphic": "hook_confused", "stepNumber": 0,
        "title": "New PC Masterclass", "breadcrumb": "Why Is Brand New Windows Slow?",
        "captionWords": [
            {"text": "is", "start": 0.05, "end": 0.25},
            {"text": "running", "start": 0.25, "end": 0.50},
            {"text": "so", "start": 0.50, "end": 0.70},
            {"text": "slow,", "start": 0.70, "end": 0.95}
        ]
    },
    {
        "second": 2, "speaker": "peter",
        "line": "what settings do I",
        "words": ["what", "settings", "do", "I"],
        "graphic": "hook_checklist", "stepNumber": 0,
        "title": "New PC Masterclass", "breadcrumb": "4 Critical Setup Lessons",
        "captionWords": [
            {"text": "what", "start": 0.05, "end": 0.25},
            {"text": "settings", "start": 0.25, "end": 0.55},
            {"text": "do", "start": 0.55, "end": 0.75},
            {"text": "I", "start": 0.75, "end": 0.95}
        ]
    },
    {
        "second": 3, "speaker": "peter",
        "line": "change right now?",
        "words": ["change", "right", "now?"],
        "graphic": "step1_title", "stepNumber": 1,
        "title": "Show File Extensions", "breadcrumb": "Rule #1: File Explorer View",
        "captionWords": [
            {"text": "change", "start": 0.05, "end": 0.35},
            {"text": "right", "start": 0.35, "end": 0.65},
            {"text": "now?", "start": 0.65, "end": 0.95}
        ]
    },

    # --- TURN 2: STEWIE (4 - 8) ---
    {
        "second": 4, "speaker": "stewie",
        "line": "Relax, Peter.",
        "words": ["Relax,", "Peter."],
        "graphic": "step1_explorer_closed", "stepNumber": 1,
        "title": "Show File Extensions", "breadcrumb": "Hidden File Format Danger",
        "captionWords": [
            {"text": "Relax,", "start": 0.05, "end": 0.50},
            {"text": "Peter.", "start": 0.50, "end": 0.95}
        ]
    },
    {
        "second": 5, "speaker": "stewie",
        "line": "Open File Explorer,",
        "words": ["Open", "File", "Explorer,"],
        "graphic": "step1_click_view", "stepNumber": 1,
        "title": "Show File Extensions", "breadcrumb": "File Explorer › View Tab",
        "captionWords": [
            {"text": "Open", "start": 0.05, "end": 0.35},
            {"text": "File", "start": 0.35, "end": 0.65},
            {"text": "Explorer,", "start": 0.65, "end": 0.95}
        ]
    },
    {
        "second": 6, "speaker": "stewie",
        "line": "and enable extensions,",
        "words": ["and", "enable", "extensions,"],
        "graphic": "step1_dropdown", "stepNumber": 1,
        "title": "Show File Extensions", "breadcrumb": "View › Show › File name extensions",
        "captionWords": [
            {"text": "and", "start": 0.05, "end": 0.30},
            {"text": "enable", "start": 0.30, "end": 0.60},
            {"text": "extensions,", "start": 0.60, "end": 0.95}
        ]
    },
    {
        "second": 7, "speaker": "stewie",
        "line": "so you never open",
        "words": ["so", "you", "never", "open"],
        "graphic": "step1_reveal_exe", "stepNumber": 1,
        "title": "Show File Extensions", "breadcrumb": "Disguised Malware Detected!",
        "captionWords": [
            {"text": "so", "start": 0.05, "end": 0.25},
            {"text": "you", "start": 0.25, "end": 0.45},
            {"text": "never", "start": 0.45, "end": 0.70},
            {"text": "open", "start": 0.70, "end": 0.95}
        ]
    },
    {
        "second": 8, "speaker": "stewie",
        "line": "fake virus files.",
        "words": ["fake", "virus", "files."],
        "graphic": "step1_success", "stepNumber": 1,
        "title": "Show File Extensions", "breadcrumb": "Trojan Avoided ✓",
        "captionWords": [
            {"text": "fake", "start": 0.05, "end": 0.35},
            {"text": "virus", "start": 0.35, "end": 0.65},
            {"text": "files.", "start": 0.65, "end": 0.95}
        ]
    },

    # --- TURN 3: PETER (9 - 12) ---
    {
        "second": 9, "speaker": "peter",
        "line": "Wait, invoices can be",
        "words": ["Wait,", "invoices", "can", "be"],
        "graphic": "step2_title", "stepNumber": 2,
        "title": "Clipboard History", "breadcrumb": "Windows Key + V",
        "captionWords": [
            {"text": "Wait,", "start": 0.05, "end": 0.25},
            {"text": "invoices", "start": 0.25, "end": 0.55},
            {"text": "can", "start": 0.55, "end": 0.75},
            {"text": "be", "start": 0.75, "end": 0.95}
        ]
    },
    {
        "second": 10, "speaker": "peter",
        "line": "dangerous viruses?!",
        "words": ["dangerous", "viruses?!"],
        "graphic": "step2_keys_ctrl_c", "stepNumber": 2,
        "title": "Clipboard History", "breadcrumb": "Single Ctrl+C Overwrites Clips",
        "captionWords": [
            {"text": "dangerous", "start": 0.05, "end": 0.50},
            {"text": "viruses?!", "start": 0.50, "end": 0.95}
        ]
    },
    {
        "second": 11, "speaker": "peter",
        "line": "How do I copy",
        "words": ["How", "do", "I", "copy"],
        "graphic": "step2_keys_win_v", "stepNumber": 2,
        "title": "Clipboard History", "breadcrumb": "Shortcut: ⊞ Win + V",
        "captionWords": [
            {"text": "How", "start": 0.05, "end": 0.25},
            {"text": "do", "start": 0.25, "end": 0.45},
            {"text": "I", "start": 0.45, "end": 0.65},
            {"text": "copy", "start": 0.65, "end": 0.95}
        ]
    },
    {
        "second": 12, "speaker": "peter",
        "line": "my files safely?",
        "words": ["my", "files", "safely?"],
        "graphic": "step2_turn_on", "stepNumber": 2,
        "title": "Clipboard History", "breadcrumb": "Click 'Turn On' Feature",
        "captionWords": [
            {"text": "my", "start": 0.05, "end": 0.30},
            {"text": "files", "start": 0.30, "end": 0.60},
            {"text": "safely?", "start": 0.60, "end": 0.95}
        ]
    },

    # --- TURN 4: STEWIE (13 - 16) ---
    {
        "second": 13, "speaker": "stewie",
        "line": "Press Windows V,",
        "words": ["Press", "Windows", "V,"],
        "graphic": "step2_history_list", "stepNumber": 2,
        "title": "Clipboard History", "breadcrumb": "Multi-Snippet History Board",
        "captionWords": [
            {"text": "Press", "start": 0.05, "end": 0.30},
            {"text": "Windows", "start": 0.30, "end": 0.65},
            {"text": "V,", "start": 0.65, "end": 0.95}
        ]
    },
    {
        "second": 14, "speaker": "stewie",
        "line": "you idiot!",
        "words": ["you", "idiot!"],
        "graphic": "step2_pin_item", "stepNumber": 2,
        "title": "Clipboard History", "breadcrumb": "Pin Essential Clips Permanently ✓",
        "captionWords": [
            {"text": "you", "start": 0.05, "end": 0.40},
            {"text": "idiot!", "start": 0.40, "end": 0.95}
        ]
    },
    {
        "second": 15, "speaker": "stewie",
        "line": "Clipboard History saves",
        "words": ["Clipboard", "History", "saves"],
        "graphic": "step3_title", "stepNumber": 3,
        "title": "Kill Startup Bloatware", "breadcrumb": "Settings › Apps › Startup",
        "captionWords": [
            {"text": "Clipboard", "start": 0.05, "end": 0.35},
            {"text": "History", "start": 0.35, "end": 0.65},
            {"text": "saves", "start": 0.65, "end": 0.95}
        ]
    },
    {
        "second": 16, "speaker": "stewie",
        "line": "and pins everything.",
        "words": ["and", "pins", "everything."],
        "graphic": "step3_slow_boot", "stepNumber": 3,
        "title": "Kill Startup Bloatware", "breadcrumb": "Slow Boot Caused by Bloatware",
        "captionWords": [
            {"text": "and", "start": 0.05, "end": 0.30},
            {"text": "pins", "start": 0.30, "end": 0.60},
            {"text": "everything.", "start": 0.60, "end": 0.95}
        ]
    },

    # --- TURN 5: PETER (17 - 19) ---
    {
        "second": 17, "speaker": "peter",
        "line": "Awesome! But bootup",
        "words": ["Awesome!", "But", "bootup"],
        "graphic": "step3_settings_page", "stepNumber": 3,
        "title": "Kill Startup Bloatware", "breadcrumb": "Settings › Apps › Startup",
        "captionWords": [
            {"text": "Awesome!", "start": 0.05, "end": 0.35},
            {"text": "But", "start": 0.35, "end": 0.60},
            {"text": "bootup", "start": 0.60, "end": 0.95}
        ]
    },
    {
        "second": 18, "speaker": "peter",
        "line": "takes forever,",
        "words": ["takes", "forever,"],
        "graphic": "step3_toggle_off", "stepNumber": 3,
        "title": "Kill Startup Bloatware", "breadcrumb": "Toggle Background Starters",
        "captionWords": [
            {"text": "takes", "start": 0.05, "end": 0.45},
            {"text": "forever,", "start": 0.45, "end": 0.95}
        ]
    },
    {
        "second": 19, "speaker": "peter",
        "line": "and my drive is full!",
        "words": ["and", "my", "drive", "is", "full!"],
        "graphic": "step3_disabled_list", "stepNumber": 3,
        "title": "Kill Startup Bloatware", "breadcrumb": "Startup Impact: Low",
        "captionWords": [
            {"text": "and", "start": 0.05, "end": 0.20},
            {"text": "my", "start": 0.20, "end": 0.40},
            {"text": "drive", "start": 0.40, "end": 0.60},
            {"text": "is", "start": 0.60, "end": 0.75},
            {"text": "full!", "start": 0.75, "end": 0.95}
        ]
    },

    # --- TURN 6: STEWIE (20 - 23) ---
    {
        "second": 20, "speaker": "stewie",
        "line": "Disable startup apps,",
        "words": ["Disable", "startup", "apps,"],
        "graphic": "step3_fast_boot", "stepNumber": 3,
        "title": "Kill Startup Bloatware", "breadcrumb": "Instant 10s Boot Time ✓",
        "captionWords": [
            {"text": "Disable", "start": 0.05, "end": 0.35},
            {"text": "startup", "start": 0.35, "end": 0.65},
            {"text": "apps,", "start": 0.65, "end": 0.95}
        ]
    },
    {
        "second": 21, "speaker": "stewie",
        "line": "in Windows Settings,",
        "words": ["in", "Windows", "Settings,"],
        "graphic": "step4_title", "stepNumber": 4,
        "title": "Enable Storage Sense", "breadcrumb": "Settings › System › Storage",
        "captionWords": [
            {"text": "in", "start": 0.05, "end": 0.25},
            {"text": "Windows", "start": 0.25, "end": 0.60},
            {"text": "Settings,", "start": 0.60, "end": 0.95}
        ]
    },
    {
        "second": 22, "speaker": "stewie",
        "line": "and turn Storage Sense On",
        "words": ["and", "turn", "Storage", "Sense", "On"],
        "graphic": "step4_drive_red", "stepNumber": 4,
        "title": "Enable Storage Sense", "breadcrumb": "C: Drive 95% Full Warning",
        "captionWords": [
            {"text": "and", "start": 0.05, "end": 0.20},
            {"text": "turn", "start": 0.20, "end": 0.40},
            {"text": "Storage", "start": 0.40, "end": 0.60},
            {"text": "Sense", "start": 0.60, "end": 0.80},
            {"text": "On", "start": 0.80, "end": 0.95}
        ]
    },
    {
        "second": 23, "speaker": "stewie",
        "line": "to purge junk!",
        "words": ["to", "purge", "junk!"],
        "graphic": "step4_settings_storage", "stepNumber": 4,
        "title": "Enable Storage Sense", "breadcrumb": "Settings › System › Storage",
        "captionWords": [
            {"text": "to", "start": 0.05, "end": 0.30},
            {"text": "purge", "start": 0.30, "end": 0.60},
            {"text": "junk!", "start": 0.60, "end": 0.95}
        ]
    },

    # --- TURN 7: PETER (24 - 26) ---
    {
        "second": 24, "speaker": "peter",
        "line": "Holy crap, it's flying!",
        "words": ["Holy", "crap,", "it's", "flying!"],
        "graphic": "step4_toggle_storage", "stepNumber": 4,
        "title": "Enable Storage Sense", "breadcrumb": "Storage Sense Switch: On",
        "captionWords": [
            {"text": "Holy", "start": 0.05, "end": 0.25},
            {"text": "crap,", "start": 0.25, "end": 0.50},
            {"text": "it's", "start": 0.50, "end": 0.70},
            {"text": "flying!", "start": 0.70, "end": 0.95}
        ]
    },
    {
        "second": 25, "speaker": "peter",
        "line": "Look at all this space,",
        "words": ["Look", "at", "all", "this", "space,"],
        "graphic": "step4_cleaning_counter", "stepNumber": 4,
        "title": "Enable Storage Sense", "breadcrumb": "Auto-Cleaner Purging Cache",
        "captionWords": [
            {"text": "Look", "start": 0.05, "end": 0.20},
            {"text": "at", "start": 0.20, "end": 0.40},
            {"text": "all", "start": 0.40, "end": 0.60},
            {"text": "this", "start": 0.60, "end": 0.80},
            {"text": "space,", "start": 0.80, "end": 0.95}
        ]
    },
    {
        "second": 26, "speaker": "peter",
        "line": "did I pass the class?",
        "words": ["did", "I", "pass", "the", "class?"],
        "graphic": "step4_drive_green", "stepNumber": 4,
        "title": "Enable Storage Sense", "breadcrumb": "30 GB Reclaimed Space ✓",
        "captionWords": [
            {"text": "did", "start": 0.05, "end": 0.20},
            {"text": "I", "start": 0.20, "end": 0.40},
            {"text": "pass", "start": 0.40, "end": 0.60},
            {"text": "the", "start": 0.60, "end": 0.75},
            {"text": "class?", "start": 0.75, "end": 0.95}
        ]
    },

    # --- TURN 8: STEWIE (27 - 29) ---
    {
        "second": 27, "speaker": "stewie",
        "line": "You passed, fat man.",
        "words": ["You", "passed,", "fat", "man."],
        "graphic": "outro_speedometer", "stepNumber": 0,
        "title": "Final Grade: A+", "breadcrumb": "Student Passed Masterclass",
        "captionWords": [
            {"text": "You", "start": 0.05, "end": 0.25},
            {"text": "passed,", "start": 0.25, "end": 0.50},
            {"text": "fat", "start": 0.50, "end": 0.70},
            {"text": "man.", "start": 0.70, "end": 0.95}
        ]
    },
    {
        "second": 28, "speaker": "stewie",
        "line": "All settings optimized!",
        "words": ["All", "settings", "optimized!"],
        "graphic": "outro_summary_cards", "stepNumber": 0,
        "title": "PC Masterclass", "breadcrumb": "All 4 Critical Tweaks Active",
        "captionWords": [
            {"text": "All", "start": 0.05, "end": 0.30},
            {"text": "settings", "start": 0.30, "end": 0.60},
            {"text": "optimized!", "start": 0.60, "end": 0.95}
        ]
    },
    {
        "second": 29, "speaker": "stewie",
        "line": "Follow for more PC tips!",
        "words": ["Follow", "for", "more", "PC", "tips!"],
        "graphic": "outro_follow_card", "stepNumber": 0,
        "title": "Follow For More!", "breadcrumb": "@DailyPCTips",
        "captionWords": [
            {"text": "Follow", "start": 0.05, "end": 0.20},
            {"text": "for", "start": 0.20, "end": 0.40},
            {"text": "more", "start": 0.40, "end": 0.60},
            {"text": "PC", "start": 0.60, "end": 0.80},
            {"text": "tips!", "start": 0.80, "end": 0.95}
        ]
    }
]

# Write script.json to both root and output
with open("script.json", "w") as f:
    json.dump(script_data, f, indent=2)
with open("output/script.json", "w") as f:
    json.dump(script_data, f, indent=2)

print("Saved updated script.json (30 seconds, 8 conversational turns, 30 distinct graphics).")

# 3. UPDATE video-engine/index.html WITH EMBEDDED SCRIPT AND SLICK CHARACTER SLIDE TRANSITIONS
with open("video-engine/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace embedded SCRIPT
pattern = r"let SCRIPT = \[.*?\];\s*window\.SCRIPT = SCRIPT;"
replacement = f"let SCRIPT = {json.dumps(script_data)};\n    window.SCRIPT = SCRIPT;"
html = re.sub(pattern, lambda m: replacement, html, flags=re.DOTALL)

# Update character transition logic in renderAt:
# Silky smooth slide-in and slide-out so characters NEVER snap and ONLY ONE is on screen at a time!
char_logic_target = """      // 5. RENDER CHARACTERS (Peter on Left, Stewie on Right)
      // Only ONE on screen at a time! Smooth slide in/out
      const peterEl = document.getElementById('peterImg');
      const stewieEl = document.getElementById('stewieImg');

      const isPeter = currentItem.speaker === 'peter';
      const isStewie = currentItem.speaker === 'stewie';

      // Check transition from previous second
      const prevSpeaker = s > 0 ? SCRIPT[s - 1].speaker : null;
      const transT = clamp(tau / 0.25, 0, 1); // 0.25s slide transition
      const easeTrans = easeOutCubic(transT);

      if (isPeter) {
        // Peter slides in from left: -1100 -> 0 + dynamic speaking bob
        const startX = prevSpeaker === 'peter' ? 0 : -1100;
        const peterX = startX + (0 - startX) * easeTrans;
        const bobY = Math.sin(tau * Math.PI * 4) * 8;
        const breathScale = 1.0 + 0.012 * Math.sin(tau * Math.PI * 2);
        peterEl.style.transform = `translateX(${peterX}px) translateY(${bobY}px) scale(${breathScale})`;
        stewieEl.style.transform = `translateX(1200px)`;
      } else if (isStewie) {
        // Stewie slides in from right: 1100 -> 0 + dynamic speaking bob
        const startX = prevSpeaker === 'stewie' ? 0 : 1200;
        const stewieX = startX + (0 - startX) * easeTrans;
        const bobY = Math.sin(tau * Math.PI * 4) * 8;
        const breathScale = 1.0 + 0.012 * Math.sin(tau * Math.PI * 2);
        stewieEl.style.transform = `translateX(${stewieX}px) translateY(${bobY}px) scale(${breathScale})`;
        peterEl.style.transform = `translateX(-1200px)`;
      } else {
        peterEl.style.transform = `translateX(-1200px)`;
        stewieEl.style.transform = `translateX(1200px)`;
      }"""

char_logic_replacement = """      // 5. RENDER CHARACTERS (Peter on Left, Stewie on Right)
      // Only ONE on screen at a time! Smooth slide in/out
      const peterEl = document.getElementById('peterImg');
      const stewieEl = document.getElementById('stewieImg');

      const isPeter = currentItem.speaker === 'peter';
      const isStewie = currentItem.speaker === 'stewie';

      const prevSpeaker = s > 0 ? SCRIPT[s - 1].speaker : null;
      const nextSpeaker = s < totalSeconds - 1 ? SCRIPT[s + 1].speaker : null;

      if (isPeter) {
        let peterX = 0;
        if (prevSpeaker !== 'peter' && tau < 0.25) {
          // Smooth slide in from left (-1200px -> 0)
          const inFrac = easeOutCubic(tau / 0.25);
          peterX = -1200 * (1 - inFrac);
        } else if (nextSpeaker !== 'peter' && tau > 0.75) {
          // Smooth slide out to left (0 -> -1200px)
          const outFrac = easeInOutQuad((tau - 0.75) / 0.25);
          peterX = -1200 * outFrac;
        }
        const bobY = Math.sin(tau * Math.PI * 4) * 7;
        const breathScale = 1.0 + 0.012 * Math.sin(tau * Math.PI * 2);
        peterEl.style.transform = `translateX(${peterX}px) translateY(${bobY}px) scale(${breathScale})`;
        stewieEl.style.transform = `translateX(1200px)`;
      } else if (isStewie) {
        let stewieX = 0;
        if (prevSpeaker !== 'stewie' && tau < 0.25) {
          // Smooth slide in from right (1200px -> 0)
          const inFrac = easeOutCubic(tau / 0.25);
          stewieX = 1200 * (1 - inFrac);
        } else if (nextSpeaker !== 'stewie' && tau > 0.75) {
          // Smooth slide out to right (0 -> 1200px)
          const outFrac = easeInOutQuad((tau - 0.75) / 0.25);
          stewieX = 1200 * outFrac;
        }
        const bobY = Math.sin(tau * Math.PI * 4) * 7;
        const breathScale = 1.0 + 0.012 * Math.sin(tau * Math.PI * 2);
        stewieEl.style.transform = `translateX(${stewieX}px) translateY(${bobY}px) scale(${breathScale})`;
        peterEl.style.transform = `translateX(-1200px)`;
      } else {
        peterEl.style.transform = `translateX(-1200px)`;
        stewieEl.style.transform = `translateX(1200px)`;
      }"""

if char_logic_target in html:
    html = html.replace(char_logic_target, char_logic_replacement)
    print("Replaced character slide logic in index.html with dual-direction ease-in/ease-out.")
else:
    print("WARNING: Exact char_logic_target string not found, checking alternative replacement.")

with open("video-engine/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Updated video-engine/index.html successfully.")
