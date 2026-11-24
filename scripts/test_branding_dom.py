import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

async def verify():
    html_path = Path("video-engine/index.html").resolve().as_uri()
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1920})
        await page.goto(html_path)
        
        # Test t=0.5
        await page.evaluate("window.renderAt(0.5)")
        pill = await page.evaluate("document.getElementById('pillTag').textContent")
        step = await page.evaluate("document.getElementById('stepLabel').textContent")
        title = await page.evaluate("document.getElementById('sceneTitle').textContent")
        bread = await page.evaluate("document.getElementById('breadcrumb').textContent")
        print(f"t=0.5: pill='{pill}' | step='{step}' | title='{title}' | bread='{bread}'")
        
        # Test t=29.5
        await page.evaluate("window.renderAt(29.5)")
        bread29 = await page.evaluate("document.getElementById('breadcrumb').textContent")
        card_html = await page.evaluate("document.getElementById('screen').innerHTML")
        has_ez_peter = "@Ez_peter" in card_html
        has_daily = "DailyPC" in card_html
        print(f"t=29.5: bread='{bread29}' | has_ez_peter={has_ez_peter} | has_daily={has_daily}")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(verify())
