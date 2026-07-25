# From Clicking Reports to Talking with the ERP

*What Model Context Protocol could mean for accounting*

---

**PythonMuse LLC**
*Published July 2026*

![From ERP Menus to AI Agents](./visuals/34_hero.png)

---

For decades, becoming proficient in an enterprise resource planning system meant learning where everything lived.

Which menu contains the report? Which filters should be selected? Is the useful version under "Financial," "Custom," or a submenu last updated by someone who left the company in 2019?

Experienced accountants became valuable not only because they understood accounting, but also because they knew how to persuade the ERP to surrender the required information. That is a real skill. It is also not the skill anyone puts on a resume.

That interface is beginning to change.

Artificial intelligence is moving beyond answering questions from uploaded files. It is increasingly being connected to live business systems, where it can retrieve data, run approved tools, analyze results, and potentially initiate actions.

One technology helping make this possible is the **Model Context Protocol**, commonly known as MCP.

For accountants, the significance of MCP is not the protocol itself. Most accountants do not need another technical acronym competing for space with GAAP, EBITDA, ASC, ERP, KPI, and the other abbreviations already occupying our working memory.

The more important development is the change in how accountants may interact with financial systems.

Instead of finding the correct report, applying the correct filters, exporting the results, and repeating the process in another system, an accountant may increasingly describe the desired outcome:

> "Prepare consolidated revenue and gross margin by entity, translate the foreign subsidiary into U.S. dollars, identify intercompany differences, and explain material variances from budget."

The system could then determine which approved tools and data sources are required to complete the request.

The accountant would spend less time navigating software and more time defining the accounting question, reviewing exceptions, and validating the answer.

That sounds promising. It also raises several important questions.

What exactly does MCP do? How is it different from an API? How could it support multi-ERP accounting workflows? What new risks does it create? Most importantly, what remains the responsibility of the accountant?

## From System Navigation to Business Intent

Traditional ERP systems require users to translate a business question into a sequence of system actions.

Consider a relatively simple request:

> "Which customers experienced a gross-margin decline of more than five percentage points this quarter?"

To answer it, an accountant may need to:

1. Identify the correct sales or profitability report.
2. Determine whether the report includes revenue and cost information at the customer level.
3. Apply the correct period and entity filters.
4. Export the results.
5. Retrieve the prior-period data.
6. Combine the files.
7. Calculate the change in gross margin.
8. Investigate unusual results.
9. Prepare commentary for management.

In a conversational environment, the accountant begins with the business question instead.

The AI assistant may identify the required data, retrieve it through approved tools, perform the calculation, and present the customers meeting the requested criteria.

This does not mean the AI suddenly understands the company's accounting better than the controller. It means the interface is shifting from **navigation** to **intent**.

The user explains what is needed. The system helps determine where to find it.

## What MCP Is—and What It Is Not

MCP is an open standard designed to connect AI applications with external data sources, tools, and systems. It gives an AI client a standardized way to discover what tools are available, understand what those tools do, and call them using defined inputs.

An API, by comparison, is usually a system-specific interface through which one application requests data or performs an operation in another application.

MCP does not necessarily replace APIs. In many implementations, an MCP server sits above existing APIs, databases, reports, and business logic. It translates those capabilities into tools that an AI assistant can understand and use.

A simplified architecture might look like this:

```text
Accountant
    ↓
AI assistant or governed agent
    ↓
MCP server
    ↓
ERP APIs, reports, databases and business logic
    ↓
Financial and operational systems
```

The MCP server might expose tools such as:

```text
get_trial_balance(entity, period)
get_open_receivables(as_of_date)
run_saved_report(report_id, filters)
retrieve_vendor_invoice(invoice_number)
prepare_journal_entry(parameters)
```

Notice what is missing from that list: nothing that lets the AI post an entry, delete a vendor, or email the auditor a confession on your behalf.

The AI assistant does not receive unrestricted access to the entire ERP simply because MCP is present. The organization determines which tools are available, what permissions apply, which actions are read-only, and when approval is required.

MCP is therefore better understood as a **connection and tool-use layer**.

