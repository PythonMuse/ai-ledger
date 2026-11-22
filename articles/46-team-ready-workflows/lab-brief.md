# Lab Brief: I Built the Workflow. Now How Does My Team Use It?

**PythonMuse Lab · Article 46** · Status: In review

## The one-sentence problem
An accountant has used AI to build a working, tested workflow, but the colleagues who need to run it each month don't use Python or a code editor, and nobody has defined how they should run it, check it, and escalate.

## Audience
Mixed: builders (accountants who have built a workflow with an AI co-pilot), operators (accountants who will run it), reviewers, and accounting leaders deciding who does what. No coding knowledge is assumed for the article.

## Reader payoff
- **Immediate benefit:** the reader can name who designs, builds, operates, reviews, and maintains a workflow; picture a simple front door for it; list what the operator must check after a run; and run a handoff test with a colleague.
- **Key takeaway:** we won't all need the same technical skills, but we all need to understand our responsibilities, how our workflows operate, and how to validate the results.

## Learning outcomes
After this Lab, the reader can:
1. Understand why separating the builder from the operator matters, and why the operator should not review their own run.
2. Recognize what an operator must validate after a run (tie to the control balance, customer count, credits and missing due dates, a sample of unflagged items), and that a green check is not a sign-off.
3. Optionally, run and adapt a tested AR aging demo with two front doors sharing one calculation script.

## The one accounting task and the one concept it proves
- **Task:** month-end accounts receivable aging and exception review.
- **Concept:** AI helps build the process; tested deterministic code runs it behind a simple front door; a person validates and an independent reviewer signs off.

## Operator journey
input → checks → confirmation → execution → output → review → escalation

- The operator **can** stop at any point (cancel before running).
- The operator **must** stop when a check is red, when the total does not reconcile, when the file differs from one already used for the period, or when asked to change a rule.

## Package inventory
| Layer | File or link | Status |
|---|---|---|
| Understand | [README.md](./README.md) | Draft (in review) |
| Implement | [technical-appendix.md](./technical-appendix.md) | Draft (in review) |
| Experiment | `PythonMuse/pythonmuse-ar-operator-handoff-demo` | Tested locally; not yet published |
| Visuals | `visuals/` (6 article visuals, 6 slide variants, 2 social cards, 2 demo screenshots) | Built and checked |

## Inspiration and attribution
A conversation with JJ, who asked what happens after a workflow works and the team needs to use it. The roles idea comes from our own observations on how the profession is evolving.

## Cross-links
- Links to: From One-Time Analysis to Repeatable Workflows; When to Trust AI to Run Your Accounting Workflows; What the Heck Is a Script?; From AI Answers to Audit Trails; From Reports to Requests; Don't Just Prompt AI. ONBOARD It.; You Built an AI Workflow. What Happens If You Win the Lottery?; AI Helped Me Build It. AI Does Not Have to Run It.
- Linked from: From One-Time Analysis to Repeatable Workflows; From Reports to Requests; Don't Just Prompt AI. ONBOARD It.; You Built an AI Workflow. What Happens If You Win the Lottery?; AI Helped Me Build It. AI Does Not Have to Run It.
