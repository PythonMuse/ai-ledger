# AI Governance in Accounting: The Technical Appendix

*The technical appendix for _AI in Accounting Is Not the Wild West Anymore_: the standards detail, the newer AICPA and Big Four publications, recommended training, and every source with its date and authority level*

---

**PythonMuse LLC**
*Published November 2026*

---

This page is for readers who want the citation-level detail behind the article. [The article](./README.md) stands on its own; nothing here changes its argument. Think of this as the workpapers behind the memo.

One distinction runs through everything below, so it is worth stating up front:

- **Authoritative** means a requirement you, or your auditor, must follow: GAAP, PCAOB and AICPA auditing standards, the AICPA Code of Professional Conduct for CPAs.
- **Nonauthoritative** means guidance, practice aids, templates and professional insights. It is useful and often persuasive, but it is not a requirement.
- **Proposed** means an exposure draft. It is not effective, and the final version may change.

---

## 1. The FASB and ASU 2025-06

As of November 2026, we have not found a FASB (Financial Accounting Standards Board) Accounting Standards Update (ASU) that specifically addresses AI-generated financial information. We reviewed the ASUs issued in 2026 that we could access (ASU 2026-01 through 2026-03), and none of them concerns AI. We could not access the FASB's full online index during this review, so treat this as "none found," not "none exists."

The closest the FASB has come is in the Basis for Conclusions of ASU 2025-06, *Intangibles -- Goodwill and Other -- Internal-Use Software (Subtopic 350-40): Targeted Improvements to the Accounting for Internal-Use Software* (September 2025). In paragraphs BC66 and BC67, the Board notes that some comment letter respondents asked whether the existing software cost guidance applies to training an AI model and to data conversion costs.

The Board considered the question and "decided not to provide specific guidance for training an AI model and data conversion costs." It viewed that clarification as beyond the scope of this targeted update.

That is a narrow point. It does not mean AI-related costs sit outside GAAP, and the ASU does not create any new AI governance requirement. It simply means the FASB did not use this update to answer the AI question.

**Who the standards apply to.** GAAP applies to the financial statements regardless of how a number was produced. Auditing standards govern the auditors, not the company. PCAOB standards apply to audits of public companies (and broker-dealers registered with the SEC). AICPA auditing standards apply to audits of private companies and other non-issuers. Management remains responsible for the financial reporting and the internal controls behind it under either regime.

---

## 2. The PCAOB Technology-Assisted Analysis Amendments

The PCAOB (Public Company Accounting Oversight Board) amended AS 1105, *Audit Evidence*, and AS 2301, *The Auditor's Responses to the Risks of Material Misstatement*. The Board adopted the amendments on June 12, 2024 (PCAOB Release No. 2024-007), and the SEC approved them on August 20, 2024.

They are effective for audits of financial statements for fiscal years beginning on or after December 15, 2025.

**They do not require full-population testing.** The adopting release describes the requirements as principles-based and "intended to be applied to all means of selecting items for a test of details (e.g., selecting all items, selecting specific items, and audit sampling)." Traditional audit sampling remains available. Auditors must still design procedures appropriate to the assessed risks and obtain sufficient appropriate audit evidence.

**They are not generative AI standards.** The release says the amendments focus on technology-assisted analysis, "not specific matters relating to other technology applications used in audits (e.g., blockchain or artificial intelligence)."

**What they do sharpen** is attention to the information itself. When the auditor uses information the company provides in electronic form, the amendments require the auditor to evaluate whether that information is reliable for the purposes of the audit. That means understanding where it came from and how the company received, maintained and processed it, and testing whether it was modified, or testing the controls over it. A PCAOB policy statement (September 2025) and staff guidance (October 2025) address how that evaluation is applied in practice.

For accounting professionals, the practical translation is simple. A spreadsheet or a screenshot is not automatically bad evidence, and a polished data extract is not automatically good evidence. What matters is whether you can show where the information came from and that nobody (and nothing) changed it along the way. That is relevance, reliability, completeness and accuracy, judged against the purpose the information is used for.

---

## 3. The AICPA Practice Aid and the SOC 2 Proposal

### The October 2026 practice aid

*Artificial Intelligence (AI) Considerations for Financial Statement Auditors* (resource dated October 12, 2026; announced October 13, 2026) is a **nonauthoritative** practice aid. It looks at AI from both sides of the audit.

