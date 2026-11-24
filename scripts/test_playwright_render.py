import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
import os

async def test_render():
    os.makedirs("test_frames", exist_ok=True)
    html_path = Path("video-engine/index.html").resolve().as_uri()
    print("Loading HTML:", html_path)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
        await page.goto(html_path)
        await page.wait_for_timeout(500)
        
        # Test sample timestamps
        sample_times = [0.5, 4.5, 7.5, 11.5, 18.5, 25.5, 29.5]
        for t in sample_times:
            await page.evaluate(f"window.renderAt({t})")
            await page.wait_for_timeout(50)
            frame_path = f"test_frames/sample_{int(t):02d}s.png"
            await page.screenshot(path=frame_path)
            print(f"Captured {frame_path}")
            
        await browser.close()
    print("Sample render test completed successfully!")

if __name__ == "__main__":
    asyncio.run(test_render())
