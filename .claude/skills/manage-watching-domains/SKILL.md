---
name: manage-watching-domains
description: Manage domain-watch surveillance configs — seed new domains, review scan status and proposals, activate Watch Log proposals into thinking topics, pause domains, and update PIRs or watch queries
automation: manual
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
user-invocable: true
argument-hint: "[review|seed|activate|pause|update] [domain-slug]"
---

# Manage Watching Domains

Human-in-the-loop manager for the domain-watch surveillance layer. Handles the full lifecycle: seeding new domains for continuous monitoring, reviewing scan status and signal level, activating Watch Log proposals into thinking topics, pausing domains, and updating intelligence requirements.

**Companion skills:**
- `.claude/skills/domain-watch/SKILL.md` — the autonomous scanning engine (runs daily, perceives and proposes)
- `.claude/skills/manage-thinking-topics/SKILL.md` — manages the thinking topics that watching domains feed into

**Architecture:** domain-watch perceives and auto-activates qualifying signals
(or injects evidence into an existing active topic); incubation-loop analyses.
This manager reviews those outcomes and manually activates any remaining
unactivated proposals through its approval gate. Domain-watch's starvation-floor
rule remains autonomous; this manager does not add a retrospective approval gate.

## State Dependencies

| Source | Location | Read | Write | Description |
|--------|----------|------|-------|-------------|
| Watching Registry | `Brain/05-Meta/Watching/WATCHING-REGISTRY.md` | ✓ | ✓ | Master list of domains + scan status |
| Domain Configs | `Brain/05-Meta/Watching/[domain-slug].md` | ✓ | ✓ | Per-domain PIRs, queries, baseline counts |
| Watch Log | `Brain/05-Meta/Watching/WATCH-LOG.md` | ✓ | ✓ | Proposals awaiting activation |
| Thinking Registry | `Brain/05-Meta/Thinking/THINKING-REGISTRY.md` | ✓ | ✓ | Destination when activating proposals |
| Thinking Files | `Brain/05-Meta/Thinking/[topic-slug].md` | | ✓ | Created during activation |

## Modes

Invoke with one of five modes. If no mode is provided, default to `review`.

---

## Mode: review

**Purpose:** Full status dashboard — what domains are active, when they last scanned, what signal level they found, and what proposals are sitting in the Watch Log awaiting your decision.

### Step 1: Read Registry and Date

```bash
date '+%Y-%m-%d'
```

Read `Brain/05-Meta/Watching/WATCHING-REGISTRY.md`. Parse all domains.

### Step 2: Load Domain Summaries

For each domain, read `Brain/05-Meta/Watching/[domain-slug].md`. Extract:
- `label` - human-readable name
- `mode` - surveillance or hypothesis
- `last_scan` - date of last scan (null = never scanned)
- `notes_at_scan` - baseline note count
- `spawn_threshold` - delta needed to trigger proposal
- `priority_intelligence_requirements` - list of PIRs (count them)
- `watch_queries` - list of search terms (count them)

### Step 3: Load Watch Log Proposals

Read `Brain/05-Meta/Watching/WATCH-LOG.md`.

Separate already activated outcomes from proposals awaiting a decision.
Recognize both `**Activated:**` (manual) and `**Auto-activated:**` markers.
Also exclude logged starvation-floor activations and evidence injections from
the pending-proposal list: verify their target against the Thinking Registry
and topic file. If a marker and target disagree, report the inconsistency rather
than treating it as permission to create or activate a duplicate.
For each remaining unactivated proposal:
- Domain slug
- Signal level (HIGH/MEDIUM)
- Scan date
- Proposed central question
- Suggested slug
- Whether it has been activated or not

### Step 4: Present Status Report

```
## Watching Domains: Status Review [DATE]

### Active Domains (N)

| Domain | Mode | Last Scan | Notes @ Scan | Threshold | PIRs | Status |
|--------|------|-----------|-------------|-----------|------|--------|
| [label] | surveillance/hypothesis | YYYY-MM-DD or never | N | +N | N | active |

### Proposals Awaiting Activation (N)

| Domain | Signal | Scan Date | Proposed Question | Suggested Slug |
|--------|--------|-----------|------------------|----------------|

### Paused Domains (N)

| Domain | Paused Since | Reason |
|--------|-------------|--------|

### Summary
- [N] domains under active surveillance
- [N] proposals waiting for your activation decision
- [N] domains never scanned (next domain-watch run will establish baseline)
- Next domain-watch run: daily at 7am UTC
```

If unactivated proposals are waiting: **"[N] unactivated proposals in Watch Log — run `/manage-watching-domains activate [slug]` to review one for activation."**

If domains have `last_scan: null`: **"[N] domains have never been scanned — run `/domain-watch` to establish baselines."**

---

## Mode: seed

**Purpose:** Add a new domain to the surveillance registry.

**Argument:** domain slug (e.g., `quantum-computing-applications`)

### Step 1: Gather Requirements

If the domain slug is not provided, ask for it. Then gather:

