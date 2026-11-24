import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

async def test():
    html_path = Path('video-engine/index.html').resolve().as_uri()
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1080, 'height': 1920})
        page.on('console', lambda msg: print('PAGE LOG:', msg.text))
        page.on('pageerror', lambda err: print('PAGE ERROR:', err))
        await page.goto(html_path)
        await page.wait_for_timeout(300)
        for t in [0.0, 1.5, 3.8, 4.0, 4.2, 8.8, 9.2, 16.8, 20.2, 29.5]:
            await page.evaluate(f"window.renderAt({t})")
            title = await page.evaluate("document.getElementById('sceneTitle').textContent")
            peter_tf = await page.evaluate("document.getElementById('peterImg').style.transform")
            stewie_tf = await page.evaluate("document.getElementById('stewieImg').style.transform")
            print(f"t={t:4.1f}s | Title: {title:<25} | Peter: {peter_tf[:35]:<35} | Stewie: {stewie_tf[:35]}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test())
