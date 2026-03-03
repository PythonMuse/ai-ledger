# Your AI Co-Pilot for Accounting: A Hands-On Guide to Claude Code in VS Code

*How two CSV files, plain English questions, and zero formulas revealed a margin crisis in under 10 minutes*

---

**By Sean Toohey**

If someone told you a year ago that you could open two spreadsheets, type a question in plain English, and get a CFO-ready margin analysis back in seconds -- you'd probably ask what they were selling. But that's exactly what's happening right now with AI coding assistants, and accounting professionals are uniquely positioned to benefit. You don't need to learn Python. You don't need to be a developer. You just need to know what questions to ask -- and that's something accountants have always been good at.

This article walks you through a real working example, step by step. By the end, you'll have everything you need to try it yourself.

---

## What We're Working With

**The tool:** Claude Code, an AI assistant that runs inside Visual Studio Code (VS Code) -- a free, lightweight code editor from Microsoft.

**The scenario:** A fictional company called **CodeCritters Inc.** sells premium AI-themed desk fidgets -- think collectible desk toys for the tech crowd. Three product lines:

- **PyPal** -- a friendly snake-shaped fidget coil (*$108--$130*)
- **ByteBot** -- an articulated robot desk companion (*$170--$190*)
- **TensorTurtle** -- a premium kinetic desk sculpture (*$238--$270*)

**The data:** Two CSV files. That's it.

- `pythonmuse_orders_revenue.csv` -- 20 orders across 2024--2025 with customer, product, quantity, price, and salesperson
- `pythonmuse_orders_costs.csv` -- matching cost records with vendor, material cost, labor employee, hours, and rates

No pivot tables. No VLOOKUP. No macros. Just raw data and a conversation.

---

## Getting Started (The 5-Minute Setup)

If you've never opened VS Code before, here's all you need:

1. **Download VS Code** from code.visualstudio.com (free)
2. **Install Claude Code** by following the setup instructions at claude.ai/claude-code
3. **Create a project folder** with your CSV files inside a `data_raw/` subfolder
4. **Open the folder** in VS Code (File > Open Folder)
5. **Open the terminal** (Ctrl + ` on Windows, Cmd + ` on Mac)
6. Type `claude` and hit Enter

That's it. You're now talking to an AI that can read, analyze, and reason about your data.

> **For the accountants reading this:** The left panel in VS Code is just a file explorer -- like Windows Explorer or Finder. The bottom panel is your conversation with Claude. Think of it as a chat window that happens to understand spreadsheets.

---

## The First Question: "What Am I Looking At?"

Let's start the way any good analysis starts -- with orientation.

**What you type:**

```
Read the two CSV files in the data_raw folder and give me a summary
of what we're working with. How many orders, what time period, what
products, and who is selling.
```

**What Claude returns:**

Claude reads both files and reports back: 20 orders spanning January 2024 through November 2025. Three products across three price tiers. Five salespeople. Five production employees. Three material vendors. Revenue and cost data linked by order ID.

No formulas written. No column headers deciphered manually. You asked a question; you got context.

This might seem simple, but consider what just happened: the AI parsed two separate CSV files, identified their schemas, recognized the join key (`order_id`), and summarized the business structure. Your first interaction took less time than opening a file in Excel.

---

## Where It Gets Interesting: Margin Analysis

Here's where accountants will sit up straight.

**What you type:**

```
Join the revenue and cost data on order_id. Calculate gross profit
and gross margin percentage for every order. Show results sorted by
margin, worst first.
```

**What Claude finds:**

![Chart: Gross Margin by Order](visuals/01_margin_by_order.png)
*Figure 1: Gross margin percentage by order. Red bars indicate orders below 20% -- all are TensorTurtle products sourced from SiliconSerpent Supply Co.*

The three worst-performing orders jump off the screen:

| Order | Salesperson | Product | Revenue | COGS | Margin |
|-------|-------------|---------|--------:|-----:|-------:|
| 2010 | Noah Patel | TensorTurtle | $6,664 | $5,572 | **16.4%** |
| 2008 | Liam Carter | TensorTurtle | $8,400 | $6,960 | **17.1%** |
| 2004 | Noah Patel | TensorTurtle | $7,650 | $6,300 | **17.6%** |