1. **Label** - Human-readable domain name (e.g., "Quantum Computing Applications")
2. **Mode** - `surveillance` (watch for accumulation of notes on a topic) or `hypothesis` (track whether specific claims become answerable)
   - Use `surveillance` for broad domains you want to monitor
   - Use `hypothesis` for specific questions where you're waiting for evidence
3. **Watch queries** - 2-4 semantic search terms that capture what to look for in the KB (these run against Local Brain Search)
4. **Priority Intelligence Requirements** - 2-4 specific questions you want answered when the domain produces new signal. These should be answerable (not vague). Examples:
   - Bad: "What's happening with quantum computing?"
   - Good: "Is there evidence that quantum advantage has been demonstrated for a practical ML task?"
5. **Spawn threshold** - How many new notes must accumulate before triggering a proposal (default: 3; use 2 for fast-moving areas, 5 for slow ones)
6. **Why this domain** - 1-2 sentences on why it warrants ongoing surveillance
7. **What would trigger incubation** - Concrete examples of the kind of signal worth an incubation topic

### Step 2: Validate Slug

Check that `Brain/05-Meta/Watching/[domain-slug].md` does NOT already exist. If it does, warn and stop.

Check the slug is not already in the registry. If it is, warn and stop.

### Step 3: Create Domain Config

```bash
date '+%Y-%m-%d'
```

Create `Brain/05-Meta/Watching/[domain-slug].md`:

```markdown
---
created: YYYY-MM-DD
updated: YYYY-MM-DD
created_by: claude-sonnet-4-6
updated_by: claude-sonnet-4-6
agent_version: 01.25
slug: [domain-slug]
label: "[Human-readable label]"
mode: [surveillance|hypothesis]
watch_queries:
  - "[primary search term]"
  - "[secondary search term]"
priority_intelligence_requirements:
  - "PIR 1: [specific answerable question]"
  - "PIR 2: [specific answerable question]"
last_scan: null
notes_at_scan: 0
spawn_threshold: [N]
---

# Watching: [Label]

## Why This Domain
[1-2 sentences on why this domain warrants ongoing surveillance]

## What Would Trigger Incubation
[Concrete examples of the kind of signal that would warrant a thinking topic]

## Related Thinking Topics
None yet.
```

### Step 4: Add to Registry

Edit `Brain/05-Meta/Watching/WATCHING-REGISTRY.md`:

Add a row to the domains table:
```
| [domain-slug] | [label] | [mode] | null | active |
```

Update `updated` and `updated_by` in frontmatter.

### Step 5: Confirm

Report:
- Domain config created at `Brain/05-Meta/Watching/[domain-slug].md`
- Registry updated - domain is now active
- First domain-watch run will establish the baseline note count (no proposal on first run)
- Subsequent runs will detect delta against baseline and score signal

---

## Mode: activate

**Purpose:** Take a Watch Log proposal and create a thinking topic from it, completing the perception → deliberation handoff.

**Argument:** suggested-slug from a Watch Log proposal (or domain-slug to pick the latest proposal for that domain)

### Step 1: Load the Proposal

Read `Brain/05-Meta/Watching/WATCH-LOG.md`.

Find the proposal matching the slug argument. If multiple proposals exist for the same domain, show them all and ask which to activate.

If the proposal is already marked `**Activated:**` or `**Auto-activated:**`,
or records a starvation-floor activation or evidence injection into an existing
topic, show that outcome and stop. Do not activate it again. If its recorded
target is missing, report the inconsistency without recreating it automatically.

Extract from the proposal:
- Proposed central question
- Suggested slug
- Initial hypotheses (H1, H2) and starting confidence
- Known evidence (note links and external sources)
- Signal basis (why this was flagged)

### Step 2: Validate No Duplicate

Check that `Brain/05-Meta/Thinking/[suggested-slug].md` does NOT already exist.

Check that the slug is not already in the Thinking Registry. If so, warn and offer to use a variant slug.

### Step 3: Gather Any Additions

Present the proposed central question and hypotheses. Ask:

> "Activating: **[suggested-slug]**
>
> Central question: [question]
> H1: [statement] (~X%)
> H2: [statement] (~Y%)
>
> Any changes before creating? (Press enter to accept as-is, or describe revisions)"

**[APPROVAL GATE]** Wait for response.

### Step 4: Create Thinking File

Create `Brain/05-Meta/Thinking/[suggested-slug].md` using the standard incubation-loop template:

```markdown
---
created: YYYY-MM-DD
updated: YYYY-MM-DD
created_by: claude-sonnet-4-6
updated_by: claude-sonnet-4-6
agent_version: 01.25
topic: "[exact central question]"
run_count: 0
last_run: null
status: active
---

# Thinking: [Topic Title]

## Central Question
[The exact question from the proposal, with any revisions]

## Why This Question Matters
[1-2 sentences synthesized from the Watch Log signal basis]

## Initial Hypotheses
| Hypothesis | Initial Confidence | Basis |
|-----------|-------------------|-------|
| H1: [statement] | X% | [from proposal known evidence] |
| H2: [statement] | Y% | [from proposal known evidence] |

## Known Evidence (Pre-Run)
[Note links and external sources from the Watch Log proposal]

## Constraints and Assumptions
[Any scope limits worth noting]

---
*Analytical runs will be appended below by the incubation loop*
```