It is not an accounting policy.

It is not a consolidation methodology.

It is not a substitute for access controls.

And it is certainly not an accounting degree delivered over Wi-Fi.

## A Fictional Multi-ERP Consolidation Example

Consider a fictional organization with two entities:

- A U.S. entity using **QuickBooks Online**
- A Canadian entity using **Sage Intacct**

The following example is intentionally generic and does not represent the systems, structure, or processes of any specific organization.

Management asks the accounting team to prepare the monthly consolidated financial review.

The review must include:

- Revenue and gross margin by entity
- Translation of the Canadian results into U.S. dollars
- Intercompany eliminations
- Comparison with budget
- Identification of material variances
- Draft management commentary
- A list of exceptions requiring review

Today, the process may depend on separate exports, mapping files, exchange-rate schedules, and a consolidation workbook held together by formulas, institutional knowledge, and a healthy amount of optimism.

An MCP-enabled workflow could operate differently.

The accountant might request:

> "Prepare the June consolidated financial review using the approved June closing rates. Identify unmapped accounts, unresolved intercompany differences, and variances exceeding the established materiality threshold."

The AI assistant could then call several approved tools:

```text
get_qbo_trial_balance(period="2026-06")
get_intacct_trial_balance(period="2026-06")
get_approved_fx_rates(period="2026-06")
get_chart_of_accounts_mapping()
get_intercompany_mapping()
get_budget(period="2026-06")
run_consolidation(period="2026-06")
run_validation(period="2026-06")
```

Behind the scenes, the workflow would:

1. Retrieve the U.S. trial balance.
2. Retrieve the Canadian trial balance.
3. Confirm that both periods are complete.
4. Apply the approved chart-of-accounts mapping.
5. Translate the Canadian entity using the approved exchange rates.
6. Identify and eliminate intercompany balances.
7. Compare actual results with budget.
8. Flag unmapped accounts and out-of-balance conditions.
9. Prepare draft variance commentary.
10. Preserve an audit log of the tools, parameters, files, and rates used.

The resulting package might include:

- Consolidated financial statements
- Entity-level supporting schedules
- Foreign-exchange calculations
- Intercompany exceptions
- Unmapped accounts
- Budget variances
- Source totals
- Retrieval timestamps
- Draft commentary
- Reviewer checklist

The accountant would still review the results before they are distributed.

That distinction matters.

MCP may help retrieve and coordinate the information, but the accounting conclusions still depend on controlled mappings, approved policies, deterministic calculations, and professional review.

## Why Direct ERP Access Does Not Automatically Create Accounting Intelligence

One of the easiest mistakes to make is assuming that access to better data automatically produces better accounting.

An AI assistant may successfully retrieve a trial balance while still misunderstanding:

- Whether a balance is presented as a debit or credit
- Whether the period is open or closed
- Whether the report includes posted or unposted transactions
- Whether the amount is in local or reporting currency
- Whether the request is for an individual entity or a consolidated group
- Whether a statistical account should be included
- Whether management reporting differs from GAAP reporting
- Whether an adjustment was recorded in the ledger or only in the consolidation workbook
- Whether an intercompany difference represents timing, foreign exchange, or an actual error

These issues are not technological trivia. They determine whether the result is correct.

The AI therefore needs more than access to the ERP. It needs governed accounting context.

That context may include:

- Chart-of-accounts mappings
- Department and entity hierarchies
- Accounting policies
- Foreign-exchange rules
- Materiality thresholds
- Intercompany relationships
- Report definitions
- Period-close status
- Approval requirements
- Validation procedures

MCP can help the AI reach the information. Accountants must still define what the information means.

## Try It Yourself: A Companion Repository

A practical demonstration does not need to connect to a live ERP.

In fact, the first version probably should not.

A safe educational repository could simulate the entire workflow using fictional CSV files. One data source represents QuickBooks Online, while another represents Sage Intacct.

The objective is not to build a production-ready consolidation platform. It is to show accountants how an AI assistant can select controlled tools, retrieve data from multiple sources, apply transparent accounting logic, and produce reviewable outputs.

