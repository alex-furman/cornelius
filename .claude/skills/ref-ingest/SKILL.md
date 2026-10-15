---
name: ref-ingest
description: The single entry point for incoming information of ANY kind about a reference entity (a person, org, product, engagement, or watched competitor). Extracts entity facts, RESOLVES them to the one existing canonical note (never duplicating), reconciles new-vs-old, and upserts (overwrite body, re-stamp as_of, append Change Log), then reindexes. Extends manage-reference-data with entity resolution + reconciliation + the market-vs-CRM automation split. Company is the default scope. NEVER writes any provenance but reference; NEVER crystallizes/lifecycle-classifies/promotes a record into an insight.
automation: gated
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion, Skill]
user-invocable: true
argument-hint: "[scope=Company] <entity name or the incoming info> [--source <where it came from>] [--no-reindex]"
metadata:
  version: "1.1"
  created: 2026-07-08
  author: Cornelius
  changelog:
    - "1.1: Fix — Step 3 named a phantom agents-as-product/ sub-scope; type: agent notes live in products/. Corrected."
    - "1.0: Initial version — extract→resolve→reconcile→gate→upsert entry point for the Company reference family; overwrite-only market branch invariant; composes ref-supersede; grows manage-reference-data"
---

# Ref Ingest

> ℹ️ **First, set expectations:** before anything else, print one short line with this skill's version and its most recent change — the top entry of `metadata.changelog` above — e.g. `ref-ingest v1.0 — recent: initial version`. Then proceed.

The **one operation every input funnels through** for a reference scope: `incoming info → resolve → reconcile → upsert`. It grows the manual single-upsert `manage-reference-data` with the two load-bearing hard parts — **entity resolution** (is this new "Reply" the existing `Reply.io`?) and **reconciliation** (new fact contradicts old → overwrite / supersede-with-history / flag) — plus the **automation split by scope**.

**Read first (authoritative — this skill enforces, does not restate):**
- `resources/layered-brains/COMPANY-BRAIN-SCHEMA.md` → "The update model", "The two axes" (sub-scope routing + `type:`/`relationship:` enums), "Automation boundary — split by scope".
- `resources/layered-brains/REFERENCE-SCOPE-SCHEMA.md` → the reference-kind frontmatter contract.
- `.claude/skills/manage-reference-data/SKILL.md` → the seed upsert (Step 0 scope check + the frontmatter template). This skill is its richer successor; it does not duplicate the contract.

## Composes

- `/ref-supersede` — when reconciliation finds a **validity transition** that needs a prior snapshot (contract renewal, role/price change), hand off instead of overwriting. **Never invoked on the market/autonomous branch** (see the invariant).

## State Dependencies

| Source | Location | Read | Write | Description |
|--------|----------|------|-------|-------------|
| Company family | `Brain/Company/{people,orgs,products,engagements,market}/*.md` | ✓ | ✓ | Entity notes (one note = one entity) |
| Scope registry | `resources/local-brain-search/memory_config.py` | ✓ | | Confirm reference-kind |
| LBS index | `resources/local-brain-search/data/` | ✓ | ✓ (reindex) | FAISS + graph; reindexed after a write |
| Search wrappers | `resources/local-brain-search/run_search.sh` | ✓ | | Entity-resolution search under a `core,Company` mount |

## The automation split (load-bearing)

| Sub-scope | Writer | This skill |
|-----------|--------|------------|
| `market/` (watched competitors/ecosystem) | autonomous | **auto-overwrite, no gate** — reference facts sit outside the `encountered→endorsed` gate |
| `people/ orgs/ products/ engagements/` (transacted CRM) | curated | **human-gated** — present the diff, get approval before writing |

**Invariant (what makes any autonomous caller safe):** the `market/` branch is **overwrite-only** — it never opens an approval gate and **never calls `/ref-supersede`**. A validity transition in `market/` that would need a snapshot is *flagged for a human `ref-supersede`*, not auto-run. So a scheduled caller (e.g. `ref-refresh`, or domain-watch in 9e) that routes market items here always takes a gate-free path.

---

## Process

### Step 1 — Resolve the scope + confirm reference-kind

```bash
cd resources/local-brain-search
SCOPE="${scope:-Company}"
./venv/bin/python - "$SCOPE" <<'PY'
import sys, memory_config as mc
f = sys.argv[1]
print("kind:", mc.scope_kind(f), "| is_reference:", mc.is_reference_scope(f))
PY
```
If `is_reference` is False → **stop** (this skill only writes reference scopes). See the schema doc's "Adding a new reference scope".

### Step 2 — Extract candidate entity facts

