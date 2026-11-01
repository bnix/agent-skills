---
name: practice-questions
description: Write AWS Certified Generative AI Developer – Professional (AIP-C01) practice exam questions from the vault study notes, checked against the AWS Documentation MCP. Two modes - (1) "quiz me" asks one interactive question at a time, waits for the answer, gives feedback, and logs the result to practice_log.md; (2) "create/make a quiz deck" (or flashcards) writes a deck file under StudyKit/genai-professional/. Use for "quiz me", "test me", "practice question", "new deck", "quiz deck", or "flashcards".
argument-hint: "[quiz me | deck <topic>] [optional topic]"
---

# Practice Questions (AIP-C01)

Request: $ARGUMENTS

Choose the mode from the request:
- **Quiz mode** for "quiz me", "test me", or "ask me a question". One question at a time, interactive.
- **Deck mode** for "create/make/add a deck" or "flashcards". Writes a file and doesn't quiz.

Both modes write questions the same way. **Before writing any question, read [references/item-writing.md](references/item-writing.md).** It covers the exam's question format, how to write a stem, how to build distractors, and how to verify answers.

## Sources (both modes)

- Topic content: the relevant `GenAI_Cert/\d+-*.md` notes. Use `GenAI_Cert/README.md` to find them.
- Exam style: `Practice Questions.md` (real-style examples with per-option rationales).
- Distractor patterns: `GenAI_Cert/26-exam-strategy-trap-patterns.md` and `exam_misses_review.md`.
- Weak areas: `exam_misses_review.md` and the `Result:` lines in `practice_log.md`.
- Facts and citations: the `Docs:` links in the notes, plus `search_documentation` → `read_documentation`/`read_sections` from the AWS Documentation MCP. **The correct answer and the reason each distractor is wrong must both be confirmed in the docs**, not only in a note. If a note disagrees with the docs, go with the docs and tell the user which note needs fixing. Don't edit notes.

## Quiz mode

1. **Pick the topic.** Use the topic the user names. Otherwise, pick one using spacing and interleaving:
   - Look at the last ~10 `Result:` lines in `practice_log.md`. Favor concepts that were missed or answered with `guess` at least a day ago. Avoid the topic of the previous 2 questions.
   - Otherwise sample by exam domain weight (see item-writing.md) and favor the weak areas in `exam_misses_review.md`.
   - Don't repeat a stem that's already in `practice_log.md`. Test the same concept from a new angle instead.
2. **Write and verify the question** following item-writing.md. Finish verifying before you show anything.
3. **Ask it.** Show only the stem and lettered options (A–D, or A–E and up for "Select TWO."). Don't show hints, topic labels that give the answer away, or the answer. Ask for the answer **and a confidence level: sure / unsure / guess**. **Stop and wait for the reply.**
4. **Give feedback** after they answer:
   - Say whether they were right, then give the correct option(s) and why, tied to the specific requirement clauses in the stem.
   - Say why each distractor is wrong in one or two sentences, and name the trap pattern it uses (from note 26).
   - Include a "Learn more" doc link for the correct answer and for any distractor whose reason needs a source.
   - Wrong but **sure**: name the exact misconception plainly. These high-confidence errors are the most worth fixing, so point to the note section to reread.
   - Right but **guess** or **unsure**: say the answer was correct but not yet reliable, and give the one fact that settles it.
5. **Log it.** Append the question to `practice_log.md` in the same format as the existing entries: a `---` separator, the stem, then `Answer option N` / `A. …` / `Why this is correct` or `Why this would be incorrect` / `Learn more about [..](..) .` for each option. After the last option, add one line:
   `Result: correct|incorrect (picked B; answer C) · confidence: sure|unsure|guess · topic: <note-file-slug> · domain: D<n> · <YYYY-MM-DD>`
6. Offer another question. After a miss, suggest coming back to the concept in a later session with a different question rather than right away, and offer to add it to a deck.

## Deck mode

Read [references/deck-format.md](references/deck-format.md) for the file format, which the quiz app parses.

1. **Scope.** Identify the topic or exam section and read the related notes, the note 26 traps for that area, and the matching rows in `exam_misses_review.md`.
2. **Check existing decks** in `StudyKit/genai-professional/`. If a deck on this topic exists, ask whether to append to it or start a new deck. When appending, **never edit existing `### ` prompt lines**: a question's identity is a hash of its prompt text, so editing a prompt erases its study history. Don't duplicate a question that's already in any deck.
3. **Plan the deck** before writing. Default to 10–15 questions unless the user gives a number. Cover each subtopic, use about 25–30% multiple-response questions, and spread the trap patterns so the deck doesn't reuse one distractor trick. For decks that span domains, weight questions by domain.
4. **Write each question** following item-writing.md. Verify every correct answer and every distractor's reason against the docs.
5. **Spread out answer positions.** Across the deck, the correct answer should land in each position about equally often, without an obvious pattern.
6. **Validate** before reporting:
   ```bash
   python3 <skill-dir>/scripts/check_deck.py StudyKit/genai-professional/<deck>.md
   ```
   It checks the frontmatter, options, multiple-response count wording, explanations and links, answer-position spread, and duplicate prompts across all decks. Fix every `ERROR`, and fix each `WARN` or explain why it can stay.
7. **Report** the deck path, the question count (single-answer vs. multiple-response), the answer-position spread, the subtopics and trap patterns covered, and any disagreements between notes and docs. Commit only when the user explicitly asks, and stage only the deck file.

`<skill-dir>` is this skill's base directory. Run commands from the vault root.
