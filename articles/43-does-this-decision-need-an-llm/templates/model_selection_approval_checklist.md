# "Why This Model?" Approval Checklist

*A companion template for [Does This Decision Actually Need a Large Language Model?](../README.md)*

When an AI use case comes forward for approval, the usual questions are about security, privacy, accuracy, and the vendor. They matter. This checklist adds the one that comes first: **why is this the model being proposed?**

It complements the model-selection checklist in [Model Selection Is an Accounting Control](../../36-model-selection-is-a-control/README.md) and the onboarding steps in [Don't Just Prompt AI. ONBOARD It.](../../35-onboard-ai-workflows/README.md). Use it per step, not per process.

---

**Use case / step:** [ ]  **Proposed method:** [ ] Rule [ ] Decision model [ ] LLM [ ] Person [ ] Combination

**Proposed by:** [ ]  **Reviewed by:** [ ]  **Date:** [ ]

## 1. Does the step need a model at all?

- [ ] Is the rule already known? If it can be written as an `IF` statement, a lookup, or a match, it belongs in deterministic logic, not a model of any kind.
- [ ] If a model is proposed for a step with a known rule, the reason is documented: [ ]

## 2. What shape is the answer?

- [ ] Can the possible outcomes be listed in advance? List them: [ ]
- [ ] Is there an "other" or "cannot tell" option, so the model is never forced into a wrong box?
- [ ] Does the step need text to be **written** (a summary, a draft, an explanation), or only **chosen** from the list?
- [ ] Does it need extended reasoning across a long document, or a single bounded judgment?

## 3. Is the proposed model matched to that shape?

- [ ] **LLM proposed for a bounded choice** (e.g. "classify notes into six categories"): why is generation or extended reasoning needed? [ ]
- [ ] **Decision model proposed for open-ended analysis** (e.g. a contract-accounting conclusion): why is a bounded answer enough? [ ]
- [ ] Is the model the smallest one that performed acceptably on **our** work, **our** data, and **our** acceptance criteria, rather than the winner of a public benchmark?

## 4. Evidence and data

- [ ] What is the minimum evidence the model needs? Only those fields are sent.
- [ ] Where does the model run, what does the provider retain, and does that fit policy? (See [If the Data Can't Leave, Bring the Model In](../../41-bring-the-model-in/README.md).)
- [ ] Do any customer contracts restrict AI, machine learning, automated decision-making, or external processing for this data? (See [Your AI Workflow Was Approved. Did Anyone Read the Customer Contract?](../../38-ai-workflow-customer-contract/README.md).) Changing the model type does not change the answer.
- [ ] Could any input text be written to steer the answer (customer notes, employee explanations, vendor emails)? How is that contained?

## 5. Errors and uncertainty

- [ ] How will errors be measured? Pilot reference: [ ]
- [ ] What does a wrong answer cost? Minor / costly / control failure.
- [ ] What happens when confidence is low? Is it written down what the workflow does at each confidence level, who reviews, and what the model may never do?
- [ ] If the model returns no rationale, what evidence will the reviewer and the auditor rely on instead? (See [From AI Answers to Audit Trails](../../32-from-ai-answers-to-audit-trails/README.md).)
- [ ] Has cost been assessed as cost per acceptable decision, including review time and errors, not just model price? (See the [cost workbook](./cost_per_acceptable_decision.xlsx).)

## 6. Authority

- [ ] Which decisions stay with a person? [ ]
- [ ] The model's output is a classification or a recommendation, not an approval, a posting, or a payment.
- [ ] No decision about an individual (credit, employment, a customer's standing) rests on the model's score alone.

## Decision

[ ] Approved as proposed   [ ] Approved with a different method: [ ]   [ ] Not approved

**Reason:** [ ]

---

*PythonMuse LLC | www.pythonmuse.com. Educational purposes only; not professional advice. Content licensed under CC BY-NC-SA 4.0.*