From the incoming info (the user in conversation · a document/contract/deck/call · a domain-watch market signal · another agent's report), pull the **atomic facts about one real-world entity**: display name + aliases, `type:`, the relation to us (`relationship:`), body facts, and any term-bearing fact (a contract window, a role start, a price effective date).

### Step 3 — Route to the sub-scope (watch vs transact)

Apply the partition rule from COMPANY-BRAIN-SCHEMA "The two axes":
- an entity you **watch** (competitor, competitor product, ecosystem player) → `market/`
- an entity you **own or transact with** (self, client, prospect, partner, vendor, your offering, internal agent, a deal) → `people/ orgs/ products/ engagements/` by `type:`. The internal agent workforce (`type: agent`) lives in `products/` alongside own products — there is no separate `agents/` sub-scope.
- `type:`/`relationship:` values MUST come from the schema doc's enum (person·organization·product·agent·engagement·interaction × the relationship axis). Never invent a value.

### Step 4 — ENTITY RESOLUTION (never duplicate)

Find the one canonical note this fact belongs to before writing:
```bash
# semantic: does an entity like this already exist in the family?
BRAIN_READ_SCOPE=core,Company resources/local-brain-search/run_search.sh "<entity name + a distinctive fact>" --limit 8 --json
# exact/alias: title + body match
grep -rilE "<name>|<alias1>|<alias2>" Brain/Company/
```
- **Match found** → this is an *update* to that note. Use its exact path.
- **Ambiguous** (2+ plausible matches, e.g. "Reply" vs "Reply.io") → present the candidates and ask which entity this is (`AskUserQuestion`); do NOT guess a new note into existence.
- **No match** → genuinely new entity → *add*.

### Step 5 — RECONCILIATION (new fact vs old)

Compare the incoming fact to the note's current body:
| Situation | Action |
|-----------|--------|
| New fact **corrects/refreshes** an existing fact (same validity window) | **overwrite** the body (Step 6) |
| A **validity window closed** and a full prior snapshot matters (contract renewed, role changed, price re-termed) | hand to **`/ref-supersede`** — *CRM only; on `market/` flag for a human instead* |
| New fact **contradicts** old with no clear winner | **flag** — surface both, ask; do not silently overwrite |

### Step 6 — Automation gate + upsert

- **`market/`** → proceed (no gate). **CRM sub-scopes** → show the before/after diff and get explicit approval (`AskUserQuestion`) before writing.
- Write the note with the reference frontmatter contract (copy the template from `manage-reference-data` Step 2 — do not restate it here). On update: **overwrite the body** (current truth), preserve `created`/`created_by`, re-stamp `as_of` + `updated` to today, bump `updated_by` to your model. Append a `## Change Log` line:
  ```markdown
  ## Change Log
  - 2026-07-08 — <what changed> (source: <where it came from>)
  ```
- **Going forward only:** for a term-bearing fact, add `valid_from:`/`valid_until:`. **Do NOT** backfill these onto notes that lack them — incremental adoption.

### Step 7 — Reindex (unless deferred)

```bash
cd resources/local-brain-search && ./run_index.sh && ./run_daemon.sh restart   # daemon on :7437, RESTART not reload
```
Content-hash detection → a changed note triggers a **full FAISS rebuild** (minutes). Reference notes are **BDG-excluded**, so **no `run_brain_graph.sh bootstrap` is needed**. If invoked with `--no-reindex` (batch mode, e.g. by `ref-refresh` over many market items), **skip this step** and let the batch caller reindex once at the end.

---

## Verification

- **Round-trip:** after an add/overwrite + reindex, the entity **surfaces under a mount** and is **absent unmounted**:
  ```bash
  BRAIN_READ_SCOPE=core,Company resources/local-brain-search/run_search.sh "<entity>" --limit 5 --json   # present
  resources/local-brain-search/run_search.sh "<entity>" --limit 5 --json                                  # absent (core default)
  ```
- **Learn-gate held:** reference identifiers never enter `data/q_values.json`; core hits in a mixed read can still train. Use `--no-track` for a verification search that must leave learning state byte-unchanged.
- **Audit trail:** the note has a new `## Change Log` line; the body is the current truth (no append-only drift); `as_of` = today.
- **No duplicate:** exactly one note exists for the entity (`grep -ril "<name>" Brain/Company/` returns one canonical file).

## This skill must refuse to

- Write into a non-reference / core / cognitive folder, or set any `provenance` but `reference`.
- **Create a duplicate** entity note when resolution finds (or is unsure of) an existing one.
- **Auto-supersede or gate-skip on a CRM sub-scope**, or run `/ref-supersede` on the `market/` branch.
- Crystallize, lifecycle-classify, synthesis-pulse, or **promote a record into an endorsed cognitive insight** — that crossing stays the human `encountered → endorsed` act.
