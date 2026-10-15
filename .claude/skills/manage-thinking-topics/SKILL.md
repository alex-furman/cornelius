---
name: manage-thinking-topics
description: Manage the incubation loop topic lifecycle — seed new questions, review status, crystallize converged conclusions, and retire stale topics
automation: manual
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
user-invocable: true
argument-hint: "[seed|review|crystallize|retire] [topic-slug]"
---

# Manage Thinking Topics

Human-in-the-loop manager for the incubation loop topic registry. Handles the full lifecycle: seeding new questions into analysis, reviewing current status, graduating converged conclusions to permanent notes, and retiring topics no longer worth pursuing.

**Companion skill:** `.claude/skills/incubation-loop/SKILL.md` — the analytical engine that processes active topics.

## State Dependencies

| Source | Location | Read | Write | Description |
|--------|----------|------|-------|-------------|
| Thinking Registry | `Brain/05-Meta/Thinking/THINKING-REGISTRY.md` | ✓ | ✓ | Master list of all topics + status |
| Topic Files | `Brain/05-Meta/Thinking/[topic-slug].md` | ✓ | ✓ | Per-topic reasoning journal |
| Permanent Notes | `Brain/02-Permanent/` | | ✓ | Atomic crystallized conclusions (graph-integrated, future-reasoning substrate) |
| Synthesis Reports | `Brain/05-Meta/Reports/` | | ✓ | Terminal crystallized conclusions (decision-input snapshots, excluded from LBS index) |
| AI Extracted Notes | `Brain/AI Extracted Notes/` | | ✓ | Alternative destination for crystallized notes |

## Modes

Invoke with one of four modes. If no mode is provided, default to `review`.

---

## Mode: review

**Purpose:** Show the full topic landscape at a glance - what's active, what needs crystallization, what's done.

### Step 1: Read Registry

```bash
date '+%Y-%m-%d'
```

Read `Brain/05-Meta/Thinking/THINKING-REGISTRY.md`.

### Step 2: For Each Active Topic - Load Summary

For each topic with `status: active`, read its thinking file. Extract:
- `run_count` - how many iterations completed
- `last_run` - date of last iteration
- Current leading hypothesis + confidence score
- Next move in rotation (run_count mod 6)
- Any open questions flagged

### Step 3: For Each Converged Topic - Load Summary

For each topic with `status: converged`, read its thinking file. Extract:
- The converged conclusion (Current Best Answer from last run)
- Confidence score at convergence
- Run count at convergence

### Step 4: Present Status Report

Output a structured report:

```
## Thinking Topics: Status Review [DATE]

### Active Topics (N)
| Topic | Runs | Last Run | Leading Hypothesis | Confidence | Next Move |
|-------|------|----------|-------------------|------------|-----------|

### Converged — Ready for Crystallization (N)
| Topic | Runs | Conclusion Summary | Confidence |
|-------|------|-------------------|------------|

### Crystallized — Done (N)
| Topic | Permanent Note | Crystallized |
|-------|---------------|-------------|

### Summary
- [N] topics in active analysis
- [N] topics ready for crystallization (action needed)
- [N] topics fully crystallized
- Next incubation-loop run: processes all active topics
```

If there are converged topics, highlight: **"[N] topics ready for crystallization — run `/manage-thinking-topics crystallize [slug]` to graduate each one."**

---

## Mode: seed

**Purpose:** Add a new question to the incubation loop.

**Argument:** topic slug (e.g., `agent-memory-architecture`)

### Step 1: Gather Requirements

If the topic slug is not provided, ask for it. Then gather:

1. **Central question** - The exact question being analyzed. Precise framing matters - vague questions stay vague.
2. **Why it matters** - 1-2 sentences on stakes or relevance.
3. **Initial hypotheses** - At least 2 competing hypotheses with rough initial confidence percentages (must sum to ~100%).
4. **Known evidence** - Any notes or sources already known to be relevant (optional).
5. **Constraints/assumptions** - What's taken as given? What's out of scope? (optional)

### Step 2: Validate Slug

Check that `Brain/05-Meta/Thinking/[topic-slug].md` does NOT already exist. If it does, warn and stop.

Check that the slug is not already in the registry. If it is, warn and stop.

### Step 3: Create Topic File

```bash
date '+%Y-%m-%d'
```

Create `Brain/05-Meta/Thinking/[topic-slug].md`:

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
[Any notes or sources already known to be relevant, or "None identified yet."]

