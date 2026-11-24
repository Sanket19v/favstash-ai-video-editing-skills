import asyncio
import edge_tts
import subprocess
import os

test_lines = [
    ("Stop right now!", "en-GB-RyanNeural"),
    ("Wait, why?", "en-US-GuyNeural"),
    ("Check these settings.", "en-GB-RyanNeural"),
    ("First, show extensions.", "en-GB-RyanNeural"),
    ("What extensions?", "en-US-GuyNeural"),
    ("Open File Explorer.", "en-GB-RyanNeural"),
    ("Click View, then Show.", "en-GB-RyanNeural"),
    ("Check file extensions.", "en-GB-RyanNeural"),
    ("Wait, it is an exe?!", "en-US-GuyNeural"),
    ("You almost got hacked!", "en-GB-RyanNeural"),
    ("Next, clipboard history.", "en-GB-RyanNeural"),
    ("I love copy paste!", "en-US-GuyNeural"),
    ("Press Win plus V.", "en-GB-RyanNeural"),
    ("Click turn on.", "en-GB-RyanNeural"),
    ("All my clips are here!", "en-US-GuyNeural"),
    ("Pin whatever you need.", "en-GB-RyanNeural"),
    ("Third, kill startup apps.", "en-GB-RyanNeural"),
    ("My PC is so slow!", "en-US-GuyNeural"),
    ("Go to Apps, Startup.", "en-GB-RyanNeural"),
    ("Toggle off the junk.", "en-GB-RyanNeural"),
    ("Goodbye Spotify launch!", "en-US-GuyNeural"),
    ("Instant fast boot.", "en-GB-RyanNeural"),
    ("Fourth, Storage Sense.", "en-GB-RyanNeural"),
    ("What does that do?", "en-US-GuyNeural"),
    ("Go to System, Storage.", "en-GB-RyanNeural"),
    ("Turn on Storage Sense.", "en-GB-RyanNeural"),
    ("Cleans all temp junk.", "en-GB-RyanNeural"),
    ("Freed twenty gigs!", "en-US-GuyNeural"),
    ("My PC flies now!", "en-US-GuyNeural"),
    ("Follow for more PC tips!", "en-GB-RyanNeural"),
]

async def measure_all():
    os.makedirs("temp_test", exist_ok=True)
    for i, (line, voice) in enumerate(test_lines):
        path = f"temp_test/test_{i}.mp3"
        comm = edge_tts.Communicate(line, voice)
        await comm.save(path)
        cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", path]
        res = subprocess.run(cmd, capture_output=True, text=True)
        dur = float(res.stdout.strip())
        print(f"[{i:02d}] {dur:.2f}s | {voice.split('-')[2][:4]} | \"{line}\"")

if __name__ == "__main__":
    asyncio.run(measure_all())
