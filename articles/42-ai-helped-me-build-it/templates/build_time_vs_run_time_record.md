# Build-Time vs. Run-Time AI Record

*A companion template for [AI Helped Me Build It. AI Does Not Have to Run It.](../README.md)*

Use one record per workflow. The point is to make AI's role a **design decision someone approved**, not a default nobody noticed. It takes about fifteen minutes, and it answers the first question a reviewer will ask: "Where exactly is the AI in this?"

Copy this file, fill in the brackets, and keep it with the workflow (next to its README or Human Instructions).

---

## 1. The workflow

| Field | Entry |
|---|---|
| Workflow name | [e.g. Monthly duplicate-payment test] |
| Business purpose | [one sentence] |
| Owner | [name / role] |
| Backup operator | [name / role] |
| Where it lives | [folder or repository path] |
| Version / commit in use | [e.g. v1.2 / a1b2c3d] |

## 2. Build time: what AI did while the workflow was designed

Tick everything that applies and add a note.

| AI helped to... | Yes / No | Notes |
|---|---|---|
| Explain the existing manual procedure | | |
| Draft the script, query, or formula | | |
| Explain the code line by line | | |
| Generate mock or synthetic test data | | |
| Suggest edge cases and test cases | | |
| Troubleshoot errors | | |
| Draft documentation | | |

**Tool and model used at build time:** [e.g. Claude Code (model name), OpenAI Codex, GitHub Copilot agent mode, Copilot in Excel]

## 3. What data did the model see during the build?

| Data type | Seen by the model? | Approved by |
|---|---|---|
| Synthetic / mock data only | [Yes / No] | |
| Anonymized or sanitized production data | [Yes / No] | |
| Production data | [Yes / No] | |
| Column names and structure only (no values) | [Yes / No] | |

If anything other than synthetic data was used, note the approval and the data classification it fell under.

## 4. Run time: does AI have a role when the workflow runs?

Pick one.

- [ ] **No run-time AI.** The approved script, query, or formula does all recurring work. AI is out of the production path.
- [ ] **Run-time AI for specific steps only.** List them below.
- [ ] **Run-time AI coordinates the workflow** (for example, an agent calling approved deterministic tools). List the tools and boundaries below.

| Step | What AI does at run time | Why AI (not a rule) | Data it sees | Output reviewed by |
|---|---|---|---|---|
| [e.g. Draft variance commentary] | [Drafts questions for the account owner] | [Language interpretation] | [Variance summary only] | [Senior accountant] |

## 5. Boundaries enforced at run time

| Boundary | How it is enforced | Harness-enforced or instruction-only? |
|---|---|---|
| [e.g. Cannot read payroll folder] | [Claude Code `permissions.deny` rule] | [Harness-enforced] |

See the [Boundary Audit](./boundary_audit.md) if you are not sure which column a boundary belongs in.

## 6. Approval of the design

| Field | Entry |
|---|---|
| Design approved by | [name / role] |
| Date | [date] |
| Next review | [date, or "on any change to AI's role"] |
| Linked release checklist | [link to completed Deterministic Script Release Checklist] |

---

*PythonMuse LLC | www.pythonmuse.com. Educational purposes only; not professional advice. Content licensed under CC BY-NC-SA 4.0.*
