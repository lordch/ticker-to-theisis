---
name: ticker-to-thesis
description: Generate institutional-quality buyside investment memos from a stock ticker symbol. Use this skill whenever the user wants investment analysis, a buyside memo, equity research, or stock evaluation. Trigger on any mention of analyzing a stock, writing a memo, building an investment thesis, evaluating whether to buy/sell/short a company, or casual questions like "what do you think about $AAPL" or "look into MSFT for me". Even vague requests like "research this company" or "is X a good investment" should use this skill.
---

# Ticker to Thesis

Generate institutional-quality buyside investment memos through systematic research, multi-perspective analysis, and iterative debate. Research is driven by a structured framework with saturation tracking. Six distinct investing philosophies analyze the same ticker, a Research Director pressure-tests each view, and a final synthesis produces a unified institutional memo. Every stage persists its output to files — subsequent agents read from those files, ensuring zero information loss.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| **Ticker** | Yes | Stock ticker symbol (e.g., AAPL, MSFT) |
| **Prompt** | No | Specific research question or angle to investigate |
| **Preliminary thinking** | No | Initial research notes, thesis, or context |

## Output

A polished 4,000-5,000 word buyside memo in markdown, saved to `analyses/{TICKER}-{YYYY-MM-DD}/07-final-memo.md`. Reads as one mind's institutional conviction — no trace of the multi-agent process. Includes executive summary with TL;DR, business quality assessment, investment thesis with variant view, valuation with sensitivity tables, key analytical tensions, catalysts, risks with kill conditions, position sizing, and a bottom line.

### Analysis Folder Structure

```
analyses/{TICKER}-{YYYY-MM-DD}/
  00-search-strategy.md           # Research framework + saturation criteria
  01-source-discovery.md          # Curated link list with value ratings
  02-source-analysis.md           # Analysis of sources through framework
  03-saturation-tracker.md        # Living saturation tracker + recommendation
  04-research-synthesis.md        # Consolidated research packet
  05-six-lens/
    quality-compounder.md
    imaginative-growth.md
    fundamental-ls.md
    deep-value.md
    event-driven.md
    macro-tactical.md
  06-rd-review.md
  07-final-memo.md
  sources/                        # Raw scraped/downloaded sources
    primary--{name}.md
    fact--{name}.md
    fact--{name}.pdf
    opinion--{name}.md
    ...
```

---

## Workflow

### Phase 0: Setup

Create the analysis folder structure:
1. Create `analyses/{TICKER}-{YYYY-MM-DD}/`
2. Create `analyses/{TICKER}-{YYYY-MM-DD}/sources/`
3. Create `analyses/{TICKER}-{YYYY-MM-DD}/05-six-lens/`

If a folder for this ticker and date already exists, append a sequence number: `AAPL-2026-02-08-2`.

---

### Phase 1a: Search Strategy

**Agent:** Search Strategist (subagent, general-purpose)
**Reads:** Ticker, user prompt, preliminary thinking
**Writes:** `00-search-strategy.md`
**Reference:** `references/search-strategist-prompt.md`

The strategist creates a structured research framework:

1. **Key Questions** — organized by category (Business Model, Competitive Dynamics, Financials, Management, Growth Drivers, Risks & Catalysts, Macro Context)
2. **Priority** — each question tagged `critical` / `important` / `supplementary`
3. **Saturation Criteria** — for each question, what counts as "enough" (e.g., "3+ independent sources with quantitative data", "1 primary source with direct voice")
4. **Search Plan** — concrete query strings to execute, ordered by priority

The search strategy adapts to the ticker: a mega-cap like AAPL gets different questions than a small-cap biotech or a SPAC.

---

### Phase 1b: Source Discovery

**Agent:** Source Scout (subagent, general-purpose) — may run multiple rounds
**Reads:** `00-search-strategy.md` (+ `03-saturation-tracker.md` if round 2+)
**Writes:** `01-source-discovery.md` (appends in subsequent rounds)

The scout executes the search plan via WebSearch and builds a curated link list:

```markdown
| # | URL | Title | Type | Value (1-5) | Addresses Questions | Comment |
|---|-----|-------|------|-------------|--------------------:|---------|
```

**Type** classification: `primary` / `fact` / `opinion` (per evidence hierarchy)
**Value** rating: 1 (skip) to 5 (must-read)
**Comment**: 1-2 sentences on why this source is or isn't worth scraping

The scout does NOT scrape content yet — this is a map of the terrain. The goal is 15-25 discovered links per round, from which the best will be collected.

