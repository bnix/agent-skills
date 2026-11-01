# Agent Skills

My central repository for Agent skills. The current skills support studying for AWS exams using an [Obsidian](https://obsidian.md) vault and companion project [Study Kit](https://github.com/bnix/study-kit).

## Note enhancement, study aid generation skills]

Skills for managing an Obsidian notes vault and generating practice quizzes and podcasts.

| Skill | Use it for | Writes |
| --- | --- | --- |
| [note-fact-check](note-fact-check/SKILL.md) | Fact-check, correct, and enhance a study note against AWS docs; number new drafts; keep vault README index in sync | `GenAI_Cert/NN-*.md`, `GenAI_Cert/README.md` |
| [practice-questions](practice-questions/SKILL.md) | "Quiz me" (interactive, logged) and quiz/flashcard deck authoring | `practice_log.md`, `StudyKit/genai-professional/*.md` |
| [study-podcast](study-podcast/SKILL.md) | A 10–15 minute two-voice audio episode on one topic | `Podcasts/<date>-<slug>/` |

## Example Usage

You're watching an AWS certification lecture and taking notes using Obsidian. Your notes need to be enhanced with more detail and cross-referenced against AWS documentation.
Ask your LLM to enhance a note file and, using the `note-fact-check` skill, the note will be updated with greater detail and citations using AWS documentation.

## Requirements

### AWS MCP server

Fact-checking against AWS docs is mandatory to ensure correctness of generated notes, practice question, and podcasts. Install the **AWS Documentation MCP server** ([`awslabs.aws-documentation-mcp-server`](https://github.com/awslabs/mcp/tree/main/src/aws-documentation-mcp-server)). Without it, the skills can't verify claims.


### Kokoro TTS model

Podcast generation uses [Koroko](https://huggingface.co/hexgrad/Kokoro-82M) to locally generate audio.