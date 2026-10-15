---
name: incubation-loop
description: Autonomous iterative thinking loop - processes active topics using rotating analytical moves (ACH, Bayesian updating, steelmanning, cross-domain bridging, implication checks) and persists reasoning state across scheduled runs
automation: autonomous
schedule: "0 7 * * *"
allowed-tools: Read, Write, Grep, Glob, Bash, WebSearch, Skill
user-invocable: true
argument-hint: "[topic-slug] (optional - processes all active topics if omitted)"
metadata:
  version: "1.22"
  updated: 2026-07-18
  changelog:
    - "1.22: Assumption Audit trigger-definition rule — when a committed fork/leg has committed EFFECTS but its TRIGGER lacks a wire-class definition (e.g. a 'did not convene' day-close test), the audit's product is the committed trigger definition: a positive-wire path (fires at its arrival, stale-guards binding), a silence-based path gated to day-close PLUS one news-cycle allowance (bare day-close firing barred — the observability filter is readout lag, not event absence), and a provisionality/unwind rider on any silence-based firing (a later wire proving the event occurred supersedes-and-replaces in full — unwind, not booking-audit, because the firing was made on certified absence) (Run 30 hold-state pattern)"
    - "1.21: Implication Check sensor-validity probes — a probe may target the institutional validity of a committed observable surface (does the named microphone/institution currently sit/publish?), exempt from the injection-first bar because scans observe wires, not institutional status; a validity finding books as framework structure (sensor re-scope, ladder compression, named restoration re-open), never event weights, and silence from an institutionally-dark surface is voided as color (Run 5 Kuwait-Assembly-suspension pattern)"
    - "1.20: ACH matrix-integrity pass codified — when the rotation returns ACH to a topic whose posterior has not moved since the standing matrix was built, run an integrity pass (elimination check / tether check / new-evidence placement with an explicit diagnosticity verdict) instead of a rebuild; never eliminate a hypothesis inside the pre-arrival window of its own committed discriminator (Run 13/25 pattern)"
    - "1.19: Assumption Audit attribution-vs-booking separation — when an audit challenges the interpretive basis of a committed leg (choice vs inability, deliberate vs stray) but the leg's hypothesis is scoped such that the outcome disconfirms it under ALL readings (e.g. window-scoped), the leg stands at full weight and no booking-audit opens; the challenge's real content books as attribution structure on DOWNSTREAM machinery (re-arm/decay schedules, successor readings) with a named wire-class re-open condition (Run 24 choice-revelation pattern)"
    - "1.18: Implication Check decomposition pre-commitment rule — when a leading hypothesis's implications accrue asymmetrically across separable components (e.g. propensity vs location vs timing), commit the decomposition AND the post-arrival reading of the relevant committed leg BEFORE the discriminator fires (color, never weights), foreclosing both post-hoc escapes: inflating a leg-firing into full refutation, or discounting it because the disconfirmed component 'moved elsewhere' (Run 23 displacement pattern)"
    - "1.17: Cross-Domain Bridge pre-fire annotation rule — when a bridge's insight concerns a pre-registered event that has NOT yet fired, convert it into a pre-committed interpretive annotation on that event's committed legs (narrative color, never weights), fixed BEFORE the outcome is known - so arrival narratives cannot inflate or half-promote a leg after the fact (Run 22 announcable-not-package pattern)"
    - "1.16: Steelman Opposition survivorship rule — when a steelman of a STANDING RULE (a binding, guard, or booking convention, rather than a hypothesis) fails, do not leave the rule defended-by-argument only: arm an explicit falsifier condition (a named future observable that would re-open the question as a v1.10 booking-audit candidate at its own arrival, color instrument never booking), converting the surviving rule into an instrumented commitment (Run 21 fear-family dissociation-falsifier pattern)"
    - "1.15: Partial-trigger rule (v1.7) adapted to NAMED FLAGS — a flag carries no committed bands, so a partial execution has no evidential component to book at a band edge; the epistemic component books in full as a RE-ARM of the flag's remainder with a sharpened class test, and repeated same-class executions accrue grade within their stream, never fresh spread (Run 19 Ev-W pattern)"
    - "1.14: Step 7 exhaustion-window exclusion extended to CONTEXT-CLASS arrivals — a run where an arrival landed but booked nothing because no committed leg binds it at all (context-only streams like P5, rhetoric-class items) is stasis by discipline, same as empty/gated windows, and does not count toward the 5-run window"
    - "1.13: Bayesian empty-window consolidation is repeatable — a previously consolidated ledger that accretes amendments across subsequent runs is re-consolidated into a superseding version with per-cell run citations (Run 14 Ledger v2 pattern)"
    - "1.12: Step 7 exhaustion-window exclusion extended to GATED-arrival zero-drift runs — a run where an arrival landed but booked nothing because its booking authority sits at a committed future read-point is stasis by discipline, same as an empty window, and does not count toward the 5-run window"
    - "1.11: Framework-exhaustion sharpening (Step 7) — empty-arrival-window zero-drift runs do not count toward the 5-run exhaustion window (stasis by discipline is not stasis by exhaustion), and the step-1 framework audit is determinative: pending pre-registered discriminators inside the topic's committed window DEFER the trigger rather than converging past them"
    - "1.10: Guard-interaction rule (Step 5) — pre-registered ratio/laundering guards bind EVENT bookings; an analytical move (steelman, assumption audit) may revise a prior booking only via an explicit booking-audit that either preserves the guarded ratio (joint deflation/inflation) or documents why the revision is not the laundering the guard polices"
    - "1.9: Injection adjudication precedence (Step 5, all moves) — un-priced arrivals in a fresh domain-watch injection (structural-break candidates, actor inversions, ordered adjudication lists) are adjudicated and booked as argued arrivals BEFORE the rotation move runs; the move then operates on the post-adjudication posterior"
    - "1.8: Successor-topic pre-registration rule — inherited event labels do NOT inherit committed effects; a successor topic must re-derive every LR/band against its OWN hypothesis field, and cross-hypothesis couplings discovered by earlier moves (e.g. an option-value asymmetry) must be committed INTO the table so a future arrival cannot be post-hoc read as moving only one hypothesis"
    - "1.7: Partial-trigger adjudication rule — when a pre-registered event fires partially, book the epistemic component of its committed effect in full, the evidential component at the lower band edge, mark it PARTIALLY CONSUMED with an explicit re-fire condition, and record all movement as a P-table event (not framework drift)"
    - "1.6: Bayesian empty-window rule extended — when pre-registration is already complete, consolidate scattered P-table commitments into one standing reference (event/state/effect); slow-accrual evidence books at natural granularity, never per-slot"
    - "1.5: Step 9 run-slot clock caveat — take the changelog HHMM suffix from the Execution Context timestamp, not the container's `date` (which can lag hours and collide with an existing file)"
    - "1.4: Bayesian Update empty-arrival-window rule — posterior = prior with zero drift when nothing new arrived; spend the run pre-registering LRs/posterior bands for named watch events instead of manufacturing movement"
    - "1.3: Implication Check injection-first rule — score against a fresh (<24h) domain-watch evidence injection instead of firing duplicate web probes; bank the probe budget"
    - "1.2: Step 9 changelog filename now carries the UTC run-slot suffix (YYYY-MM-DD-HHMM) — the loop runs multiple times per day and date-only names collide"
    - "1.1: Registry size discipline (Step 8) — single one-line last_incubation_run overwritten in place, no _prior_* history keys, no analytical narrative in the registry; converged rows capped to a one-sentence conclusion + pointer to the topic file's Final Synthesis"
    - "1.0: Initial version"
