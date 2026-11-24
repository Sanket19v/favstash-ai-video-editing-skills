import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1080, "height": 1920})
        html_path = os.path.abspath("video-engine/index.html")
        await page.goto(f"file:///{html_path.replace(os.sep, '/')}")
        await page.wait_for_timeout(500)
        
        test_times = [1.0, 14.5, 20.5, 24.5, 29.0, 38.0, 46.5, 55.5, 63.5, 66.5, 76.0]
        os.makedirs("test_frames", exist_ok=True)
        for t in test_times:
            await page.evaluate(f"window.renderAt({t})")
            snap_path = f"test_frames/rammap_t_{int(t*10):03d}.png"
            await page.screenshot(path=snap_path)
            print(f"Captured test frame at t={t}s -> {snap_path}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
