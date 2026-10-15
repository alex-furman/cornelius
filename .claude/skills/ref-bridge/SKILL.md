---
name: ref-bridge
description: Bridge reference entities to the cognitive knowledge base — "this client maps to that insight you had." A thin mode over connection-finder that mounts core,Company/<sub> and surfaces entity↔insight bridges, making the reference scope more than a CRM. READ-ONLY sense — it surfaces candidate bridges for human consideration and MUST refuse to promote a record into an endorsed insight (the guarded encountered→endorsed boundary). Company is the default scope.
automation: manual
allowed-tools: [Read, Bash, Glob, Grep, Skill]
user-invocable: true
argument-hint: "[scope=Company] <entity name or sub-scope, e.g. 'Acme Corp' | 'engagements'>"
metadata:
  version: "1.1"
  created: 2026-07-08
  author: Cornelius
  changelog:
    - "1.2: Fix — spreading mode drifts to the KB's densest hub (Identity/Dopamine), returning spurious bridges for cross-cluster entities (most Company products/agents); run BOTH modes, static is primary, judge relevance. Corrected the over-stated '0.5 returns []' claim — 0.35 is a floor, not a universal fix (validated 2026-07-08)"
    - "1.1: Fix — working core-vocabulary example query + --threshold 0.35 (0.5 default silently returned []); note book-shelf concepts need Books mounted"
    - "1.0: Initial version — thin mode over find-connections with a core,Company/<sub> mount; surfaces entity↔insight bridges; refuses to promote"
---

# Ref Bridge

> ℹ️ **First, set expectations:** before anything else, print one short line with this skill's version and its most recent change — the top entry of `metadata.changelog` above — e.g. `ref-bridge v1.0 — recent: initial version`. Then proceed.

**Why reference data lives *in the brain* and not in a spreadsheet.** A CRM stores clients; a second brain can tell you *which of your insights a client is a live instance of*. `ref-bridge` mounts a reference sub-scope alongside `core` and finds the bridges from an entity to the user's cognitive notes ("Acme Corp, the lighthouse deal ↔ your note on land-and-expand / reference-customer leverage").

It is **read-only sense**. It surfaces candidates; it never writes, and — critically — it **never promotes** a record into an endorsed insight. A record *informing* a thought is fine; a record *becoming* the user's `originated`/`endorsed` thought is the one line the reference kind exists to hold, and it stays the human `encountered → endorsed` act.

**Read first:** `resources/layered-brains/COMPANY-BRAIN-SCHEMA.md` → "The playbook suite" (`ref-bridge` row) + "Automation boundary"; `resources/layered-brains/REFERENCE-SCOPE-SCHEMA.md`.

## Composes

- `/find-connections` — the connection-discovery engine; this skill runs it with the reference scope mounted and frames the output as entity→cognitive-note bridges. (Do not re-implement connection logic.)

## State Dependencies

| Source | Location | Read | Write | Description |
|--------|----------|------|-------|-------------|
| Company family | `Brain/Company/*/*.md` | ✓ | | The entity anchor(s) |
| Core KB + wrappers | `Brain/{02-Permanent,03-MOCs,AI Extracted Notes,01-Sources}/`, `resources/local-brain-search/run_connections.sh` · `run_search.sh` | ✓ | | Bridged-to cognitive notes |

## Process

### Step 1 — Pick the anchor + read its themes

