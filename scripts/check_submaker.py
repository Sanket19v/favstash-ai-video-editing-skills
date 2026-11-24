import asyncio
import edge_tts

async def check_submaker():
    submaker = edge_tts.SubMaker()
    communicate = edge_tts.Communicate("Stop right there!", "en-GB-RyanNeural")
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            pass
        elif chunk["type"] == "SentenceBoundary":
            submaker.feed(chunk)
    print("SubMaker subs:", submaker.get_srt())

if __name__ == "__main__":
    asyncio.run(check_submaker())