On one side, it considers how a company's use of AI in financial reporting or controls can affect the audit. That includes how it may affect the auditor's risk assessment, the quality of the data behind it, and the controls around it. As the AICPA announcement notes, data quality "can significantly affect the reliability of an AI system."

On the other side, it considers how audit firms use AI tools themselves. That includes establishing quality management policies and procedures, the competence of the engagement team, and "appropriate supervision, review and audit conclusions," with "continued attention to professional judgment and professional skepticism."

None of those ideas is new. The practice aid does not create new requirements; it shows how the responsibilities auditors already have apply when AI is in the picture. As the AICPA's chief auditor put it in the Journal of Accountancy, "the auditor remains responsible for the audit and the audit opinion." The AICPA has said future updates will cover assessing the risk of material misstatement and evaluating audit evidence when entities use AI.

The practice aid itself is available to AICPA members. The descriptions above are drawn from the AICPA's public resource page and announcement.

### The proposed SOC 2 Trust Services Criteria update

On October 28, 2026, the AICPA released an exposure draft of updated SOC 2 Trust Services Criteria. The proposal includes expanded considerations for emerging technologies, including AI, with new points of focus covering AI governance, model monitoring, prompt manipulation and data poisoning.

**This is a proposal, not an effective requirement.** Comments are due January 15, 2027. If it is approved, the AICPA has indicated it would apply to engagements beginning on or after December 31, 2027, with early adoption permitted. The final version may change.

Why a finance team should care: if you rely on SOC 2 reports from vendors whose services touch your financial data, future reports may say more about how those vendors govern AI.

---

## 4. Big Four Publications in More Detail

These are professional insights and recommendations, not accounting or auditing standards. Each recommendation below is attributed to the publication that makes it.

