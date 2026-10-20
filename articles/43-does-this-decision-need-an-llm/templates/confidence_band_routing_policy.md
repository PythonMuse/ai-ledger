# Confidence Band Routing Policy

*A companion template for [Does This Decision Actually Need a Large Language Model?](../README.md)*

A decision model's probability is only useful if the workflow already knows what to do with it. This template records, for one decision, what each confidence band is allowed to do, who owns it, and how you will know the bands are still right.

> **Set the bands from your own labeled results.** The cut-offs below are deliberately left blank. Do not copy numbers from an article, a vendor example, or another team. Run a pilot first (see the [Decision Model Pilot Worksheet](./decision_model_pilot_worksheet.xlsx)), look at where the wrong answers cluster, and weigh what a wrong answer costs in each band.

---

**Decision:** [e.g. AR collection-note reason code]  **Model and version:** [ ]  **Provider / environment:** [ ]

**Allowed choices (defined before testing):** [ ]  **Includes "other" / "cannot tell"?** [ ] Yes [ ] No

**Policy owner:** [ ]  **Approved by:** [ ]  **Date:** [ ]  **Pilot reference:** [ ]

---

## 1. The bands

| Band | Probability range | What the workflow may do | What it may **not** do | Who reviews | Evidence kept |
|---|---|---|---|---|---|
| **Auto-route** | ≥ [ ] | Send the item to the matching queue | Approve, post, pay, write off, or contact the customer | Sample of [ ]% reviewed [weekly / monthly] | Item ID, choice, probability, model version, timestamp |
| **Confirm** | [ ] to [ ] | Suggest a queue; a person confirms with one click | Move the item without confirmation | [role] | Above, plus who confirmed and any change |
| **Escalate** | < [ ] | Send to a person (or a stronger method) with no suggestion pre-selected | Route automatically | [role] | Above, plus the final answer and reason |
| **No probability** | Blank (refusal, error, or a fallback that returned none) | Treat as Escalate | Treat a missing number as zero risk | [role] | Above, plus why no probability came back |

**Never automated, whatever the probability:** [e.g. anything over $[ ], any credit memo, any decision about an individual employee or customer's creditworthiness]

## 2. Before go-live

- [ ] Allowed choices written down before testing, including an "other" or "cannot tell" option.
- [ ] Pilot run on at least [ ] historical items with known outcomes (synthetic or approved data only).
- [ ] Accuracy recorded **by band**, not just overall.
- [ ] Every wrong answer in the Auto-route band reviewed. Cut-off raised until what remains is acceptable.
- [ ] Error severity assessed: annoying, costly, or control failure.
- [ ] Question and option wording frozen (results can change when wording or option order changes).
- [ ] Inputs reviewed for untrusted text that could steer the answer (customer notes, employee explanations). See [When the Invoice Starts Giving Orders](../../37-when-the-invoice-gives-orders/README.md).
- [ ] Data sent to the model limited to the minimum evidence the decision needs.

## 3. Ongoing monitoring

| Check | How often | Owner | Trigger for review |
|---|---|---|---|
| Sample of Auto-route items re-checked by a person | [ ] | [ ] | Any control-failure error |
| Share of items in each band | [ ] | [ ] | Escalations up or down by more than [ ]% |
| Accuracy by band on newly labeled items | [ ] | [ ] | Any band below its pilot accuracy |
| Model, version, or provider change | On every change | [ ] | Re-run the pilot before relying on the old bands |
| Question wording or allowed choices change | On every change | [ ] | Re-run the pilot |

## 4. Sign-off

| Role | Name | Date |
|---|---|---|
| Process owner | | |
| Reviewer / control owner | | |

---

*PythonMuse LLC | www.pythonmuse.com. Educational purposes only; not professional advice. Content licensed under CC BY-NC-SA 4.0.*