All three share the same DNA: TensorTurtle product, SiliconSerpent vendor, 2025 order. That's not a coincidence -- that's a procurement problem hiding in plain sight.

Meanwhile, the healthiest margins (41--43%) belong to PyPal orders in 2024. The pattern is clear before we even ask the next question.

---

## The Number That Should Worry the CEO

**What you type:**

```
Compare 2024 vs 2025: total revenue, total COGS, gross profit, and
gross margin percentage. Is margin compressing?
```

**What Claude finds:**

![Chart: Year-over-Year Comparison](visuals/02_yoy_comparison.png)
*Figure 2: Revenue grew 27% while gross profit stayed flat -- the classic "growing into lower profitability" pattern.*

| Metric | 2024 | 2025 | Change |
|--------|-----:|-----:|-------:|
| Revenue | $60,099 | $76,344 | **+27.0%** |
| COGS | $37,082 | $53,425 | +44.1% |
| Gross Profit | $23,017 | $22,919 | **-0.4%** |
| Gross Margin | 38.3% | 30.0% | **-8.3 pts** |

Read that again. Revenue grew 27 percent. Gross profit *declined*. The company is selling more and keeping less.

A headline-only review would celebrate the top-line growth. A controller would see the margin compression. Claude found both in under five seconds -- and it didn't need a pivot table to do it.

> **The accounting insight:** This is the difference between bookkeeping and advisory. The books show revenue is up. The analysis shows profitability is eroding. AI gets you to the analysis faster, so you spend your time on the advisory.

---

## Who's Actually Making Money?

**What you type:**

```
Rank all salespeople by total gross profit. Show their total revenue,
total GP, and margin percentage.
```

**What Claude finds:**

![Chart: Salesperson Performance](visuals/03_salesperson_gp.png)
*Figure 3: Emma Chen dominates revenue and GP, but Olivia Brooks quietly posts the highest margin rate at 40.8%.*

| Rank | Salesperson | Revenue | Gross Profit | Margin |
|------|-------------|--------:|------------:|-------:|
| 1 | Emma Chen | $47,070 | $18,145 | 38.5% |
| 2 | Sophia Ramirez | $25,450 | $9,582 | 37.6% |
| 3 | Liam Carter | $24,724 | $7,212 | 29.2% |
| 4 | Olivia Brooks | $14,275 | $5,825 | **40.8%** |
| 5 | Noah Patel | $24,924 | $5,172 | **20.8%** |

Two stories here:

**Story 1: Noah Patel's volume is misleading.** He generates nearly the same revenue as Liam Carter ($24.9K vs $24.7K) but produces $2,000 less gross profit. His 20.8% margin is nearly half the company average. If his commission is revenue-based, the company is incentivizing the wrong behavior.

**Story 2: Olivia Brooks is the quiet star.** Fewest orders on the team, but the highest margin rate at 40.8%. If management is only looking at a revenue leaderboard, they're overlooking their most efficient seller.

**The concentration risk is real, too.** A follow-up question reveals Emma Chen represents **34.5% of total revenue**. If she leaves, takes a medical leave, or her territory softens -- more than a third of the top line is at risk.

![Chart: Revenue Concentration](visuals/04_revenue_concentration.png)
*Figure 4: Revenue concentration by salesperson. Emma Chen at 34.5% represents material key-person risk.*

---

## Following the Money Upstream: Vendor Costs

**What you type:**

```
Calculate average material cost per order by vendor, comparing 2024
vs 2025. Which vendor shows the steepest cost increase?
```

**What Claude finds:**

![Chart: Vendor Cost Inflation](visuals/05_vendor_costs.png)
*Figure 5: All three vendors show cost inflation, but SiliconSerpent Supply Co. leads at nearly 48% year-over-year.*

| Vendor | 2024 Avg | 2025 Avg | YoY Increase |
|--------|--------:|--------:|-----------:|
| SiliconSerpent Supply Co | $2,725 | $4,020 | **+47.5%** |
| QuantumCoil Materials | $2,400 | $3,267 | +36.1% |
| NeuralNest Components | $2,600 | $3,500 | +34.6% |