---

# Incubation Loop

> ℹ️ **First, set expectations:** before anything else, print one short line with this skill's version and its most recent change — the top entry of `metadata.changelog` above — e.g. `incubation-loop vX.Y — recent: <summary>`. Then proceed.

Autonomous thinking engine. Each scheduled run advances all active thinking topics by one analytical move, persisting reasoning state across runs until convergence.

## Purpose

Continuous intellectual iteration on open questions. Uses a rotating set of research-validated analytical moves (ACH, Bayesian updating, dialectical steelmanning, cross-domain bridging) to build toward well-grounded conclusions - without requiring human presence in each cycle.

**Design principle:** Each run does one move per topic. Depth accumulates across runs. No single run tries to "solve" the question.

## State Dependencies

| Source | Location | Read | Write | Description |
|--------|----------|------|-------|-------------|
| Thinking Registry | `Brain/05-Meta/Thinking/THINKING-REGISTRY.md` | ✓ | ✓ | Active topics + status |
| Thinking Files | `Brain/05-Meta/Thinking/[topic-slug].md` | ✓ | ✓ | Per-topic reasoning journal |
| Local Brain Search | `resources/local-brain-search/` | ✓ | | Semantic search for KB evidence |
| Permanent Notes | `Brain/02-Permanent/` | ✓ | | Primary evidence source |
| Session Changelogs | `Brain/05-Meta/Changelogs/` | | ✓ | Run log |

## Prerequisites

- Registry file exists at `Brain/05-Meta/Thinking/THINKING-REGISTRY.md`
- At least one active topic seeded (see Seeding section below) - or none, in which case the **Starvation Floor (Step 1a)** self-seeds one from the watched domains
- Local Brain Search index up-to-date

## Composes

