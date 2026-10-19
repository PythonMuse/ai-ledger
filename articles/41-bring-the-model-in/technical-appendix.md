# If the Data Can't Leave: The Technical Appendix

*Under the hood of Article 41: where the model can run, how to choose and test one, the companion test kit, and the controls you still need*

---

**PythonMuse LLC**
*Published October 2026*

---

This page is for readers who saw a use for local AI in their own work and want to try it. [The article](./README.md) stands on its own; nothing here changes its argument. Think of this as the workpapers behind the memo.

The sections follow the order you would work in: decide where the model runs, run a first test, build a proper benchmark, then put the controls around it. Deal vocabulary is at the end if you need it.

---

## 1. Where the Model Can Run

"Local" is one end of a spectrum. Along it you might use:

- a desktop app such as Ollama or LM Studio on an approved machine
- a model server your company runs, shared through a browser
- your company's own cloud account, through Azure OpenAI or Amazon Bedrock
- an enterprise subscription such as ChatGPT Enterprise, Gemini Enterprise, or Microsoft 365 Copilot

These options are not interchangeable. Each comes with its own contract, access rules, and settings to review. Start from what your data classification policy and client contracts allow, then choose where the model runs, not the other way around.

The test is the same everywhere: same narrow task, same finished engagements, same pass bar. The worked examples in this series, including the test kit, were built with the Claude extension in Visual Studio Code, but nothing in the method depends on that choice.

---

## 2. Running Your First Local Test

### What a "smaller model" means

A model's size is quoted in **parameters**: the billions of numeric settings it learned during training. More parameters generally means more general knowledge, and more memory needed to run it. As a rough guide:

- **7 to 14 billion parameters ("7B–14B")** runs on a laptop with 16 to 32 GB of memory. In Ollama's library, an 8B model is about a 5 GB download, and a 14B model is about 9 GB.
- **Around 70 billion parameters** needs a different machine: roughly 64 GB or more of unified memory, or a GPU workstation. A 70B model is about a 43 GB download.

The trade-off is the same one described in [Model Selection Is an Accounting Control](../36-model-selection-is-a-control/README.md): pay for the capability you need, not the capability you don't.

