# Quiz Deck Format

Each `.md` file under `StudyKit/genai-professional/` is one deck, covering a topic or an exam section. A quiz app parses these files, so follow the format exactly.

## Question deck (default)

```markdown
---
title: Bedrock Data Ingestion and OpenSearch
cert: AWS Certified GenAI Professional
tags: [bedrock, opensearch, rag]
---

### A company needs to ingest documents into a knowledge base for RAG. Which approach meets the requirement with the least operational overhead?

- [ ] Manually chunk and embed documents, then write vectors directly to OpenSearch.
- [ ] Run a Lambda function nightly to re-embed the entire corpus.
- [x] Use an Amazon Bedrock Knowledge Base data source with automatic chunking.
- [ ] Store raw documents in S3 and query them with Athena at inference time.

> A Bedrock Knowledge Base data source handles chunking, embedding, and indexing automatically, removing the need to manage a custom ingestion pipeline.

Learn more: [Ingesting data into a knowledge base](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-ingest.html)
```

Rules:

- **Frontmatter** (YAML) is required. `title` is required. `cert` and `tags` are optional deck-level metadata. Use `cert: AWS Certified GenAI Professional` to match the existing decks.
- **Questions** start at a `### ` heading (level 3) and run until the next `### ` heading or the end of the file. Paragraphs between the heading and the option list are part of the prompt, so you can write the scenario in the heading and put the "Which solution…" question and "Select TWO." in the paragraphs after it.
- **Options** are one GFM task list (`- [ ]` / `- [x]`) right after the prompt. Checked items are correct. If more than one item is checked, the app shows a multiple-response question (checkboxes) automatically, with no extra flag. Still write "Select TWO." (or THREE.) in the prompt, to match the real exam.
- **Explanation** is the first blockquote (`> ...`) after the option list. It's optional but should always be included.
- **References** are any Markdown links after the explanation, shown as "Learn more" links. You can include any number.
- **Randomize** the correct answer position and spread it across the deck. The correct answer can't always be the same option.
- A question's identity (used to track study history) is a hash of its prompt text. Reordering questions keeps their history, but **editing a prompt erases it**.

## Flashcard deck

For recalling facts (limits, defaults, definitions), use `kind: flashcards` in the frontmatter. Each card is a `### ` question followed by answer paragraphs, with no options:

```markdown
---
title: Bedrock Retrieval Essentials
kind: flashcards
cert: AWS Certified GenAI Professional
tags: [bedrock, rag, flashcards]
---

### In hierarchical chunking, which chunks are searched and which are returned?

Small **child** chunks are searched, for precision. Their **parent** chunk is returned, for fuller context.
```

Keep each card to one fact or contrast, with a short answer, and phrase the question so the answer has to be recalled, not recognized.