In round 2+, the scout receives the saturation tracker and focuses searches on gaps: specific queries targeting unsaturated questions.

---

### Phase 1c: Source Collection

**Agent:** Source Collector (subagent, general-purpose)
**Reads:** `01-source-discovery.md` (sources rated 3+)
**Writes:** files in `sources/`, updates `01-source-discovery.md` with collection status

For each high-value source:

- **HTML pages** → WebFetch → save as markdown to `sources/{type}--{short-name}.md`
- **PDFs** (SEC filings, reports) → download via `curl` to `sources/{type}--{short-name}.pdf`
- **Earnings transcripts** → WebFetch → save as markdown

Each saved file starts with a metadata header:

```markdown
---
url: https://...
type: primary | fact | opinion
accessed: 2026-02-08
value_rating: 4
addresses: Business Model, Financials
---
```

Naming convention: `{type}--{short-descriptive-name}.{ext}`
Examples: `primary--ceo-interview-cnbc-q3-2024.md`, `fact--10k-2024.pdf`, `opinion--ms-initiation-report.md`

The collector uses parallel WebFetch/curl calls internally for efficiency.

**Failed sources:** The collector will inevitably fail to collect some sources (paywalls, login walls, JS-heavy pages, rate limits). For each failed source, the collector appends to a `## Failed Sources` section at the end of `01-source-discovery.md`:

```markdown
## Failed Sources

| # | URL | Title | Value | Reason | Addresses Questions |
|---|-----|-------|-------|--------|--------------------:|
| 1 | https://... | MS Initiation Report | 5 | Paywall | Valuation, Competitive |
| 2 | https://... | WSJ Deep Dive | 4 | Login required | Management, Strategy |
```

---

### Checkpoint #1a: Failed Sources

**Actor:** Orchestrator (main context)
**Reads:** `01-source-discovery.md` (Failed Sources section)

If there are failed high-value sources (rated 4-5), present them to the user:

> "Te źródła zostały ocenione jako wartościowe, ale nie udało się ich automatycznie zebrać:
> 1. [MS Initiation Report](url) (wartość: 5) — paywall — dotyczy: Valuation, Competitive
> 2. [WSJ Deep Dive](url) (wartość: 4) — login required — dotyczy: Management, Strategy
>
> Czy chcesz któreś z nich dostarczyć ręcznie?"

**If user wants to provide sources:**
1. Ask the user WHICH sources they will provide (do not create placeholder files preemptively)
2. For each confirmed source, create a placeholder `.md` file in `sources/` with only the metadata header and an instruction comment:

```markdown
---
url: https://...
type: opinion
accessed: 2026-02-08
value_rating: 5
addresses: Valuation, Competitive
status: awaiting-manual-input
---

<!-- Wklej treść źródła poniżej tej linii. Usuń tę instrukcję po wklejeniu. -->
```

3. Wait for the user to confirm they've pasted the content
4. Verify the files have content beyond the header before proceeding

**If user declines or there are no failed sources:** proceed directly to Phase 1d.

---

### Phase 1d: Source Analysis

**Agent:** Source Analyst (subagent, general-purpose)
**Reads:** all files in `sources/`, `00-search-strategy.md`
**Writes:** `02-source-analysis.md`, `03-saturation-tracker.md`
**Reference:** `references/source-analyst-prompt.md`

The analyst reads each source against the research framework:

1. **Per-source analysis**: key findings tagged to framework questions, evidence quality assessment, notable quotes (with exact attribution)
2. **Cross-source synthesis**: where sources agree/conflict, emerging patterns
3. **Saturation tracker update**: for each question — % saturated, which sources contributed, what's missing
4. **Recommendation**: "continue research" (with specific gaps to target) or "saturated — proceed to synthesis" (with justification)

Saturation thresholds:
- `critical` questions: must reach 80%+ saturation
- `important` questions: must reach 60%+
- `supplementary` questions: 40%+ (or skip if critical+important are saturated)

---

### Checkpoint #1b: Research Saturation

**Actor:** Orchestrator (main context)
**Reads:** `03-saturation-tracker.md`

Present to the user:
- Current saturation state (summary table)
- Agent's recommendation (continue / sufficient)
- If continue: what specific gaps remain and what targeted searches would address them

**User decides:**
- "Szukaj dalej" → loop back to Phase 1b with targeted queries (scout reads updated tracker)
- "Wystarczy" → proceed to Phase 1f

---

