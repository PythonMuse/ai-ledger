# "Control or Polite Request?" Boundary Audit

*A companion template for [AI Helped Me Build It. AI Does Not Have to Run It.](../README.md)*

*"It says right there in the agent file: do not touch the payroll folder."*

That sentence is an instruction. The model is asked to follow it. A hard boundary is enforced by the harness itself. This audit sorts every boundary you *think* you have into one of two columns.

---

## How to run the audit

1. Open every skill file, agent file, and project instruction file (`CLAUDE.md`, `AGENTS.md`, Copilot instructions, and so on) the workflow uses.
2. List every sentence that sets a boundary: "never," "do not," "only," "must not," "always ask before."
3. For each one, find out whether something **outside the model** enforces it: a permission rule, a tool allowlist, folder access, a sandbox, an approval prompt.
4. If nothing does, it is **instruction-only**. Decide whether that is acceptable for this boundary. If it is not, name the fix.

**Rule of thumb:** the more it would hurt if the boundary failed (restricted data, posting, payments, external sharing), the less acceptable "instruction-only" becomes.

---

## Audit table

| # | Boundary as written | Where it is written | Enforced by the harness? | How (setting / mechanism) | Acceptable as is? | Fix, owner, due date |
|---|---|---|---|---|---|---|
| 1 | | | Harness-enforced / Instruction-only | | Yes / No | |
| 2 | | | | | | |
| 3 | | | | | | |
| 4 | | | | | | |
| 5 | | | | | | |

---

## Example rows

These examples show the idea. Setting names change often, so check your provider's current documentation before relying on any of them.

| # | Boundary as written | Where it is written | Enforced by the harness? | How (setting / mechanism) | Acceptable as is? | Fix |
|---|---|---|---|---|---|---|
| A | "Do not read or edit anything in /payroll." | Agent file (Claude Code) | **Instruction-only** (as written) | None. The sentence asks. | No: payroll is restricted data. | Add `"Read(./payroll/**)"` and `"Edit(./payroll/**)"` to `permissions.deny` in `.claude/settings.json`. Note the scope: deny rules cover Claude's file tools and recognized shell commands, not a script that opens files itself. For OS-level enforcement, enable the Claude Code sandbox. |
| B | "This reviewer agent only reads files." | Subagent file (Claude Code) | **Harness-enforced** | `tools: Read, Glob, Grep` in the subagent's frontmatter is an allowlist. Tools not listed are not available. | Yes | None. (If the `tools:` line is omitted, the subagent inherits every available tool, so check it is there.) |
| C | "Never write outside the project folder." | `AGENTS.md` (OpenAI Codex) | **Harness-enforced**, if configured | `sandbox_mode = "workspace-write"` in Codex `config.toml` (OS-enforced); `approval_policy = "on-request"` makes Codex ask before stepping outside it. | Yes, once confirmed in config | Confirm the setting is actually in the team's config, not just someone's laptop. |
| D | "Always ask me before running terminal commands." | Copilot instructions file (GitHub Copilot agent mode in VS Code) | **Harness-enforced** by default, **but can be switched off** | Terminal commands and tool calls need approval under the default permission level, unless auto-approved (for example via `chat.tools.terminal.autoApprove`) or the session uses "Allow all" / Autopilot. Turn off tools you don't need in the tools picker. | Only if auto-approve is not enabled | Check user and workspace settings for auto-approve rules; document which commands, if any, are approved. |
| E | "Don't change the formulas on the Calc tab." | Note in cell A1 (Excel, no harness) | **Instruction-only** | None. | Depends on the workbook | Protect the sheet or workbook, and restrict edit access to the folder. |

---

## Sign-off

| Reviewed by | Date | Boundaries reviewed | Instruction-only boundaries accepted (with reason) | Fixes raised |
|---|---|---|---|---|
| | | | | |

---

*PythonMuse LLC | www.pythonmuse.com. Educational purposes only; not professional advice. Content licensed under CC BY-NC-SA 4.0.*