SiliconSerpent is the primary supplier for TensorTurtle -- the same product line with all three sub-20% margin orders. The root cause chain is now visible:

```
SiliconSerpent costs up 48%
  --> TensorTurtle COGS rising
    --> Margins compressing below 20%
      --> Company GP flat despite 27% revenue growth
```

One more question rounds out the picture:

```
Are labor hours per unit increasing? Compare 2024 vs 2025.
```

**Answer:** 2024 averaged 0.80 labor hours per unit. 2025 averages 0.99 -- a **24% increase** in production time per unit. The margin squeeze is coming from both material costs and labor inefficiency.

---

## Asking the Strategic Question

This is the prompt that usually gets the strongest reaction in a room full of accountants and finance professionals:

**What you type:**

```
Based on everything you've analyzed, give me a 5-point executive
summary with recommended actions for CodeCritters management.
```

**What Claude produces:**

> 1. **Margin compression is the headline, not revenue growth.** Gross margin declined from 38.3% to 30.0% despite a 27% revenue increase. Costs are outpacing pricing power.
>
> 2. **Renegotiate or replace SiliconSerpent Supply Co.** Material costs from this vendor are up 48% YoY and they supply the most margin-impaired product line.
>
> 3. **Reprice TensorTurtle immediately.** Three orders fell below 20% margin in 2025. At current cost trajectories, this product line risks becoming unprofitable without a price adjustment to the $310+ range.
>
> 4. **Address revenue concentration risk.** Emma Chen represents 34.5% of revenue. Succession planning, territory balancing, or a second senior hire should be considered.
>
> 5. **Audit production efficiency.** Labor hours per unit increased 24%, adding to the cost pressure. Investigate whether this stems from new employee onboarding, product complexity, or process degradation.

That's a CFO-ready memo. Generated from two CSV files and a conversation. No Python script. No dashboard build. No VLOOKUP chain. Just questions asked in plain English.

---

## What This Means for Accounting Professionals

Let's be direct about what AI does and doesn't change for our profession.

**What it doesn't replace:**
- Professional judgment on materiality and risk
- Understanding of GAAP, IFRS, and regulatory context
- Client relationships and trust
- Accountability for the numbers

**What it dramatically accelerates:**
- Getting from raw data to initial analysis
- Exploring patterns and anomalies across data sets
- Drafting narratives and executive summaries
- Testing "what-if" scenarios without building models from scratch
- Cross-referencing multiple data sources

The workflow isn't "AI does the accounting." The workflow is: **AI gets you to the insight in minutes, and you spend your hours on judgment, context, and advice.** The competitive advantage shifts from *who can build the best spreadsheet* to *who can ask the best questions*.

---

## Try It Yourself

Everything in this article is reproducible. Here's what you need:

1. **VS Code** (free): [code.visualstudio.com](https://code.visualstudio.com)
2. **Claude Code**: [claude.ai/claude-code](https://claude.ai/claude-code)
3. **The sample data**: The CSV files used in this article are included in the [`data/`](data/) folder of this repository

Start with the simplest prompt: *"Read this file and tell me what you see."* Then ask the questions you'd normally answer with a pivot table. You'll find that the tool meets you where you already are -- you just get there faster.

---

## The Five Prompts Every Accountant Should Try First

If you only have 10 minutes, paste these into Claude one at a time with your own data:

1. **"Read [file] and summarize the data structure, time period, and key fields."**
2. **"Calculate gross margin per [transaction/order/project] and flag anything below [X]%."**
3. **"Compare [metric] year over year. Is the trend improving or deteriorating?"**
4. **"Rank [dimension] by [profitability measure]. Who's the top performer and who's underperforming?"**
5. **"Based on this analysis, what are the top 3 risks or action items for management?"**

These five prompts work whether you're analyzing orders, projects, clients, departments, or cost centers. The data changes; the analytical pattern stays the same.

---

*The sample data and scripts referenced in this article are available in this repository. The author used Claude Code running in VS Code on Windows. All analysis was performed live -- no results were pre-calculated or staged.*