## Constraints and Assumptions
[What are you taking as given? What's out of scope?]

---
*Analytical runs will be appended below by the incubation loop*
```

### Step 4: Add to Registry

Read `Brain/05-Meta/Thinking/THINKING-REGISTRY.md`.

Add a row to the **Active Topics** table:

```
| [topic-slug] | [central question] | active | 0 | null |
```

Update `updated` and `updated_by` in frontmatter.

### Step 5: Confirm

Report:
- Topic file created at `Brain/05-Meta/Thinking/[topic-slug].md`
- Registry updated - topic is now active
- First incubation-loop run will apply: **ACH Audit** (move 0)
- Estimated convergence: 4-6 runs (~4-6 days at daily schedule)

---

## Mode: crystallize

**Purpose:** Graduate a converged topic — either as an **atomic permanent note** (Brain/02-Permanent/, graph-integrated) or as a **terminal synthesis report** (Brain/05-Meta/Reports/, excluded from semantic indexing). Choose based on whether the conclusion is generative (future reasoning will reuse it) or terminal (snapshot of what was concluded).

**Argument:** topic slug of a converged topic

**If no slug is provided:** read the registry, present the converged topics (with one-line conclusions), and ask which to crystallize before proceeding. If prior session context points at a specific topic or pair (e.g., a just-completed analysis that named them), recommend it as the first option. Accept common misspellings of the mode name (e.g., "crystalize").

### Step 1: Load Converged Topic

Read `Brain/05-Meta/Thinking/[topic-slug].md`.

Verify `status: converged`. If not converged, warn and stop.

**Extraction strategy (prefer the canonical block, fall back gracefully):**

1. **First, look for `## Final Synthesis`** - a canonical block appended when the loop transitions a topic to converged. If present, this is the authoritative source. Extract from it:
   - Conclusion (the substantive answer)
   - Confidence and leading hypothesis
   - Key evidence (already curated)
   - Remaining uncertainty
   - Related topics (if any)

2. **If no Final Synthesis block exists** (legacy topics from before the standardized format), read only the *last 200 lines* of the file rather than the full thinking journal (some are 5,000+ lines). Extract:
   - The central question (from frontmatter)
   - The most recent "Current Best Answer" section
   - The most recent "Updated Hypotheses" table for confidence scores
   - Any "Open Questions" flagged in the final run

3. Read the full file only if the last 200 lines do not contain a "Current Best Answer" or equivalent conclusion.

### Step 2: Search for Existing Notes

```bash
resources/local-brain-search/run_search.sh "[central question keywords]" --limit 5 --mode spreading
```

Check if a permanent note already exists covering this conclusion. If so, note the overlap and ask whether to update it or create a new note.

### Step 3: Choose Destination

Before drafting, decide the destination based on the nature of the conclusion:

| Signal | Destination |
|---|---|
| Conclusion is **one atomic insight** that future reasoning will cite | `Brain/02-Permanent/` (permanent note) |
| Conclusion has **multiple co-equal findings** that belong together (e.g., a four-stage architecture, a stratified framework) | `Brain/05-Meta/Reports/` (synthesis report) |
| Conclusion is a **snapshot of a moment** (geopolitical assessment, project-stack analysis) — decision-input, not future-reasoning substrate | `Brain/05-Meta/Reports/` (synthesis report) |
| Conclusion captures a **generative principle** that will be reasoned FROM in other contexts | `Brain/02-Permanent/` (permanent note) |
| Topic is **transitory** — relevant for current decisions, unlikely to be revisited | `Brain/05-Meta/Reports/` (synthesis report) |

**[APPROVAL GATE]** Propose the destination and ask the user to confirm or override:
> "Recommend: **[destination]** because **[reason]**. Confirm, or override to **[other destination]**?"

Synthesis reports do not participate in connection-finder or semantic search (the `Reports/` folder is excluded from LBS indexing). They are visible in Obsidian and can link OUT to permanent notes via `[[wiki-links]]`, but permanent notes should rarely link IN to reports.

### Step 4: Draft Content

Adapt the draft to the chosen destination:

**If permanent note (Brain/02-Permanent/):**
- Written in the user's voice, not as a report
- Leads with the conclusion, not the process
- Cites the key evidence that drove the conclusion
- Notes remaining uncertainty or caveats
- Atomic — one main insight, ~50-100 lines

**If synthesis report (Brain/05-Meta/Reports/):**
- Long-form is appropriate — can be 200-600+ lines
- Lead with executive summary, then layered detail
- Multiple findings organized by section (each finding need not be atomic)
- Cite full evidence base with sources/URLs where applicable
- Wiki-link OUT to relevant permanent notes; reports are terminal

Propose the draft to the user for review before writing.

**[APPROVAL GATE]** Present the draft. Ask: "Write this to `[chosen destination path]`? (Yes / revise the draft / skip crystallization)"

### Step 5: Write to Destination

On approval, write the file with proper frontmatter:

```yaml
---
created: YYYY-MM-DD
updated: YYYY-MM-DD
created_by: claude-sonnet-4-6
updated_by: claude-sonnet-4-6
agent_version: 01.25
provenance: ai-inferred
---
```

**Provenance (mandatory):** Crystallized conclusions are agent-synthesized, so default `provenance: ai-inferred`. Per CLAUDE.md's guarded boundary, this only becomes `endorsed` or `originated` through an explicit endorsement act by the user at the **[APPROVAL GATE]** above - never set it automatically. If the user states the conclusion is his own thinking, set `provenance: endorsed` (or `originated` if it is purely his idea the loop merely formalized).

For synthesis reports, kebab-case the filename; add a date suffix if the report is a dated snapshot (e.g., `trinity-production-architecture-2026-05-26.md`).

### Step 6: Update Topic File

Edit `Brain/05-Meta/Thinking/[topic-slug].md`:
- Set `status: crystallized`
- Update `updated` and `updated_by`
- Append a final note (adapt to destination):

```markdown
---

**CRYSTALLIZED [DATE]** → [[Destination Note or Report Name]]

*Conclusion graduated to [permanent knowledge base | synthesis reports]. Thinking file archived.*
```

### Step 7: Update Registry

In `Brain/05-Meta/Thinking/THINKING-REGISTRY.md`:
- Remove the row from **Converged** table
- Add a row to **Crystallized** table:

```
| [topic-slug] | [[Destination Note or Report Name]] | YYYY-MM-DD |
```

If the existing Crystallized table column header is still "Permanent Note", update it to "Destination" so it accommodates both atomic notes and synthesis reports.

Update `updated` and `updated_by` in frontmatter.

### Step 8: Confirm

Report:
- File written at `[full destination path]`
- Topic marked crystallized
- Registry updated

---

## Mode: retire

**Purpose:** Remove a topic from active analysis without crystallizing it (topic no longer relevant, question was wrong, superseded by new evidence).

**Argument:** topic slug

### Step 1: Load Topic

Read `Brain/05-Meta/Thinking/[topic-slug].md`. Show:
- Current status
- Run count
- Current leading hypothesis and confidence

### Step 2: Confirm Retirement

**[APPROVAL GATE]** Ask:
> "Retiring '[topic-slug]' will stop it from being processed by the incubation loop. The thinking file will be kept for reference but marked retired. Reason for retiring? (or type 'cancel')"

Capture the reason.

### Step 3: Update Topic File

Edit `Brain/05-Meta/Thinking/[topic-slug].md`:
- Set `status: retired`
- Update `updated` and `updated_by`
- Append:

```markdown
---

**RETIRED [DATE]**

*Reason: [reason given]*

*Topic removed from active analysis. Thinking file kept for reference.*
```

### Step 4: Update Registry

In `Brain/05-Meta/Thinking/THINKING-REGISTRY.md`:
- Remove the row from whichever table it was in (Active or Converged)
- Do NOT add to Crystallized table (it wasn't graduated)

Optionally add a **Retired** section if one doesn't exist:

```markdown
## Retired

| Topic Slug | Reason | Retired On |
|------------|--------|------------|
```

Update `updated` and `updated_by` in frontmatter.

### Step 5: Confirm

Report:
- Topic marked retired in `Brain/05-Meta/Thinking/[topic-slug].md`
- Removed from registry active/converged table
- Thinking file preserved at full path for future reference

---

## Move Rotation Reference

When seeding or reviewing, the next analytical move is determined by `run_count mod 6`:

| run_count % 6 | Move |
|--------------|------|
| 0 | ACH Audit — eliminate weak hypotheses |
| 1 | Bayesian Update — explicit confidence tracking |
| 2 | Steelman Opposition — dialectical challenge |
| 3 | Cross-Domain Bridge — consilience from another field |
| 4 | Implication Check — falsificationism |
| 5 | Assumption Audit — find load-bearing shaky premises |

---

## Convergence Criteria (Reference)

A topic converges when ALL:
- `run_count >= 4`
- Same hypothesis has led for 3+ consecutive runs
- Confidence delta between last two runs < 5 percentage points
- No major open questions flagged in last run

The incubation-loop skill checks this automatically after each run.

---

## Error Handling

| Error | Recovery |
|-------|----------|
| Registry missing | Stop; inform user to seed registry via incubation-loop skill |
| Topic file missing for registry entry | Log warning; continue with other topics |
| Slug already exists (seed mode) | Stop; show existing file path |
| Topic not converged (crystallize mode) | Stop with current run count and status |
| KB search returns empty | Skip search step; note in output |

---

## Self-Improvement

After completing this skill's primary task, consider tactical improvements:

- [ ] **Review execution**: Were there friction points, unclear steps, or inefficiencies?
- [ ] **Identify improvements**: Could step ordering, prompts to the user, or output formatting be clearer?
- [ ] **Scope check**: Only execution changes — NOT changes to the incubation-loop analytical framework itself
- [ ] **Apply improvement** (if identified):
  - [ ] Edit this SKILL.md with the specific improvement
  - [ ] Keep changes minimal and focused
- [ ] **Version control**:
  - [ ] `git add .claude/skills/manage-thinking-topics/SKILL.md`
  - [ ] `git commit -m "refactor(manage-thinking-topics): <brief improvement>"`
