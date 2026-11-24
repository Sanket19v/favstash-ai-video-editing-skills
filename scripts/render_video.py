import asyncio
import os
import sys
import subprocess
from pathlib import Path
from playwright.async_api import async_playwright

TOTAL_SECONDS = 30
FPS = 30
TOTAL_FRAMES = TOTAL_SECONDS * FPS # 900 frames: 0 to 899
NUM_WORKERS = 4

async def render_worker(worker_id, frame_indices, out_dir, hide_captions=False):
    html_path = Path("video-engine/index.html").resolve().as_uri()
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
        await page.goto(html_path)
        await page.wait_for_timeout(200)
        
        if hide_captions:
            await page.evaluate("window.hideCaptions = true;")
            
        for count, frame_idx in enumerate(frame_indices):
            t = frame_idx / float(FPS)
            await page.evaluate(f"window.renderAt({t})")
            frame_path = os.path.join(out_dir, f"frame_{frame_idx:04d}.png")
            await page.screenshot(path=frame_path)
            
            if (count + 1) % 50 == 0 or (count + 1) == len(frame_indices):
                print(f"[Worker {worker_id}] Rendered frame {frame_idx + 1}/{TOTAL_FRAMES} (t={t:.2f}s)")
                
        await browser.close()

async def render_frames_pool(out_dir, hide_captions=False):
    os.makedirs(out_dir, exist_ok=True)
    all_frames = list(range(TOTAL_FRAMES))
    chunk_size = (TOTAL_FRAMES + NUM_WORKERS - 1) // NUM_WORKERS
    
    tasks = []
    for w_id in range(NUM_WORKERS):
        start_i = w_id * chunk_size
        end_i = min(start_i + chunk_size, TOTAL_FRAMES)
        worker_frames = all_frames[start_i:end_i]
        if worker_frames:
            tasks.append(render_worker(w_id, worker_frames, out_dir, hide_captions))
            
    await asyncio.gather(*tasks)

def build_mp4(frames_dir, audio_file, out_mp4):
    print(f"Building {out_mp4} with ffmpeg...")
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", os.path.join(frames_dir, "frame_%04d.png"),
        "-i", audio_file,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "18",
        "-preset", "fast",
        "-c:a", "aac",
        "-b:a", "192k",
        "-movflags", "+faststart",
        "-t", "30.0",
        out_mp4
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"FFmpeg error: {res.stderr}")
        sys.exit(1)
    print(f"Successfully generated {out_mp4}")

async def render_thumbnail():
    print("Generating high-converting thumbnail...")
    html_path = Path("video-engine/index.html").resolve().as_uri()
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
        await page.goto(html_path)
        # Second 2 is the 4 critical steps hook with checklist and both hook text
        await page.evaluate("window.renderAt(2.2);")
        thumb_path = "output/thumbnail.png"
        await page.screenshot(path=thumb_path)
        await browser.close()
    print(f"Saved {thumb_path}")

async def main():
    os.makedirs("output", exist_ok=True)
    audio_file = "audio/master_30s.wav"
    
    # 1. Render main video frames
    print("=== Step 1: Rendering 900 frames for output.mp4 ===")
    await render_frames_pool("frames", hide_captions=False)
    build_mp4("frames", audio_file, "output/output.mp4")
    
    # 2. Render nocaptions video frames
    print("\n=== Step 2: Rendering 900 frames for output_nocaptions.mp4 ===")
    await render_frames_pool("frames_nocaptions", hide_captions=True)
    build_mp4("frames_nocaptions", audio_file, "output/output_nocaptions.mp4")
    
    # 3. Render thumbnail
    print("\n=== Step 3: Generating thumbnail.png ===")
    await render_thumbnail()
    
    # 4. Verify output duration
    cmd_probe = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", "output/output.mp4"]
    res = subprocess.run(cmd_probe, capture_output=True, text=True)
    dur = float(res.stdout.strip())
    print(f"\nFinal output.mp4 verified duration: {dur:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())
