# Same Prompt, Two Sessions: The Setup

**Date run:** October 12, 2026
**Tool:** Claude Code CLI 2.1.233
**Model:** `claude-sonnet-5-5` (the same model for both sessions)

## The prompt

Both sessions received exactly this text, word for word:

```text
Write a Python script using pandas that reads ap_payments.csv (columns: payment_id, vendor_name, invoice_number, amount, payment_date) and finds possible duplicate payments: same vendor, same invoice number, same amount, paid within 30 days of each other. Write the results to duplicate_payment_exceptions.csv. Reply with only the code.
```

It is written the way an accountant might ask: plain English, the approved criteria stated, nothing about edge cases.

## How the sessions were kept independent

Each session was a separate, one-shot run from its own empty folder:

```bash
claude -p "<prompt>" --model claude-sonnet-5-5 --no-session-persistence
```

- Neither session could see this repository, the article, our own script, the sample data, or the other session's answer.
- Neither had any earlier conversation to draw on.

## What was saved

- [`session_a.py`](./session_a.py) and [`session_b.py`](./session_b.py) are each session's reply, unedited. The only change is removing the markdown code fences around the code.
- [`compare.py`](./compare.py) runs both scripts on a copy of the article's synthetic [`ap_payments.csv`](../../data/ap_payments.csv) and compares what each did with every seeded edge case against the hand-checked [`expected_exceptions.csv`](../../data/expected_exceptions.csv).

The results are in [RESULTS.md](./RESULTS.md).

Run it again yourself and you may get a third version. That is rather the point.
