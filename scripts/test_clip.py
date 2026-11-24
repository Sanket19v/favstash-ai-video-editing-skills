import asyncio
import edge_tts
import json
import subprocess

async def test_clip():
    communicate = edge_tts.Communicate("Stop right there!", "en-GB-RyanNeural")
    words = []
    with open("test_out.mp3", "wb") as f:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                words.append({
                    "offset": chunk["offset"] / 10000000.0,
                    "duration": chunk["duration"] / 10000000.0,
                    "text": chunk["text"]
                })
    print("Words:", words)
    
    # Check duration with ffprobe
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", "test_out.mp3"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    print("Duration:", res.stdout.strip())

if __name__ == "__main__":
    asyncio.run(test_clip())
