# Don't Trust the Model to Find What You Already Know Is There

**Schema-Driven Data Sanitization for Small Business Accounting in the Age of AI**

*~27 min read*

---

OpenAI recently released something called [Privacy Filter](https://huggingface.co/openai/privacy-filter). If that name makes you picture a pair of reading glasses that blacks out your Social Security number — honestly, you're not far off.

Privacy Filter is an AI model that scans text and identifies sensitive information: names, addresses, emails, phone numbers, account numbers, dates, URLs, and secrets. Think of it as a very fast, very literal intern who reads every document you hand it and highlights anything that looks personal. Unlike most AI tools you've probably encountered, this one doesn't live in the cloud. It runs on your laptop. Your data never leaves your desk.

For the technically curious: it's a 1.5B-parameter bidirectional token classification model, open-weight under an Apache 2.0 license, that labels an entire document in a single forward pass. For everyone else: it's free, it's fast, and it works offline.

It's also, by its own authors' admission, not enough.

Its authors describe it through its [system card](https://cdn.openai.com/pdf/c66281ed-b638-456a-8ce1-97e9f5264a90/OpenAI-Privacy-Filter-Model-Card.pdf)[^3] — a document that AI developers publish to explain what a model does, how it works, and where it falls short (think of it as the nutrition label for an AI model). The system card is refreshingly honest. The model is described as "a redaction and data minimization aid, not an anonymization, compliance, or a safety guarantee." It warns against over-reliance, flags failure modes around uncommon names and domain-specific identifiers, and explicitly cautions against deployment in financial workflows without additional safeguards. The recommendations section closes with a single, quiet imperative: use this as *part of* a holistic privacy-by-design approach.

That raises a practical question. If you're running a small-to-medium accounting department — not publicly traded, not subject to SOX, but still handling real financial data with real confidentiality obligations — what does "holistic privacy-by-design" actually look like when you want to use AI tools for analysis?

This post works through that question. The answer, I think, is simpler and more reliable than most people expect — though it depends on one important distinction. Sometimes the data you want to analyze comes from systems *you* operate (your accounting software, your payroll system, your CRM exports), and you already know — or can readily document — its schema (i.e., the column names and their meanings within your data). Other times it arrives as a third-party artifact (a vendor's PDF report, a scanned bank statement, a CSV from a tool you didn't design), and the schema is something you have to *construct* before you can sanitize. Both cases land in the same deterministic pipeline. They just enter it through different doors. We'll walk through both.

> **A note on how this post was made.** This article was developed collaboratively with Claude Opus 4.6 (Anthropic), using extended thinking to reason through the architecture. I provided the research direction and editorial framing; Claude researched the Privacy Filter system card, synthesized the COSO and CIA triad mappings, and drafted the technical pipeline and code examples. The initial prompt produced a strong first draft — but the published version is the result of multiple rounds of collaborative revision, where I reviewed each section, challenged assumptions, expanded scope, and refined the argument with Claude iterating alongside me. That process matters: working with any AI system, agentic or otherwise, requires human judgment at every stage. The tool accelerates the work; it doesn't replace the editorial responsibility. The initial prompt that started this conversation is included as a footnote.[^1]

## Wait — Why Can't I Just Send My Data to Claude?

Before we get into the architecture, we need to address something that isn't obvious to everyone: **why sending your accounting data to a cloud AI model is a concern in the first place.**

This matters because a significant number of business users — including otherwise sharp, tech-literate professionals — don't fully register the implications. When you paste a spreadsheet into Claude, upload a CSV to a competitor's chatbot, or send a JSON payload to any AI API, you are transmitting that data to a server operated by a third party. It leaves your machine, traverses the internet, and arrives at infrastructure you don't control.

For casual questions, this is fine. For business financial data, it introduces real risks — and those risks map directly to what information security professionals call the **CIA triad**[^2]: *Confidentiality* (is your data exposed to unauthorized parties?), *Integrity* (can you trust that your data hasn't been altered or misrepresented?), and *Availability* (do you maintain control and access to your own data independent of third parties?). We'll map the full architecture to CIA in detail later, but it's worth naming the framework now because every concern below is a CIA concern. For example:

**Your data may be used for model training.** Most major AI providers now offer opt-out mechanisms or enterprise tiers with contractual data protections, but the defaults vary, the policies change, and the specifics matter. If you're on a free tier or a consumer plan, your data may be fair game for training future models. That means your vendor payment history, your employee compensation data, your client billing records could become part of a model's learned patterns — diffused, anonymized in theory, but incorporated permanently. Read the terms of service. Then read them again. Better yet, paste those terms into a model and ask it to flag anything that concerns a small business handling financial data — AI is excellent at parsing dense legal language for red flags. But after your first, second, or third pass with AI, consult an actual professional. The model can surface the questions; a lawyer can answer them.

**Even with no-training guarantees, data is processed on third-party infrastructure.** The prompt and the response exist, however briefly, on servers you don't own. Staff at the provider may have access for debugging, safety review, or abuse monitoring. Subprocessors may be involved. I trust that Anthropic is protecting my data appropriately — but I'm also realistic enough to know that someone, somewhere, is attempting to penetrate those protection layers. That's not a criticism of any specific provider; it's the nature of cloud infrastructure.

The practical decision heuristic is this: **would you be comfortable if an adversary found this specific data?** If the answer is no (e.g., if the data includes SSNs, bank routing numbers, employee compensation details, or client financial records whose exposure would cause real harm) then it should never go to the cloud in identifiable form. Full stop. Address this first. No risk/reward analysis, no "but the analytical benefit is substantial" — sanitize it before anything else. That's what the sanitization pipeline in this post is for, and it's a prerequisite to every decision that follows.

What does "sanitize" mean in practice? We'll walk through a rigorous architecture later in this post, but even before you get there, the basics are accessible to anyone who can work a spreadsheet. Before sending any financial data to a cloud model, at minimum: delete columns that contain direct identifiers you don't need for the analysis (e.g., if you're analyzing expense trends, you probably don't need the vendor's EIN or bank routing number — drop them entirely). Replace names with generic labels (e.g., "Vendor A," "Vendor B") and keep a local-only key that maps the labels back to real names. Remove or redact free-text fields like memo and notes columns, which tend to accumulate sensitive details that don't follow any predictable format. Strip any row that contains data you wouldn't want read aloud in a room full of strangers. These steps are not sophisticated — they won't catch everything, and they don't scale well — but they're infinitely better than pasting raw data into a cloud prompt and hoping for the best. The full pipeline described later in this post formalizes and automates these instincts.

Only *after* you've handled the non-negotiables does the risk/reward calculus enter the picture. If the analytical benefit is substantial (e.g., "help me understand what I need to do to accommodate the latest revenue forecasts," or "flag anomalies in our expense patterns before the board meeting") then it's worth engaging. Accommodate the CIA triad per your local legislation, understand the risk, understand the reward, and decide accordingly. Not every piece of financial data carries the same sensitivity, and treating everything as equally untouchable means you never get the benefit of the tools. The goal is *deliberate risk management*, not blanket avoidance.

**Context creates sensitivity that individual fields don't carry.** A vendor name alone isn't particularly sensitive. A dollar amount alone isn't sensitive. But "Vendor: Lakeside Family Counseling, Amount: $4,200/month, GL: Employee Benefits — Mental Health" tells a story about your employees' benefits structure that you probably don't want in a training dataset. Financial data is *relational* — the sensitivity lives in the connections between fields, not in any single field. PII (personally identifiable information) detection models don't evaluate relational sensitivity. They look at individual tokens and decide whether each one looks like a name, an address, or a number. The contextual meaning of the *combination* is invisible to them.

**Breach notification obligations may apply.** If you send identifiable financial data to a cloud service and that service experiences a data breach, you may have notification obligations to affected individuals — your employees, your vendors, your clients. These obligations vary significantly by region and local legislation; what triggers notification in California differs from what triggers it in Texas, the EU, or Canada. The fact that *you* didn't get breached, that a third party you voluntarily shared data with got breached, doesn't necessarily reduce your obligations. But here's the practical upside: if you sanitize your data before it ever leaves your environment, you don't need to parse the notification requirements for every jurisdiction. The cheapest breach to remediate is the one where sensitive data was never transmitted in the first place.

**Your clients and vendors may not have consented.** When a vendor sends you an invoice with their bank routing number and EIN, they consented to *you* processing that data for payment purposes. They did not consent to you uploading it to a cloud AI service for analysis. This may not create legal liability in every jurisdiction, but it can create trust and relationship problems that matter more than legal exposure for a small business.

None of this means you can't use cloud AI for financial analysis. It means you need to think carefully about *what* you send, and you need to make that decision deliberately rather than by default. The architecture in this post is designed to let you get the analytical benefits of cloud AI while keeping the sensitive content local.

## Why Probabilistic PII Detection Is the Wrong Primary Control

So you've recognized that raw data shouldn't go to the cloud unexamined. The natural next step is to reach for a PII detection tool — like the Privacy Filter model — to scrub sensitive information before transmission.

This is better than sending raw data. But it's the wrong *primary* control, and the system card itself explains why.

The Privacy Filter model detects eight categories of sensitive spans:

- account numbers
- addresses
- emails
- names
- phone numbers
- URLs
- dates
- secrets

The Privacy Filter model is tunable — you can adjust how aggressive it is. Set it cautious, and it will only flag things it's very confident about, which means it might miss some sensitive items but won't waste your time with false alarms. Set it aggressive, and it will catch more, but it might also flag your company name as a person or redact a street name that's actually a product line. That dial matters, and we'll revisit it when we discuss where Privacy Filter fits in the pipeline.

But consider the system card's own failure modes:

- **Under-detection** of uncommon personal names, regional naming conventions, and domain-specific identifiers
- **Over-redaction** of public entities, organizations, and common nouns in ambiguous contexts
- **Missed secrets** for novel credential formats and project-specific token patterns
- **Fragmented span boundaries** in mixed-format text with heavy punctuation

Now map those failure modes onto accounting data. An accounting dataset is *dense* with exactly the patterns this model struggles with:

- Vendor names that are also common words ("Summit", "Apex", "First Choice"). 
- Account numbers in non-standard formats specific to your bank. 
- Tax ID fragments embedded in memo fields. 
- Dollar amounts that become sensitive in context even though they're not PII in isolation — knowing that your company paid exactly $47,250 to a specific vendor in a specific month can be a material business secret even after the vendor name is masked.

The fundamental issue is this: **a probabilistic model (i.e., one that makes educated guesses based on patterns it learned during training) is guessing about what's sensitive in your data. For the data you control, you already know — or can readily find out — what is sensitive.** 

- You designed the schema, or your accounting software did and you can inspect it. 
- You chose the column names, or they're documented in the export specification. 
- You know which fields contain customer names and which contain GL account descriptions. 
- You know the format of your bank's account numbers. 
- You know that the memo field in your AP ledger sometimes contains SSN fragments because someone entered them there in 2019 and you haven't cleaned it up yet.

For data that *isn't* yours by design — a vendor's quarterly statement, a scanned report from your bank, a CSV from a third-party system you didn't build — you may not know the schema yet. That doesn't change the conclusion, but it changes the order of operations: you build the schema first (with help, including from probabilistic tools), then apply the same deterministic sanitization (i.e., a known input always produces the same sanitized output). We'll come back to this case shortly.

You can make **deterministic** decisions about this data (i.e., decisions that follow concrete rules you define, removing any guesswork from the results). Using a probabilistic model as the *primary* gate between your raw data and a cloud API means trusting educated guesses to rediscover structural knowledge you already possess. That's architecturally backwards.

The fair challenge here: do you *really* know your schema as well as you think? What about the third-party PDF a vendor emailed you that you converted to CSV and never audited? The comment field where an employee pasted a client's home address because it was faster than switching to the CRM? The bank feed description that embeds a counterparty's full name in a free-text string? Before you proceed with confidence, ask yourself:

- **Have you audited free-text and memo fields?** These are the most common place for sensitive data to hide outside its designated column. People put whatever is convenient in a notes field — SSNs, phone numbers, medical context, personal addresses — because the field accepts anything.
- **Do you ingest third-party documents?** Vendor invoices, bank statements, client-provided spreadsheets, and scanned PDFs all carry schemas you didn't design. If you're converting these into your data pipeline, you're inheriting their structure — and their surprises.
- **Are there legacy data entry patterns?** In every accounting system that's been in use for more than a year, someone has entered data in a way the system wasn't designed for. Old workarounds become invisible. The "Customer Name" field that someone once used to store a spouse's contact number is now a quiet liability.
- **Do any fields concatenate information?** Transaction descriptions from bank feeds often smash together merchant names, reference numbers, partial account numbers, and location data into a single string. These are quasi-structured at best.
- **Have you checked what your export actually includes?** The CSV export from your accounting software may include fields you never see in the UI — internal IDs, audit timestamps, user login names — that carry more information than you'd expect.

This isn't a reason to abandon the deterministic approach — it's a reason to take the schema inventory step seriously and to treat the ML verification layer (i.e., Privacy Filter) as a genuine safety net rather than a formality. You start from what you know, then you hunt for what you don't.

And when the data isn't from a system you control at all — when it arrives as a vendor PDF or a scanned report — the "schema inventory" step becomes a *schema discovery* step, and the order of operations shifts. We'll address that case explicitly in Stage 1 of the pipeline below.

## The Right Architecture: Schema-Driven Transformation

The better approach inverts the dependency. Instead of asking a model "what's sensitive here?", you start from what you know — or take the time to learn — about your data and build deterministic transformations.

The pipeline looks like this:

**1. Schema Inventory (or Discovery, for third-party documents) → 2. Synthetic Data Generation → 3. Transformation Script Development → 4. Deterministic Sanitization → 5. Verification → 6. Cloud Analysis → 7. Result Re-identification**

Let's walk through each stage.

### Stage 1: Schema Inventory

There are two ways data arrives in your pipeline, and the inventory step looks different in each. Most workflows will involve both.

**1a. Sources you control.** Document every data source that originates from a system you operate. For a typical small business accounting department, this includes:

- **Chart of accounts** — GL account numbers, names, and hierarchies
- **Vendor master** — names, addresses, tax IDs, bank details, contact info
- **Customer master** — names, addresses, credit terms, payment history
- **Employee records** — names, compensation, tax withholdings, bank routing for direct deposit
- **Transaction ledgers** — AP, AR, GL, with memo/description fields
- **Bank feeds** — transaction descriptions, reference numbers, counterparty identifiers

For each source, classify every field into one of three categories:

- **Direct identifiers**: Fields that name a specific person or entity (customer name, employee name, vendor contact)
- **Quasi-identifiers**: Fields that become identifying in combination (date + amount + GL code might uniquely identify a transaction and its parties)
- **Analytical payload**: The data the cloud model actually needs to do useful work (amounts, dates, account categories, period indicators)

This classification is the critical step. It requires human judgment about your specific business context, and no ML model can do it for you.

**1b. Sources you don't control (schema discovery).** Vendor PDFs, scanned bank statements, third-party reports, and CSV exports from tools you didn't design all share a common feature: you didn't pick the schema, and it may not be documented anywhere. For these, the inventory step is preceded by *discovery* — you have to figure out what's in the document before you can classify it. A practical workflow:

- **Extract the content into structured text.** Native PDFs can be parsed; scanned PDFs need OCR. The extracted text is usually messy by default — fragmented lines, inconsistent formatting — and that's normal.
- **Sample and inspect manually.** Take a representative set of documents from the same source and read them. What fields appear, in what order, and how much does the layout vary across documents? A vendor's invoice format is usually consistent within a vendor and wildly different across vendors.
- **Run a probabilistic PII tool over the extracted text.** This is the one stage in the pipeline where Privacy Filter (or a similar model) earns a *primary* role rather than a verification role. You don't have structural knowledge yet, so probabilistic detection is the best signal you've got. Treat its output as a starting hypothesis about what's sensitive in the document, then verify it against your manual inspection.
- **Construct a tentative schema and validate it.** Write down what you found — fields, formats, free-text vs. structured, where sensitive content tends to land. Test the schema against more samples from the same source. If it holds, you've turned an unknown into a known.
- **Then proceed as in 1a.** Once you have a schema, classify the fields and design transformations the same way you would for a controlled source.

The important property is that schema discovery is a *one-time* (or once-per-source) cost — with one realistic caveat. Once you understand a vendor's invoice format, you don't have to re-discover it every month; you apply the same deterministic transformations to every new document from that vendor. Formats *can* change, though — most often when a vendor upgrades their reporting software, switches billing platforms, or redesigns their invoice template. It's not common, but it happens. Periodically spot-check incoming documents against your discovered schema, and treat any unexpected variance as a trigger to re-run discovery before the new format flows downstream.

### Stage 2: Synthetic Data Generation

Once you've inventoried your schema, generate synthetic datasets that mirror the *structure* of your real data without containing any real values. This serves two purposes:

First, it gives you a safe development environment. You can hand synthetic data to a cloud model, iterate on prompts and analysis scripts, and refine your workflow without any risk of exposure. The model doesn't need real data to help you build the sanitization pipeline — it needs structurally accurate data.

Second, it validates your schema inventory — and is especially valuable when the inventory came from discovery rather than design. If your synthetic data generator can't produce realistic-looking records for a particular table or document, that's a signal you haven't fully understood the structure of that data source. For schemas you discovered (rather than designed), this is often where gaps in the discovery step surface.

Synthetic generation for accounting data is straightforward:

```python
"""
Synthetic data generator for accounting sanitization development.
Produces structurally accurate fake data for pipeline testing.
"""
import random
import string
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

def generate_vendor_master(n=50):
    """Generate synthetic vendor records matching real schema."""
    vendors = []
    for i in range(n):
        vendors.append({
            "vendor_id": f"V-{i+1:04d}",
            "vendor_name": fake.company(),
            "tax_id": fake.ssn(),  # EIN format
            "address": fake.address(),
            "contact_name": fake.name(),
            "contact_email": fake.email(),
            "contact_phone": fake.phone_number(),
            "payment_terms": random.choice(["Net 15", "Net 30", "Net 45", "Net 60"]),
            "bank_routing": fake.aba(),
            "bank_account": ''.join(random.choices(string.digits, k=random.randint(8,12)))
        })
    return vendors

def generate_ap_ledger(vendors, n=500):
    """Generate synthetic AP transactions referencing vendor master."""
    ledger = []
    gl_accounts = [
        ("6010", "Office Supplies"), ("6020", "Professional Services"),
        ("6030", "Utilities"), ("6040", "Insurance"),
        ("6050", "Rent"), ("6060", "Travel & Entertainment"),
        ("6070", "Software Subscriptions"), ("6080", "Equipment Maintenance"),
    ]
    base_date = datetime(2025, 1, 1)
    for i in range(n):
        vendor = random.choice(vendors)
        gl = random.choice(gl_accounts)
        amount = round(random.uniform(50, 25000), 2)
        txn_date = base_date + timedelta(days=random.randint(0, 365))
        ledger.append({
            "txn_id": f"AP-{i+1:06d}",
            "txn_date": txn_date.strftime("%Y-%m-%d"),
            "vendor_id": vendor["vendor_id"],
            "vendor_name": vendor["vendor_name"],
            "gl_account": gl[0],
            "gl_description": gl[1],
            "amount": amount,
            "memo": fake.sentence(nb_words=8),
            "check_number": f"{random.randint(10000, 99999)}" if random.random() > 0.3 else None,
            "status": random.choice(["Posted", "Posted", "Posted", "Void"]),
        })
    return ledger
```

The key insight: this synthetic data is *cheap to produce and structurally identical to real data*. You can iterate rapidly on transformation scripts using synthetic data, then apply the proven scripts to real data with high confidence.

### Stage 3: Transformation Script Development

With synthetic data in hand, develop deterministic transformation scripts. These are not ML models — they're straightforward data processing pipelines that you can read, audit, test, and version control.

The transformations fall into a few patterns:

**Pseudonymization via lookup tables**: Replace direct identifiers with consistent synthetic values. Vendor "Acme Consulting" becomes "Vendor_0017" everywhere, preserving referential integrity across tables. Store the mapping in an encrypted lookup table that never leaves your local environment.

```python
"""
Deterministic sanitizer: replaces known PII fields with
pseudonymized values using a stable, reproducible mapping.
"""
import hashlib
import json

class DeterministicSanitizer:
    def __init__(self, salt: str):
        self.salt = salt
        self._lookup = {}

    def pseudonymize(self, value: str, category: str) -> str:
        """Generate a stable pseudonym for a given value."""
        if value is None:
            return None
        key = f"{category}:{value}"
        if key not in self._lookup:
            hash_input = f"{self.salt}:{key}".encode()
            digest = hashlib.sha256(hash_input).hexdigest()[:8]
            self._lookup[key] = f"{category.upper()}_{digest}"
        return self._lookup[key]

    def sanitize_ap_record(self, record: dict) -> dict:
        """Sanitize a single AP ledger record."""
        sanitized = record.copy()

        # Direct identifiers: pseudonymize
        sanitized["vendor_name"] = self.pseudonymize(
            record["vendor_name"], "vendor"
        )
        sanitized["memo"] = self._scrub_memo(record["memo"])

        # Remove fields that should never leave local environment
        for field in ["check_number"]:
            sanitized.pop(field, None)

        # Analytical payload passes through unchanged:
        # txn_date, gl_account, gl_description, amount, status
        return sanitized

    def _scrub_memo(self, memo: str) -> str:
        """
        Replace known patterns in free-text memo fields.
        This is where a model like Privacy Filter adds value
        as a secondary verification layer.
        """
        if memo is None:
            return None
        # Apply regex patterns for known sensitive formats
        # SSN, EIN, phone, email patterns, etc.
        import re
        memo = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[SSN_REDACTED]', memo)
        memo = re.sub(r'\b\d{2}-\d{7}\b', '[EIN_REDACTED]', memo)
        memo = re.sub(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            '[EMAIL_REDACTED]', memo
        )
        # Names from vendor/customer master get pseudonymized
        # using the same lookup table for consistency
        return memo

    def export_mapping(self, filepath: str, encryption_key: bytes = None):
        """Export the pseudonym mapping for later re-identification."""
        # In production, encrypt this file at rest
        with open(filepath, 'w') as f:
            json.dump(self._lookup, f, indent=2)
```

**Generalization**: Replace precise values with ranges or categories where the cloud model doesn't need exact figures. Individual transaction amounts become buckets ($0–1K, $1K–5K, $5K–25K) if the analysis is about patterns rather than exact reconciliation.

**Suppression**: Remove fields entirely when they add no analytical value but carry risk. Check numbers, bank routing numbers, and employee SSN fragments get dropped, not masked.

**Perturbation**: Add calibrated noise to numerical fields when the analysis is statistical. If you're looking for seasonal expense trends, shifting every amount by ±3% preserves the pattern while preventing exact reconstruction.

### Stage 4: Deterministic Sanitization of Real Data

Once your transformation scripts are tested against synthetic data and verified to preserve the analytical properties you need, apply them to real data. This step is mechanical — the same scripts, the same transformations, applied to real inputs.

The output is a sanitized dataset that:
- Contains no direct identifiers
- Preserves referential integrity through consistent pseudonymization
- Retains the analytical payload the cloud model needs
- Is produced by auditable, version-controlled, deterministic code
- It requires no cloud interaction, all processing is done locally.

### Stage 5: Verification

Before the sanitized output leaves your environment, run it through a probabilistic PII detector — Privacy Filter or a similar model — as a verification step. If the model flags residual sensitive data in something the deterministic sanitizer was supposed to have cleaned, treat each flag as a signal: a gap in the schema inventory, a transformation script that missed a case, or a free-text field with content you didn't anticipate. The flag rate should be low. When it isn't, the answer is to fix the deterministic layer, not to lean harder on the probabilistic one.

This stage is the architectural complement to Stages 1–4: deterministic transformation handles the known structure, and probabilistic verification catches what the structural knowledge missed. The full architectural reasoning — including the role this layer plays during schema discovery for third-party documents, and the option to run the verification model entirely on your own hardware — is in the "Where Privacy Filter Fits" section below.

### Stage 6: Cloud Analysis

Send the sanitized, verified dataset to the cloud model. Because you've preserved the structural relationships in the data, the model can perform the analysis you need: anomaly detection, trend analysis, narrative generation, forecasting. It's working with real patterns from your real data, but it never sees the identities behind those patterns.

### Stage 7: Result Re-identification (Local)

When the cloud model returns results that reference pseudonymized entities ("VENDOR_a3f2c1e8 shows a 340% increase in Q3 expenses"), you re-identify locally using your encrypted lookup table. The re-identification step happens entirely in your local environment. The cloud model never needs to know that VENDOR_a3f2c1e8 is Acme Consulting.

## Where Privacy Filter Fits: The Verification Layer

Stage 5 above describes *what* the verification step does. This section explains *why* the architecture puts probabilistic detection there rather than at the front, and why the same model that's the wrong primary control is the right verification layer.

This is exactly the role the system card envisions. The model becomes part of a "holistic privacy-by-design approach" rather than being asked to shoulder the entire burden alone. Its false negatives become less dangerous because the deterministic layer has already handled the known structure. Its false positives become useful signals rather than disruptive over-redaction, because you can investigate each flag against your schema inventory.

There is one exception to this verification-layer framing: during *schema discovery* for third-party documents (Stage 1b above), Privacy Filter steps forward as a primary tool rather than a backstop. When you don't yet have a schema, you don't yet have deterministic rules — and probabilistic detection is the best initial signal about what's in the document. The role flips back to verification once discovery is complete and the deterministic transformations are in place. The same model serves both functions; it's the position in the pipeline that changes.

For a small business, this is where a critical distinction enters the picture — one that many people aren't aware exists: **you can run AI models on your own computer, without sending any data to the cloud.**

When most people think of AI, they think of a website — Claude, ChatGPT, Gemini — where you type a prompt and get a response from a model running on someone else's servers. But there's a growing ecosystem of models designed to run entirely on hardware you own. The Privacy Filter is one of them. At 1.5B parameters with only 50M active, it runs comfortably on a standard office laptop or desktop. It works fine on a CPU alone — no graphics card required. If your machine does have a GPU with 4GB or more of memory, it'll run even faster, but it's not a requirement. (Not sure what any of that means? Ask your IT person whether your office machines can "run a 1.5B parameter model locally" — if they know, they'll tell you; if they don't, that's useful information too.) You install it once using Python's `transformers` library, and from that point forward, every document you process stays on your machine. Nothing is transmitted. No API calls. No cloud dependency. Your data never leaves your desk.

This is the key reason Privacy Filter earns its place in this architecture. The *privacy-critical* step — verifying that your sanitization didn't miss anything — happens in an environment you fully control. Tools like [Ollama](https://ollama.com) make running local models even more accessible, providing a simple interface to download and run a growing library of open-weight models without needing to write Python. If you're new to the concept of local AI, Ollama is a good place to start exploring what's possible on your own hardware.

The broader point is this: "AI" doesn't have to mean "cloud." For tasks where data sensitivity is the primary concern, local models give you the analytical capability without the exposure. They're smaller, less capable than the cloud models you'd use for complex analysis — but for a focused task like PII detection, that's exactly the right tradeoff.

## Mapping to CIA and COSO

For those coming from a controls and audit background, this architecture maps cleanly to both the CIA triad and the COSO framework[^4]. Even though COSO is most commonly associated with SOX compliance for public companies, its five-component structure provides useful scaffolding for any organization that wants to think systematically about controls — including private small businesses that will never file a 10-K.

### CIA Triad

**Confidentiality**: The deterministic sanitizer is the primary confidentiality control. It ensures that sensitive data never leaves the local environment in identifiable form. The encrypted pseudonym mapping is the critical asset — its compromise would allow re-identification, so it requires the same protections as the underlying data. The Privacy Filter model serves as a detective control, catching confidentiality failures before they reach the cloud.

**Integrity**: Schema-driven transformation preserves analytical integrity by design. Because you're transforming based on known structure rather than pattern-matching against content, you can verify that the relationships in the data that matter for analysis are preserved. Referential integrity (the same vendor gets the same pseudonym everywhere) is guaranteed by the lookup table, not hoped for by the model. A perturbation budget (the ±3% noise) is documented and bounded, so downstream consumers of the analysis know exactly how much precision was traded for privacy.

**Availability**: The architecture keeps the local environment as the authoritative data source and the cloud model as a processing resource, not a storage dependency. If the cloud API is unavailable, your data and your sanitization pipeline are unaffected. If you need to switch cloud providers, you re-run the sanitized data through a different API. The deterministic pipeline is portable — it's Python scripts and lookup tables, not a vendor-locked SaaS integration.

### COSO Internal Control Components

**Control Environment**: The schema inventory establishes organizational commitment to data classification. It doesn't need to be elaborate — for a small business, a spreadsheet that maps each data source to its fields and sensitivity classifications is sufficient. What matters is that someone has made deliberate decisions about what's sensitive and documented them.

**Risk Assessment**: The synthetic data generation step is an implicit risk assessment. Building synthetic data forces you to confront the actual structure of your data and ask "what could go wrong if this field leaked?" Fields you can't easily synthesize are often the ones with the most complex sensitivity profiles — and therefore the ones that need the most careful transformation design.

**Control Activities**: The deterministic sanitization scripts *are* the control activities. They're specific, testable, and auditable. Unlike a probabilistic model whose behavior changes with input distribution, a deterministic script does the same thing every time. You can write unit tests for it. You can diff its output across versions. You can show it to an auditor and they can read it.

**Information and Communication**: The pseudonym mapping table and transformation documentation serve the communication function. Anyone in the organization who needs to understand what was done to the data before it was sent to the cloud can read the transformation scripts and the mapping table. This is radically more transparent than "we ran it through a PII detection model."

**Monitoring**: The Privacy Filter model, run as a post-sanitization audit, is the monitoring function. Regular execution against sanitized outputs provides ongoing assurance that the deterministic controls are working as intended. Flagged items become investigation triggers — and because the flag rate should be very low (the deterministic layer handles the known structure), each flag gets meaningful attention rather than being lost in a flood of false positives.

## Practical Recommendations for Small Business Accounting

If you're an accounting manager or controller at a small business considering AI-assisted analysis, here's the implementation path:

**Start with the schema inventory — including for recurring third-party documents.** For data from systems you control, this is a one-time effort that pays dividends beyond the AI use case. For recurring third-party documents (a vendor's monthly invoice, a bank's standard statement format), invest the time once to *discover* the schema and write it down. From that point forward, every new document from that source slots into the same deterministic pipeline. Schemas don't usually change once a vendor settles on a format, but they can — most often when a vendor upgrades their reporting software or switches billing platforms — so spot-check periodically and re-run discovery if you see unexpected variance. Understanding exactly what sensitive data you hold, where it lives, and what format it takes is foundational to any data governance posture. You probably have a rough sense of this already — formalize it.

**Generate synthetic data early.** Use libraries like Python's Faker[^5] to produce structurally accurate test data. Share the synthetic data freely with cloud models while developing your analysis workflows. This lets you iterate on the analytical approach without any privacy risk, and it builds the muscle memory for thinking about data structure separately from data content.

**Build deterministic sanitizers for structured fields.** For the vast majority of accounting data, you either know the schema or can document it once and reuse the documentation. Write transformation scripts that handle that known structure. Keep them simple, readable, and version-controlled. Don't over-engineer — a Python script with clear comments is better than a complex framework.

**Use ML-based PII detection for free-text fields, as a verification layer, and during schema discovery.** Memo fields, notes, and description columns are where unstructured PII lurks within otherwise structured data — and for third-party documents you're seeing for the first time, probabilistic detection plays a bigger role still, because it's the best initial signal you have before you've built a schema. In all of these cases, a model like Privacy Filter adds genuine value — not as the primary gate for known-schema data, but as a net for the things your inventory didn't anticipate and as a starting point when there is no inventory yet. Run it locally if you can; the model is small enough.

**Document everything.** The transformation scripts, the schema inventory, the pseudonym mapping (encrypted), the Privacy Filter audit results. This documentation is your evidence that you've taken reasonable care with data confidentiality — which matters for client relationships, insurance, and potential regulatory interactions even if you're not subject to SOX.

**Test with real data in a controlled setting before going to production.** Run your sanitization pipeline against a sample of real data, then manually review the output. Are there fields you missed? Patterns in memo fields you didn't anticipate? Names leaking through in unexpected places? This is where you discover the gaps that synthetic data couldn't reveal.

## Where We Can Go Deeper

The architecture above is the *what*. Several topics that would round out a production deployment are out of scope for this post — each warrants its own treatment. A short tour of the open questions, with where I'd start:

- **How do you test sanitization scripts and catch regressions when input formats drift?** The transformations are production code, and silent drift in an upstream format (a renamed column, a new field, a re-templated PDF) can quietly bypass them. A reasonable starting point: unit tests against synthetic fixtures (you already have the generator from Stage 2), golden-output tests that fail loudly when transformation behavior changes, and a small regression suite that runs whenever a schema is re-discovered. The harder open question is the *trigger* — how do you know an input format has actually drifted enough to warrant a re-run, before a sanitization gap goes live?

- **Who owns the schema inventory, and how do changes to transformation scripts get reviewed?** These are organizational questions, not technical ones, and the answers vary by company size. For a small team, a single person who owns the inventory document and signs off on transformation changes is probably enough. For a larger team, treating the inventory and the scripts as version-controlled code with normal code review applies cleanly. The encryption key for the pseudonym lookup table needs its own answer — who holds it, where it's stored, how it's rotated, and what happens when the holder leaves.

- **What evidence do you keep, and how would you respond to an auditor or insurer asking to see it?** The COSO mapping above gestures at this, but a full treatment would cover concrete artifacts: pinned versions of the transformation scripts, run logs, the Privacy Filter flags and how each was investigated, and a retention period for all of the above. A reasonable default is to keep everything tied to a sanitization run for at least as long as you'd retain the underlying source data, and to treat the script repository itself as a piece of audit evidence.

Each of these warrants its own post. Naming them here rather than treating them lightly is deliberate — sanitization-script testing in particular needs a careful walkthrough, given how easily a regression in your transformation layer can defeat the rest of the architecture.

## The Broader Point

The OpenAI Privacy Filter model is a genuinely useful tool, and its system card is a model of responsible disclosure about limitations. But the most important thing in the system card isn't the model architecture or the performance metrics — it's the framing. The repeated insistence that this is "one of multiple layers" points to a deeper truth about data privacy in the AI era.

For most business data, the problem isn't that we don't know what's sensitive. It's that we reach for probabilistic detection when we should be applying the structural knowledge we already have — or could readily acquire. The exciting ML model feels like the sophisticated solution. The boring Python script that pseudonymizes column 3 and drops column 7 feels like it can't possibly be enough. But for structured data with known schemas — which is what accounting data overwhelmingly is, once you've taken the time to inventory it — the boring script is the *correct* primary control, and the ML model is the *correct* verification layer. Even when the schema isn't yours to begin with — when the data arrives as a vendor PDF or an opaque third-party export — the right move is to *build* a schema once and then proceed deterministically, not to outsource the question to a probabilistic guess every time.

Get the architecture right, and you can use cloud AI tools for financial analysis with confidence — not because you trust the model to find every sensitive field, but because you *know* what you transformed, and you can prove it.

---

[^1]: The prompt that initiated this collaboration: *"I was reviewing the system card for the openai privacy-filter model. We are interested in getting a better understanding of how to appropriately mask data to ensure confidentiality, integrity, and availability of systems (CIA). Particularly in local accounting settings where cloud models may interact with data. The COSO framework touches on these topics. In reading the system card, the authors warn that it is not an all in one solution, but more simply, a piece of a bigger pipeline. In the context of a small-to-medium accounting department for a small business (i.e., not publicly traded), what appropriate safeguards should be recommended and demonstrated to better understand the scope and concerns in this area. I was envisioning local model as a preferred facility for this task, but I think it may be easier to model the datasets and produce fake data to help models (i.e., local or cloud) to develop the scripts necessary to sanitize data that then allows cloud models to assist in further analysis of properly transformed datasets. Can we think through this? This sounds like a good blog post for us."*

[^2]: The CIA triad (Confidentiality, Integrity, Availability) is formally defined in NIST Special Publication 800-12 Rev 1, *An Introduction to Information Security* (National Institute of Standards and Technology). Available at: https://csrc.nist.gov/publications/detail/sp/800-12/rev-1/final

[^3]: The OpenAI Privacy Filter System Card is available as a detailed PDF at: https://cdn.openai.com/pdf/c66281ed-b638-456a-8ce1-97e9f5264a90/OpenAI-Privacy-Filter-Model-Card.pdf — the model repository, including weights and source code, is hosted at: https://huggingface.co/openai/privacy-filter

[^4]: Committee of Sponsoring Organizations of the Treadway Commission (COSO), *Internal Control — Integrated Framework* (originally issued 1992, updated 2013). COSO is jointly sponsored by the AICPA, IMA, AAA, IIA, and FEI. Framework guidance and supplemental publications are available at: https://www.coso.org/guidance-on-ic

[^5]: Faker is an open-source Python library for generating realistic synthetic data. Documentation and installation instructions are available at: https://faker.readthedocs.io/en/master/