### Phase 1f: Research Synthesis

**Agent:** Research Synthesizer (subagent, general-purpose)
**Reads:** `02-source-analysis.md`, `03-saturation-tracker.md`
**Writes:** `04-research-synthesis.md`

Consolidates all research findings into a single "research packet":

1. **Organized by framework questions** (not by source) — each question gets a consolidated answer with evidence chain
2. **Key Forces candidates** — the 1-3 forces that will materially move the needle (Big Story identification)
3. **Evidence quality summary** — primary source count, fact vs. opinion ratio
4. **Known gaps and limitations** — explicitly called out
5. **Raw data points** — key financials, metrics, quotes preserved for analysts

This file becomes the **sole required input** for the Six-Lens analysts. They may optionally reference `sources/` for deeper dives, but `04-research-synthesis.md` should be self-sufficient.

---

### Phase 2: Six-Lens Analysis

**Agents:** 6× analyst subagents (general-purpose, **launched in parallel**)
**Each reads:** `04-research-synthesis.md` + their philosophy from `references/investing-philosophies.md` + `references/analyst-prompt.md`
**Each writes:** `05-six-lens/{philosophy}.md`

Analyze the ticker through each of six investing philosophies:

| Philosophy | Core Question | Time Horizon |
|------------|--------------|--------------|
| **Quality Compounder** | Can this business compound for 20 years? | Forever |
| **Imaginative Growth** | What could go very, very right? | 5+ years |
| **Fundamental L/S** | What does 100hrs of diligence reveal the market is missing? | 1-3 years |
| **Deep Value** | What would a private buyer pay? | Patient |
| **Event-Driven** | What specific event forces a re-pricing? | 6-18 months |
| **Macro-Tactical** | What is liquidity doing and who benefits? | Regime-dependent |

**For each philosophy, produce:**
1. A clear directional view (long, short, or pass — never "it depends")
2. The 1-3 key forces that will materially move the needle
3. A variant view — why the market is wrong
4. Quantified valuation with entry price
5. Kill conditions with specific thresholds
6. Cross-framework acknowledgment (if passing, which other lens might see opportunity)

Each analysis should be substantive (2,000-3,000 characters minimum) — not a summary, but a real analytical position.

**The Big Story anchor:** Every analysis must orbit 1-3 key forces that will materially move the company over the next 3-5 years. An analysis that covers 10 small things instead of going deep on 1-3 material forces has lost the thread.

---

### Phase 3: Research Director Review

**Agent:** Research Director (subagent, general-purpose)
**Reads:** all 6 files in `05-six-lens/`, `04-research-synthesis.md`
**Writes:** `06-rd-review.md`
**Reference:** `references/rd-review-prompt.md`

As Research Director, critically review all six analyses:

1. **Challenge each position** — If bullish, probe the bear case. If bearish, probe the bull case.
2. **Assess the Big Story** — Did each analyst identify the right key forces?
3. **Surface disagreements** — Where do the six philosophies conflict most consequentially?
4. **Identify the top 3 analytical tensions** — The substantive debates the synthesis must resolve.
5. **Run a pre-mortem** — "Assume we're 2 years out and the investment failed. What happened?"
6. **Push on evidence quality** — Are claims grounded in primary sources from the research packet?

---

### Checkpoint #2: Research Director Findings

**Actor:** Orchestrator (main context)
**Reads:** `06-rd-review.md`

Present to the user:
- Key analytical tensions identified by the RD
- Major disagreements between philosophies
- RD's assessment: are there critical gaps requiring iteration?

**User decides:**
- "Iteruj" → optional iteration round (analysts respond to RD, RD reviews again)
- "Syntezuj" → proceed to Final Synthesis

---

### Phase 4: Iterate (Optional)

If the user chooses to iterate:
- Each analyst responds to the RD critique (accept/reject/partially accept with evidence)
- Analysts update their files in `05-six-lens/`
- RD reviews again, updates `06-rd-review.md`

One iteration is usually sufficient. The goal is depth on the key forces, not exhaustive debate.

---

### Phase 5: Final Synthesis

**Agent:** Final Synthesizer (subagent, general-purpose)
**Reads:** `06-rd-review.md`, all files in `05-six-lens/`, `04-research-synthesis.md`
**Writes:** `07-final-memo.md`
**References:** `references/rd-synthesis-prompt.md`, `references/writing-craft-engine.md`

Synthesize all perspectives into a single, coherent institutional memo.

**Format (strict):**

