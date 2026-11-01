# Writing AIP-C01 Exam Questions

These rules make practice questions match the real exam and teach the right lessons. A question that cues its answer or rests on a wrong fact trains the wrong habit.

## The real exam (from the AWS exam guide)

Source: [AIP-C01 exam guide](https://docs.aws.amazon.com/aws-certification/latest/ai-professional-01/ai-professional-01.html)

- **Multiple choice:** one correct answer and three distractors (4 options).
- **Multiple response:** two or more correct answers out of **five or more** options. Credit is all-or-nothing. The real exam states the count, as in "(Select TWO.)". Always state it. Don't write "select all that apply" (the misses review shows the hidden count causes over-selection that the real exam doesn't test).
- 65 scored questions plus 10 unscored. There's no penalty for guessing.
- Domain weights, used to spread topics:

| Domain | Weight | Typical notes |
| --- | --- | --- |
| D1 FM Integration, Data Management & Compliance | 31% | 01, 02, 04, 05, 06, 08, 13, 14, 15, 21 |
| D2 Implementation & Integration | 26% | 12, 16, 17, 19, 22, 23, 25 |
| D3 AI Safety, Security & Governance | 20% | 03, 10, 11, 20, 27 |
| D4 Operational Efficiency & Optimization | 12% | 09, 18 |
| D5 Testing, Validation & Troubleshooting | 11% | 03, 24 |

The note mapping is approximate. The task statements on each [domain page](https://docs.aws.amazon.com/aws-certification/latest/ai-professional-01/ai-professional-01-domain1.html) are authoritative.

- Check scope: the correct answer should use [in-scope services](https://docs.aws.amazon.com/aws-certification/latest/ai-professional-01/aip-01-in-scope-services.html). Model development and training, advanced ML techniques, and feature engineering are out of scope for this exam.

## Stem

- Follow the `Practice Questions.md` pattern: **company scenario → current state → requirements → constraint qualifier → question**. For example: "…The solution must X. The solution must Y. Which solution will meet these requirements with the LEAST operational overhead?"
- Every requirement clause must matter: each distractor should fail at least one specific clause or the qualifier (LEAST operational overhead, MOST cost-effective, lowest latency, MOST secure). If removing a clause doesn't change the answer, cut the clause.
- Test **application and analysis**, meaning choosing between workable designs, not recalling a definition. Put pure recall (a limit, a default) into flashcards, or into a scenario where the limit decides the answer (for example "datasets up to 50 MB" ruling out real-time inference).
- Use one concept per question, or a deliberate combination the exam is known to test (for example several guardrail features in one stem).
- Write in plain, neutral language. Use current service names. Use the same API and feature names the docs use, in code format where a note uses it (`InvokeModel`, `RetrieveAndGenerate`).

## Options

- **Distractors are real AWS features used wrongly**, not made-up services or API parameters. A fake feature can stick in memory as a fact. Use the patterns from note 26 and `exam_misses_review.md`:
  - A partial solution that meets some requirements but misses one.
  - A design that works but adds a custom Lambda, a second store, or orchestration that a built-in feature already handles ("least effort ≠ fewest services").
  - A detective control (Config, CloudWatch alarms) where the stem needs a preventive one.
  - The right service in the wrong role.
  - A managed feature applied outside its supported scope (wrong model family, Region, or data type).
  - A keyword lure: a stem word that points to the wrong service.
  - An offline mechanism (an evaluation job) where the stem needs a runtime control (guardrails).
- Keep options alike in length, grammar, and detail. **The correct answer must not stand out as the longest or most hedged option.** Don't use "all/none of the above". Don't let options overlap. Don't repeat a distinctive stem word only in the correct option.
- Multiple response: use 5 options for "Select TWO." and 6 for "Select THREE.". You can include two different mechanisms that each work (co-correct answers, such as IAM SAML federation and IAM Identity Center with an external IdP) when the docs support both.

## Verification (required before showing or saving)

1. Confirm the correct answer in the AWS docs and keep the URL.
2. For each distractor, ask "could this also meet every requirement?" If yes, change the stem or the distractor. Confirm in the docs the reason each distractor fails, especially for limits and supported-scope claims.
3. If the docs and a note disagree, go with the docs and tell the user which note needs fixing.

## Explanation

- First the correct answer, tied to the requirement clauses it meets.
- Then one sentence per distractor saying which clause or qualifier it fails.
- Then "Learn more" links to `docs.aws.amazon.com` pages you actually read. Never cite a URL you didn't open.
