# Lab Brief: Your AI Workflow Is Running. Who Is Watching It?

**PythonMuse Lab · Article 47** · Status: In review

## The one-sentence problem
An AI-assisted accounting workflow reports "Completed successfully," but nobody can say what it processed, what went wrong along the way, who reviewed it, or where the evidence is, because nobody decided what the workflow should record or who should watch it.

## Audience
Mixed: accounting and finance professionals who rely on, own, or review AI-assisted workflows (operators, reviewers, controllers), plus builders who want to add logs and telemetry. No coding knowledge is assumed for the article.

## Reader payoff
- **Immediate benefit:** the reader can explain logs, metrics, and traces in accounting terms; say why Git records the version but not the run; sort workflow evidence into three layers (change control, execution, accounting control); and describe what turns a metric into a monitoring control (owner, expectation, threshold, review, escalation, evidence).
- **Key takeaway:** a successful run is a claim, not evidence. If AI is performing accounting work, we should be able to answer the same questions we ask of any other accounting process: what happened, what went wrong, who reviewed it, and where is the evidence?

## Learning outcomes
After this Lab, the reader can:
1. Tell the difference between recording activity and monitoring it, and explain why native AI tracing shows execution but does not prove the accounting is right.
2. Ask where monitoring data goes and what it contains, before anyone turns on content capture.
3. Optionally, run a small fictional bank reconciliation that writes an activity log, run metrics, a `workflow_failed` event, and an OpenTelemetry trace, and try five experiments on it.

## The one accounting task and the one concept it proves
- **Task:** a daily bank reconciliation, fictional data, six transactions.
- **Concept:** Git tells you which version was meant to run, telemetry tells you what ran, and accounting control evidence tells you whether the required controls operated. You need all three, connected by a run ID.

## Operator journey
input → checks → confirmation → execution → output → review → escalation

- The run records its version, tolerance, and expected count at the start, and its counts and status at the end.
- A person **must** stop when the completeness check fails (`incomplete`), when a run is `failed`, when an expected run is missing altogether, or when the exception rate moves outside the threshold the control owner set.

## Package inventory
| Layer | File or link | Status |
|---|---|---|
| Understand | [README.md](./README.md) | Draft (in review) |
| Implement | [technical-appendix.md](./technical-appendix.md), with [code/bank_rec.py](./code/bank_rec.py) and [code/otel_demo.py](./code/otel_demo.py) | Tested (both scripts run on Windows/PowerShell, Python 3.14, OpenTelemetry SDK 1.45.2; outputs match hand-calculated figures) |
| Experiment | Not in scope for this Lab. The appendix code is small enough to run inline, so there is no companion repository. | n/a |
| Visuals | `visuals/` (6 article visuals, 6 slide variants, 2 social cards) | Built and checked |

## Inspiration and attribution
Assumption (to confirm with the user): a question left open while writing about data lineage (once you know where the data came from, how do you know what the AI workflow did with it while it ran?), sharpened by Anthropic's October 2026 announcement of OpenTelemetry tracing on the Claude Platform, which featured an accounting software company. FloQast is quoted only from that public announcement; no individual is named.

## Cross-links
- Links to: How to Use AI in Accounting Without Sending the Wrong Data; When to Trust AI to Run Your Accounting Workflows; Git Explained Using Accounting Terms; Pull Requests Are Internal Controls; From AI Answers to Audit Trails; Model Selection Is an Accounting Control; You Built an AI Workflow. What Happens If You Win the Lottery?; AI Helped Me Build It. AI Does Not Have to Run It.; I Built the Workflow. Now How Does My Team Use It?
- Linked from: From AI Answers to Audit Trails; You Built an AI Workflow. What Happens If You Win the Lottery?; AI Helped Me Build It. AI Does Not Have to Run It.; I Built the Workflow. Now How Does My Team Use It?
- Deferred: the data lineage article (unmerged at the time of writing). See `backlog.md`.