```
# $TICKER: [One-liner thesis that captures the investment case]

## 1. Executive Summary
[Recommendation, conviction, key reasoning]

**TL;DR:**
- [Recommendation + conviction level]
- [Key thesis driver]
- [Primary risk or kill condition]
- [Valuation vs. current price]

## 2. Business Quality Assessment
## 3. Investment Thesis & Variant View
## 4. Valuation
## 5. Key Analytical Tensions (3 debates)
## 6. Catalysts
## 7. Risks & Kill Conditions
## 8. Position Sizing Rationale
## 9. Bottom Line

Sources:
[table of all sources with links]
```

**Synthesis rules:**
- Write as "we" — the firm's collective view. Never reference individual analysts or the debate process.
- Where analysts agreed: state the conclusion with conviction.
- Where analysts disagreed: address the disagreement explicitly. If your conclusion contradicts majority view, include a "Why the Bears/Bulls Are Wrong" section.
- If 3+ analysts flagged a specific risk, you must address it by name.
- IRR hurdle: Longs require ≥15% expected IRR. Shorts require ≥20-25%. If returns don't clear, recommendation is PASS.
- Show the valuation work: methodology, assumptions, sensitivity table.
- Kill conditions must be specific and verifiable, not generic.

**Writing standards:**
- 80%+ active voice
- Vary sentence length: 60% medium, 25% short, 15% long
- No throat-clearing openings. Start with the punch.
- No trailing summary closings. End with impact.
- Kill hedge words on beliefs: "could potentially be attractive" → "attractive"
- One idea per paragraph, topic sentence first

---

### Phase 6: Self-Check

Before delivering, verify:

1. Header is `# $TICKER: [thesis]` — nothing before it
2. Executive Summary ends with exactly 4 TL;DR bullets
3. Bottom Line section exists before Sources
4. 4,000-5,000 words with methodology shown
5. All 3 analytical tensions have full for/against/resolution
6. Sensitivity table included in valuation
7. IRR explicitly calculated and clears hurdle (or recommendation is PASS)
8. Kill conditions are specific with measurable thresholds
9. No trace of multi-agent process visible
10. Sources table with all citations and links
11. All analysis files exist in the folder structure
12. `sources/` directory contains the raw collected sources

---

## Agent Orchestration Summary

```
ORCHESTRATOR (main context)
│
├─ [1] Search Strategist       → 00-search-strategy.md
├─ [2] Source Scout             → 01-source-discovery.md     (may loop)
├─ [3] Source Collector         → sources/*
│   └─ reports failed sources in 01-source-discovery.md
├─── ★ CHECKPOINT #1a: user provides manual sources (if needed)
├─ [4] Source Analyst           → 02-source-analysis.md + 03-saturation-tracker.md
├─── ★ CHECKPOINT #1b: user approves saturation or requests more research
│     └─ if more research → back to [2] Source Scout
├─ [5] Research Synthesizer     → 04-research-synthesis.md
├─ [6a-6f] Six Lens Analysts   → 05-six-lens/*.md           (PARALLEL)
├─ [7] Research Director        → 06-rd-review.md
├─── ★ CHECKPOINT #2: user approves or requests iteration
└─ [8] Final Synthesizer        → 07-final-memo.md
```

---

## Bucket Classification

The memo must classify into exactly one investment bucket. Read `references/memo-engine.md` for detailed bucket templates.

| Bucket | Description | Key Requirements |
|--------|-------------|-----------------|
| **Long-term Compounder** | Quality business, multi-year hold | ROIC 5yr+, moat evidence, DCF explicit |
| **Catalyst-Driven Long** | Event-driven, 6-18 month | Catalyst timing, probability-weighted return |
| **Short Position** | Overvalued, broken thesis | Squeeze risk quantified, max 3% position |
| **Secular Short** | Structural decline, 3-5+ year | Secular force quantified, max 1-2% position |

No hedging between buckets. If passing, specify an action price and information trigger.

---

## Scoring Target

The memo targets a score of 7+ across these dimensions:

| Dimension | Weight | What 8-10 Looks Like |
|-----------|--------|---------------------|
| Thesis Clarity | 25% | Falsifiable + variant view + "wrong if" conditions |
| Evidence Quality | 25% | Primary research from multiple categories |
| Valuation Rigor | 20% | Multiple methods + sensitivity + derived entry price |
| Risk Framework | 15% | Specific kill conditions with milestones |
| Decision Readiness | 15% | Entry/exit/sizing + action price if passing |
