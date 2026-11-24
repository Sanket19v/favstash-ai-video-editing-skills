import asyncio
import edge_tts

async def check_chunks():
    communicate = edge_tts.Communicate("Stop right there!", "en-GB-RyanNeural")
    chunk_types = set()
    async for chunk in communicate.stream():
        chunk_types.add(chunk["type"])
        if chunk["type"] != "audio":
            print("Non-audio chunk:", chunk)
    print("All chunk types seen:", chunk_types)

if __name__ == "__main__":
    asyncio.run(check_chunks())
