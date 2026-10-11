# If the Data Can't Leave, Bring the Model In

*Exploring local LLMs for valuation, M&A, and other confidential financial work*

---

**PythonMuse LLC**
*Published October 2026*

![Where does the model run? From a consumer app to an air-gapped room: more control, and more responsibility, at every step](./visuals/41_hero.png)

---

I recently had lunch with a valuation specialist. Think M&A transactions, securities and debt valuations, private-company financials, cap tables, and plenty of information that definitely should not accidentally find its way onto the internet. When our conversation turned to AI, it ended fairly quickly. The work is too confidential, and Excel is still where much of it happens.

That is a perfectly reasonable concern. In valuation work, confidentiality is not a nice-to-have control. It is part of the product. But on the drive home, I kept wondering whether it should have been the end of the AI conversation or the beginning of a different one. Every hour a specialist spends locating, comparing, and reformatting information is an hour not spent doing what they were hired to do: analyze.

That is the tension: the data may be too valuable to expose, but the specialist's time is also too valuable to waste.

Maybe the question is not, "Can we use AI?" Maybe the better question is, "Where does the AI need to run?"

Local does not necessarily mean installing an AI model on every employee's laptop. It means running the model in an environment the company controls: perhaps a dedicated workstation, an internal server, a private data center, or another isolated environment. Employees can still use it through a normal browser or internal application, because the model can run centrally for many people. The trade-off is that local means more control and more responsibility. Someone has to manage the infrastructure, access, updates, and testing.

> **📎 Quick definition: what "local" means.** A **large language model (LLM)** is the engine behind tools like ChatGPT, Claude, Gemini, and Copilot. A **hosted "frontier" model** is one of the most capable of those engines, run by its provider on the provider's servers. You reach it over the internet, even on an enterprise plan. A **local (or on-premises) model** runs on hardware your company controls, from a single approved workstation to a server room. Most local models are **open-weight**: the trained model file is published so anyone can download and run it. "Open-weight" is not the same as "free to use for anything." Each one comes with its own license, which we'll get to.

And local is not the only secure option. Enterprise AI platforms can provide contractual, privacy, retention, and security protections that may be entirely appropriate. What matters is what your contracts, customers, [data classification](../06-safe-ai-data-workflows/README.md), and risk tolerance permit. That's the territory of [Your AI Workflow Was Approved. Did Anyone Read the Customer Contract?](../38-ai-workflow-customer-contract/README.md). If you're weighing a vendor's platform, [Buy the Platform. Own the Accounting Logic.](../39-buy-platform-own-accounting-logic/README.md) covers what its SOC report does and does not tell you.

If an approved enterprise platform meets those requirements, great. If it does not, that does not automatically mean "no AI." It may simply mean the architecture needs to change.

> **🛠️ Reminder — this is a framework.** The worked examples in this series, including the test kit this article points to, were built with the Claude extension in Visual Studio Code, because that is what our environment uses. Nothing in the method depends on that choice, and in this article, *where the model runs* is the whole point. Along that spectrum you might use:
>
> - a desktop app such as Ollama or LM Studio on an approved machine
> - a model server your company runs, shared through a browser
> - your company's own cloud account, through Azure OpenAI, Amazon Bedrock, or Google Cloud's Gemini Enterprise Agent Platform (formerly Vertex AI)
> - an enterprise subscription such as ChatGPT Enterprise, Gemini Enterprise, or Microsoft 365 Copilot
>
> The test is the same everywhere: same narrow task, same finished engagements, same pass bar. The tool changes; the test does not. This series teaches the framework, not the vendor.

---

## Start With the Work, Not the Model

This is where I think many AI conversations go backward.

We start with: *"What model should we buy?"*

Instead, start with: *"What work are our people spending time on that AI may be able to help with?"*

For a valuation firm, I would not begin by asking AI to perform a valuation. There are plenty of lower-risk opportunities first.

Consider the information surrounding a transaction or security valuation: financing agreements, debt documents, cap tables, term sheets, financial statements, historical workpapers, prior valuations, customer correspondence, and supporting market data.

An AI system could help identify what documents arrived and what is missing. It could extract agreed-upon terms. It could compare this quarter's materials with the prior quarter and identify what changed. It could find the source supporting an assumption. It could flag inconsistencies between a cap table and a transaction document.

It could also help an analyst locate similar historical work without spending twenty minutes opening folders named things like "FINAL," "FINAL2," and my personal favorite, "FINAL_USE_THIS_ONE."

