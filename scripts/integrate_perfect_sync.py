import json
import re

print("=== Integrating Frame-Perfect Aligned Captions into Engine ===")

with open("video-engine/aligned_captions.json", "r", encoding="utf-8") as f:
    aligned_data = json.load(f)

chunks = aligned_data["chunks"]
turn_ranges = aligned_data["turn_ranges"]

# 1. GENERATE output/captions.srt WITH EXACT TIMESTAMPS
def format_srt_time(sec):
    hrs = int(sec // 3600)
    mins = int((sec % 3600) // 60)
    secs = int(sec % 60)
    millis = int((sec - int(sec)) * 1000)
    return f"{hrs:02d}:{mins:02d}:{secs:02d},{millis:03d}"

srt_lines = []
for i, c in enumerate(chunks):
    start_str = format_srt_time(c["start"])
    end_str = format_srt_time(c["display_end"])
    spk_label = "Peter" if c["speaker"] == "peter" else "Stewie"
    line_text = " ".join(w["text"] for w in c["words"])
    srt_lines.append(f"{i+1}\n{start_str} --> {end_str}\n[{spk_label}] {line_text}\n")

with open("output/captions.srt", "w", encoding="utf-8") as f:
    f.write("\n".join(srt_lines))
print(f"Generated output/captions.srt with {len(chunks)} timed subtitle entries.")

# 2. UPDATE video-engine/index.html
with open("video-engine/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace or embed ALIGNED_CAPTIONS in index.html
aligned_json_str = json.dumps(aligned_data)
aligned_embed = f"window.ALIGNED_CAPTIONS = {aligned_json_str};\n    let ALIGNED_CAPTIONS = window.ALIGNED_CAPTIONS;"

if "window.ALIGNED_CAPTIONS" in html:
    html = re.sub(r'window\.ALIGNED_CAPTIONS\s*=\s*\{.*?\};\s*let ALIGNED_CAPTIONS = window\.ALIGNED_CAPTIONS;', aligned_embed, html, flags=re.DOTALL)
else:
    # Insert right before let SCRIPT
    html = html.replace("let SCRIPT =", f"{aligned_embed}\n    let SCRIPT =")

# 3. UPDATE CAPTION RENDERING LOGIC IN window.renderAt(t)
# Instead of guessing from 1-second chops, read the exact active chunk and word at continuous time clampedT!
old_cap_block = """      // 4. RENDER CAPTIONS
      const capEl = document.getElementById('captions');
      if (window.hideCaptions) {
        capEl.style.display = 'none';
      } else {
        capEl.style.display = 'flex';"""

new_cap_block = """      // 4. RENDER CAPTIONS - EXACT ACOUSTIC ALIGNMENT (NEVER DRIFTS)
      const capEl = document.getElementById('captions');
      if (window.hideCaptions) {
        capEl.style.display = 'none';
      } else {
        capEl.style.display = 'flex';
        
        // Find the active caption chunk for time clampedT
        const chunks = ALIGNED_CAPTIONS.chunks;
        let activeChunk = null;
        for (let i = 0; i < chunks.length; i++) {
          if (clampedT >= chunks[i].start && clampedT < chunks[i].display_end) {
            activeChunk = chunks[i];
            break;
          }
        }
        if (!activeChunk && chunks.length > 0) {
          // If in a micro-pause, retain the nearest chunk
          if (clampedT >= chunks[chunks.length - 1].start) {
            activeChunk = chunks[chunks.length - 1];
          } else {
            for (let i = 0; i < chunks.length - 1; i++) {
              if (clampedT >= chunks[i].display_end && clampedT < chunks[i+1].start) {
                activeChunk = chunks[i];
                break;
              }
            }
          }
        }

        if (activeChunk && activeChunk.words.length > 0) {
          // Find the active word within the active chunk at time clampedT
          let activeWordIdx = 0;
          for (let i = 0; i < activeChunk.words.length; i++) {
            if (clampedT >= activeChunk.words[i].global_start) {
              activeWordIdx = i;
            }
          }

          capEl.innerHTML = activeChunk.words.map((w, idx) => {
            const isActive = idx === activeWordIdx;
            return `<span class="caption-word ${isActive ? 'word-active' : ''}">${w.text}</span>`;
          }).join('');
        }
      }"""

# Replace caption rendering block in index.html
pattern_cap = r"// 4\. RENDER CAPTIONS.*?capEl\.innerHTML = activeChunk\?.*?\}\s*\}"
# Let's search for the start of // 4. RENDER CAPTIONS until // 5. RENDER CHARACTERS
idx_cap_start = html.find("// 4. RENDER CAPTIONS")
idx_char_start = html.find("// 5. RENDER CHARACTERS")

if idx_cap_start != -1 and idx_char_start != -1:
    html = html[:idx_cap_start] + new_cap_block + "\n\n      " + html[idx_char_start:]
    print("Replaced caption rendering logic in renderAt with acoustic-aligned lookup.")
else:
    print("WARNING: Could not find caption markers in index.html!")

# 4. UPDATE CHARACTER RENDERING LOGIC IN window.renderAt(t)
# Match character visibility and slides to turn_ranges
new_char_block = """// 5. RENDER CHARACTERS (Peter on Left, Stewie on Right)
      // Only ONE on screen at a time! Smooth slide in/out aligned to speaker turns
      const peterEl = document.getElementById('peterImg');
      const stewieEl = document.getElementById('stewieImg');

      // Determine current speaking turn
      const turns = ALIGNED_CAPTIONS.turn_ranges;
      let activeTurn = null;
      let activeTurnIdx = -1;
      for (let i = 0; i < turns.length; i++) {
        if (clampedT >= turns[i].start && clampedT <= turns[i].end) {
          activeTurn = turns[i];
          activeTurnIdx = i;
          break;
        }
      }
      if (!activeTurn && turns.length > 0) {
        // In transition between turns
        for (let i = 0; i < turns.length - 1; i++) {
          if (clampedT > turns[i].end && clampedT < turns[i+1].start) {
            // Halfway transition point
            const mid = (turns[i].end + turns[i+1].start) / 2;
            if (clampedT < mid) {
              activeTurn = turns[i];
              activeTurnIdx = i;
            } else {
              activeTurn = turns[i+1];
              activeTurnIdx = i + 1;
            }
            break;
          }
        }
        if (!activeTurn) activeTurn = turns[turns.length - 1];
      }

      const isPeter = activeTurn && activeTurn.speaker === 'peter';
      const isStewie = activeTurn && activeTurn.speaker === 'stewie';

      if (isPeter) {
        // Slide in at start of turn, slide out at end of turn
        const turnElapsed = clampedT - activeTurn.start;
        const turnRemaining = activeTurn.end - clampedT;
        let peterX = 0;
        if (turnElapsed < 0.25) {
          const inFrac = easeOutCubic(clamp(turnElapsed / 0.25, 0, 1));
          peterX = -1200 * (1 - inFrac);
        } else if (turnRemaining < 0.25) {
          const outFrac = easeInOutQuad(clamp((0.25 - turnRemaining) / 0.25, 0, 1));
          peterX = -1200 * outFrac;
        }
        const bobY = Math.sin(clampedT * Math.PI * 4) * 7;
        const breathScale = 1.0 + 0.012 * Math.sin(clampedT * Math.PI * 2);
        peterEl.style.transform = `translateX(${peterX}px) translateY(${bobY}px) scale(${breathScale})`;
        stewieEl.style.transform = `translateX(1200px)`;
      } else if (isStewie) {
        const turnElapsed = clampedT - activeTurn.start;
        const turnRemaining = activeTurn.end - clampedT;
        let stewieX = 0;
        if (turnElapsed < 0.25) {
          const inFrac = easeOutCubic(clamp(turnElapsed / 0.25, 0, 1));
          stewieX = 1200 * (1 - inFrac);
        } else if (turnRemaining < 0.25) {
          const outFrac = easeInOutQuad(clamp((0.25 - turnRemaining) / 0.25, 0, 1));
          stewieX = 1200 * outFrac;
        }
        const bobY = Math.sin(clampedT * Math.PI * 4) * 7;
        const breathScale = 1.0 + 0.012 * Math.sin(clampedT * Math.PI * 2);
        stewieEl.style.transform = `translateX(${stewieX}px) translateY(${bobY}px) scale(${breathScale})`;
        peterEl.style.transform = `translateX(-1200px)`;
      } else {
        peterEl.style.transform = `translateX(-1200px)`;
        stewieEl.style.transform = `translateX(1200px)`;
      }"""

idx_char_start = html.find("// 5. RENDER CHARACTERS")
idx_char_end = html.find("    };\n\n    // Load script.json")

if idx_char_start != -1 and idx_char_end != -1:
    html = html[:idx_char_start] + new_char_block + "\n" + html[idx_char_end:]
    print("Replaced character rendering logic with turn-aligned timing.")
else:
    print("WARNING: Could not find character block markers in index.html!")

with open("video-engine/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Updated video-engine/index.html successfully!")
