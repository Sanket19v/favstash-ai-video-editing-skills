import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

async def verify():
    html_path = Path("video-engine/index.html").resolve().as_uri()
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1920})
        await page.goto(html_path)
        await page.wait_for_timeout(300)
        
        test_times = [0.2, 1.2, 1.5, 1.8, 2.1, 2.7, 3.2, 4.2, 6.0, 9.0, 11.5, 12.5, 16.5, 20.0, 24.0, 28.0]
        for t in test_times:
            await page.evaluate(f"window.renderAt({t})")
            active = await page.evaluate("() => { const el = document.querySelector('.caption-word.word-active'); return el ? el.textContent : 'NONE'; }")
            all_words = await page.evaluate("() => { return Array.from(document.querySelectorAll('.caption-word')).map(e => e.textContent).join(' '); }")
            p_style = await page.evaluate("() => document.getElementById('peterImg').style.transform")
            s_style = await page.evaluate("() => document.getElementById('stewieImg').style.transform")
            spk = "Peter" if "translateX(-1200" not in p_style else ("Stewie" if "translateX(1200" not in s_style else "None")
            print(f"t={t:4.1f}s | Spk: {spk:<6} | active: [{active:^12}] | line: \"{all_words}\"")
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(verify())