None of this requires AI to replace valuation judgment. It requires AI to reduce the time professionals spend hunting for information.

> **📎 Quick definition: valuation terms in one breath.** For readers outside deal work:
>
> - **Term sheet:** the non-binding summary of a proposed investment.
> - **Financing agreement:** the signed, binding version. When the two disagree, the signed one wins.
> - **Cap table (capitalization table):** who owns how many shares of each class.
> - **Liquidation preference:** how much preferred investors get back before common shareholders see anything if the company is sold or wound down (for example, "1x" means their money back first).
> - **Participation:** whether they also share in what's left after that.
> - **Conversion terms:** how preferred shares turn into common shares.
> - **Distribution (liquidation) waterfall:** the calculation that runs the proceeds through all of those rules in order.
> - **Discounted cash flow (DCF)** and **Black-Scholes:** standard valuation models, one for a business's future cash flows and one for option-like securities.

This is not purely theoretical. IBM's [case study of Bay Point Advisors](https://www.ibm.com/case-studies/bay-point), an Atlanta-based investment firm focused on private debt, describes a platform called Atlas. It lets clients ask questions of secure data rooms in plain language and get citation-backed answers. It uses a retrieval design, and IBM says document-level permissions are enforced end to end. Bay Point built it on Azure OpenAI with IBM watsonx.data and DataStax rather than on a local model, which fits the point. The architecture has to match what the data allows, and AI is already reducing manual work around confidential private-market information.

---

## Start With What You Did, Not What You Will Do

Start with work you already completed successfully. Pick one narrow task from a prior engagement, such as a financing agreement from last year's closed transaction that a person processed by hand. Give it to the best model you are permitted to run (ask your AI what "best" means if you are not sure), and compare the output with what the valuation professional actually produced.

