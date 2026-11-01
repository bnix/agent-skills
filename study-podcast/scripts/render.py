#!/usr/bin/env python
"""Render a study-podcast script.md to a loudness-normalized MP3 with chapters.

Usage (run with the Kokoro venv):
    ~/.local/share/study-podcast/.venv/bin/python \
        <skill-dir>/scripts/render.py Podcasts/<date>-<slug>/script.md

Run from the vault root. <skill-dir> is this skill's base directory.

Script format (see SKILL.md):
    YAML frontmatter, then lines of
      [CHAPTER: name]
      HOST: text            (bold markers like **HOST:** are fine)
      EXPERT: text ... [PAUSE 5s] ... text
      [PAUSE 5s]            (standalone)
    A line of exactly `---` after the body starts the claim ledger and ends parsing.
"""

import argparse
import json
import re
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

import numpy as np

SAMPLE_RATE = 24000
DEFAULT_SPEED = 1.1
MIN_MINUTES, TARGET_MINUTES, MAX_MINUTES = 10, 13, 15
VOICES = {"HOST": "af_heart", "EXPERT": "am_michael"}
SEED = 0

SPEAKER_RE = re.compile(r"^\**\s*(HOST|EXPERT)\s*:\s*\**\s*(.*)$")
CHAPTER_RE = re.compile(r"^\[CHAPTER:\s*(.+?)\]\s*$")
PAUSE_RE = re.compile(r"\[PAUSE\s+(\d+(?:\.\d+)?)\s*s\]", re.IGNORECASE)


def parse_script(path):
    """Return (title, events). Events: ('chapter', name) | ('say', speaker, text) | ('pause', secs)."""
    lines = path.read_text(encoding="utf-8").splitlines()
    title = path.parent.name
    i = 0
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                break
            m = re.match(r"^title:\s*['\"]?(.*?)['\"]?\s*$", lines[i])
            if m:
                title = m.group(1)
        i += 1

    events = []
    for raw in lines[i:]:
        line = raw.strip()
        if line == "---":
            break  # claim ledger follows
        if not line:
            continue
        m = CHAPTER_RE.match(line)
        if m:
            events.append(("chapter", m.group(1)))
            continue
        m = SPEAKER_RE.match(line)
        if m:
            speaker, text = m.groups()
        elif PAUSE_RE.fullmatch(line):
            speaker, text = None, line
        else:
            continue  # headings, stage notes, etc.
        # Split inline pauses out of spoken text.
        pos = 0
        for pm in PAUSE_RE.finditer(text):
            chunk = text[pos:pm.start()].strip()
            if chunk and speaker:
                events.append(("say", speaker, chunk))
            events.append(("pause", float(pm.group(1))))
            pos = pm.end()
        chunk = text[pos:].strip()
        if chunk and speaker:
            events.append(("say", speaker, chunk))
    return title, events


def load_lexicon(path):
    if not path or not path.exists():
        return []
    lex = json.loads(path.read_text(encoding="utf-8"))
    # Longest terms first so "IAM Identity Center" wins over "IAM".
    return [(re.compile(r"(?<![\w-])" + re.escape(k) + r"(?![\w-])"), v)
            for k, v in sorted(lex.items(), key=lambda kv: -len(kv[0]))]


def apply_lexicon(text, lexicon):
    text = re.sub(r"[*_`]", "", text)  # strip markdown emphasis
    for pattern, spoken in lexicon:
        text = pattern.sub(spoken, text)
    return text


def silence(seconds):
    return np.zeros(int(seconds * SAMPLE_RATE), dtype=np.float32)


def synthesize(events, lexicon, speed, gap_ms):
    import torch
    from kokoro import KPipeline

    torch.manual_seed(SEED)
    pipeline = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")

    pieces, chapters = [], []
    cursor = 0  # samples written so far
    turns = sum(1 for e in events if e[0] == "say")
    done = 0
    for ev in events:
        if ev[0] == "chapter":
            chapters.append((ev[1], cursor))
            continue
        if ev[0] == "pause":
            audio = silence(ev[1])
        else:
            _, speaker, text = ev
            spoken = apply_lexicon(text, lexicon)
            chunks = [r.audio.cpu().numpy() if hasattr(r.audio, "cpu") else np.asarray(r.audio)
                      for r in pipeline(spoken, voice=VOICES[speaker], speed=speed, split_pattern=None)
                      if r.audio is not None]
            audio = np.concatenate(chunks + [silence(gap_ms / 1000)]).astype(np.float32)
            done += 1
            print(f"\r  synthesized {done}/{turns} turns", end="", file=sys.stderr, flush=True)
        pieces.append(audio)
        cursor += len(audio)
    print(file=sys.stderr)
    return np.concatenate(pieces), chapters


