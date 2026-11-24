import json

with open('script.json') as f:
    script = json.load(f)

for item in script:
    s = item['second']
    line = item.get('line', '')
    caps = item.get('captionWords', [])
    print(f"sec {s:2d}: spk={item['speaker']:<6} words_count={len(caps)} line='{line}'")