- `/domain-watch` - invoked by the Starvation Floor (Step 1a) when the active queue is empty, to formulate and activate a new topic from the domains under surveillance. Called by its unversioned name so its fixes propagate.

---

## Process

### Step 1: Get Date and Load Registry

```bash
date '+%Y-%m-%d'
```

Read `Brain/05-Meta/Thinking/THINKING-REGISTRY.md`. Parse all topics with `status: active`.

If registry does not exist, create it:

```markdown
---
created: YYYY-MM-DD
updated: YYYY-MM-DD
created_by: claude-sonnet-4-6
updated_by: claude-sonnet-4-6
agent_version: 01.25
---

# Thinking Registry

Active questions under continuous analysis.

| Topic Slug | Central Question | Status | Runs | Last Run |
|------------|-----------------|--------|------|----------|
```

If no active topics found, do NOT exit - run the **Starvation Floor (Step 1a)** so the thinking engine never idles.

### Step 1a: Starvation Floor (only if zero active topics)

The thinking engine must never sit idle. If Step 1 found **no active topics**:

1. Invoke `/domain-watch` (cross-skill). Its Starvation Floor guarantees at least one new topic is activated into the Thinking Registry, formulated from the domains under surveillance.
2. Re-read `Brain/05-Meta/Thinking/THINKING-REGISTRY.md` and parse `status: active` topics again.
3. If one or more active topics now exist, continue to Step 2 and process them this run.
4. Only if `/domain-watch` still produced no topic (e.g. no domains configured), log to changelog and exit cleanly.

This makes topic generation autonomous: when human-seeded questions run out, the agent proactively formulates its own next question from the watched domains rather than going quiet. Crystallization of any resulting conclusion stays manual (human judgment).

### Step 2: For Each Active Topic - Load State

Read `Brain/05-Meta/Thinking/[topic-slug].md`.

Parse frontmatter fields:
- `run_count` (required) - how many iterations completed; drives move rotation
- `last_run` (required) - date of last iteration
- `status` (required) - active / converged / crystallized / retired
- `last_move` (optional, written by loop) - which move was applied in the most recent run; informational
- `convergence_count` (optional, written by loop) - number of consecutive runs at or near convergence criteria; used by framework-exhaustion detection in Step 7
- `topic` (set at seeding) - the central question being analyzed