![MCP Consolidation Architecture](./visuals/34_architecture.png)

The companion repository is structured as follows:

```text
accounting-mcp-demo/
│
├── README.md
├── AGENTS.md
│
├── data/
│   ├── qbo_trial_balance.csv
│   ├── intacct_trial_balance.csv
│   ├── budget.csv
│   └── exchange_rates.csv
│
├── mappings/
│   ├── chart_of_accounts.yml
│   ├── departments.yml
│   └── intercompany.yml
│
├── mcp_server/
│   ├── server.py
│   └── tools.py
│
├── accounting/
│   ├── normalize.py
│   ├── translate_fx.py
│   ├── eliminate_intercompany.py
│   └── validate.py
│
└── tests/
    └── test_consolidation.py
```

The demonstration exposes only a small number of tools:

```text
get_trial_balance(entity, period)
get_budget(period)
get_exchange_rate(currency, period)
get_account_mapping(source_system)
get_intercompany_balances(period)
run_consolidation(period)
run_validation(period)
```

Every tool is read-only against local sample files. Nothing in the demo can post, delete, or transmit anything — on purpose.

The user could then ask:

> "Consolidate both entities for June 2026 and show me any accounts that were not mapped."

The AI would decide which tools to call, but Python performs the accounting calculations.

This separation is important.

Natural language can determine what the user is asking. Deterministic code should perform calculations that must be repeatable.

The AI may choose the recipe. It should not quietly reinvent the laws of arithmetic because it was feeling creative that afternoon.

> **🛠️ Reminder — this is a framework.** The companion repository was built and tested using Claude in VS Code, through the GitHub Copilot extension — that's the daily setup behind the code and the screenshots you'd see if I recorded them. But MCP itself is an open, provider-neutral protocol, not a Claude feature. The same server, tools, and sample data connect just as well to Claude Desktop or the Claude Code CLI, and the same *pattern* — a governed tool layer between an AI client and your ERP — applies whether your organization standardizes on ChatGPT with Projects, Gemini with workspace integrations, or Microsoft Copilot Studio's own connector model. This series teaches the framework, not the vendor.

