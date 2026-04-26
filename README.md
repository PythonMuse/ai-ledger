# ai-ledger

Practical Python, AI, and automation for accounting and finance teams. Built for professionals who want to work faster and go deeper — without becoming developers.

Each article includes the full write-up, sample data, and the code to reproduce every chart.

---

## Articles

| # | Title | Topics |
|---|-------|--------|
| 00 | [True or False: AI Will Replace My Job?](articles/00-ai-will-not-replace-your-job/) | Career perspective, Python fundamentals, durable skills, why Python Muse exists |
| 00.5 | [Where to Start If You're Ready to Work With AI](articles/00.5-where-to-start-with-ai/) | Getting started, VS Code, Python setup, Microsoft Copilot, mindset shift |
| 01 | [Your AI Co-Pilot for Accounting](articles/01-ai-copilot-for-accounting/) | Margin analysis, vendor cost inflation, salesperson performance, revenue concentration |
| 02 | [Ways to Use Claude: Choosing the Right Interface](articles/02-ways-to-use-claude/) | Claude.ai, API, Claude Code, interface comparison, getting started |
| 03 | [Getting the Right Tools Installed: A Safe Starting Point for Accounting Teams](articles/03-getting-the-right-tools-installed/) | IT approvals, secure adoption, VS Code and Python setup framing, low-risk pilot use cases |
| 04 | [AI in Accounting Is Not the Wild West Anymore](articles/04-ai-governance-in-accounting/) | AI governance, COSO framework, PCAOB updates, Big Four guidance, audit-ready workflows |
| 05 | [Reproducible Accounting](articles/05-reproducible-accounting/) | Accounting as code, audit evidence, version control, reproducible financial reporting |
| 06 | [How to Use AI in Accounting Without Sending the Wrong Data](articles/06-safe-ai-data-workflows/) | Data masking, local vs cloud processing, safe AI workflows, QuickBooks demo, validation hooks |
| 07 | [AI Governance for Controllers](articles/07-ai-governance-for-controllers/) | COSO framework, controller governance, use case inventory, AI skills, agents, VS Code |
| 08 | [Why Claude "Forgets" -- And How to Fix It](articles/08-why-claude-forgets/) | Context window, external memory, project files, plan.md, status_update.md, CLAUDE.md |
| 09 | [How Accountants Learn AI](articles/09-how-accountants-learn-ai/) | Excel-to-AI learning path, 13-skill framework, Markdown, Python, Git, hooks, canary, project hygiene |
| 10 | [AI in Accounting: Real Use Cases -- and How to Structure Them](articles/10-ai-use-cases-and-structure/) | Reconciliations, variance analysis, ad hoc analysis, 3-tier classification, exploratory vs repeatable vs audit-ready |
| 11 | [From One-Time Analysis to Repeatable Workflows](articles/11-one-time-to-repeatable-workflows/) | 9-step workflow pattern, data masking, headers-only, hooks, plan approval, SKILL documentation |
| 12 | [When to Trust AI to Run Your Accounting Workflows](articles/12-audit-ready-ai-workflows/) | Audit-ready framework, COSO mapping, governance controls, logged execution, canary checks |
| 13 | [AI in Accounting Isn't Just About Efficiency -- It's About Control](articles/13-zero-trust-ai-accounting/) | Zero Trust for AI, OWASP LLM risks, data controls, trust but verify, four-level framework, checklist |
| 14 | [Stop Using One AI Like It Is Excel](articles/14-ai-team-for-accountants/) | Claude vs ChatGPT vs Copilot, model orchestration, skills, GitHub as distribution layer, folder structure as prompt |
| 15 | ["AI Can't Work With Our Excel Files"... or Can It?](articles/15-ai-and-excel-files/) | Excel instruction layer, SKILL for spreadsheets, three-tier data approach, train once reuse forever |
| 16 | [The PDF Token Trap](articles/16-pdf-token-trap/) | PDF-to-Markdown workflow, token efficiency, data masking, reusable Skills, convert once reuse forever |
| 17 | [The Power of Skills and Agents: How Accountants Actually Use AI](articles/17-skills-and-agents-for-accountants/) | Skills, agents, workflow design, internal controls, living documentation |
| 17b | [Your First CLAUDE.md: How Accountants Define the Agent](articles/17b-your-first-claude-md/) | CLAUDE.md structure, governance documentation, accounting-specific rules, workflow kit |
| 18 | [Scheduled Workflows for Accounting Teams](articles/18-scheduled-workflows/) | Scheduled tasks, cron, automation, recurring workflows |
| 19 | [Multi-Agent Orchestration for Accountants](articles/19-multi-agent-orchestration/) | Multi-agent, orchestration, parallel workflows, accounting automation |
| 20 | [Version Control for Accountants](articles/20-version-control-for-accountants/) | Git, version control, audit trail, reproducibility |
| 21 | [The 3 Mindsets of AI Adoption in Accounting](articles/21-three-mindsets-of-ai-adoption/) | Mindset, change management, Builder/Stabilizer/Protector, AI adoption |
| 22 | [The Workings Layer: Fitting AI Into the Files You Can't Change](articles/22-workings-layer-method/) | Workings layer, folder structure, CLAUDE.md placement, legacy files, audit-ready |
| 23 | [Don't Trust the Model to Find What You Already Know Is There](articles/23-schema-driven-sanitization/) | Schema-driven sanitization, PII detection, data privacy, accounting data workflows, Privacy Filter |

---

## How to Use This Repo

Each article folder is self-contained:

```
articles/
└── 01-ai-copilot-for-accounting/
    ├── README.md            ← the article
    ├── visuals/             ← charts referenced in the article
    ├── data/                ← sample CSV files
    └── generate_visuals.py  ← script to reproduce all charts
```

To reproduce the analysis in any article:
1. Download the `data/` folder
2. Open it in VS Code with Claude Code installed
3. Follow the prompts in the article

---

## Who This Is For

Contributions are welcome from:
- Accountants and controllers
- Finance analysts
- Auditors
- Data professionals supporting finance teams
- Developers building finance tools

Whether you write code or review accounting logic, there's a way to help.

---

## Current Contribution Needs

- Bank reconciliation example with sample data
- AR aging notebook
- AP exception testing example
- Safe, anonymized finance datasets
- Reviewers for accounting accuracy
- Beginner-friendly documentation improvements

See the full list at [community/ideas-wanted.md](community/ideas-wanted.md).

---

## How to Contribute

Open an issue, comment on an existing request, or submit a pull request.

See [CONTRIBUTING.md](CONTRIBUTING.md) for details and [community/roadmap.md](community/roadmap.md) for where the project is headed.

---

## License

This project uses a dual license:

- **Written content** (articles, templates, worksheets, examples, documentation) is licensed under [CC BY-NC-SA 4.0](LICENSE) — you may share and adapt with attribution, for non-commercial purposes, under the same license.
- **Python source code** (`.py` files) is licensed under the [MIT License](LICENSE-CODE) — free to use, modify, and distribute.

See [LICENSE](LICENSE) and [LICENSE-CODE](LICENSE-CODE) for full details.

---

## ⚠️ Disclaimer

This repository is provided for educational purposes only.

- Not accounting, audit, tax, or legal advice  
- No guarantee of accuracy or completeness  
- Use at your own risk  

---

### AI Usage Notice
This repository may include AI-assisted workflows and scripts.

Users must:
- Validate all outputs independently  
- Ensure data privacy and compliance  
- Avoid using sensitive or confidential data without proper controls  

PythonMuse LLC is not responsible for any outcomes resulting from use of this code.

---

*By Svetlana Toohey*
