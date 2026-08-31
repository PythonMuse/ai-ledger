# Model Selection Decision Record

**Workflow:** [Name of the workflow, e.g. Monthly expense variance commentary]
**Owner:** [Name / Role]
**Decision date:** [YYYY-MM-DD]
**Next re-validation:** [YYYY-MM-DD, or "after any model tier or version change"]

Companion to [Model Selection Is an Accounting Control](../articles/36-model-selection-is-a-control/README.md). Fill this in once per workflow, not once per prompt. Its purpose is to make the capability decision reviewable — so that six months from now someone can see what level of AI capability was chosen for this work, why, and when that choice should be revisited.

---

## Pre-Flight: The Seven Questions

Work through these before assigning the task. If you cannot answer one of them, that is the finding — not a reason to skip it.

- [ ] **1. What exactly is the task?** Is the model being asked to extract, transform, draft, analyze, or support judgment?
- [ ] **2. Is the information permitted in this environment?** Data governance is resolved *before* capability is considered.
- [ ] **3. How much reasoning does the task require?** Routine work may prioritize speed; complex work may need depth.
- [ ] **4. What happens if the output is wrong?** Financial, operational, reporting, or compliance consequence.
- [ ] **5. How easily can the result be verified?** Apply the verification-cost test: delegate when the output can be verified reliably, at a cost proportionate to the value and risk of the task. Cheap to verify is not the same as safe to accept.
- [ ] **6. Does the model cost match the value of the task?** Matters most for recurring or high-volume workflows.
- [ ] **7. When should the workflow escalate?** Defined in advance — to a stronger capability level, and to a human reviewer.

---

## The Decision

| Design element | Documented decision |
|---|---|
| **Task** | [What the AI is being asked to produce] |
| **Task type** | [Extract / transform / draft / analyze / support judgment] |
| **Permission determination** | [What data is permitted here, and what is excluded. Reference your AI permissions framework.] |
| **Capability level** | [Fast / general-purpose / reasoning] |
| **Why this level** | [One or two sentences. This is the field a reviewer will actually read.] |
| **Environment** | [Approved cloud / enterprise-controlled / private / local] |
| **Inputs** | [What the model receives, and who validated it] |
| **Escalation trigger — capability** | [The specific condition that moves this to a stronger level] |
| **Escalation trigger — human** | [The specific condition that moves this to a named reviewer] |
| **Reviewer** | [Name / Role who must approve before the output is used] |
| **Evidence retained** | [Source file, instructions, output, validation evidence, and the model that ran] |

---

## Consequence and Verification

Complexity and consequence are different axes. Higher complexity may require a stronger model; higher consequence requires stronger controls. Record both, because the second one is the answer a bigger model cannot buy.

| Assessment | Response |
|---|---|
| **Consequence if wrong** | [Low / moderate / high — and what specifically is affected] |
| **Controls added for consequence** | [Validation steps, structured outputs, approval gates, read-only sources, logging] |
| **Verification method** | [How a reviewer confirms the output is right, not just plausible] |
| **Verification effort** | [Cheap / moderate / expensive relative to doing the work manually] |

---

## Model Change Control

A model change is a change to this control. Record what actually ran, not only what the procedure specifies.

- [ ] The model and version that ran is captured in the evidence for each execution
- [ ] The version is pinned where the platform allows it
- [ ] The workflow is re-validated after any tier or version change
- [ ] Evidence preserves the specific run — inputs, outputs, validation — not just the model name
- [ ] Someone is responsible for noticing when the platform changes models on its own

| Date | Change observed | Re-validated by | Outcome |
|---|---|---|---|
| [YYYY-MM-DD] | [e.g. tier renamed, version retired, admin enabled a new family, Auto routing changed] | [Name] | [Approved / rejected / controls updated] |

---

## Review Notes

[Anything a future reviewer needs to know: rejected alternatives, known limitations, exceptions encountered in practice, or conditions under which this decision should be revisited early.]

---

*Template from [PythonMuse LLC — The AI Ledger](https://github.com/PythonMuse/ai-ledger). Educational purposes only; not professional advice.*