**Deloitte, [Putting new COSO GenAI internal controls guidance into practice](https://www.deloitte.com/us/en/services/audit-assurance/blogs/accounting-finance/coso-ai-framework-internal-controls-for-generative-ai.html) (June 2026).**
- Build cross-functional GenAI governance with clear roles, accountability and escalation.
- Keep a GenAI use-case inventory, and link financially relevant use cases to processes, assertions and key controls.
- Use a use-case-based approach to decide how much human involvement each use case needs.

**KPMG, [COSO releases roadmap on internal control over generative AI](https://kpmg.com/us/en/frv/reference-library/2026/coso-releases-roadmap-internal-control-over-generative-ai.html) (April 2026).**
- Summarizes COSO's guidance and its relevance to internal control over financial reporting.

**EY, [AI audit readiness for financial reporting](https://www.ey.com/en_us/insights/assurance/ai-audit-readiness-for-financial-reporting) (September 2026).**
- Design for traceability and reproducibility.
- Document data lineage for each in-scope AI use case.
- Define human review procedures, especially when AI-enabled controls are first implemented, and retain evidence of management review and challenge.
- Establish governance for changes to AI systems, such as model updates, retraining, and prompt and parameter changes.

**PwC, [Financial reporting oversight](https://www.pwc.com/us/en/services/governance-insights-center/library/financial-reporting-oversight.html).**
- Written for audit committees overseeing financial reporting, including where AI is entering the process.

---

## 5. Recommended Training

Several professional programs connect AI governance with the internal control frameworks already used in financial reporting. Course formats, schedules and availability change, so check each provider's site for current offerings.

**[Auditing Artificial Intelligence (AI): A Hands-On Course for Internal Auditors](https://www.theiia.org/en/products/learning-solutions/course/auditing-artificial-intelligence-ai-a-hands-on-course-for-internal-auditors/)**
Institute of Internal Auditors (IIA)
Focus: AI governance frameworks, risk evaluation, control testing

**Essentials for AI Auditing**
Institute of Internal Auditors (IIA)
Focus: AI risk taxonomy and governance structures

**[ChatGPT & Internal Audit: Governance of the Utilization of Generative AI](https://www.theiia.org/en/products/learning-solutions/on-demand/chatgpt--internal-audit-governance-of-the-utilization-of-generative-ai/)**
Institute of Internal Auditors (IIA)
Focus: controls around LLM usage and AI documentation

**[COSO Internal Control Certificate Program](https://www.theiia.org/en/products/learning-solutions/course/coso-internal-control-certificate/)**
COSO (offered through the IIA and other professional bodies)
Focus: applying the COSO framework to governance and monitoring

---

## Sources

All sources were retrieved on November 18, 2026.

| Source | Date | What kind of guidance it is |
| --- | --- | --- |
| [FASB, Accounting Standards Updates Issued](https://www.fasb.org/standards/accounting-standard-updates) | Ongoing | Authoritative (GAAP) |
| [FASB, ASU 2025-06, including Basis for Conclusions BC66--BC67](https://storage.fasb.org/ASU%202025-06.pdf) | September 2025 | Authoritative (the Basis for Conclusions explains the Board's reasoning and is not itself part of the Codification) |
| [PCAOB, amendments to AS 1105 and AS 2301](https://pcaobus.org/oversight/standards/standard-setting-research-rulemaking-related-activities/amendments-related-to-certain-aspects-of-designing-and-performing-audit-procedures-that-involve-technology-assisted-data-analysis) | Adopted June 12, 2024; effective for fiscal years beginning on or after December 15, 2025 | Authoritative (PCAOB auditing standards) |
| [PCAOB, implementation resources](https://pcaobus.org/oversight/standards/implementation-resources-PCAOB-standards-rules/amendments-related-to-aspects-of-designing-and-performing-audit-procedures-that-involve-technology-assisted-analysis-of-information-in-electronic-form) | Updated October 1, 2025 | Policy statement and staff guidance |
| [AICPA Code of Professional Conduct](https://pub.aicpa.org/codeofconduct/Ethics.aspx) | Ongoing | Authoritative for AICPA members |
| [COSO, Achieving Effective Internal Control Over Generative AI (GenAI)](https://www.coso.org/generative-ai) | February 23, 2026 | Nonauthoritative guidance applying the 2013 Internal Control -- Integrated Framework |
| [AICPA, Small Firm Generative AI Policy Template](https://on-demand.aicpalearningcenter.org/resources/download/aicpa-small-firm-generative-artificial-intelligence-ai-policy-template) | April 29, 2026 | Nonauthoritative template |
| [AICPA, TQA Section 9561](https://www.aicpa-cima.com/resources/download/tqa-section-9561-soc-examinations-effect-of-the-service-organizations-use-of-ai-on-soc1-and-soc2-examinations) | September 11, 2026 | Technical questions and answers (nonauthoritative) |
| [AICPA, AI Considerations for Financial Statement Auditors](https://www.aicpa-cima.com/resources/article/explore-new-aicpa-guidance-on-artificial-intelligence-ai-and-the-financial-statement-audit) | October 12, 2026 | Nonauthoritative practice aid |
| [AICPA, announcement of the practice aid](https://www.aicpa-cima.com/news/article/aicpa-releases-guidance-to-help-auditors-address-the-use-of-ai-in-financial-reporting-and-auditing) | October 13, 2026 | News release |
| [Journal of Accountancy, AI and the audit](https://www.journalofaccountancy.com/news/2026/oct/ai-and-the-audit-aicpa-publishes-practice-aid-to-assist-auditors.html) | October 2026 | News coverage |
| [AICPA, proposed update of SOC 2 Trust Services Criteria](https://www.aicpa-cima.com/news/article/aicpa-proposes-update-of-soc-2-r-trust-services-criteria-to-enhance-the-relevance-usability-and-value-of-cpas-reports) | October 28, 2026 | Proposal (exposure draft); comments due January 15, 2027 |
| Deloitte, KPMG, EY and PwC publications (linked in section 4) | April--September 2026 | Professional insights, not standards |

---

*Back to the article: [AI in Accounting Is Not the Wild West Anymore](./README.md)*

*Related: [AI Governance for Controllers](../07-ai-governance-for-controllers/) | [Reproducible Accounting](../05-reproducible-accounting/) | [When to Trust AI to Run Your Accounting Workflows](../12-audit-ready-ai-workflows/) | [Let AI Do the Research. You Set the Boundaries.](../44-ai-research-boundaries/README.md)*

*© 2026 PythonMuse LLC. Content licensed under [CC BY-NC-SA 4.0](../../LICENSE); code licensed under [MIT](../../LICENSE-CODE).*
