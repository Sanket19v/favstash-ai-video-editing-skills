import requests

API_KEY = "sk-fish-PJ2OwPuOjXeKCRmc4Bpzvzl4dAbrUZUig08hfnbgFNg"
PETER_ID = "b1d36a18f8d84bd59dead30474cbe3d7"
STEWIE_ID = "08311ef33d5243ef9d8cdd87234e5982"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Test Peter
payload_p = {
    "text": "Holy crap, Stewie! What are you doing?",
    "reference_id": PETER_ID,
    "format": "mp3"
}

resp_p = requests.post("https://api.fish.audio/v1/tts", headers=headers, json=payload_p)
print("Peter status:", resp_p.status_code, "Length:", len(resp_p.content))

# Test Stewie
payload_s = {
    "text": "Silence, you fool! Change these settings immediately.",
    "reference_id": STEWIE_ID,
    "format": "mp3"
}

resp_s = requests.post("https://api.fish.audio/v1/tts", headers=headers, json=payload_s)
print("Stewie status:", resp_s.status_code, "Length:", len(resp_s.content))
