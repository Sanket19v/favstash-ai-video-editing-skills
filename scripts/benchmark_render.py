import asyncio
import time
from pathlib import Path
from playwright.async_api import async_playwright
import os

async def benchmark():
    os.makedirs("bench_frames", exist_ok=True)
    html_path = Path("video-engine/index.html").resolve().as_uri()
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
        await page.goto(html_path)
        
        t0 = time.time()
        for i in range(30):
            t = i / 30.0
            await page.evaluate(f"window.renderAt({t})")
            await page.screenshot(path=f"bench_frames/frame_{i:04d}.png")
        t1 = time.time()
        print(f"30 frames took {t1 - t0:.2f}s ({30 / (t1 - t0):.1f} fps)")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(benchmark())
