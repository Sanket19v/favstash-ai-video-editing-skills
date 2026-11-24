dialogue = [
    {"character": "Peter Griffin", "sentence": "Can Windows really use my computer without permission?"},
    {"character": "Stewie Griffin", "sentence": "It already is. You've been seeding Windows updates to strangers since the day you installed it."},
    {"character": "Peter Griffin", "sentence": "So everyone's computer is doing this?"},
    {"character": "Stewie Griffin", "sentence": "Every Windows 10 and 11 PC is secretly part of Microsoft's free CDN network, and one toggle in Settings turns it all off."},
    {"character": "Peter Griffin", "sentence": "Wait, like BitTorrent seeding?"},
    {"character": "Stewie Griffin", "sentence": "Exactly. But Microsoft never told you this was turned on by default."},
    {"character": "Peter Griffin", "sentence": "How much bandwidth are we talking?"},
    {"character": "Stewie Griffin", "sentence": "Therefore, some users report 80% of their upload speed getting consumed, which is why your Zoom calls freeze."},
    {"character": "Peter Griffin", "sentence": "That seems illegal."},
    {"character": "Stewie Griffin", "sentence": "It's buried in the terms you didn't read. But here's what's worse: Task Manager hides it as Service Host, Network Service. So you can't even see what's happening."},
    {"character": "Peter Griffin", "sentence": "Right. You just see mystery processes eating bandwidth."},
    {"character": "Stewie Griffin", "sentence": "Therefore, most people blame their ISP instead of Windows."},
    {"character": "Peter Griffin", "sentence": "Why would Microsoft do this?"},
    {"character": "Stewie Griffin", "sentence": "They deliver 3.5 billion updates monthly. Peer-to-peer means they offload server costs to your electricity bill and internet plan."},
    {"character": "Peter Griffin", "sentence": "Do they at least limit it to your local network?"},
    {"character": "Stewie Griffin", "sentence": "That's the misdirection. There's a setting for PCs on my local network. But the default includes PCs on the internet."},
    {"character": "Peter Griffin", "sentence": "You're uploading to random strangers worldwide."},
    {"character": "Stewie Griffin", "sentence": "Yep. Your gaming laptop in Ohio might be seeding updates to someone in Germany right now."},
    {"character": "Peter Griffin", "sentence": "How do I stop this immediately?"},
    {"character": "Stewie Griffin", "sentence": "Open Windows Settings. Go to Windows Update. Click Advanced Options. Then Delivery Optimization. Toggle Allow Downloads from Other PCs to Off."},
    {"character": "Peter Griffin", "sentence": "That's it?"},
    {"character": "Stewie Griffin", "sentence": "That's it. Five clicks and you're no longer Microsoft's free bandwidth."},
    {"character": "Peter Griffin", "sentence": "So Task Manager lies, and now Windows steals bandwidth."},
    {"character": "Stewie Griffin", "sentence": "Task Manager doesn't lie. It just shows you what Microsoft wants you to see."}
]

total_words = sum(len(d["sentence"].split()) for d in dialogue)
print(f"Total lines: {len(dialogue)}")
print(f"Total words: {total_words}")
print(f"Estimated speech duration: ~{total_words / 150 * 60:.1f}s ({total_words / 150:.1f} minutes)")
