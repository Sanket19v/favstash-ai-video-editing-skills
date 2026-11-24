import requests
import json
import base64

API_KEY = "sk-fish-PJ2OwPuOjXeKCRmc4Bpzvzl4dAbrUZUig08hfnbgFNg"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "model": "s2.1-pro-free"
}

payload = {
    "text": "Stop right there!",
    "reference_id": "08311ef33d5243ef9d8cdd87234e5982",
    "format": "mp3"
}

resp = requests.post("https://api.fish.audio/v1/tts/stream/with-timestamp", headers=headers, json=payload, stream=True)
print("SSE status:", resp.status_code)

words = []
audio_bytes = bytearray()
for raw_line in resp.iter_lines(decode_unicode=True):
    if not raw_line or not raw_line.startswith("data:"):
        continue
    payload_str = raw_line[len("data:"):].strip()
    if payload_str == "[DONE]":
        break
    try:
        event = json.loads(payload_str)
        if "audio_base64" in event:
            audio_bytes.extend(base64.b64decode(event["audio_base64"]))
        if "alignment" in event and event["alignment"]:
            for seg in event["alignment"].get("segments", []):
                words.append(seg)
    except Exception as e:
        pass

print(f"Captured {len(audio_bytes)} audio bytes, words: {words}")
