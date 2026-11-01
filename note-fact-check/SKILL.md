---
name: note-fact-check
description: Fact-check, correct, and enhance an AWS GenAI Professional (AIP-C01) study note in the Obsidian vault against the AWS Documentation MCP, then format it to vault conventions and sync GenAI_Cert/README.md. Use when asked to research, fact-check, verify, enhance, expand, or "add" a note, including a new draft that has no number yet.
argument-hint: "[note path or topic]"
---

# Fact-check and Enhance a Study Note

Target: $ARGUMENTS

These notes are the source for practice questions, quiz decks, and podcasts for the **AWS Certified Generative AI Developer – Professional (AIP-C01)** exam. Exact details matter: limits, defaults, supported options, feature names, and "pick X over Y when…" distinctions are what exam questions are built from. A wrong fact here spreads into every question generated from it.

## Workflow

1. **Read first.** Read the target note and `GenAI_Cert/README.md`. Note where the topic sits in the README tables, and whether the "Gaps worth filling" section names it.
2. **Check overlap.** Skim the related numbered notes before writing anything. If another note already covers something in depth, link to it (`[18 — Cost](18-cost-and-performance-optimization.md#heading)`) instead of explaining it again.
3. **Verify every non-trivial claim** with the AWS Documentation MCP (`search_documentation`, then `read_documentation`/`read_sections`; use `search_table` for quotas and supported-model tables):
   - Fix anything wrong or outdated in place. Don't add new facts around a claim you haven't verified.
   - Check service and feature names against current docs. Renames and retirements are common, for example SageMaker → SageMaker AI and Kendra in maintenance mode. Note when a feature is preview-only or limited to certain Regions.
   - Write numbers exactly as the docs state them, with their units and scope (per account, per Region, per index, per call).
   - Keep the doc URL for each fact you verify. Those URLs go in `Docs:`.
4. **Enhance for exam use** where the docs support it:
   - Contrast tables or "pick X when…" lines for features that are easy to confuse.
   - The limits and defaults most likely to be tested.
   - Common traps, linked to the matching section of `26-exam-strategy-trap-patterns.md` instead of copied.
   - If the topic is mostly an out-of-scope service for AIP-C01 ([out-of-scope list](https://docs.aws.amazon.com/aws-certification/latest/ai-professional-01/aip-01-out-of-scope-services.html)), say so in one line instead of expanding it.
5. **Number new drafts.** If the note has no leading number, rename it to the next free `\d+-*.md` number (check `ls GenAI_Cert/`) with a kebab-case slug, and format it to the conventions below.
6. **Update `README.md` in the same pass:** change the "N topic files fact-checked" count and the file range, add or update the table row in the right section, and trim or update the "Gaps worth filling" bullet this note covers.
7. **Report:** list what you corrected (old claim → new claim, with the source), what you added, and any other notes that now contradict the docs. Don't edit those other notes unless asked.
8. **Commit only when the user explicitly asks.** Stage only the note and `README.md`, not unrelated untracked files. Write a commit message that says what was fact-checked, corrected, and added.

## Note conventions

- `#` title that matches the topic, with `##`/`###` subsections.
- **Bold** key terms the first time they appear, for example `**RAG (Retrieval-Augmented Generation)**`.
- Cross-references are standard Markdown links to files in the same folder, such as `[08-opensearch.md](08-opensearch.md)`, which Obsidian resolves. `#heading` anchors are optional.
- End the note with a `---` separator followed by:
  - `Related:` links to other numbered notes, separated by ` · `.
  - `Docs:` links to the primary AWS documentation pages cited for the note, separated by ` · `.

Example footer:

```markdown
---
Related: [OpenSearch](08-opensearch.md) · [RAG Fundamentals & Vector Stores](01-rag-fundamentals.md)
Docs: [What is S3 Vectors](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors.html) · [Limitations and restrictions](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-limitations.html)
```