### Step 5: Add to Thinking Registry

Edit `Brain/05-Meta/Thinking/THINKING-REGISTRY.md`:

Add a row to the **Active Topics** table:
```
| [suggested-slug] | [central question] | active | 0 | null |
```

Update `updated` and `updated_by` in frontmatter.

### Step 6: Mark Proposal as Activated

Edit `Brain/05-Meta/Watching/WATCH-LOG.md`:

Find the proposal entry and append under it:
```
**Activated:** [[suggested-slug]] — YYYY-MM-DD
```

Update `updated` and `updated_by` in frontmatter.

### Step 7: Update Domain Config (Related Thinking Topics)

Edit `Brain/05-Meta/Watching/[domain-slug].md`:

In the **Related Thinking Topics** section, add:
```
- [[suggested-slug]] — activated YYYY-MM-DD
```

Update `updated` and `updated_by` in frontmatter.

### Step 8: Confirm

Report:
- Thinking file created at `Brain/05-Meta/Thinking/[suggested-slug].md`
- Added to Thinking Registry as active
- Watch Log entry marked activated
- Domain config updated with related topic link
- First incubation-loop run will apply: **ACH Audit** (move 0)

---

## Mode: pause

**Purpose:** Temporarily suspend a domain from scanning (without deleting its config or history).

**Argument:** domain slug

### Step 1: Load Domain

Read `Brain/05-Meta/Watching/[domain-slug].md`. Show:
- Label, mode, last scan date, note count at last scan
- Any related thinking topics

### Step 2: Confirm Pause

**[APPROVAL GATE]** Ask:
> "Pausing '[label]' will stop domain-watch from scanning this domain on scheduled runs. The config and Watch Log history are preserved. Reason for pausing? (or type 'cancel')"

Capture the reason.

### Step 3: Update Domain Config

Edit `Brain/05-Meta/Watching/[domain-slug].md`:
- Add `paused_reason: "[reason]"` to frontmatter
- Add `paused_on: YYYY-MM-DD` to frontmatter
- Update `updated` and `updated_by`

### Step 4: Update Watching Registry

Edit `Brain/05-Meta/Watching/WATCHING-REGISTRY.md`:
- Change the domain's `Status` column to `paused`
- Update `updated` and `updated_by` in frontmatter

### Step 5: Confirm

Report:
- Domain config updated with pause reason and date
- Registry status set to paused
- To resume: edit the domain config, remove `paused_reason` and `paused_on`, set registry status back to `active`

---

## Mode: update

**Purpose:** Modify a domain's PIRs or watch queries to sharpen its signal detection.

**Argument:** domain slug

### Step 1: Load Current Config

Read `Brain/05-Meta/Watching/[domain-slug].md`. Display current:
- Watch queries (numbered list)
- Priority Intelligence Requirements (numbered list)
- Spawn threshold

### Step 2: Gather Changes

**[APPROVAL GATE]** Ask:
> "What do you want to update for '[label]'?
> 1. Add/remove/edit a watch query
> 2. Add/remove/edit a PIR
> 3. Change the spawn threshold
> (or describe the change directly)"

Apply the requested changes. Do not overwrite other frontmatter fields.

### Step 3: Write Updated Config

Edit `Brain/05-Meta/Watching/[domain-slug].md`:
- Update the changed fields in frontmatter
- Set `updated: YYYY-MM-DD` and `updated_by: claude-sonnet-4-6`

### Step 4: Confirm

Report the specific fields changed and their new values.

---

## Error Handling

| Error | Recovery |
|-------|----------|
| Watching Registry missing | Stop; inform user to create it or run `/domain-watch` first |
| Domain config missing for registry entry | Log warning; show the slug and offer to remove the orphaned registry entry |
| Slug already exists (seed mode) | Stop; show existing file path |
| No proposals in Watch Log (activate mode) | Report; suggest running `/domain-watch` to scan domains |
| Proposal already activated (activate mode) | Stop; show the thinking topic it was activated into |
| Domain already paused (pause mode) | Show current pause reason; ask if they want to resume instead |

---

## Self-Improvement

After completing this skill's primary task, consider tactical improvements:

- [ ] **Review execution**: Were there friction points, unclear steps, or inefficiencies?
- [ ] **Identify improvements**: Could the review output, activation flow, or PIR guidance be sharper?
- [ ] **Scope check**: Only execution changes — NOT changes to the perceive-flag-propose pipeline design
- [ ] **Apply improvement** (if identified):
  - [ ] Edit this SKILL.md with the specific improvement
  - [ ] Keep changes minimal and focused
- [ ] **Version control**:
  - [ ] `git add .claude/skills/manage-watching-domains/SKILL.md`
  - [ ] `git commit -m "refactor(manage-watching-domains): <brief improvement>"`
