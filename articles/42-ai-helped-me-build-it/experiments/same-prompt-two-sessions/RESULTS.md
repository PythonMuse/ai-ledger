# Same Prompt, Two Sessions: The Results

Same model, same prompt, two fresh sessions ([setup](./prompt.md)). Both scripts ran without errors and looked reasonable. Both even agreed on "within 30 days" (29 days flagged, 31 not). Then we ran them against the article's seeded sample data:

| Edge case | Approved answer | Session A | Session B |
|---|---|---|---|
| "INV-1043" vs. "inv 1043", 10 days apart | Flagged | Not flagged | Not flagged |
| Same invoice, 29 days apart | Flagged | Flagged | Flagged |
| Same invoice, 31 days apart | Not flagged | Not flagged | Not flagged |
| Blank invoice number (two payments) | Sent to a person | **Flagged as a duplicate of each other** | **Not in the output (never reported)** |
| Blank vendor name | Sent to a person | Not in the output (never reported) | **Not in the output (never reported)** |
| "ABC Corp" vs. "ABC Corporation" | Not flagged (missed by design) | Not flagged | Not flagged |
| **Pairs flagged** | **2** | **2** | **1** |

Reproduce it with `python compare.py`.

## What differed, and why it matters

- **Two different answers to the same question.** Session A reported two possible duplicates; Session B reported one. Same model, same words, same data.
- **Session A invented a duplicate.** It turned each blank invoice number into the text "nan", so the two Tailspin Catering payments with no invoice number "matched" each other. This is the exact bug our own first draft had, the one described in the article.
- **Session B quietly shrank the population.** It dropped every payment with a blank vendor or invoice number before testing, and never said so. Its output looks cleaner than Session A's, and it is worse: three payments were never tested, and nothing in the report tells you.
- **Both missed a real duplicate.** Neither removed punctuation and spaces, so "INV-1043" and "inv 1043" never matched.
- **Neither is "wrong" in an obvious way.** Both are tidy, commented, plausible scripts. You would only find these problems by running them against data with a known answer.

## The takeaway

Variation at **build time** is manageable. You test a version against a known answer, fix what it gets wrong, approve it, and freeze it. That is what the article's own script went through.

Variation at **run time** is the problem. If every month is a fresh session, every month is a new interpretation of the rules. Some months it invents a duplicate; some months it quietly skips payments. And you would have to re-review the logic every time.

**AI helped build it. AI does not have to run it.**
