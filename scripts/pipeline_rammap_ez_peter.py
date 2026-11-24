"""
=============================================================================
PIPELINE: Windows 11 RAMMap Memory Optimization by Ez_peter
=============================================================================
This self-contained master pipeline builds and renders the complete 60 FPS
vertical reel in the signature Ez_peter format:
- Warm Cream Canvas (#f8f4ee)
- Header Pill: PC TIPS BY EZ_PETER
- Silver Laptop Frame with bottom notch and webcam bezel
- Real-time Windows 11 Fluent UI inside the laptop (78 dynamic scene states)
- Center 64px viral captions with royal blue active word pill (#1a6cf0)
- Peter Griffin on Left, Stewie Griffin on Right (cubic ease slide-in)
- Output video: output/windows-11-rammap-free-10gb-ram-ez-peter.mp4
=============================================================================
"""

import asyncio
import os
import sys
import subprocess
import shutil
import time
from pathlib import Path
from playwright.async_api import async_playwright

TOTAL_SECONDS = 77.83
FPS = 60
TOTAL_FRAMES = int(round(TOTAL_SECONDS * FPS))  # 4,670 frames
NUM_WORKERS = 12

FRAMES_DIR = "frames_rammap_render"
OUT_DIR = "output"
OUT_VIDEO_NAME = "windows-11-rammap-free-10gb-ram-ez-peter.mp4"
FINAL_MP4_PATH = os.path.join(OUT_DIR, OUT_VIDEO_NAME)
AUDIO_FILE = "audio/master_rammap.wav"
SRT_FILE = "video-engine/captions.srt"
ARTIFACT_DIR = r"C:\Users\Sanket\.gemini\antigravity\brain\0742d493-2333-419a-a81d-2677e2100688"

async def render_worker(worker_id: int, frame_indices: list):
    html_path = Path("video-engine/index.html").resolve().as_uri()
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--disable-background-timer-throttling",
                "--disable-backgrounding-occluded-windows",
                "--disable-renderer-backgrounding",
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--force-color-profile=srgb"
            ]
        )
        page = await browser.new_page(
            viewport={"width": 1080, "height": 1920},
            device_scale_factor=1
        )
        await page.goto(html_path)
        await page.wait_for_timeout(300)
        
        total_for_worker = len(frame_indices)
        for count, frame_idx in enumerate(frame_indices):
            t = frame_idx / float(FPS)
            await page.evaluate(f"window.renderAt({t})")
            frame_path = os.path.join(FRAMES_DIR, f"frame_{frame_idx:05d}.jpg")
            await page.screenshot(path=frame_path, type="jpeg", quality=95)
            
            if (count + 1) % 150 == 0 or (count + 1) == total_for_worker:
                print(f"[Worker {worker_id:02d}] {count + 1}/{total_for_worker} frames ({((count + 1)/total_for_worker)*100:.1f}%) | Current t={t:.2f}s")
                
        await browser.close()

async def render_all_frames():
    if os.path.exists(FRAMES_DIR):
        shutil.rmtree(FRAMES_DIR, ignore_errors=True)
    os.makedirs(FRAMES_DIR, exist_ok=True)
    
    all_frames = list(range(TOTAL_FRAMES))
    chunk_size = (TOTAL_FRAMES + NUM_WORKERS - 1) // NUM_WORKERS
    
    tasks = []
    for w_id in range(NUM_WORKERS):
        start_i = w_id * chunk_size
        end_i = min(start_i + chunk_size, TOTAL_FRAMES)
        worker_frames = all_frames[start_i:end_i]
        if worker_frames:
            tasks.append(render_worker(w_id, worker_frames))
            
    print(f"=== Starting Fast Final Video Render ===")
    print(f"Output File: {FINAL_MP4_PATH}")
    print(f"Duration: {TOTAL_SECONDS}s | FPS: {FPS} | Total Frames: {TOTAL_FRAMES}")
    print(f"Workers: {len(tasks)} (using {NUM_WORKERS} CPU cores)")
    print("---------------------------------------------------------------")
    
    start_time = time.time()
    await asyncio.gather(*tasks)
    render_duration = time.time() - start_time
    print("---------------------------------------------------------------")
    print(f"All {TOTAL_FRAMES} frames rendered in {render_duration:.1f}s ({render_duration/60:.2f} min)!")
    return render_duration

def encode_final_video():
    print(f"\nMuxing 60 FPS video + audio + soft captions into {FINAL_MP4_PATH}...")
    encode_start = time.time()
    
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", os.path.join(FRAMES_DIR, "frame_%05d.jpg"),
        "-i", AUDIO_FILE
    ]
    if os.path.exists(SRT_FILE):
        cmd.extend(["-i", SRT_FILE])
        
    cmd.extend([
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "18",
        "-preset", "fast",
        "-c:a", "aac",
        "-b:a", "192k"
    ])
    
    if os.path.exists(SRT_FILE):
        cmd.extend(["-c:s", "mov_text", "-metadata:s:s:0", "language=eng"])
        
    cmd.extend([
        "-movflags", "+faststart",
        "-t", f"{TOTAL_SECONDS:.3f}",
        FINAL_MP4_PATH
    ])
    
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"FFmpeg encoding error:\n{res.stderr}")
        sys.exit(1)
        
    encode_duration = time.time() - encode_start
    print(f"FFmpeg encoding completed in {encode_duration:.1f}s!")
    
    # Also keep a synchronized copy at output/output.mp4
    shutil.copy(FINAL_MP4_PATH, os.path.join(OUT_DIR, "output.mp4"))
    
    # Copy to artifact directory if available
    if os.path.exists(ARTIFACT_DIR):
        shutil.copy(FINAL_MP4_PATH, os.path.join(ARTIFACT_DIR, OUT_VIDEO_NAME))
        shutil.copy(FINAL_MP4_PATH, os.path.join(ARTIFACT_DIR, "output.mp4"))
        print(f"Saved to artifact directory: {ARTIFACT_DIR}")
        
    # Clean temporary frame files
    shutil.rmtree(FRAMES_DIR, ignore_errors=True)
    print("Cleaned temporary frame cache.")

async def main():
    overall_start = time.time()
    os.makedirs(OUT_DIR, exist_ok=True)
    
    # 1. Compile engine
    subprocess.run([sys.executable, "scripts/build_rammap_engine_cream_format.py"], check=True)
    
    # 2. Render frames
    await render_all_frames()
    
    # 3. Encode final video
    encode_final_video()
    
    total_time = time.time() - overall_start
    print(f"\n===============================================================")
    print(f"COMPLETE: Video created in {total_time:.1f}s ({total_time/60:.2f} min)!")
    print(f"Final Video File: {os.path.abspath(FINAL_MP4_PATH)}")
    print(f"===============================================================")

if __name__ == "__main__":
    asyncio.run(main())