You do not need a server for a first check. A decent laptop and a free desktop app are enough. [Ollama](https://ollama.com), which we first met in [Don't Trust the Model to Find What You Already Know Is There](../23-schema-driven-sanitization/README.md), and [LM Studio](https://lmstudio.ai) are two examples, not endorsements.

### Three cautions before anything confidential goes near that laptop

- **The laptop has to be approved to hold the test material.** Running the model locally does not make an unapproved device approved.
- **The app and the model have separate licenses and settings.** Ollama is MIT-licensed open source. LM Studio is proprietary software whose terms allow personal and internal business use. Check each app's update and telemetry settings, not just the model's.
- **Confirm it works with the network off.** If the test only passes while the Wi-Fi is on, you have learned something important about where your data goes.

### Read the model's license

A free model is not always licensed for business. [Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B) uses Apache 2.0, a standard permissive license. [Llama 3.3](https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct) uses Meta's own community license, which includes an acceptable-use policy, requires a "Built with Llama" notice if you distribute it, and requires very large companies to request a separate license.

Neither is good or bad. They are different contracts, and someone should read the one you're relying on.

---

## 3. Building Your Own Benchmark

A benchmark is a fixed exam: the same documents, the same questions, and the same grading rules for every model you test. Public benchmarks measure general ability, and their questions can leak into a model's training data. Your completed engagements test your own work, and they are almost certainly not in any model's training data. [Model Selection Is an Accounting Control](../36-model-selection-is-a-control/README.md) explains why the public leaderboard has the shelf life of a banana.

### Pick tasks that look like real work

- extract security terms
- compare periods
- identify missing documentation
- locate support for an assumption
- flag conflicting information
- answer questions with citations
- refuse to answer when the evidence is insufficient

### Keep practice and scoring separate

This rule matters more than sample size: **do not tune your prompts on the same engagements you score.** Keep a practice set for adjusting the instructions and a separate scoring set for the verdict. You don't test a control with the same sample you used to design it. Tune on the scoring set and you've measured how well the prompt fits those engagements, not how well the model does the work.

### How many engagements

Start with 5 to 10 engagements on one task type. Before anything goes into production, widen the test to 50 to 100 historical engagements where the answers and supporting evidence are already known. Those are practical sizes for building confidence, not a statistical sample.

Historical does not mean nonconfidential. Use only material approved for the test, or redact or synthesize it.

### Compare models fairly

Test several models on the same set: one or two smaller local models, a larger local model, and your company's approved enterprise AI platform if it has one. For a local model, cost means hardware, power, and staff time to maintain it, not a per-use fee. Compare on that basis, or you'll be comparing apples to invoices.

If the enterprise model does substantially better, you may have a model or hardware gap, and the answer may be a dedicated AI workstation rather than a server room. Only use test material cleared for *sending to that vendor*; cleared for internal use is a different approval. If neither model performs acceptably, the workflow may simply not be ready for AI.

---

## 4. The Companion Test Kit

The [Local LLM Test Kit](https://github.com/PythonMuse/pythonmuse-local-llm-test-kit) lets you practice the method before you use your own engagements. It includes:

- fictional deal documents, split into a practice set and a scoring set
- an answer key with citations
- a scoring rubric with a pass bar
- a small Python runner that sends each engagement to a model running locally through Ollama and scores the results

The scoring set is deliberately booby-trapped with:

- a term sheet that disagrees with the signed agreement
- a valuation date that was never agreed
- a cap table that doesn't tie
- another client's document misfiled in the wrong folder

No Ollama yet? The kit also replays two sets of example responses, so you can watch the scoring work first. One of them gets every answer right and still fails. The article's scorecard shows why. Setup steps are in the kit's README.

---

## 5. Retrieval, Context Windows, and Hallucination

**Retrieval-augmented generation (RAG)** means the AI looks things up in your approved folder first, then answers from what it found, ideally citing the exact document. It's the difference between asking a colleague what they remember and asking them to pull the file. Bay Point's Atlas, from [IBM's case study](https://www.ibm.com/case-studies/bay-point), uses this design. Citations make the answer checkable, which is the whole argument of [From AI Answers to Audit Trails](../32-from-ai-answers-to-audit-trails/README.md).

A model's **context window** is its working memory: how much text it can consider at once. It's the problem behind [Why Claude "Forgets"](../08-why-claude-forgets/README.md) and [The PDF Token Trap](../16-pdf-token-trap/README.md). A small local model may not hold an entire deal room, which matters much less when retrieval hands it only the documents relevant to the question.

**Hallucination** is the usual name for a model making things up. The two practical defenses are the ones the article uses: require a citation for every answer, and explicitly allow the answer *"I do not have enough evidence to answer this."* A citation is still a claim to check, not proof.

---

## 6. The Local Security Checklist

Running the model inside your building changes where the risk sits. It doesn't remove any of it. You still need:

- authentication and permissions
- least-privilege access
- logging and monitoring
- data-retention rules
- network controls
- secure document handling
- human oversight

[AI in Accounting Isn't Just About Efficiency — It's About Control](../13-zero-trust-ai-accounting/README.md) is the long version of that list. Three items deserve their own note:

**Model versions.** The model you tested in March is not automatically the model running in September. Pin the version you approved, and retest before replacing it.

**Prompt injection.** A document can still contain instructions, and a local model can still follow them. [When the Invoice Starts Giving Orders](../37-when-the-invoice-gives-orders/README.md) covers the controls.

**The ethical wall, enforced in retrieval.** Document permissions have to decide what the user may retrieve *before* the model receives anything. Filter at the retrieval step, by engagement and by user, and log what was retrieved for whom. Once a document is in the model's context, it is too late to ask nicely.

---

## 7. ONBOARD, Applied to a Local Model

The same [ONBOARD checklist](../35-onboard-ai-workflows/README.md) used across this series, applied here:

- **O — Organize the workspace and define AI's role.** Use an isolated, approved environment for the model and the test material. Define the role in one line: *retrieve and cite, never calculate.*
- **N — Name the assignment.** Pick one narrow task, such as extracting liquidation preference terms, not "help with valuations."
- **B — Brief AI on the business.** Give it the authorized documents for this engagement and nothing else. Spell out what "acceptable" means, as set by the specialist.
- **O — Obtain and approve a plan.** Get the test plan, the practice and scoring sets, and the pass bar approved before the first run, not after you see the results.
- **A — Allow controlled execution.** Use least-privilege access and permission-aware retrieval, so the ethical wall is enforced before the model sees anything. Calculations stay in Excel or Python.
- **R — Review the work and evidence.** Score the output against completed engagements and the approved pass bar. Check every citation, not just the answers.
- **D — Document what was learned.** Record the approved model and version, the failures you found, and what will trigger a retest, such as a new model version, a new task, or a new document type.

When the pilot works and people start depending on it, [You Built an AI Workflow. What Happens If You Win the Lottery?](../40-builder-to-production/README.md) covers how it graduates into a production process someone else can run.

---

## 8. Valuation Terms in One Breath

For readers outside deal work:

- **Term sheet:** the non-binding summary of a proposed investment.
- **Financing agreement:** the signed, binding version. When the two disagree, the signed one wins.
- **Cap table (capitalization table):** who owns how many shares of each class.
- **Liquidation preference:** how much preferred investors get back before common shareholders see anything if the company is sold or wound down (for example, "1x" means their money back first).
- **Participation:** whether they also share in what's left after that.
- **Conversion terms:** how preferred shares turn into common shares.
- **Distribution (liquidation) waterfall:** the calculation that runs the proceeds through all of those rules in order.
- **Discounted cash flow (DCF)** and **Black-Scholes:** standard valuation models, one for a business's future cash flows and one for option-like securities.

---

## Sources

- IBM — [Bay Point Advisors case study](https://www.ibm.com/case-studies/bay-point) (Atlas: Azure OpenAI, IBM watsonx.data and DataStax, retrieval-augmented generation, citation-backed answers, document-level permissions)
- Ollama — [Chat API documentation](https://docs.ollama.com/api/chat) and [MIT license](https://github.com/ollama/ollama/blob/main/LICENSE)
- Ollama library — [Qwen3](https://ollama.com/library/qwen3) and [Llama 3.3](https://ollama.com/library/llama3.3) download sizes
- LM Studio — [App Terms of Use](https://lmstudio.ai/app-terms)
- Qwen — [Qwen3-8B model card](https://huggingface.co/Qwen/Qwen3-8B) (Apache 2.0)
- Meta — [Llama 3.3 70B Instruct model card](https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct) (Llama 3.3 Community License)
- PythonMuse — [Local LLM Test Kit companion repository](https://github.com/PythonMuse/pythonmuse-local-llm-test-kit)

Every link above was checked in October 2026. Download sizes, licenses, and product names change quickly, so re-check them before you rely on any of them.

---

*Back to the article: [If the Data Can't Leave, Bring the Model In](./README.md)*

*Related: [How to Use AI in Accounting Without Sending the Wrong Data](../06-safe-ai-data-workflows/README.md) | [Don't Trust the Model to Find What You Already Know Is There](../23-schema-driven-sanitization/README.md) | [Model Selection Is an Accounting Control](../36-model-selection-is-a-control/README.md) | [Your AI Workflow Was Approved. Did Anyone Read the Customer Contract?](../38-ai-workflow-customer-contract/README.md)*

*© 2026 PythonMuse LLC. Content licensed under [CC BY-NC-SA 4.0](../../LICENSE); code licensed under [MIT](../../LICENSE-CODE).*
