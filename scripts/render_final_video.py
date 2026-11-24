"""
Standalone Fast Video Renderer: Windows 11 RAMMap Memory Optimization by Ez_peter
==================================================================================
Renders the complete 60 FPS vertical video (output/output.mp4) at maximum speed.
Ensures that upon completion, ONLY output/output.mp4 remains in the output directory
with all intermediate frames, snapshots, and caches completely cleared.
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
TOTAL_FRAMES = int(round(TOTAL_SECONDS * FPS))  # 4,670 frames: 0 to 4669
NUM_WORKERS = 12

FRAMES_DIR = "frames_final_render"
OUT_DIR = "output"
OUT_MP4 = os.path.join(OUT_DIR, "output.mp4")
AUDIO_FILE = "audio/master_rammap.wav"
SRT_FILE = "video-engine/captions.srt" if os.path.exists("video-engine/captions.srt") else "output/captions.srt"
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
            # Deterministic render at time t
            await page.evaluate(f"window.renderAt({t})")
            frame_path = os.path.join(FRAMES_DIR, f"frame_{frame_idx:05d}.jpg")
            await page.screenshot(path=frame_path, type="jpeg", quality=95)
            
            if (count + 1) % 100 == 0 or (count + 1) == total_for_worker:
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
            
    print(f"=== Starting Fast Final Video Render for RAMMap ===")
    print(f"Target: {OUT_MP4}")
    print(f"Duration: {TOTAL_SECONDS}s | FPS: {FPS} | Total Frames: {TOTAL_FRAMES}")
    print(f"Parallel Workers: {len(tasks)} (using {NUM_WORKERS} CPU cores)")
    print("---------------------------------------------------------------")
    
    start_time = time.time()
    await asyncio.gather(*tasks)
    render_duration = time.time() - start_time
    print("---------------------------------------------------------------")
    print(f"All {TOTAL_FRAMES} frames rendered in {render_duration:.1f}s ({render_duration/60:.2f} min)!")
    return render_duration

def encode_final_video():
    print(f"\nMuxing 60 FPS video + audio + soft captions into {OUT_MP4}...")
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
        OUT_MP4
    ])
    
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"FFmpeg encoding error:\n{res.stderr}")
        sys.exit(1)
        
    encode_duration = time.time() - encode_start
    print(f"FFmpeg encoding completed in {encode_duration:.1f}s!")
    
    # Copy to artifact directory if available
    if os.path.exists(ARTIFACT_DIR):
        shutil.copy(OUT_MP4, os.path.join(ARTIFACT_DIR, "output.mp4"))
        print(f"Copied final video to artifact directory: {ARTIFACT_DIR}")
        
    # Verify stream metrics
    cmd_probe = [
        "ffprobe", "-v", "error",
        "-show_entries", "stream=index,codec_type,codec_name,r_frame_rate,duration",
        "-of", "default=noprint_wrappers=1",
        OUT_MP4
    ]
    res_probe = subprocess.run(cmd_probe, capture_output=True, text=True)
    print(f"\nFinal Video Verified Stream Metrics:\n{res_probe.stdout.strip()}")

def cleanup_workspace():
    """Cleans up temporary frames and ensures ONLY output.mp4 remains in output/"""
    print("\n--- Cleaning up temporary files & non-video assets ---")
    
    # 1. Remove temporary frames folder
    if os.path.exists(FRAMES_DIR):
        shutil.rmtree(FRAMES_DIR, ignore_errors=True)
        print(f"  Removed temporary frames directory: {FRAMES_DIR}")
        
    # 2. Clean test_frames if exists
    if os.path.exists("test_frames"):
        shutil.rmtree("test_frames", ignore_errors=True)
        print("  Removed test_frames directory.")
        
    # 3. Clean output directory: keep ONLY output.mp4
    if os.path.exists(OUT_DIR):
        for item in os.listdir(OUT_DIR):
            item_path = os.path.join(OUT_DIR, item)
            if item != "output.mp4":
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path, ignore_errors=True)
                else:
                    try:
                        os.remove(item_path)
                    except Exception:
                        pass
        print(f"  Output directory cleaned: ONLY {OUT_MP4} remains.")

async def main():
    overall_start = time.time()
    os.makedirs(OUT_DIR, exist_ok=True)
    
    # 1. Render all frames in parallel
    await render_all_frames()
    
    # 2. Encode to final MP4
    encode_final_video()
    
    # 3. Clean up all intermediate assets so ONLY output.mp4 remains
    cleanup_workspace()
    
    total_time = time.time() - overall_start
    print(f"\n===============================================================")
    print(f"COMPLETE: Final 60 FPS video successfully created in {total_time:.1f}s ({total_time/60:.2f} min)!")
    print(f"Directory Contents of '{OUT_DIR}':")
    for f in os.listdir(OUT_DIR):
        print(f"  -> {f}")
    print(f"===============================================================")

if __name__ == "__main__":
    asyncio.run(main())
