# Shape of the Answer Card

*A one-page companion to [Does This Decision Actually Need a Large Language Model?](../README.md). Print it and keep it at the desk.*

Before you choose a model, look at the shape of the answer the step needs. Ask this of **each step**, not once for the whole process.

---

## What shape is the answer?

| What the work requires | A reasonable place to start |
|---|---|
| A known calculation, threshold, match, or rule | **Deterministic automation** (formula, Power Query, SQL, Python) |
| A bounded choice among answers you can list in advance | **Decision model** (or another classification approach) |
| A score or probability used to prioritize | **Decision model** or a predictive model trained on your history |
| Interpreting or writing open-ended language | **Large language model (LLM)**, validated |
| Material professional judgment or accountability | **A qualified person** |

This is a starting point, not a hierarchy. Real workflows combine these, and some steps can be solved more than one way.

---

## Five questions

| # | Question | If yes |
|---|---|---|
| 1 | **Is the rule known?** Could you write it as an `IF` statement? | Encode the rule. No model needed. |
| 2 | **Can the outcomes be listed in advance?** Five reason codes, six queues, a 1-to-4 scale? | A decision model may fit. Add an "other" or "cannot tell" option. |
| 3 | **Is open-ended language really needed?** Must the answer be *written*, or only *chosen*? | If it must be written, an LLM earns its place. If only chosen, it probably doesn't. |
| 4 | **What is the minimum evidence?** Which fields does the step actually need to see? | Send only those. The safest confidential field is the one you never provide. |
| 5 | **Who owns the consequence?** Approval, accounting treatment, a decision about a person? | A person keeps it. The model sorts; it does not approve. |

---

## Three reminders

- **Classification authority is not approval authority.** Routing an invoice exception is not approving the invoice.
- **A probability is only useful with a plan.** Decide what happens at each confidence level *before* you see the numbers, and set the levels from your own labeled results.
- **A decision model is not a loophole.** If a contract or policy restricts AI or automated decision-making, swapping model types does not make that restriction go away.

---

*PythonMuse LLC | www.pythonmuse.com. Educational purposes only; not professional advice. Content licensed under CC BY-NC-SA 4.0.*
