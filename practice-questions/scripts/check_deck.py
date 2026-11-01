#!/usr/bin/env python3
"""Validate a QuizMe deck file (stdlib only).

Usage (from the vault root):
    python3 <skill-dir>/scripts/check_deck.py QuizMeDecks/genai-professional/<deck>.md

Prints ERROR / WARN lines and a summary. Exit code 1 if any ERROR.
Duplicate prompts are checked against every other .md deck in the same folder.
"""

import re
import sys
from collections import Counter
from pathlib import Path

OPTION_RE = re.compile(r"^- \[( |x|X)\] (.+)$")
COUNT_WORDS = {2: "TWO", 3: "THREE", 4: "FOUR"}


def parse(path):
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    fm = {}
    body_start = 0
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                body_start = i + 1
                break
            if ":" in lines[i]:
                k, v = lines[i].split(":", 1)
                fm[k.strip()] = v.strip()
    questions, cur = [], None
    for raw in lines[body_start:]:
        if raw.startswith("### "):
            cur = {"heading": raw[4:].strip(), "prompt": [], "options": [],
                   "explanation": False, "links": 0, "stage": "prompt"}
            questions.append(cur)
            continue
        if cur is None:
            continue
        m = OPTION_RE.match(raw)
        if m and cur["stage"] in ("prompt", "options"):
            cur["stage"] = "options"
            cur["options"].append((m.group(1).lower() == "x", m.group(2)))
            continue
        if cur["stage"] == "options" and raw.strip() and not m:
            cur["stage"] = "after"
        if cur["stage"] == "prompt":
            cur["prompt"].append(raw)
        elif raw.startswith(">"):
            cur["explanation"] = True
        if cur["stage"] == "after":
            cur["links"] += len(re.findall(r"\]\((https?://[^)]+)\)", raw))
    return fm, questions


def norm(s):
    return re.sub(r"\s+", " ", s).strip().lower()


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    path = Path(sys.argv[1])
    fm, qs = parse(path)
    errors, warns = [], []
    flash = fm.get("kind", "").lower() == "flashcards"

    if not fm:
        errors.append("missing YAML frontmatter")
    elif not fm.get("title"):
        errors.append("frontmatter has no title")
    if not qs:
        errors.append("no '### ' questions found")

    positions, multi = Counter(), 0
    for n, q in enumerate(qs, 1):
        tag = f"Q{n} ({q['heading'][:60]}...)"
        if flash:
            if q["options"]:
                warns.append(f"{tag}: flashcard deck question has options")
            continue
        opts = q["options"]
        correct = [i for i, (ok, _) in enumerate(opts) if ok]
        if len(opts) < 4:
            errors.append(f"{tag}: {len(opts)} options (need 4+)")
        if not correct:
            errors.append(f"{tag}: no option marked [x]")
            continue
        prompt = norm(q["heading"] + " " + " ".join(q["prompt"]))
        if len(correct) == 1:
            positions[correct[0] + 1] += 1
            if len(opts) != 4:
                warns.append(f"{tag}: single-answer question with {len(opts)} options (exam uses 4)")
        else:
            multi += 1
            word = COUNT_WORDS.get(len(correct), str(len(correct))).lower()
            if f"select {word}" not in prompt and f"choose {word}" not in prompt:
                errors.append(f"{tag}: {len(correct)} correct but prompt lacks 'Select {word.upper()}.'")
            if len(opts) < 5:
                errors.append(f"{tag}: multiple-response needs 5+ options, has {len(opts)}")
        if "all that apply" in prompt:
            warns.append(f"{tag}: 'select all that apply' (real exam states the count)")
        lengths = [len(t) for _, t in opts]
        longest = max(range(len(opts)), key=lambda i: lengths[i])
        if len(correct) == 1 and longest == correct[0] and lengths[longest] > 1.4 * sorted(lengths)[-2]:
            warns.append(f"{tag}: correct option is much longer than the others (length cue)")
        if not q["explanation"]:
            warns.append(f"{tag}: no '>' explanation")
        if q["links"] == 0:
            warns.append(f"{tag}: no Learn more link")

    single = sum(positions.values())
    if single >= 4:
        top_pos, top_n = positions.most_common(1)[0]
        if top_n / single > 0.4:
            warns.append(f"answer position {top_pos} is correct in {top_n}/{single} single-answer questions")

    heads = Counter(norm(q["heading"]) for q in qs)
    for h, c in heads.items():
        if c > 1:
            errors.append(f"duplicate prompt within deck: {h[:70]}")
    for other in path.parent.glob("*.md"):
        if other.resolve() == path.resolve():
            continue
        _, oqs = parse(other)
        for oq in oqs:
            if norm(oq["heading"]) in heads:
                warns.append(f"prompt also in {other.name}: {oq['heading'][:70]}")

    for e in errors:
        print("ERROR", e)
    for w in warns:
        print("WARN ", w)
    kind = "flashcards" if flash else f"{len(qs) - multi} single / {multi} multiple-response"
    spread = ", ".join(f"{p}:{positions[p]}" for p in sorted(positions)) or "n/a"
    print(f"{path.name}: {len(qs)} questions ({kind}); correct-position spread {spread}; "
          f"{len(errors)} errors, {len(warns)} warnings")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
