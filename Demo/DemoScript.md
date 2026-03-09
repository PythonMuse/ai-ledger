# CodeCritters AI Finance Demo -- Full Script

## For Accounting Professionals New to VS Code + Claude Code

---

## The Business Scenario

**Company:** CodeCritters Inc.
**What they sell:** Premium AI-themed desk fidgets and collectibles

| Product | Description | Price Range |
|---------|-------------|-------------|
| **PyPal** | A friendly Python snake fidget coil | $108 - $130 |
| **ByteBot** | An articulated robot desk companion | $170 - $190 |
| **TensorTurtle** | A premium kinetic desk sculpture | $238 - $270 |

**Sales Team (5):** Emma Chen, Liam Carter, Sophia Ramirez, Noah Patel, Olivia Brooks
**Production Team (5):** Ava Thompson, Marcus Lee, Dana Kim, Jake Rivera, Priya Singh
**Vendors (3):** SiliconSerpent Supply Co, QuantumCoil Materials, NeuralNest Components
**Data:** 20 orders across 2024-2025 (10 per year)

---

## Pre-Demo Setup (5 minutes before)

1. Open VS Code
2. Open the `PythonMuse` folder (File > Open Folder)
3. Open the terminal (Ctrl + `)
4. Verify Claude Code is running: type `claude` in terminal
5. Have `data_raw/` folder visible in the Explorer sidebar
6. **Pre-calculate nothing.** Let AI derive everything live. That is the point.

---

## Part 1: Orientation (The "Wow, This Is My Workspace" Moment)

> **Talking point:** "This is VS Code -- think of it as a smart notebook for your data. The left panel shows your files. The right side panel is where we talk to Claude."

### Prompt 1 -- Let Claude Introduce Itself to the Data

```
Read the two CSV files in the data_raw folder and give me a summary of what
we're working with. How many orders, what time period, what products, and
who is selling.
```

**What Claude should find:**
- 20 orders (10 in 2024, 10 in 2025)
- 3 products: PyPal, ByteBot, TensorTurtle
- 5 salespeople, 5 production employees
- 3 vendors
- Revenue file links to cost file via `order_id`

> **Why this matters for accountants:** "Notice we didn't write a single formula. We didn't pivot anything. We asked a question in plain English and got a structured answer from raw data."

---

## Part 2: Margin Analysis (The Core Demo)

### Prompt 2 -- Gross Margin Per Order

```
Join the revenue and cost data on order_id. Calculate gross profit and gross
margin percentage for every order. Show results sorted by margin, worst first.
```

**Expected results (verify Claude gets these):**

| Order | Salesperson | Product | Revenue | COGS | GP | Margin |
|-------|-------------|---------|---------|------|----|--------|
| 2010 | Noah Patel | TensorTurtle | $6,664 | $5,572 | $1,092 | **16.4%** |
| 2008 | Liam Carter | TensorTurtle | $8,400 | $6,960 | $1,440 | **17.1%** |
| 2004 | Noah Patel | TensorTurtle | $7,650 | $6,300 | $1,350 | **17.6%** |
| 1004 | Noah Patel | TensorTurtle | $5,000 | $3,760 | $1,240 | 24.8% |
| 1010 | Noah Patel | TensorTurtle | $5,610 | $4,120 | $1,490 | 26.6% |
| ... | ... | ... | ... | ... | ... | ... |
| 1009 | Emma Chen | PyPal | $8,050 | $4,600 | $3,450 | 42.9% |

> **Talking point:** "Three orders are below 20% margin -- and they're ALL TensorTurtle orders sourced from SiliconSerpent. That's not a coincidence. That's a procurement issue an accountant would want to escalate."

### Prompt 3 -- Year-Over-Year Margin Trend

```
Compare 2024 vs 2025: total revenue, total COGS, gross profit, and gross
margin percentage. Is margin compressing?
```

**Expected results:**

| Year | Revenue | COGS | Gross Profit | Margin |
|------|---------|------|-------------|--------|
| 2024 | $60,099 | $37,082 | $23,017 | **38.3%** |
| 2025 | $76,344 | $53,425 | $22,919 | **30.0%** |

- Revenue grew **27.0%**
- Gross profit **declined 0.4%** (essentially flat)
- Margin compressed **8.3 percentage points**

> **Talking point:** "Revenue is up 27% -- a CEO might celebrate. But GP is flat. The company is growing itself into lower profitability. This is exactly the kind of insight a good accountant brings to the table, and Claude found it in seconds."

---

## Part 3: Sales Performance

### Prompt 4 -- Top 3 Salespeople by Gross Profit

```
Rank all salespeople by total gross profit. Show their total revenue, total GP,
and margin percentage. Who are the top 3?
```

**Expected results:**

| Rank | Salesperson | Revenue | Gross Profit | Margin |
|------|-------------|---------|-------------|--------|
| 1 | Emma Chen | $47,070 | $18,145 | 38.5% |
| 2 | Sophia Ramirez | $25,450 | $9,582 | 37.6% |
| 3 | Liam Carter | $24,724 | $7,212 | 29.2% |
| 4 | Olivia Brooks | $14,275 | $5,825 | 40.8% |
| 5 | Noah Patel | $24,924 | $5,172 | 20.8% |

> **Talking point:** "Noah Patel has nearly the same revenue as Liam Carter ($24.9K vs $24.7K), but his GP is $2,000 less. Revenue without margin context is misleading. Also notice Olivia Brooks -- fewest orders but highest margin rate at 40.8%. She might be your most efficient seller."

### Prompt 5 -- Revenue Concentration Risk

```
What percentage of total revenue does each salesperson represent? Is there
concentration risk?
```

**Expected results:**

| Salesperson | Revenue | % of Total |
|-------------|---------|-----------|
| Emma Chen | $47,070 | **34.5%** |
| Sophia Ramirez | $25,450 | 18.7% |
| Noah Patel | $24,924 | 18.3% |
| Liam Carter | $24,724 | 18.1% |
| Olivia Brooks | $14,275 | 10.5% |

Total revenue: **$136,443**

> **Talking point:** "Emma Chen represents over a third of all revenue. If she leaves, gets sick, or her territory softens -- that's a material risk. This is PE-level due diligence thinking, and the AI just surfaced it from two CSV files."

---

## Part 4: Vendor Cost Analysis

### Prompt 6 -- Which Vendor Shows Rising Costs?

```
Calculate average material cost per order by vendor, comparing 2024 vs 2025.
Which vendor shows the steepest cost increase?
```

**Expected results:**

| Vendor | 2024 Avg | 2025 Avg | Increase |
|--------|---------|---------|----------|
| SiliconSerpent Supply Co | $2,725 | $4,020 | **+47.5%** |
| QuantumCoil Materials | $2,400 | $3,267 | +36.1% |
| NeuralNest Components | $2,600 | $3,500 | +34.6% |

> **Talking point:** "SiliconSerpent is inflating nearly 50% year over year. And remember those three sub-20% margin orders? All SiliconSerpent. A controller would want to renegotiate or find an alternate supplier for TensorTurtle materials."

### Prompt 7 -- Labor Efficiency

```
Are labor hours per unit increasing? Compare average labor hours per unit
sold in 2024 vs 2025.
```

**Expected results:**
- 2024: 304 total labor hours / 380 units = **0.80 hrs/unit**
- 2025: 447 total labor hours / 450 units = **0.99 hrs/unit**
- Increase: **+24%**

> **Talking point:** "We're getting less efficient on the production floor. Each unit takes 24% more labor than last year. Combined with material inflation, this explains the margin compression."

---

## Part 5: Strategic / PE-Level Questions

### Prompt 8 -- Orders Below 20% Margin

```
List all orders with gross margin below 20%. What do they have in common?
```

**Expected answer:** Orders 2004, 2008, 2010 -- all in 2025, all TensorTurtle, all sourced from SiliconSerpent Supply Co.

> **Talking point:** "The AI doesn't just list the numbers -- it identifies the pattern. This is the kind of analysis that takes hours in Excel pivot tables. Here it took seconds."

### Prompt 9 -- Pricing Strategy

```
If material cost inflation continues at the current rate, how should we
adjust TensorTurtle pricing to preserve a 30% gross margin?
```

**Expected direction:** Claude should estimate the projected COGS and back-calculate a required selling price. Given SiliconSerpent's ~48% inflation, TensorTurtle's average cost basis is climbing rapidly. To hit 30% margin, pricing may need to increase from ~$250 to ~$310+ range, or the company needs to switch vendors.

> **Talking point:** "We just asked the AI a forward-looking strategic question -- not a lookup, not a formula. It reasoned through a what-if scenario. This is the difference between reporting and advising."

### Prompt 10 -- What Should Management Do?

```
Based on everything you've analyzed, give me a 5-point executive summary
with recommended actions for CodeCritters management.
```

**Expected themes:**
1. Margin compression is serious (38% to 30%) despite revenue growth
2. SiliconSerpent vendor relationship needs renegotiation or replacement
3. TensorTurtle product line needs pricing review
4. Revenue concentration on Emma Chen is a risk
5. Labor efficiency declining -- investigate production process

> **Talking point:** "This is a CFO-ready memo generated from two CSV files and a conversation. No Python script. No dashboard. No VLOOKUP. Just questions."

---

## Part 6: Bonus Round (If Time Permits)

### Prompt 11 -- Build a Dashboard

```
Write a Python script using pandas and matplotlib that creates a dashboard
showing: margin by salesperson, margin trend by year, and vendor cost
comparison. Save it to the dashboards folder.
```

> **Talking point:** "For the audience that wants to go further -- Claude can also write code. It just produced a working Python dashboard from the same data we were analyzing conversationally. That script is reusable and auditable."

### Prompt 12 -- Export Analysis

```
Create a combined analysis CSV in data_processed/ that includes order_id,
all revenue fields, all cost fields, gross_profit, and margin_percentage.
```

> **Talking point:** "Now we have a clean, enriched dataset we can hand to anyone -- auditors, the board, a BI tool. Claude did the join, the calculation, and the export."

---

## Presentation Flow Summary

| Section | Duration | Key Message |
|---------|----------|-------------|
| 1. Orientation | Brief | "This is your AI workspace" |
| 2. Margin Analysis | Core | "Revenue up, profit flat -- AI caught it" |
| 3. Sales Performance | Core | "Revenue ≠ profitability" |
| 4. Vendor Costs | Core | "SiliconSerpent is the problem" |
| 5. Strategic Questions | Impact | "From reporting to advising" |
| 6. Bonus | Optional | "It writes code too" |

---

## Tips for the Presenter

1. **Go slow on the first prompt.** Let people see you type in plain English and watch Claude respond. The "magic moment" is the first time it works.

2. **Pause after each result.** Ask the audience: "How long would this take you in Excel?" Let the silence do the work.

3. **Don't over-explain VS Code.** They don't need to know about extensions, terminals, or configs. Just: "This is where your files are (left), this is where you talk to AI (bottom)."

4. **If Claude gives a slightly different number**, that's fine. Rounding differences are normal. The insight is what matters, not the decimal.

5. **Have the prompts ready to paste.** Copy them from this document. Don't try to type them live under pressure.

6. **End on Prompt 10 (executive summary).** It's the most powerful finish -- an AI just wrote a management memo from raw CSVs.

7. **Anticipate the skepticism question:** "But can I trust it?" Answer: "You verify it the same way you verify any analysis -- spot check key numbers. The difference is Claude got you to the answer in minutes instead of hours. Your job shifts from building the analysis to reviewing it."

---

## Data Integrity Cheat Sheet (For Presenter Reference Only)

**Do NOT show this during the demo.** This is for you to verify Claude's answers are correct.

### Totals
- **Total Revenue:** $136,443
- **Total COGS:** $90,507
- **Total Gross Profit:** $45,936
- **Overall Margin:** 33.7%

### By Year
- **2024:** Rev $60,099 | COGS $37,082 | GP $23,017 | Margin 38.3%
- **2025:** Rev $76,344 | COGS $53,425 | GP $22,919 | Margin 30.0%

### By Salesperson (GP Rank)
1. Emma Chen: $18,145 GP (38.5% margin, 34.5% of revenue)
2. Sophia Ramirez: $9,582 GP (37.6% margin)
3. Liam Carter: $7,212 GP (29.2% margin)
4. Olivia Brooks: $5,825 GP (40.8% margin -- highest rate)
5. Noah Patel: $5,172 GP (20.8% margin -- lowest rate)

### Vendor Avg Material Cost (YoY)
- SiliconSerpent: $2,725 → $4,020 (+47.5%)
- QuantumCoil: $2,400 → $3,267 (+36.1%)
- NeuralNest: $2,600 → $3,500 (+34.6%)

### Orders Below 20% Margin
- 2010: 16.4% (Noah Patel, SiliconSerpent, TensorTurtle)
- 2008: 17.1% (Liam Carter, SiliconSerpent, TensorTurtle)
- 2004: 17.6% (Noah Patel, SiliconSerpent, TensorTurtle)

### Labor Efficiency
- 2024: 0.80 hrs/unit → 2025: 0.99 hrs/unit (+24%)
