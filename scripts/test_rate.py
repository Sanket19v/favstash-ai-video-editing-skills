import asyncio
import edge_tts
import subprocess

async def test_rate():
    test_cases = [
        ("Why, Stewie?", "en-US-GuyNeural"),
        ("Open File Explorer.", "en-GB-RyanNeural"),
        ("Check Extensions.", "en-GB-RyanNeural"),
        ("It's an EXE?!", "en-US-GuyNeural"),
        ("Malware avoided!", "en-GB-RyanNeural"),
        ("I love Ctrl C!", "en-US-GuyNeural"),
        ("Press Win plus V.", "en-GB-RyanNeural"),
        ("Follow for daily tips!", "en-GB-RyanNeural"),
    ]
    for text, voice in test_cases:
        comm = edge_tts.Communicate(text, voice, rate="+15%")
        await comm.save("test_r.mp3")
        cmd = [
            "ffmpeg", "-y", "-i", "test_r.mp3",
            "-af", "silenceremove=start_periods=1:start_threshold=-35dB,areverse,silenceremove=start_periods=1:start_threshold=-35dB,areverse",
            "test_r.wav"
        ]
        subprocess.run(cmd, capture_output=True)
        cmd2 = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", "test_r.wav"]
        res = subprocess.run(cmd2, capture_output=True, text=True)
        dur = float(res.stdout.strip())
        print(f"'{text}': {dur:.2f}s")

if __name__ == "__main__":
    asyncio.run(test_rate())