> **Clone and run it yourself:** The full sample data, MCP server, and deterministic accounting logic described above live in the companion repository, `accounting-mcp-demo`. Clone it, run the tests, then connect it to your own MCP-compatible AI client and ask it to consolidate the fictional QuickBooks Online and Sage Intacct entities end to end: **[github.com/PythonMuse/accounting-mcp-demo](https://github.com/PythonMuse/accounting-mcp-demo)**

## Opportunities Beyond Financial Reporting

Multi-ERP consolidation is only one possible application.

MCP-enabled accounting tools could support a wide range of workflows.

### Accounts receivable

An accountant could request:

> "Show customers with balances more than 45 days past due, no payment activity in the last 30 days, and open disputes exceeding $10,000."

The workflow could combine receivable balances, customer activity, dispute records, and contact information.

### Accounts payable

An agent could compare vendor invoices with purchase orders and receiving records, identify differences, and prepare exceptions for review.

### Close management

A close agent could monitor whether reconciliations are complete, supporting schedules are attached, required entries are posted, and unusual balances remain unresolved.

### Audit support

An agent could retrieve approved supporting documents, trace samples to source transactions, and assemble an evidence package without granting the auditor unrestricted access to the ERP.

### Variance analysis

The assistant could retrieve actual, budget, forecast, and prior-period data from different sources, apply materiality thresholds, and draft commentary that distinguishes facts from assumptions.

### Controlled transaction preparation

More advanced tools could prepare—but not automatically post—journal entries, customer orders, vendor bills, or reclassification requests.

The safest progression is generally:

![Retrieve to Execute Maturity Stages](./visuals/34_maturity_stages.png)

```text
Retrieve
    ↓
Analyze
    ↓
Recommend
    ↓
Prepare
    ↓
Approve
    ↓
Execute
```

Organizations should resist the temptation to skip directly from "retrieve" to "execute" merely because the demo looked impressive.

Accounting history contains enough surprises already.

## Benefits, Risks, and Suggested Controls

The potential benefits of MCP are meaningful, but each benefit introduces a corresponding governance question.

| Area | Potential benefit | Risk or challenge | Suggested control |
|---|---|---|---|
| Data access | Reduces repeated exports and uploads | Excessive access to confidential financial information | Role-based access and least-privilege permissions |
| Natural-language reporting | Reduces dependence on ERP navigation knowledge | Ambiguous requests may produce the wrong scope | Require entity, period, currency, basis, and report definition |
| Multi-ERP analysis | Creates one interface across several systems | Different charts of accounts and data structures | Controlled mappings and a governed semantic layer |
| Live information | Provides more current analysis | Data may change after the analysis is completed | Record retrieval time and period-close status |
| Consolidation | Reduces repetitive collection and normalization | Incorrect FX or elimination logic | Deterministic calculations and reconciliation controls |
| AI tool selection | Allows the system to locate relevant data | The model may select the wrong report or tool | Approved tool lists, routing rules, and testing |
| Write capability | Can prepare or execute transactions | Incorrect or unauthorized changes | Read-only by default; preview, approval, and logging |
| Auditability | Can preserve detailed records of tool calls | Logs may show what occurred without explaining why | Retain inputs, outputs, parameters, rationale, and approvals |
| Productivity | Reduces manual work | Users may overtrust polished answers | Mandatory validation and reviewer sign-off |
| Reusability | The same tools can support multiple AI clients | Broader attack surface and vendor dependency | Approved clients, authentication, monitoring, and change control |
| Data quality | Can expose issues across systems more quickly | Poor source data still produces poor results | Completeness checks, source-total reconciliations, and exception reports |
| Workflow automation | Enables recurring analysis | Broken logic may repeat at scale | Version control, testing, monitoring, and rollback procedures |

MCP does not eliminate controls. It changes where the controls must operate.

Traditional controls often focus on who can open a module, run a report, or post a transaction.

MCP-era controls must also address:

- Which AI client may connect
- Which tools the client may discover
- Which data each tool may retrieve
- Which parameters are required
- Whether an action is read-only or transactional
- Whether approval is required
- How actions are logged
- How tool changes are tested
- How results are validated

This is not a reason for accountants to step away from MCP.

It is a reason for accountants to participate early.

> **Related read:** The habits that turn a fluent AI answer into a reviewable one — tying output back to source, separating facts from assumptions, building an evidence trail — are covered in depth in [From AI Answers to Audit Trails: How Accountants Can Validate AI Output](../32-from-ai-answers-to-audit-trails/README.md). Zero Trust thinking for exactly this kind of live-system access is covered in [AI in Accounting Isn't Just About Efficiency — It's About Control](../13-zero-trust-ai-accounting/README.md).

## The Emerging AI ERP Ecosystem

The market is beginning to develop across several distinct layers.

Some companies are rebuilding the ERP around AI. Others are adding conversational access and agents to established systems. A third group is helping organizations implement, extend, and govern these capabilities. Somewhere, a conference keynote is already calling this "the agentic ERP stack." We will just call it what it is: software that is getting easier to talk to.

### Rillet: AI Built Into the Ledger

Rillet represents the AI-native ERP approach. Its Aura AI offering includes accounting agents embedded within the general ledger, natural-language access to financial information, and tools for building repeatable workflows with execution visibility and audit trails.

This model is interesting because AI is not merely placed beside the accounting system. It operates within the accounting platform itself.

Potential use cases include:

- General-ledger questions in natural language
- Flux analysis
- Accrual preparation
- Reconciliation assistance
- Recurring finance workflows
- Real-time accounting analysis

### 10X ERP: Ask, Act, and Automate

10X ERP demonstrates a broader conversational model in which users can ask questions, run reports, enter transactions, reconcile vendor invoices, and create scheduled agents from an AI interface.

Its system describes write actions that are previewed for approval, logged with before-and-after information, and designed to be reversible. It also exposes an MCP server so compatible external AI clients — including Claude and ChatGPT — can interact with the ERP directly.

Examples include:

- Asking for the top customers by revenue
- Turning a customer purchase order into a sales order
- Reconciling a vendor invoice with purchase-order receipts
- Updating records in batches
- Scheduling a recurring receivables report
- Accessing ERP data from an external AI client
- Reviewing and reversing AI-initiated changes

This provides a useful preview of a future in which the ERP interface is not limited to screens and menus. The conversation itself becomes part of the operating environment.

### Oracle NetSuite: Extending an Existing ERP Through MCP

NetSuite represents another important direction: extending a widely used ERP rather than replacing it.

Oracle's NetSuite AI Connector Service, delivered through the NetSuite MCP Standard Tools SuiteApp, uses MCP to allow compatible AI clients to interact with NetSuite data and functionality. Its standard MCP tools can work with records, reports, saved searches, and SuiteQL queries — governed by NetSuite's own role-based security — while organizations can also build custom tools.

This could allow a user to request an existing report, provide filters conversationally, retrieve the results, and continue analyzing the underlying records without first locating every function in the user interface.

For accountants who have spent years memorizing the location of saved searches, this may be both exciting and slightly unfair to all the knowledge they accumulated.

### Microsoft Dynamics 365: Connecting Agents to Data and Business Logic

Microsoft's Dynamics 365 ERP MCP server, currently rolling out for Finance and Operations, lets agents perform data operations and access finance and operations business logic directly. Microsoft has also signaled additional MCP-based capabilities for analyzing Business Performance Analytics data through natural language, though — as with any fast-moving product area — the exact tooling and naming are still evolving. Check Microsoft's own documentation for the current state before you build anything against it.

This distinction is important.

One set of tools can help agents analyze information. Another can allow them to interact with operational functionality.

Together, these capabilities point toward workflows in which an agent can identify an issue, investigate the underlying activity, and prepare a proposed response.

The governance requirements become more significant as the agent moves from answering a question to changing a record.

### The Implementation and Enablement Layer: Not Every Vendor Wants to Replace Your ERP

Most organizations will not replace their ERP simply because a newer system offers impressive AI features.

ERP replacements are expensive, disruptive, and rarely approved because someone returned from a conference excited about a chatbot.

A second category of vendor has grown up around that reality: firms that help you get AI working inside the ERP you already have, instead of selling you a new one.

**Mirage Consulting**, a specialist ERP implementation and staffing firm, is one example of that role — the kind of partner organizations already call on for NetSuite and other ERP work, increasingly asked to help design AI agents that operate inside existing environments rather than around them. **magentIQ**, a hybrid AI-and-human workforce provider for finance and accounting teams, is another — its stated position is that finance does not need more software, it needs AI agents layered onto the systems already in place, working alongside the team rather than replacing the stack.

Neither approach is right or wrong. Together they are a reminder that "AI for your ERP" is not one product category. It is a spectrum — from AI-native platforms rebuilding the ledger from scratch, to conversational layers bolted onto an existing system, to partners who show up and help you wire agents into whatever you already run.

That model matters because most companies need more than technology. They need help identifying:

- Which processes should be improved
- Which workflows are suitable for agents
- Where the necessary data resides
- How permissions should be configured
- Which actions require approval
- How the workflow will be monitored
- Who will maintain it after implementation
- How the finance team will be trained

The implementation partner may therefore evolve from configuring ERP screens and workflows to designing the governed relationship among the ERP, AI agents, employees, and internal controls.

## What the Future Accounting Technology Stack May Look Like

The future is unlikely to consist of one all-knowing AI system replacing every financial application.

A more realistic architecture will include several layers:

```text
Accountant
    ↓
AI assistant or accounting agent
    ↓
Accounting instructions and approval rules
    ↓
MCP tools
    ↓
ERP APIs, reports and business logic
    ↓
QuickBooks Online | Sage Intacct | NetSuite | Dynamics 365 | Other systems
```

The progression may occur in three stages.

### Stage One: Conversational Retrieval

The accountant asks:

> "Show overdue invoices greater than $25,000."

The agent retrieves and summarizes the information.

### Stage Two: Governed Analysis

The accountant asks:

> "Compare gross margin by department with budget, identify material changes, and retrieve the transactions contributing to the largest variance."

The agent combines multiple tools and produces a review package.

### Stage Three: Controlled Action

The accountant asks:

> "Prepare the proposed accrual, attach the supporting calculation, and route it for approval."

The agent prepares the transaction but follows established approval and posting controls.

Not every organization will reach the third stage, and not every accounting process should.

Some workflows may remain read-only. Others may permit preparation but not posting. A smaller number may eventually support controlled autonomous execution.

The appropriate level should depend on risk, materiality, data quality, system maturity, and the organization's ability to monitor the results.

> **Related read:** For a closer look at how orchestrating several specialized agents — rather than one long chat — keeps a workflow like multi-ERP consolidation reviewable, see [When One Agent Is Not Enough: Orchestrating AI Workflows in Accounting](../19-multi-agent-orchestration/README.md).

## The Accountant's Role in an MCP-Enabled Environment

As the technology becomes more capable, the accountant's responsibility does not disappear. It becomes more explicit.

Accountants will need to define:

- The authoritative source for each data element
- The meaning of financial metrics
- The relationships among entities and accounts
- The required accounting policies
- The appropriate materiality thresholds
- The approved calculations
- The necessary validations
- The permitted actions
- The required evidence
- The approval and escalation process

This work is closely aligned with the profession's existing strengths.

Accountants already understand reconciliations, access controls, segregation of duties, approvals, evidence, documentation, and review.

The challenge is to apply those principles before an AI agent begins interacting with live financial systems — not after the first unexpectedly enthusiastic journal entry appears in the ledger.

## Conclusion

MCP may fundamentally change the way accountants interact with financial systems.

Instead of learning where every report lives, accountants may increasingly describe the information or outcome they need. AI assistants could then retrieve data, coordinate tools across several systems, perform approved analyses, and prepare results for review.

That shift could reduce repetitive work, limit manual exports, and make complex multi-system analysis more accessible.

It also introduces meaningful risks.

An agent with access to live ERP data can retrieve the wrong information more efficiently than a human. An agent with write access can convert a misunderstanding into a transaction. A poorly governed workflow can repeat an error consistently, on schedule, and with excellent formatting.

The opportunity is therefore not simply to connect AI to accounting systems.

The opportunity is to connect them responsibly.

MCP is the bridge. APIs, reports, databases, and business logic remain underneath it. AI agents may travel across it. Accountants must determine where the bridge leads, who is allowed to cross, and whether anything should be posted when it reaches the other side.

For decades, accountants learned how to navigate software.

In the years ahead, software may increasingly learn how to navigate for accountants.

Our responsibility will no longer be limited to remembering which report to run.

It will be ensuring that the question is properly defined, the source is authoritative, the calculation is controlled, the action is approved, and the answer remains worthy of the trust placed in the accounting profession.

---

**A note on how this article was made.** This article started with me. The question — what MCP could mean for accountants who have spent careers learning where every report lives — and the fictional consolidation walkthrough are mine. ChatGPT (5.5, "Sol") helped me shape my notes and research into a structured first draft. Claude Sonnet and Claude Opus then reviewed that draft for accuracy — catching a few claims that needed real sourcing before publication — and helped co-build the companion demo repository so you can run this instead of just reading about it. GitHub Copilot (Claude Sonnet 5) built the final article, the companion visuals, and the remaining repo scaffolding — working from my direction and feedback at each step. I reviewed every output, pushed back on things I didn't like, and made all final content decisions. That process — bringing your own experience, using AI to build and iterate, and staying in the editorial seat throughout — is exactly what this series is about.

---

*Related: [When One Agent Is Not Enough: Orchestrating AI Workflows in Accounting](../19-multi-agent-orchestration/README.md) | [AI in Accounting Isn't Just About Efficiency — It's About Control](../13-zero-trust-ai-accounting/README.md) | [From AI Answers to Audit Trails: How Accountants Can Validate AI Output](../32-from-ai-answers-to-audit-trails/README.md) | [AI Governance for Controllers](../07-ai-governance-for-controllers/README.md)*