def write_wav(path, audio):
    pcm = (np.clip(audio, -1.0, 1.0) * 32767).astype(np.int16)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        w.writeframes(pcm.tobytes())


def ffmeta_escape(s):
    return re.sub(r"([=;#\\\n])", r"\\\1", s)


def write_ffmetadata(path, title, chapters, total_samples):
    out = [";FFMETADATA1", f"title={ffmeta_escape(title)}"]
    for idx, (name, start) in enumerate(chapters):
        end = chapters[idx + 1][1] if idx + 1 < len(chapters) else total_samples
        out += ["[CHAPTER]", f"TIMEBASE=1/{SAMPLE_RATE}", f"START={start}", f"END={end}",
                f"title={ffmeta_escape(name)}"]
    path.write_text("\n".join(out) + "\n", encoding="utf-8")


def encode_mp3(wav, meta, mp3):
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-i", str(wav), "-i", str(meta),
        "-map", "0:a", "-map_metadata", "1", "-map_chapters", "1",
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
        "-ar", str(SAMPLE_RATE), "-c:a", "libmp3lame", "-b:a", "128k",
        "-id3v2_version", "3", str(mp3),
    ], check=True)


def probe_duration(mp3):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "default=nw=1:nk=1", str(mp3)],
                         check=True, capture_output=True, text=True)
    return float(out.stdout.strip())


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("script", type=Path, help="path to script.md")
    ap.add_argument("-o", "--out", type=Path, help="output MP3 (default: episode.mp3 beside script)")
    ap.add_argument("--lexicon", type=Path, help="pronunciation map (default: Podcasts/lexicon.json)")
    ap.add_argument("--speed", type=float, default=DEFAULT_SPEED, help=f"speech rate (default {DEFAULT_SPEED})")
    ap.add_argument("--gap-ms", type=int, default=300, help="silence between turns (default 300)")
    ap.add_argument("--keep-wav", action="store_true", help="also keep the raw episode.wav")
    args = ap.parse_args()

    script = args.script.resolve()
    out = (args.out or script.with_name("episode.mp3")).resolve()
    lexicon_path = args.lexicon or script.parent.parent / "lexicon.json"

    title, events = parse_script(script)
    if not any(e[0] == "say" for e in events):
        sys.exit(f"No HOST:/EXPERT: lines found in {script}")
    words = sum(len(e[2].split()) for e in events if e[0] == "say")
    print(f"Rendering '{title}': {words} words, speed {args.speed}, "
          f"lexicon {'loaded' if lexicon_path.exists() else 'missing'} ({lexicon_path})", file=sys.stderr)

    audio, chapters = synthesize(events, load_lexicon(lexicon_path), args.speed, args.gap_ms)

    with tempfile.TemporaryDirectory() as tmp:
        wav = Path(tmp) / "episode.wav"
        meta = Path(tmp) / "chapters.txt"
        write_wav(wav, audio)
        write_ffmetadata(meta, title, chapters, len(audio))
        encode_mp3(wav, meta, out)
        if args.keep_wav:
            wav.replace(out.with_suffix(".wav"))

    dur = probe_duration(out)
    wpm = words / (dur / 60)
    ok = MIN_MINUTES * 60 <= dur <= MAX_MINUTES * 60
    print(f"Wrote {out}")
    print(f"Duration {int(dur // 60)}:{int(dur % 60):02d} | {words} words | {wpm:.0f} wpm | "
          f"{len(chapters)} chapters | "
          f"{'OK' if ok else f'OUT OF RANGE (target {MIN_MINUTES}-{MAX_MINUTES} min)'}")
    if not ok:
        target = round(TARGET_MINUTES * wpm, -1)
        print(f"Adjust script to ~{target:.0f} words for {TARGET_MINUTES} min at speed {args.speed}.")
        sys.exit(2)


if __name__ == "__main__":
    main()
