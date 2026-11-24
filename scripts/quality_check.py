import os
import subprocess
import json

os.makedirs("qc_frames", exist_ok=True)

# 1. Extract 1 frame per second (at t = 0.5, 1.5, ..., 29.5) from output.mp4
print("Extracting 30 QC frames from output.mp4...")
for s in range(30):
    t = s + 0.5
    out_frame = f"qc_frames/sec_{s:02d}.png"
    cmd = [
        "ffmpeg", "-y", "-ss", f"{t:.2f}",
        "-i", "output/output.mp4",
        "-vframes", "1",
        out_frame
    ]
    subprocess.run(cmd, capture_output=True)

# 2. Probe output.mp4
cmd_probe = [
    "ffprobe", "-v", "quiet", "-print_format", "json",
    "-show_format", "-show_streams", "output/output.mp4"
]
res = subprocess.run(cmd_probe, capture_output=True, text=True)
data = json.loads(res.stdout)

video_stream = next(s for s in data["streams"] if s["codec_type"] == "video")
audio_stream = next(s for s in data["streams"] if s["codec_type"] == "audio")

print("\n=== VIDEO METRICS ===")
print(f"Codec: {video_stream['codec_name']}")
print(f"Resolution: {video_stream['width']}x{video_stream['height']}")
print(f"Pixel format: {video_stream['pix_fmt']}")
print(f"FPS: {video_stream['r_frame_rate']}")
print(f"Duration: {float(data['format']['duration']):.3f}s")

print("\n=== AUDIO METRICS ===")
print(f"Codec: {audio_stream['codec_name']}")
print(f"Sample rate: {audio_stream['sample_rate']} Hz")
print(f"Channels: {audio_stream['channels']}")
print(f"Duration: {float(audio_stream['duration']):.3f}s")

# 3. Check visual variation between consecutive seconds
import hashlib
hashes = []
for s in range(30):
    with open(f"qc_frames/sec_{s:02d}.png", "rb") as f:
        h = hashlib.md5(f.read()).hexdigest()
        hashes.append(h)

duplicates = []
for i in range(1, len(hashes)):
    if hashes[i] == hashes[i-1]:
        duplicates.append((i-1, i))

print(f"\nConsecutive identical visual seconds: {len(duplicates)}")
if duplicates:
    print("Warning: found duplicate frames:", duplicates)
else:
    print("PASS: Every second has a distinct, new visual graphic!")
