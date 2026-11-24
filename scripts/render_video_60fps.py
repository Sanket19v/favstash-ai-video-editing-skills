import asyncio
import os
import sys
import subprocess
from pathlib import Path
from playwright.async_api import async_playwright

TOTAL_SECONDS = 30
FPS = 60
TOTAL_FRAMES = TOTAL_SECONDS * FPS # 1800 frames: 0 to 1799
NUM_WORKERS = 6

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
            
            if (count + 1) % 100 == 0 or (count + 1) == len(frame_indices):
                print(f"[Worker {worker_id}] Frame {frame_idx + 1}/{TOTAL_FRAMES} (t={t:.2f}s)")
                
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

def build_mp4(frames_dir, audio_file, out_mp4, srt_file=None):
    print(f"Building 60 FPS {out_mp4} with ffmpeg...")
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", os.path.join(frames_dir, "frame_%04d.png"),
        "-i", audio_file
    ]
    if srt_file and os.path.exists(srt_file):
        cmd.extend(["-i", srt_file])
    
    cmd.extend([
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "18",
        "-preset", "fast",
        "-c:a", "aac",
        "-b:a", "192k"
    ])
    if srt_file and os.path.exists(srt_file):
        cmd.extend(["-c:s", "mov_text", "-metadata:s:s:0", "language=eng"])
        
    cmd.extend([
        "-movflags", "+faststart",
        "-t", "30.0",
        out_mp4
    ])
    
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"FFmpeg error: {res.stderr}")
        sys.exit(1)
    print(f"Successfully generated {out_mp4} at 60 FPS (with soft subs: {bool(srt_file)})")

async def render_thumbnail():
    print("Generating high-converting thumbnail with bold captions...")
    html_path = Path("video-engine/index.html").resolve().as_uri()
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
        await page.goto(html_path)
        await page.evaluate("window.renderAt(2.2);")
        thumb_path = "output/thumbnail.png"
        await page.screenshot(path=thumb_path)
        await browser.close()
    print(f"Saved {thumb_path}")

async def main():
    os.makedirs("output", exist_ok=True)
    audio_file = "audio/master_30s.wav"
    srt_file = "output/captions.srt"
    
    # 1. Render main 60 FPS video frames with upgraded bold captions
    print("=== Step 1: Rendering 1,800 frames for output.mp4 at 60 FPS (Burned-in Bold Captions) ===")
    await render_frames_pool("frames", hide_captions=False)
    build_mp4("frames", audio_file, "output/output.mp4", srt_file=srt_file)
    
    # 2. Render nocaptions video frames
    print("\n=== Step 2: Rendering 1,800 frames for output_nocaptions.mp4 at 60 FPS ===")
    await render_frames_pool("frames_nocaptions", hide_captions=True)
    build_mp4("frames_nocaptions", audio_file, "output/output_nocaptions.mp4", srt_file=None)
    
    # 3. Render thumbnail
    print("\n=== Step 3: Generating thumbnail.png ===")
    await render_thumbnail()
    
    # 4. Generate updated demo_preview.gif (with bold blue pill captions clearly visible)
    print("\n=== Step 4: Generating updated demo_preview.gif ===")
    cmd_gif = [
        "ffmpeg", "-y", "-ss", "0", "-t", "12",
        "-i", "output/output.mp4",
        "-vf", "fps=15,scale=540:960:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=128[p];[s1][p]paletteuse=dither=bayer",
        "output/demo_preview.gif"
    ]
    subprocess.run(cmd_gif, capture_output=True)
    
    # Copy to artifact dir
    art_dir = r"C:\Users\Sanket\.gemini\antigravity\brain\0742d493-2333-419a-a81d-2677e2100688"
    if os.path.exists(art_dir):
        import shutil
        shutil.copy("output/output.mp4", os.path.join(art_dir, "output.mp4"))
        shutil.copy("output/thumbnail.png", os.path.join(art_dir, "thumbnail.png"))
        shutil.copy("output/demo_preview.gif", os.path.join(art_dir, "demo_preview.gif"))
        print("Updated artifact directory assets.")

    # 5. Verify metrics
    cmd_probe = ["ffprobe", "-v", "error", "-show_entries", "stream=index,codec_type,codec_name,r_frame_rate,duration", "-of", "default=noprint_wrappers=1", "output/output.mp4"]
    res = subprocess.run(cmd_probe, capture_output=True, text=True)
    print(f"\nFinal output.mp4 verified metrics:\n{res.stdout.strip()}")

if __name__ == "__main__":
    asyncio.run(main())
