---
name: study-podcast
description: Generate a 10–15 minute, two-voice audio study podcast (script + MP3) that goes deep on ONE AWS Certified Generative AI Developer – Professional (AIP-C01) topic from the Obsidian vault notes, fact-checked against AWS docs. Use when asked to "make a podcast", "study podcast", "audio episode", or for something to listen to while studying.
argument-hint: "[one topic, e.g. guardrails]"
---

# Study Podcast Generation

Produce a 10–15 minute, two-voice audio study episode that goes deep on a **single topic**: $ARGUMENTS

This is for personal self-study on a local machine. Keep the tooling simple, with no production hardening. Run all commands from the vault root. `<skill-dir>` below means this skill's base directory.

## 1. Choose the topic

- Each episode covers **exactly one topic** so there's room for depth. A topic is roughly one study note's subject (for example guardrails, chunking, or identity federation), not a whole exam domain.
- If the arguments name more than one topic, don't combine them. Ask the user which one to do first, and offer to make the others as separate episodes.
- If no topic is given, propose 3 single-topic candidates and confirm one with the user before writing. Rank candidates by:
  1. Weak areas in `exam_misses_review.md` and `Result:` lines in `practice_log.md` (misses, and correct answers marked `guess`).
  2. Exam domain weight: D1 FM Integration, Data Management & Compliance 31% · D2 Implementation & Integration 26% · D3 AI Safety, Security & Governance 20% · D4 Operational Efficiency & Optimization 12% · D5 Testing, Validation & Troubleshooting 11%.
  3. Topics with no episode yet in `Podcasts/`.

## 2. Inputs to read first

1. The study note(s) for the topic (`GenAI_Cert/\d+-*.md`) and `GenAI_Cert/README.md`. Skim notes that cross-reference the topic for details worth pulling in.
2. `exam_misses_review.md` and `practice_log.md`. Weight content toward weak areas within this topic.
3. `Practice Questions.md` and `GenAI_Cert/26-exam-strategy-trap-patterns.md`. Match the exam's question style and teach the common distractor traps for this topic.
4. Existing episodes in `Podcasts/`. If one already covered this topic, go deeper or take a different angle instead of repeating it.

## 3. Script requirements

- Target 1,650–2,000 spoken words. Kokoro at speed 1.1 runs about 142 words per minute including pauses and turn gaps, so that's about 12–14 minutes. Hard limits are 10–15 minutes. Report the final word count.
- Two speakers, tagged per line:
  - `HOST:` is a curious learner who sometimes gives a plausible but wrong answer.
  - `EXPERT:` corrects it right away and explains why. Never leave a wrong statement uncorrected.
- Go for depth, not breadth. Split the topic into **3 subtopics** and go past definitions: how the feature actually works, its limits and defaults, how it's configured, and how it fails or gets misused.
- Structure:
  1. **Cold open** (60 seconds or less): an exam-style scenario question on the topic. Hold the answer until later, so the listener commits to a guess first.
  2. **Three subtopic segments.** Each one covers how it works, then an "X vs. Y — pick X when…" contrast, then one memorable analogy or mnemonic, then a pause-and-answer question.
  3. **Worked scenario**: one exam-style question with several requirements, solved step by step. Check off each requirement and eliminate each distractor. Then resolve the cold open.
  4. **Lightning round**: the 5 facts, limits, or defaults on this topic that are most likely to be tested. If an earlier episode covered a related topic, one of the 5 can be a callback question to it (spaced retrieval).
  5. **Recap**: a one-sentence takeaway per subtopic.
- Mark segment boundaries with `[CHAPTER: <name>]` lines. These become MP3 chapter markers.
- Pause-and-answer format: EXPERT reads the question and options, then the pause, then gives the answer and says why each distractor is wrong. Use `[PAUSE 5s]` for a short recall question and `[PAUSE 8s]` for a full scenario with four options.
- Write for the ear. Use short sentences, expand acronyms on first use, and write numbers the way they're spoken. Don't put tables, bullets, code, or URLs in spoken lines.
- Use current service names, such as Amazon SageMaker AI and Amazon Bedrock AgentCore.
- Fact-check every non-trivial claim (limits, defaults, feature names, "least operational overhead" choices) with the AWS Documentation MCP (`search_documentation`, then `read_documentation` or `read_sections`). If a note disagrees with the docs, use the docs and tell the user which note needs fixing. Don't edit the note.

## 4. Outputs

Write to `Podcasts/<YYYY-MM-DD>-<slug>/`:

- `script.md`: frontmatter (`title`, `topic`, `word_count`, `est_duration`), the tagged script, and a trailing `---` followed by a **Claim ledger** that maps each fact to a doc URL.
- `episode.mp3`: the rendered audio.

Don't modify study notes or the README unless the user asks. Only commit when the user explicitly asks.

## 5. Audio pipeline

- Environment (already installed; don't reinstall):
  - Python venv with Kokoro at `~/.local/share/study-podcast/.venv` (Python 3.12, because Kokoro doesn't support the system's Python 3.14). Run scripts with `~/.local/share/study-podcast/.venv/bin/python`.
  - The `hexgrad/Kokoro-82M` model is in the Hugging Face cache, and CUDA (RTX 3060 Ti) works. `ffmpeg` and `ffprobe` (with libmp3lame and loudnorm) and `espeak-ng` are on the system.
  - If any of these are missing, report it with the command that fixes it. Don't install anything without asking.
- The pronunciation map is `Podcasts/lexicon.json`, a flat JSON object such as `{"IAM": "eye-am", "RAG": "rag", "SQS": "S Q S"}`. Create it if it's missing and add new terms as needed. Matching is case-sensitive and whole-word, and longer terms match first.
- **Render only with the bundled script.** Don't write or change a per-episode renderer, so the output stays consistent from run to run:

  ```bash
  ~/.local/share/study-podcast/.venv/bin/python <skill-dir>/scripts/render.py Podcasts/<YYYY-MM-DD>-<slug>/script.md
  ```

  The script:
  - Parses `HOST:`/`EXPERT:` lines, inline or standalone `[PAUSE Ns]`, and `[CHAPTER: ...]`. It stops at the claim-ledger `---`.
  - Applies the lexicon and synthesizes with Kokoro (`hexgrad/Kokoro-82M`, `lang_code="a"`, 24 kHz). `HOST` uses the `af_heart` voice and `EXPERT` uses `am_michael`, at speed **1.1** with 300 ms between turns.
  - Normalizes loudness to -16 LUFS, writes a 128 kbps MP3 with one chapter marker per `[CHAPTER]`, and checks the duration with `ffprobe`.
  - Options: `--speed` (default 1.1; change it only if the user asks), `--gap-ms`, `--lexicon`, `-o`, `--keep-wav`.
  - Exits with code 2 if the duration is outside 10–15 minutes and prints a suggested word count for 13 minutes. Adjust the script length and render again.

## 6. When done

Report the topic and its 3 subtopics, the duration, the word count, the number of pause-and-answer questions, any disagreements between notes and docs, and the full path to `episode.mp3`.