You do not need a server for this first check. For a small model, a decent laptop and a free desktop app that runs open-weight models locally are enough. [Ollama](https://ollama.com), which we first met in [Don't Trust the Model to Find What You Already Know Is There](../23-schema-driven-sanitization/README.md), and [LM Studio](https://lmstudio.ai) are two examples, not endorsements.

> **📎 Quick definition: what a "smaller model" means.** A model's size is usually quoted in **parameters**: the billions of numeric settings it learned during training. More parameters generally means more general knowledge, and more memory needed to run it. As a rough guide:
>
> - **About 7 to 14 billion parameters ("7B–14B")** runs on a laptop with 16 to 32 GB of memory. In Ollama's library, an 8B model is about a 5 GB download, and a 14B model is about 9 GB.
> - **Around 70 billion parameters** is a different machine entirely: roughly 64 GB or more of unified memory, or a GPU workstation. A 70B model is about a 43 GB download on its own.
>
> Size is not the same as the "fast, general-purpose, reasoning" capability levels in [Model Selection Is an Accounting Control](../36-model-selection-is-a-control/README.md), but the trade-off is the same one: you pay for capability you need, not capability you don't.

Three cautions before anything confidential goes near that laptop:

- **The laptop itself has to be approved to hold the test material.** Running the model locally does not make an unapproved device approved.
- **The app and the model have separate licenses and separate settings.** Ollama is MIT-licensed open source. LM Studio is proprietary software whose terms allow personal and internal business use. Check each app's update and telemetry settings separately from the model it runs.
- **Confirm it works with the network off.** If the test only passes while the Wi-Fi is on, you have learned something important about where your data goes.

Then check the model's own license, because a free model is not always licensed for business. Here's a concrete example. [Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B) is released under Apache 2.0, a standard permissive license. [Llama 3.3](https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct) uses Meta's own community license, which:

- incorporates an acceptable-use policy
- requires a "Built with Llama" notice if you distribute it
- requires very large companies to request a separate license

Neither is good or bad. They are different contracts, and someone should read the one you're relying on.

Start with perhaps 5 to 10 engagements on one task type. Before anything goes into production, widen the test to 50 to 100 historical engagements where the final answers and supporting evidence are already known. Those are practical sizes for building confidence, not a statistical sample.

There is one rule that matters more than the sample size: **do not tune your prompts on the same engagements you score.** Keep a practice set for adjusting the instructions and a separate scoring set for the verdict. You don't test a control with the same sample you used to design it, for the same reason. Tune long enough on the scoring set and you've measured how well the prompt fits those engagements, not how well the model does the work.

Historical does not mean nonconfidential. Use only material approved for the test, or redact or synthesize it where necessary.

If a local model falls short, compare it with an approved enterprise model using the same cleared test material. "Cleared" means cleared for *sending to that vendor*, not just cleared for internal use; those are two different approvals. If the enterprise model performs substantially better, you may have a model or hardware gap, and the answer may be a dedicated AI workstation rather than a server room. If neither performs acceptably, the workflow may simply not be ready for AI.

Most importantly, define "acceptable" before testing starts. The output may never match the manual work exactly, so the valuation specialist, not the person adjusting the prompts, sets the pass bar. That result is your baseline, and it tells you whether AI is an appropriate option at all.

> **Try it Monday:** Pick one closed engagement and one task. Give your co-pilot only the documents that engagement was authorized to use, and this prompt:
>
> *"Using only these documents, identify the liquidation preference, the conversion terms, and the valuation date. For each one, name the document and section it came from. If a value is not stated, answer 'insufficient evidence' instead of estimating. Do not calculate anything."*
>
> Then put the answers next to what your specialist actually concluded. The co-pilot retrieves; the specialist decides whether that was good enough.

---

## What to Test and How to Score It

What you are building is a task-specific benchmark: fixed inputs, known answers, a scoring rubric, and several models run on the same work. Public benchmarks measure general ability, and their questions can leak into a model's training data. Your completed engagements test your own work, and they are almost certainly not in any model's training data. That is a much better question than whatever this month's leaderboard says. [Model Selection Is an Accounting Control](../36-model-selection-is-a-control/README.md) explains why the leaderboard has the shelf life of a banana.

Create a set of tasks that resemble actual work:

- extract security terms
- compare periods
- identify missing documentation
- locate support for an assumption
- flag conflicting information
- answer questions with citations
- refuse to answer when the evidence is insufficient

Then test several models: one or two smaller local models, a larger local model, and, if the company already has an approved enterprise AI platform, that too.

Then compare what actually matters:

![A task-specific scorecard: six questions, a pass bar set before testing, and the same work run through every model](./visuals/41_scorecard.png)

- **Did it get the answer right?**
- **Did it cite the correct source?**
- **Did it invent anything?**
- **How often did an analyst have to correct it?**
- **How much time did it save?**
- **What did it cost to run?** For a local model, cost means hardware, power, and the staff time to maintain it, not a per-use fee. Compare it on that basis, or you'll be comparing apples to invoices.

Those numbers matter far more than whether somebody on the internet ranked Model A three points above Model B.

Your work. Your data. Your acceptance criteria.

---

## Try It With the Companion Repo

> **Run it for real:** The [Local LLM Test Kit](https://github.com/PythonMuse/pythonmuse-local-llm-test-kit) lets you practice this method before you use your own engagements. It includes:
>
> - fictional deal documents, split into a practice set and a scoring set
> - an answer key with citations
> - a scoring rubric with a pass bar
> - a small Python runner that sends each engagement to a model running locally through Ollama and scores the results
>
> The scoring set is deliberately booby-trapped with:
>
> - a term sheet that disagrees with the signed agreement
> - a valuation date that was never agreed
> - a cap table that doesn't tie
> - another client's document misfiled in the wrong folder
>
> No Ollama yet? It also replays two sets of example responses, so you can watch the scoring work first. One of them gets every answer right and still fails. You'll see why.

---

## Why a Smaller Model Might Be Enough

This is where the use case becomes interesting.

A local model may know less about the entire world than the strongest hosted frontier model. But perhaps it does not need to know the entire world.

If you are asking it:

*"Using only these seven authorized documents, identify the liquidation preference, conversion terms, valuation date, and outstanding shares, and show me where each answer came from,"*

then the most important information is already sitting inside the engagement folder.

Likewise, if the model is weaker at complex arithmetic, that matters much less if Excel or Python performs the calculation.

If it cannot hold an entire deal room in memory at once (its **context window**, the working memory problem from [Why Claude "Forgets"](../08-why-claude-forgets/README.md) and [The PDF Token Trap](../16-pdf-token-trap/README.md)), that matters less if the system retrieves only the documents relevant to the question.

> **📎 Quick definition: retrieval (RAG).** **Retrieval-augmented generation**, or RAG, means the AI looks things up in your approved folder first, then answers from what it found, ideally with a citation to the exact document. It's the difference between asking a colleague what they remember and asking them to pull the file. Bay Point's Atlas uses this design. Citations are what make the answer checkable, which is the whole argument of [From AI Answers to Audit Trails](../32-from-ai-answers-to-audit-trails/README.md).

If it occasionally tries to make things up (the problem usually called **hallucination**), require citations and explicitly allow it to respond:

*"I do not have enough evidence to answer this."*

In other words, instead of asking whether a smaller local model can compete with the smartest AI system on earth, ask whether it can reliably perform your defined workflow.

You do not need an AI that can debate philosophy, write a screenplay, and explain quantum mechanics if its actual job is to find the liquidation preference in seven documents.

Those are two very different tests.

---

## Let Excel Keep Doing What Excel Is Good At

There is another distinction I would make early in any valuation AI project.

Do not turn the LLM into the calculator simply because it can talk confidently about finance.

If the workflow requires a DCF, a Black-Scholes model, a distribution (liquidation) waterfall, a discount rate calculation, or another repeatable valuation model, keep those calculations in validated tools such as Excel or Python. Those tools are **deterministic**: the same inputs always produce the same output, the way a spreadsheet formula does. A model's answer can vary from run to run, which is exactly why [When the Invoice Starts Giving Orders](../37-when-the-invoice-gives-orders/README.md) keeps the two apart. If Python still sounds like a different department, [What the Heck Is a Script?](../25-what-the-heck-is-a-script/README.md) is the gentle introduction, and [The Workings Layer](../22-workings-layer-method/README.md) shows how it sits alongside the Excel files you can't change.

![AI retrieves and cites. Excel and Python calculate. The specialist judges.](./visuals/41_division_of_labor.png)

Let the AI help retrieve the inputs. Let validated code perform the calculation. Let AI help organize or explain the results. Then let the valuation specialist make the judgment and approve the conclusion.

That is a much cleaner division of responsibilities. AI handles language, retrieval, and organization. Validated tools handle the math. The valuation specialist handles judgment.

Excel does not need to be fired. It just may finally get a co-pilot.

---

## Local Does Not Mean Secure

This part cannot be skipped.

Putting a model on a server inside your building does not sprinkle cybersecurity fairy dust over it.

You still need authentication, permissions, least-privilege access, logging, data-retention rules, network controls, secure document handling, monitoring, and human oversight. [AI in Accounting Isn't Just About Efficiency — It's About Control](../13-zero-trust-ai-accounting/README.md) is the long version of that list. You also need model-version controls, because the model you tested in March is not automatically the model running in September. [Model Selection Is an Accounting Control](../36-model-selection-is-a-control/README.md) covers that.

[Prompt injection](../37-when-the-invoice-gives-orders/README.md) remains a problem. A document can still contain instructions, and a local model can still follow them.

So does poorly designed access.

For valuation firms, I think one of the most important risks may actually be far less exciting than anything appearing in cybersecurity headlines: **cross-client retrieval**.

Imagine years of completed deals sitting in one AI knowledge base. An analyst asks:

*"Have we valued another security with terms like this?"*

The AI finds a beautiful example.

Unfortunately, it belongs to another confidential client engagement.

The model did exactly what you asked. The system still failed.

![The permission filter has to sit before the model, not in the prompt](./visuals/41_cross_client.png)

Professional firms already have a name for the control that should have stopped it: an **ethical wall**, or information barrier, the arrangement that keeps one client's confidential information away from people who shouldn't see it. In an AI system, retrieval has to enforce that wall. Document-level permissions have to decide what the user may retrieve *before* the model receives anything. Once a document is in the model's context, it is too late to ask nicely.

A prompt saying "Please respect customer confidentiality" is not an access control.

If that worked, we could probably replace half of cybersecurity with very polite Post-it notes.

---

## ONBOARD It

Local AI does not require a new philosophy of AI governance. I would apply the same [ONBOARD checklist](../35-onboard-ai-workflows/README.md) I use for other AI workflows. Here it is, applied to a local model:

- **O — Organize the workspace and define AI's role.** Use an isolated, approved environment for the model and the test material. Define the role in one line: *retrieve and cite, never calculate.*
- **N — Name the assignment.** Pick one narrow task, such as extracting liquidation preference terms, not "help with valuations."
- **B — Brief AI on the business.** Give it the authorized documents for this engagement and nothing else. Spell out what "acceptable" means, as set by the specialist.
- **O — Obtain and approve a plan.** Get the test plan, the practice and scoring sets, and the pass bar approved before the first run, not after you see the results.
- **A — Allow controlled execution.** Use least-privilege access and permission-aware retrieval, so the ethical wall is enforced before the model sees anything. Calculations stay in Excel or Python.
- **R — Review the work and evidence.** Score the output against completed engagements, using the scorecard above. Check every citation, not just the answers.
- **D — Document what was learned.** Record the approved model and version, the failures you found, and what will trigger a retest, such as a new model version, a new task, or a new document type. [Model Selection Is an Accounting Control](../36-model-selection-is-a-control/README.md) explains why that record is a control, not paperwork.

Running a model locally gives you more control. It also gives you more responsibility. That trade-off needs to be intentional. When the pilot works and people start depending on it, [You Built an AI Workflow. What Happens If You Win the Lottery?](../40-builder-to-production/README.md) covers how it graduates into a production process someone else can run.

---

## Maybe the Conversation Should Not Have Ended

I understand why the AI conversation at lunch initially ended when confidential data came up.

That instinct is healthy. Protect the client first.

What I am questioning is what comes immediately after that.

Sensitive information may mean a consumer AI product is inappropriate. It may mean a particular hosted AI service is inappropriate. It may mean a customer contract requires the data to stay somewhere very specific.

But it does not automatically mean AI is inappropriate.

And it definitely does not mean Excel needs to carry the entire workload alone for another twenty years.

Local models have limitations. They may be less capable than the strongest hosted systems. They require engineering and maintenance. Hardware costs money. Someone has to manage them. And local should never be confused with secure.

Those are reasons to evaluate the technology carefully. They are not necessarily reasons to stop the conversation.

For organizations whose most valuable information cannot, or should not, travel freely to an outside AI platform, perhaps the better question is the one I left lunch thinking about:

**If the data cannot leave, what happens when we bring the model in?**

---

## Sources

- IBM — [Bay Point Advisors case study](https://www.ibm.com/case-studies/bay-point) (Atlas: Azure OpenAI, IBM watsonx.data and DataStax, retrieval-augmented generation, citation-backed answers, document-level permissions)
- Ollama — [Chat API documentation](https://docs.ollama.com/api/chat) and [MIT license](https://github.com/ollama/ollama/blob/main/LICENSE)
- Ollama library — [Qwen3](https://ollama.com/library/qwen3) and [Llama 3.3](https://ollama.com/library/llama3.3) download sizes
- LM Studio — [App Terms of Use](https://lmstudio.ai/app-terms)
- Qwen — [Qwen3-8B model card](https://huggingface.co/Qwen/Qwen3-8B) (Apache 2.0)
- Meta — [Llama 3.3 70B Instruct model card](https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct) (Llama 3.3 Community License)
- Google Cloud — [Introducing Gemini Enterprise Agent Platform](https://cloud.google.com/blog/products/ai-machine-learning/introducing-gemini-enterprise-agent-platform) (the evolution of Vertex AI, April 2026)
- PythonMuse — [Local LLM Test Kit companion repository](https://github.com/PythonMuse/pythonmuse-local-llm-test-kit)

Every link above was checked in October 2026. Download sizes, licenses, and product names change quickly, so re-check them before you rely on any of them.

---

**A note on how this article was made.** This article started with me. The lunch conversation with a valuation specialist, and the question I kept turning over on the drive home, are mine. This article was written in collaboration with Patrick Toohey. ChatGPT ([CONFIRM: exact ChatGPT model name]) helped us shape our notes into a first structured draft. Claude Sonnet and Claude Opus reviewed that draft and co-designed the practice test kit this article points to. Claude Code (Claude Opus 5.5) then built the final article, the visuals, the test kit's runner and tests, and the site wiring, working from my direction and feedback at each step. That review is where the ONBOARD section was corrected to match the seven steps from Article 35. It is also where every product, license, and case-study claim was checked against the vendor's own documentation, including one product name (Vertex AI) that had changed since the draft was written. I reviewed every output, pushed back on things I didn't like, and made all final content decisions. That process — bringing your own experience, using AI to build and iterate, and staying in the editorial seat throughout — is exactly what this series is about.

---

*Related: [How to Use AI in Accounting Without Sending the Wrong Data](../06-safe-ai-data-workflows/README.md) | [Don't Trust the Model to Find What You Already Know Is There](../23-schema-driven-sanitization/README.md) | [Don't Just Prompt AI. ONBOARD It.](../35-onboard-ai-workflows/README.md) | [Model Selection Is an Accounting Control](../36-model-selection-is-a-control/README.md) | [Your AI Workflow Was Approved. Did Anyone Read the Customer Contract?](../38-ai-workflow-customer-contract/README.md) | [Buy the Platform. Own the Accounting Logic.](../39-buy-platform-own-accounting-logic/README.md)*

*© 2026 PythonMuse LLC. Content licensed under [CC BY-NC-SA 4.0](../../LICENSE); code licensed under [MIT](../../LICENSE-CODE).*