Parse from body:
- `current_hypotheses` - list with confidence scores (from the most recent run's "Updated Hypotheses" table)
- Last run's "Current Best Answer" and "Open Questions"

### Step 3: Determine Next Thinking Move

Rotate through this sequence. Position = `run_count mod 6`:

| Position | Move | Research Basis |
|----------|------|----------------|
| 0 | **ACH Audit** | Heuer (CIA) - Analysis of Competing Hypotheses |
| 1 | **Bayesian Update** | Information theory - explicit confidence tracking |
| 2 | **Steelman Opposition** | Socratic dialectic - steel-man the opposite |
| 3 | **Cross-Domain Bridge** | Consilience method - what does an unrelated field say? |
| 4 | **Implication Check** | Falsificationism (Popper) - if true, what follows? Is that true? |
| 5 | **Assumption Audit** | Intelligence SAT - which premises are load-bearing and shakiest? |

### Step 4: Run KB Search for Evidence

Use Local Brain Search to find relevant notes. Run these commands from the repository root:

```bash
# --no-track: this is an autonomous loop; its reads must NOT train q-values (scope-primitive learning hygiene)
resources/local-brain-search/run_search.sh "[central question]" --limit 8 --mode spreading --no-track
resources/local-brain-search/run_search.sh "[leading hypothesis]" --limit 5 --mode spreading --no-track
```

**Environment note (Trinity container):** the bare `python3 .../search.py` form fails on hosts without system-level `faiss` (`ModuleNotFoundError: No module named 'faiss'`) - e.g. the Trinity scheduled-run container. Use the wrapper `./resources/local-brain-search/run_search.sh "[query]" [same flags]` instead; it routes through the running daemon (or a venv fallback) and honors `BRAIN_READ_SCOPE` (defaults fail-closed to `core`). Same flags apply (`--mode static|spreading`, `--threshold`, `--no-track`, `--limit`).

**Mode fallback for narrow technical topics:** Spreading activation propagates through the graph's highest-centrality hubs, so for narrow/technical questions (e.g. AI-architecture, distributed-systems topics) it can return the emotional/neuroscience mega-hubs ([[Dopamine]], [[Flow is a selfless state]], [[In Buddhism - Self is an Illusion]]) as top hits - noise, not evidence. If spreading results are dominated by off-topic hubs, re-run the same queries with `--mode static` (vector similarity), which surfaces the precise topical notes. Use whichever mode yields on-topic evidence; static is often better for technical clusters, spreading for cross-domain/synthesis topics.

**Threshold note (post-2026-06-25 cosine correction):** The corrected `cosine_ip` index lowered raw query→note similarity scores, so the default `--threshold 0.5` now frequently returns "No results found" even for on-topic queries (abstract/technical questions especially). If a search comes back empty, **re-run with `--threshold 0.25` and shorter, keyword-style queries** before concluding the KB has no evidence. Treat 0.25-0.35 hits as candidate evidence to read and judge, not as automatic relevance.

**Watch-derived topics (geopolitics/current events):** core-scoped LBS predictably returns off-topic core notes for these - their evidence lives OUTSIDE core scope, in `Brain/05-Meta/Watching/WATCH-LOG.md` (recent scan entries) and predecessor/related thinking files in `Brain/05-Meta/Thinking/`. Go to those directly (grep by slug/keyword) instead of burning search retries; a full read of the predecessor's run history often surfaces evidence its Final Synthesis omits. **Exception that DOES work on core:** search for the *analytical method* the current move needs rather than the subject matter (e.g. "evidence diagnosticity competing hypotheses" for an ACH/Assumption Audit) - the core KB's decision-science notes (Bernoulli's Fallacy, base-rate blindness, framework-exhaustion guard) are on-topic for the *reasoning*, even when nothing is on-topic for the *subject*.

Read the top 3-4 most relevant notes in full. These are the evidence base for this iteration.

### Step 5: Apply the Thinking Move

Execute the move based on what was determined in Step 3. For each move:

**Injection adjudication precedence (all moves):** if the topic file carries a domain-watch evidence injection (<24h) containing arrivals OUTSIDE the pre-registered event space (candidate structural breaks, actor inversions) or with an explicit adjudication order, execute those adjudications FIRST - void-vs-map against the stationarity caveat, partial-trigger splits per the v1.7 rule - and book them as argued arrivals BEFORE applying the rotation move. The rotation move then runs against the post-adjudication posterior. Never let a steelman/bridge/audit consume ambiguous arrivals implicitly - adjudication is a separate, ordered act (interpretation is where confirmation bias operates).

**Guard-interaction rule (all moves):** pre-registered ratio/laundering guards (e.g. "no lower-regime event may move the H1:H3 ratio") bind EVENT bookings. An analytical move that wants to revise a PRIOR booking (a steelman deflating an over-determined evidence credit, an assumption audit weakening a premise) may do so only as an explicit **booking-audit**: name the original booking being revised, and either (a) apply the revision jointly so the guarded ratio is preserved (correct when the revised credit was booked jointly to the guarded hypotheses), or (b) document why a ratio-moving revision is not the laundering the guard polices. Silent re-interpretation that drifts a guarded ratio is procedurally indistinguishable from the confirmation bias the guard exists to catch.

#### ACH Audit
- List all current competing hypotheses
- For each piece of KB evidence found: does it support, contradict, or not apply to each hypothesis?
- Build a simple diagnostic matrix (evidence × hypotheses)
- Eliminate any hypothesis that is contradicted by multiple pieces of evidence
- Update confidence scores for surviving hypotheses
- **Matrix-integrity pass (repeat-ACH rule):** when the rotation returns ACH to a topic whose posterior has NOT moved since the standing matrix was built, do not rebuild - run an integrity pass instead: (i) elimination check (does any hypothesis now face multiple independent full-weight contraries? NEVER eliminate a hypothesis inside the pre-arrival window of its own committed discriminator), (ii) tether check (does every row still map to a live committed stream? inter-run annotations enter as weight footnotes, not row changes), (iii) new-evidence placement (context-class arrivals get an explicit diagnosticity verdict on the live partition - "non-diagnostic" is a recordable finding). A rebuild without a moved posterior manufactures precision the evidence has not paid for (framework-exhaustion guard).
- **Output**: Pruned hypothesis list with updated confidence levels

#### Bayesian Update
- State prior confidence in leading hypothesis (from last run)
- Identify new evidence from KB search
- Explicitly reason: "Given this evidence, should I be more or less confident? By how much?"
- Use rough likelihood ratios (e.g., "this evidence is 3x more likely if H1 is true than if H2 is true")
- Compute and record updated posterior confidence
- **Empty arrival window:** if no genuinely new evidence has arrived since the prior run (common when the run slot lands between domain-watch scans), the honest output is posterior = prior with zero drift - do NOT manufacture 1-2pp movement from re-read evidence. Spend the run on the second half of Bayesian discipline instead: pre-register likelihood ratios and posterior bands for the topic's named watch events, so future updates are mechanical against a committed table rather than post-hoc. If pre-registration is already complete, CONSOLIDATE instead: gather commitments scattered across prior runs into one standing table (event / state: live-consumed-dormant / committed effect) so future updates read one reference, not a multi-run reconstruction. Consolidation is REPEATABLE: when a previously consolidated ledger has itself accreted amendments across subsequent runs, a later empty window re-consolidates into a superseding version (v2, v3, ...) - cite per-cell the run that committed each rule, and state explicitly that the new version supersedes the old ledger plus its scattered amendments for scoring purposes. **Successor-topic rule:** when the topic inherits a predecessor's event labels (P-table continuity), the labels do NOT carry their old committed effects - re-derive every LR/band against the successor's own hypothesis field, and commit any cross-hypothesis coupling earlier moves discovered (e.g. talks-collapse is simultaneously H1-down AND H2-up under an option-value finding) into the table itself, so no future arrival can be post-hoc scored as moving only the convenient hypothesis. Slow-accrual evidence (e.g. continued silence on a watched channel) is booked at its natural granularity (weekly), not re-scored every slot.
- **Partial-trigger adjudication (applies to ANY move consuming a pre-registered event):** when a committed event fires partially - some legs satisfied, the literal trigger not met - do not binarize (neither "not fired, ignore" nor "fired, book the full band"). Split the committed effect: book its *epistemic* component in full (which future observables discriminate; table restructuring), book its *evidential* component at the LOWER band edge, mark the event PARTIALLY CONSUMED with an explicit re-fire condition for the remainder, and record all resulting movement as a P-table event (not framework drift) so the exhaustion-guard test stays honest. **Named-flag variant:** a flag (a pre-named arrival with no committed bands) that partially executes has NO evidential component to book; its epistemic component books in full as a RE-ARM of the remainder with a sharpened class test, and repeated same-class executions accrue grade within their booked stream, never fresh spread.
- **Output**: New confidence scores with explicit reasoning for the change

#### Steelman Opposition
- State the current leading hypothesis clearly
- Construct the strongest possible argument AGAINST it - not a strawman
- Search KB explicitly for evidence supporting the opposing view
- Assess: does the steelman change the leading hypothesis, or does it survive?
- If the steelman reveals a genuine weakness, revise the hypothesis
- **Survivorship rule (steelman targets that are STANDING RULES):** when the steelman's target is a standing rule (a binding, guard, or booking convention) rather than a hypothesis, and the rule survives, do not leave it defended-by-argument only - arm an explicit falsifier: name the future observable that would re-open the question as a v1.10 booking-audit candidate at its own arrival (color instrument, never booking). A rule that survives its steelman must exit the run more falsifiable than it entered, not merely re-affirmed.
- **Output**: Steel-manned opposition + response + any hypothesis revision

#### Cross-Domain Bridge
- Identify the core mechanism or pattern in the current question
- Run KB search from an unrelated domain (e.g., if topic is about AI, search neuroscience or Buddhism)
- Find analogous patterns or contradictory evidence from that domain
- Extract what the foreign domain implies about the current question
- **Pre-fire annotation rule:** when the bridge's insight concerns a pre-registered event that has NOT yet fired, do not leave it as loose narrative - convert it into a pre-committed interpretive annotation on that event's committed legs (color, never weights), fixed BEFORE the outcome is known. This is the bridge-move analog of the steelman survivorship rule: it forecloses post-arrival framing inflation (e.g. a manufactured announcable being half-promoted toward a movement leg because coverage narrates it as historic).
- **Output**: Cross-domain insight + revised framing of the question (if warranted)

#### Implication Check
- Take the current leading hypothesis as given (temporarily)
- Derive 3-5 concrete, testable implications that should be true if the hypothesis holds
- Search KB and reason about whether those implications are actually supported
- **External probe (this move only — no other move uses WebSearch)**: If an implication concerns time-sensitive empirical state the KB cannot resolve, run up to **2 web searches per topic per run** to test it. Restrict queries to reputable sources via `site:` filtering — peer-reviewed (arxiv.org, nature.com, science.org, pubmed.ncbi.nlm.nih.gov), established outlets (economist.com, ft.com, reuters.com, apnews.com, bloomberg.com), analytical (hbr.org, quantamagazine.org). (This is a subset of the canonical allowlist in `resources/SOURCE-AUTHORITY.md` — kept inline for in-query reliability; keep in sync with that file.) **Crawler caveat:** several of these domains (reuters.com, apnews.com, ft.com, economist.com) are *not accessible to the WebSearch user-agent* and an `allowed_domains` probe restricted to them returns a 400 error — wasting one of the 2 probes. Do NOT pass those as a hard `allowed_domains` filter; instead run the query **unrestricted** (or allow only the crawlable reputable domains: bloomberg.com, nature.com, arxiv.org, hbr.org, and analytical trackers like CSIS/RUSI/AEI/Jamestown) and judge source quality manually. Tag each external finding as `[EXTERNAL: source — date]` in the run output so KB-grounded vs. web-augmented evidence is auditable.
- If an implication is clearly false, that is disconfirming evidence for the hypothesis
- **Decomposition pre-commitment rule:** when the implications accrue ASYMMETRICALLY across separable components of the hypothesis (e.g. its mechanism/propensity supported while its location or timing contrary-accrues), do not leave the asymmetry as loose narrative - commit the component decomposition and the post-arrival reading of the relevant committed leg BEFORE that discriminator fires (color, never weights). This forecloses both post-hoc escapes at the arrival: inflating the leg's committed firing into full refutation of the hypothesis, or discounting the firing because the disconfirmed component "moved elsewhere."
- **Injection-first rule:** if a recent domain-watch evidence injection in the topic file already observed the implications this run would probe (check for an `### Domain-Watch Evidence Injection` block dated within ~24h), score against the injection's tagged `[EXTERNAL]` items instead of firing new web probes - re-probing freshly-observed state duplicates rather than tests. Note the banked budget explicitly in the run output.
- **Sensor-validity probes (exempt from the injection-first bar):** a probe may target the INSTITUTIONAL VALIDITY of a committed observable surface - does the named microphone/institution currently exist and function (a parliament that sits, an agency that publishes, a data series still produced)? Scans observe wires, not institutional status, so a certified-empty scan does NOT cover this question: surface silence is ambiguous between "no event" and "no institution." A validity finding books as framework structure (sensor re-scope, committed-leg surface reassignment, named re-open condition on restoration), never as event weights - and any silence previously read as informative color from an institutionally-dark surface is retroactively voided as color.
- **Output**: Implications assessed as supported/unsupported/unknown + impact on hypothesis confidence

#### Assumption Audit
- List the 3-5 key assumptions the current reasoning rests on
- Rank by: (a) how load-bearing for the conclusion, and (b) how uncertain/shaky
- Focus scrutiny on high load-bearing + high uncertainty assumptions
- For the shakiest assumption: search KB for evidence bearing on it
- **Trigger-definition rule:** when a committed fork/leg has committed EFFECTS but its TRIGGER lacks a wire-class definition (an undefined "did it happen" test is post-hoc latitude in both directions - premature firing on filtered silence, or indefinite withholding), the audit's product is the committed trigger definition: (i) a positive-wire path firing at its arrival with stale-guards binding; (ii) a silence-based path gated to the natural read-point PLUS one news-cycle allowance (bare read-point firing barred where the observability filter is readout lag, not event absence); (iii) a provisionality/unwind rider on any silence-based firing - a later wire proving the event occurred supersedes-and-replaces in full (unwind, not booking-audit, because the firing was made on certified absence). Committed effects are never changed - only the trigger machinery is supplied.
- **Attribution-vs-booking separation:** when the audit challenges the INTERPRETIVE basis of a committed leg (choice vs inability, deliberate vs stray) but the leg's hypothesis is scoped such that the outcome disconfirms it under ALL readings (e.g. window-scoped), the leg stands at full weight and no booking-audit opens - the challenge's real content books as attribution structure on DOWNSTREAM machinery (re-arm/decay schedules, successor readings), committed pre-arrival with a named wire-class re-open condition. This keeps committed bookings robust while giving genuine audit findings a home that isn't leader-protective dilution.
- **Output**: Assumption vulnerability map + revised conclusion if key assumption weakens

### Step 6: Write Updated Thinking File

Append to `Brain/05-Meta/Thinking/[topic-slug].md`:

```markdown
### Run [N]: [Move Name] - [YYYY-MM-DD]

**KB Evidence Consulted:**
- [[Note A]] - [one line on relevance]
- [[Note B]] - [one line on relevance]

**Analysis:**
[2-4 paragraphs of actual reasoning from the move]

**Updated Hypotheses:**
| Hypothesis | Confidence | Change |
|-----------|------------|--------|
| H1: [statement] | X% | ↑/↓/→ from Y% |
| H2: [statement] | X% | ↑/↓/→ from Y% |

**Current Best Answer:** [1-2 sentences - the leading position after this run]

**Open Questions for Next Run:** [What remains unresolved or most worth probing]
```

Update the frontmatter: `updated`, `updated_by`, `run_count`, `last_run`.

### Step 7: Check Convergence

A topic has converged when ANY of the following holds:

**Standard convergence (all four must be true):**
- `run_count >= 4` (minimum 4 cycles)
- Same hypothesis has led for 3+ consecutive runs
- Confidence delta between last two runs < 5 percentage points
- No major open questions flagged in last run

**Framework exhaustion (alternate path - triggers automatic convergence):**
- `run_count >= 10` AND
- The top two hypotheses have not changed relative order for 5+ consecutive runs AND
- Neither leading hypothesis's confidence has moved by more than 2pp across those 5 runs

(The 5-run window INCLUDES the current run, evaluated after its move completes - a flip at run N makes the trigger first testable at run N+4, not N+5. **Empty-arrival-window zero-drift runs do NOT count toward the 5-run window:** a run that booked posterior = prior under the Bayesian empty-window rule - because nothing arrived, not because evidence failed to discriminate - is stasis by discipline, not by exhaustion. **Gated-arrival zero-drift runs are the same case:** a run where an arrival DID land but booked nothing because its entire booking authority sits at a committed future read-point (e.g. a day-N leg) is also stasis by discipline and does not count toward the window. **Context-class arrivals are the same case too:** a run whose only arrivals belong to streams the ledger commits to never booking (context-only rows, rhetoric-class items under a cheap-talk rule) books zero drift by discipline, not by exhaustion, and does not count toward the window.)

When framework exhaustion is detected:
1. Apply one final Assumption Audit move on the *framework itself* (not the evidence). Ask: is the analytical framework (hypothesis structure, key distinctions) discriminating between meaningfully different world-states, or producing precision on an empirically-indistinct difference?
2. Note the assessment in the run output explicitly
3. **The step-1 audit is determinative, not ceremonial.** If the topic carries pre-registered discriminators (committed P-table legs with materially separated effects) scheduled to land within its own committed window, the audit answers "still discriminating" and the trigger DEFERS - converging days before the topic's own committed discrimination events would discard the mechanical scoring the pre-registration built. Log the deferral explicitly and name the run where the audit re-runs with teeth (typically after the committed window closes with every leg modal/silent).
4. If the audit instead finds the distinction empirically indistinct: converge regardless of whether external "open questions" remain — those questions belong to a different topic (often: a parameter or timing question, not the structural question that was asked)

This guards against the "Confirmation Bias as Hyper-Precise Prior" failure mode: an analysis that produces ever-finer confidence scores on a distinction that the evidence has already shown to be analytically empty.

If converged (either path):
- Set `status: converged` in the thinking file frontmatter
- Append the canonical Final Synthesis block (see below)
- Add note: `**CONVERGED** - Ready for crystallization via /manage-thinking-topics crystallize [slug]`
- Update registry status to `converged`

If not converged: continue to next topic.

**Canonical Final Synthesis block** (appended once when status flips to `converged`):

```markdown
---

## Final Synthesis

**Conclusion:** [1-2 paragraphs in plain prose - the substantive answer]

**Confidence:** X% on H[N] (and any co-leading hypotheses)

**Key evidence:**
- [[Note A]] - [why it mattered]
- [[Note B]] - [why it mattered]
- [[Note C]] - [why it mattered]

**Convergence path:** [Standard | Framework exhaustion] after [N] runs

**Remaining uncertainty:** [1 paragraph - what's known to be unknown; what could change this]

**Related topics:** [[other-converged-slug]] (if causally connected)
```

This block is the authoritative source for crystallization. Crystallize mode reads this section first, falls back to scanning the last run's "Current Best Answer" only if absent (legacy topics).

### Step 8: Update Registry

Update `Brain/05-Meta/Thinking/THINKING-REGISTRY.md`:
- Increment run count for each processed topic
- Update last_run date
- Update status (active → converged where applicable)
- On convergence, MOVE the topic's row from **Active Topics** to **Converged (Ready for Crystallization)** using this exact row shape:

  ```
  | [slug] | [runs] | [one-sentence conclusion, ≤200 chars] → [[slug]] | [YYYY-MM-DD] |
  ```

**Registry size discipline (hard rules — the registry is an index, not a journal):**

1. Registry frontmatter may contain ONLY: `created`, `updated`, `created_by`, `updated_by`, `agent_version`, and a single `last_incubation_run` field of AT MOST one line (~200 chars): timestamp + topic(s) + move + resulting status. Example:
   `last_incubation_run: 2026-07-03 07:00 UTC — agent-zero-trust-primitive Run 1 ACH Audit, still active`
2. OVERWRITE `last_incubation_run` in place each run. NEVER append `last_incubation_run_prior_*` or any other run-history keys.
3. NEVER write analytical narrative into the registry — full reasoning already lives in the topic file (Step 6) and the session changelog (Step 9). Duplicating it in the registry made it unreadable (~100k tokens) and taxes every skill that loads it.
4. Converged-table conclusion cells stay at ONE sentence; the authoritative synthesis is the topic file's `## Final Synthesis` block, which crystallize mode reads directly.
5. If legacy oversized fields or rows exist in the registry, do NOT imitate them — follow this format.

### Step 9: Write Session Changelog

Write to `Brain/05-Meta/Changelogs/CHANGELOG - Incubation Loop YYYY-MM-DD-HHMM.md` (UTC run-slot suffix, e.g. `-1000` — the loop runs multiple times per day, so date-only names collide; this matches the existing files on disk):

**Run-slot clock caveat (Trinity container):** the container's `date` can lag the platform's scheduled-run timestamp by hours. Take HHMM from the Execution Context timestamp (or the next 2h slot after the newest existing changelog for today), not from `date` — otherwise the suffix collides with an already-written file.

```markdown
---
created: YYYY-MM-DD
updated: YYYY-MM-DD
created_by: claude-sonnet-4-6
updated_by: claude-sonnet-4-6
agent_version: 01.25
---

# Incubation Loop Session: YYYY-MM-DD

## Topics Processed

| Topic | Move Applied | Confidence Shift | Status |
|-------|-------------|-----------------|--------|
| [slug] | [move name] | [leading H]: Y% → Z% | active/converged |

## Notable Shifts
[Any hypothesis revisions, convergences, or surprising KB evidence]

## Converged Topics (Ready for Crystallization)
[List any topics that reached convergence this run]
```

---

## Seeding a New Topic

To add a topic to the loop, create `Brain/05-Meta/Thinking/[topic-slug].md`:

```markdown
---
created: YYYY-MM-DD
updated: YYYY-MM-DD
created_by: claude-sonnet-4-6
updated_by: claude-sonnet-4-6
agent_version: 01.25
topic: "[exact question being analyzed]"
run_count: 0
last_run: null
last_move: null            # optional - written by loop after each run
convergence_count: 0       # optional - written by loop; tracks consecutive runs meeting convergence criteria
status: active
---

# Thinking: [Topic Title]

## Central Question
[The exact question. Precise framing matters - ambiguous questions stay ambiguous.]

## Why This Question Matters
[1-2 sentences on stakes or relevance]

## Initial Hypotheses
| Hypothesis | Initial Confidence | Basis |
|-----------|-------------------|-------|
| H1: [statement] | X% | [prior knowledge or intuition] |
| H2: [statement] | X% | [prior knowledge or intuition] |

## Known Evidence (Pre-Run)
[Any notes or sources already known to be relevant]

## Constraints and Assumptions
[What are you taking as given? What's out of scope?]

---
*[Analytical runs will be appended below by the incubation loop]*
```

Then add to `THINKING-REGISTRY.md`:
```
| [topic-slug] | [central question] | active | 0 | null |
```

---

## Crystallization (Manual)

When a topic reaches `status: converged`, the human should:

1. Read the full thinking file
2. Run `/synthesize-insights [topic-slug]` to graduate conclusions to a permanent note
3. Archive thinking file: set `status: crystallized`
4. The permanent note becomes part of the KB for future searches

**Do not automate crystallization** - judgment calls about what conclusions deserve permanence belong to the human.

---

## Error Handling

| Error | Recovery |
|-------|----------|
| Registry missing | Create empty registry, log, exit cleanly |
| No active topics | Run Starvation Floor (Step 1a) - invoke `/domain-watch` to self-seed a topic from watched domains; only log and exit cleanly if it too produces nothing |
| KB search returns empty | Try alternate search terms from hypothesis text; if still empty, note in run log and skip KB-grounding for this move |
| Thinking file missing for active topic | Log warning in registry, skip topic |
| Run exceeds 45 minutes | Process topics in order; skip remaining, log which were skipped |

---

## Completion Checklist

- [ ] Registry read - active topics identified
- [ ] Each active topic: KB searched with relevant queries
- [ ] Each active topic: correct move in rotation applied
- [ ] Each active topic: thinking file updated with reasoning + confidence scores
- [ ] Convergence checked for each topic
- [ ] Registry updated (run counts, dates, status changes)
- [ ] Session changelog written to `Brain/05-Meta/Changelogs/`

---

## Self-Improvement

After completing this skill's primary task, consider tactical improvements:

- [ ] **Review execution**: Were there friction points, unclear steps, or inefficiencies?
- [ ] **Identify improvements**: Could the thinking moves, convergence criteria, or file structure be sharper?
- [ ] **Scope check**: Only execution changes - NOT changes to the ACH/Bayesian/dialectic framework itself
- [ ] **Apply improvement** (if identified):
  - [ ] Edit this SKILL.md with the specific improvement
  - [ ] Keep changes minimal and focused
- [ ] **Version control**:
  - [ ] `git add .claude/skills/incubation-loop/SKILL.md`
  - [ ] `git commit -m "refactor(incubation-loop): <brief improvement>"`
