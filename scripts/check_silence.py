import subprocess

for f in ["temp_test/test_0.mp3", "temp_test/test_1.mp3", "temp_test/test_13.mp3"]:
    # Run silenceremove
    out = f.replace(".mp3", "_trimmed.wav")
    cmd = [
        "ffmpeg", "-y", "-i", f,
        "-af", "silenceremove=start_periods=1:start_threshold=-50dB,areverse,silenceremove=start_periods=1:start_threshold=-50dB,areverse",
        out
    ]
    subprocess.run(cmd, capture_output=True)
    cmd2 = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", out]
    res = subprocess.run(cmd2, capture_output=True, text=True)
    print(f, "trimmed duration:", res.stdout.strip())