Resolve the entity note (or take a whole sub-scope) and **read it** to extract its distinctive themes — the economic/strategic *concepts* it embodies, not its proper nouns (e.g. Acme Corp's engagement = "one lighthouse deal deposits a reusable blueprint + license ARR + a reference case" → themes: *optionality / one-bet-many-payoffs*, *reusable-asset leverage*, *reference-proof credibility*). These themes are the query surface — the bridge is to the insight a fact *instantiates*, so search by concept.

### Step 2 — Theme-seeded CORE search (run BOTH modes; judge relevance)

A reference note's own precomputed edges cluster tightly with its **siblings** (all engagement notes look alike), and mounting `core,Company/<sub>` lets those siblings crowd out core in the results. So the method that actually surfaces entity→insight bridges is a **theme-seeded search of `core` alone**, using KB-aligned vocabulary — run in **both** modes, because they fail differently:
```bash
# the bridge: which of the user's insights is this entity a live instance of?
BRAIN_READ_SCOPE=core resources/local-brain-search/run_search.sh "<entity themes, KB vocabulary>" --mode static    --threshold 0.35 --limit 6 --json --no-track
BRAIN_READ_SCOPE=core resources/local-brain-search/run_search.sh "<entity themes, KB vocabulary>" --mode spreading --threshold 0.35 --limit 6 --json --no-track
```
**`static` is the primary finder for cross-cluster bridges; `spreading` drifts to the KB's densest hub.** Spreading activation flows toward high-centrality nodes — in this KB the Identity / Dopamine / Eight-Circuit cluster. For an entity whose true theme lives *outside* that cluster (agent architecture, orchestration, GTM — i.e. **most** Company products, agents, and engagements), spreading returns plausible-but-spurious Identity/Dopamine bridges while `static` returns the right ones (validated 2026-07-08: Trinity Cloud, themed "agent orchestration / harness is the constraint / architecture over models" → *"Most AI agents are chatbots with fancy wrappers"* · *MOC - AI and Agents* under `static`; → Identity/Dopamine notes under `spreading`). Only when the entity's theme *is* the dense decision-science/consciousness core do the two agree (Acme Corp's decision-science theme → Decision Making · Prospect Theory · Loss Aversion under both). **Read the candidates and judge whether each insight actually relates to the entity's theme — never take top-k on trust.**

**Threshold is a floor, not a filter to game.** Reference entity bodies are terse; `--threshold 0.35` is a safe floor that keeps genuinely-related notes a higher cut would drop. Depending on the query, a `0.5` cut may return the *same* bridges or an empty set (`seed_count: 0`) — it is query-dependent, not a universal failure. So if a theme returns nothing, **re-phrase toward the KB's actual concepts** rather than assuming the threshold is the problem.

**Query `core` vocabulary, not book-shelf vocabulary.** Concepts like *antifragility / optionality / convexity* live in the **non-core** `Books/` shelf, so they return nothing under a `core` mount — phrase the theme in the core KB's own words (decision science, uncertainty, prospect theory, asymmetric payoff, ergodicity). If you genuinely want to bridge to book-shelf concepts, add `Books` to the mount (`BRAIN_READ_SCOPE=core,Books`).

Optionally also mount the sub-scope (`core,Company/<sub>`) and run `/find-connections` on the entity to make it co-visible in a graph view — but treat the theme-seeded core search as the primary finder. Mixed reads can train core hits under the current per-note learn-gate. Preserve this workflow's no-learning contract by passing `--no-track` to every search, including composed searches; verify `data/q_values.json` is byte-unchanged. If a theme returns nothing above threshold, re-phrase toward the KB's actual concepts rather than lowering rigor.

### Step 3 — Frame the bridges (entity → insight)

Present each bridge as: **entity fact → the cognitive note it instantiates → why**. Prefer bridges to `02-Permanent` / `AI Extracted Notes` (the user's own thinking) over other reference notes. Label everything as **AI-surfaced candidates for human consideration** — not endorsed links.
```markdown
## Bridges for [[Acme Corp - Trinity Enterprise Build]]
- ↔ [[<permanent note>]] — this lighthouse deal is a live instance of <the insight>. (candidate)
- ↔ [[<permanent note>]] — the $20K license ARR echoes <the pricing/optionality note>. (candidate)
```

## Verification

- A theme-seeded `core` search (at `--threshold 0.35`) on a real entity's concepts surfaces **at least one bridge to a core cognitive note**, framed as entity→insight with a reason. For a **cross-cluster** entity, `--mode static` surfaces the on-theme bridges that `--mode spreading` misses by drifting to the Identity/Dopamine hub — both modes are run and the on-theme one is kept (verified 2026-07-08: Trinity Cloud → *MOC - AI and Agents* under static, Identity/Dopamine under spreading). For a **core-cluster** entity both agree (Acme Corp → Decision Making · Prospect Theory · Loss Aversion).
- With `core,Company/<sub>` mounted, the reference entity is co-visible; **unset**, it is absent from all readers (reference stays invisible by default) — the isolation control.
- Nothing is written; `data/q_values.json` is byte-unchanged after the pass.

## This skill must refuse to

- Write or mutate any note (read-only sense).
- **Promote** a reference record into an endorsed/originated cognitive insight, or create a permanent note from a record — that is the human `encountered → endorsed` act.
- Crystallize, lifecycle-classify, or synthesis-pulse a reference note.
