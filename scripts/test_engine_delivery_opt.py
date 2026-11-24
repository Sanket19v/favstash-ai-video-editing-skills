import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1080, "height": 1920})
        html_path = os.path.abspath("video-engine/index.html")
        await page.goto(f"file:///{html_path.replace(os.sep, '/')}")
        await page.wait_for_timeout(1000)
        
        test_times = [0.5, 4.0, 16.5, 25.0, 39.5, 73.0, 80.0, 92.5]
        for t in test_times:
            await page.evaluate(f"window.renderAt({t})")
            await page.wait_for_timeout(50)
            snap_path = f"frames_test_t_{int(t*10):03d}.png"
            await page.screenshot(path=snap_path)
            print(f"Captured test frame at t={t}s -> {snap_path}")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
