# Step Decision Tree Card

*A one-page companion to [AI Helped Me Build It. AI Does Not Have to Run It.](../README.md). Print it and keep it at the desk.*

Ask these questions of **each step** in a process, not once for the whole process.

---

## Before you start

**Is this step still necessary?** Automation does not cure a process that exists only because "we've always done it this way." Automating a process nobody understands is just an efficient way to produce confusion on schedule.

---

## Choose the starting approach

| # | Question | If yes | If no |
|---|---|---|---|
| 1 | Is the step necessary and understood? | Go to 2 | Simplify, document, or redesign first |
| 2 | Can we write the rule, and should the same input always give the same result? | **Start with deterministic automation** (Excel, Power Query, SQL, Python) | Go to 3 |
| 3 | Does it require interpreting language or context? | **Consider an LLM**, subject to data restrictions, validation, and review | Go to 4 |
| 4 | Do reliable historical examples hold a pattern we can't write as rules? | **Consider machine learning** | Keep it human-led, or redesign |

## Then, for every option you chose

| # | Control question | What it means |
|---|---|---|
| 5 | Does the step involve judgment, approval, restricted data, or contractual limitations? | If yes, a qualified person stays responsible, whatever technology prepared the work. |
| 6 | What evidence will show that it worked as intended? | Define validation, logging, exception handling, and sign-off **before** you build. |

---

## The four kinds of work

| Kind | The test | Typical home |
|---|---|---|
| **Rules** | Can we state exactly how the result is calculated or classified? | Formula, Power Query, SQL, Python, RPA |
| **Patterns** | Do past examples hold a relationship we can't write down? | Machine-learning model trained on your history |
| **Language** | Does it require reading or writing unstructured text? | LLM, with validation and review |
| **Judgment** | Does it need accountability, authorization, or a facts-and-circumstances conclusion? | A qualified person |

## The rule of thumb

- If the rule is known, encode the rule.
- If language must be interpreted, consider an LLM, and validate it.
- If historical examples hold a pattern you can't write down, machine learning may fit.
- If the decision needs professional accountability, keep a person responsible.

---

*PythonMuse LLC | www.pythonmuse.com. Educational purposes only; not professional advice. Content licensed under CC BY-NC-SA 4.0.*
