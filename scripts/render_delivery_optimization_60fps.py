import asyncio
import os
import sys
import subprocess
import shutil
from pathlib import Path
from playwright.async_api import async_playwright

TOTAL_SECONDS = 93.04
FPS = 60
TOTAL_FRAMES = int(round(TOTAL_SECONDS * FPS)) # 5582 frames: 0 to 5581
NUM_WORKERS = 10

OUT_DIR_CAP = "frames_delivery"
OUT_DIR_NOCAP = "frames_delivery_nocap"

async def render_worker(worker_id, frame_indices):
    html_path = Path("video-engine/index.html").resolve().as_uri()
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
        await page.goto(html_path)
        await page.wait_for_timeout(400)
        
        for count, frame_idx in enumerate(frame_indices):
            t = frame_idx / float(FPS)
            # 1. Render frame with captions
            await page.evaluate(f"window.renderAt({t})")
            cap_frame_path = os.path.join(OUT_DIR_CAP, f"frame_{frame_idx:05d}.jpg")
            await page.screenshot(path=cap_frame_path, type="jpeg", quality=95)
            
            # 2. Hide captions and screenshot nocaptions version
            await page.evaluate("document.getElementById('captions').style.display = 'none';")
            nocap_frame_path = os.path.join(OUT_DIR_NOCAP, f"frame_{frame_idx:05d}.jpg")
            await page.screenshot(path=nocap_frame_path, type="jpeg", quality=95)
            await page.evaluate("document.getElementById('captions').style.display = 'flex';")
            
            if (count + 1) % 100 == 0 or (count + 1) == len(frame_indices):
                print(f"[Worker {worker_id:02d}] Rendered {count + 1}/{len(frame_indices)} frames (t={t:.2f}s)")
                
        await browser.close()

async def render_all_frames_dual_pool():
    os.makedirs(OUT_DIR_CAP, exist_ok=True)
    os.makedirs(OUT_DIR_NOCAP, exist_ok=True)
    all_frames = list(range(TOTAL_FRAMES))
    chunk_size = (TOTAL_FRAMES + NUM_WORKERS - 1) // NUM_WORKERS
    
    tasks = []
    for w_id in range(NUM_WORKERS):
        start_i = w_id * chunk_size
        end_i = min(start_i + chunk_size, TOTAL_FRAMES)
        worker_frames = all_frames[start_i:end_i]
        if worker_frames:
            tasks.append(render_worker(w_id, worker_frames))
            
    print(f"Launching {len(tasks)} parallel workers for {TOTAL_FRAMES} frames...")
    await asyncio.gather(*tasks)
    print("All frames rendered successfully for both captioned and clean streams!")

def build_mp4(frames_dir, audio_file, out_mp4, srt_file=None):
    print(f"\nBuilding 60 FPS {out_mp4} with ffmpeg...")
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", os.path.join(frames_dir, "frame_%05d.jpg"),
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
        "-t", f"{TOTAL_SECONDS:.3f}",
        out_mp4
    ])
    
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"FFmpeg error: {res.stderr}")
        sys.exit(1)
    print(f"Successfully generated {out_mp4} at 60 FPS (with soft subs: {bool(srt_file)})")

async def render_thumbnail():
    print("Generating thumbnail with bold viral captions...")
    html_path = Path("video-engine/index.html").resolve().as_uri()
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
        await page.goto(html_path)
        # Choosing t=1.8s for thumbnail: Peter with alert badge and active word pill
        await page.evaluate("window.renderAt(1.8);")
        thumb_path = "output/thumbnail.png"
        await page.screenshot(path=thumb_path, type="png")
        await browser.close()
    print(f"Saved {thumb_path}")

def extract_qc_frames():
    print("Extracting QC verification frames from output.mp4...")
    qc_stamps = [
        ("0.5", "qc_final_00s.png"),
        ("16.5", "qc_final_16s.png"),
        ("25.0", "qc_final_25s.png"),
        ("42.0", "qc_final_42s.png"),
        ("73.5", "qc_final_73s.png"),
        ("80.5", "qc_final_80s.png"),
        ("91.5", "qc_final_91s.png"),
    ]
    for ss, fname in qc_stamps:
        out_f = os.path.join("output", fname)
        cmd = ["ffmpeg", "-y", "-ss", ss, "-i", "output/output.mp4", "-vframes", "1", out_f]
        subprocess.run(cmd, capture_output=True)
        print(f"  Extracted {out_f} at t={ss}s")

async def main():
    os.makedirs("output", exist_ok=True)
    audio_file = "audio/master_delivery_opt.wav"
    srt_file = "output/captions.srt"
    
    print(f"=== Starting 60 FPS Dual-Pass Production for Windows Delivery Optimization ===")
    print(f"Total Duration: {TOTAL_SECONDS}s | Total Frames: {TOTAL_FRAMES} | Workers: {NUM_WORKERS}")
    
    # 1. Render all frames in parallel (both captioned and clean)
    await render_all_frames_dual_pool()
    
    # 2. Build output.mp4 (with burned-in viral captions + soft CC)
    build_mp4(OUT_DIR_CAP, audio_file, "output/output.mp4", srt_file=srt_file)
    
    # 3. Build output_nocaptions.mp4 (clean video)
    build_mp4(OUT_DIR_NOCAP, audio_file, "output/output_nocaptions.mp4", srt_file=None)
    
    # 4. Render thumbnail.png
    await render_thumbnail()
    
    # 5. Extract QC frames
    extract_qc_frames()
    
    # 6. Generate demo_preview.gif
    print("\nGenerating demo_preview.gif...")
    cmd_gif = [
        "ffmpeg", "-y", "-ss", "0", "-t", "12",
        "-i", "output/output.mp4",
        "-vf", "fps=15,scale=540:960:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=128[p];[s1][p]paletteuse=dither=bayer",
        "output/demo_preview.gif"
    ]
    subprocess.run(cmd_gif, capture_output=True)
    print("Saved output/demo_preview.gif")
    
    # 7. Copy deliverables to artifact directory
    art_dir = r"C:\Users\Sanket\.gemini\antigravity\brain\0742d493-2333-419a-a81d-2677e2100688"
    if os.path.exists(art_dir):
        shutil.copy("output/output.mp4", os.path.join(art_dir, "output.mp4"))
        shutil.copy("output/output_nocaptions.mp4", os.path.join(art_dir, "output_nocaptions.mp4"))
        shutil.copy("output/thumbnail.png", os.path.join(art_dir, "thumbnail.png"))
        shutil.copy("output/demo_preview.gif", os.path.join(art_dir, "demo_preview.gif"))
        for fname in os.listdir("output"):
            if fname.startswith("qc_final_") and fname.endswith(".png"):
                shutil.copy(os.path.join("output", fname), os.path.join(art_dir, fname))
        print(f"Copied final media files and QC snapshots to artifact directory: {art_dir}")

    # 8. Verify metrics with ffprobe
    cmd_probe = ["ffprobe", "-v", "error", "-show_entries", "stream=index,codec_type,codec_name,r_frame_rate,duration", "-of", "default=noprint_wrappers=1", "output/output.mp4"]
    res = subprocess.run(cmd_probe, capture_output=True, text=True)
    print(f"\nFinal output.mp4 verified metrics:\n{res.stdout.strip()}")

if __name__ == "__main__":
    asyncio.run(main())
