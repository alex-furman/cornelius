---
name: scheduled-run
description: Wrapper for scheduled playbooks - handles git sync before and after execution
argument-hint: <playbook-name>
automation: autonomous
allowed-tools: Bash, Skill
user-invocable: true
---

# Scheduled Run

Wrapper that runs any playbook with git sync. Use this for all scheduled executions to ensure:
- Latest changes pulled before running
- All changes committed and pushed after running

## Purpose

Ensures scheduled playbooks on Trinity stay in sync with the GitHub repository.

## State Dependencies

| Source | Location | Read | Write | Description |
|--------|----------|------|-------|-------------|
| Git repo | `.git/` | ✓ | ✓ | Pull before, commit+push after |
| Playbook output | varies | | ✓ | Whatever the playbook produces |

## Arguments

`$ARGUMENTS` = The playbook name to run (e.g., `refresh-index`, `coherence-sweep`)

## Process

### Step 1: Require a Clean, Quiescent Repository

Use this wrapper only when the repository has one writer for the whole
pull/playbook/commit/push interval. Verify the existing runtime/operator
serialization; different scheduled start minutes do not establish this. If
another writer may be active or ownership is unclear, stop and report rather
than adding a lock service or guessing which files belong to this job.

Reject staged, unstaged **and untracked** owner work before pulling. A successful
`git pull --rebase` alone does not prove a clean tree. Do not stash, reset,
delete, stage or commit pre-existing owner changes to make the check pass.

```bash
require_clean_tree() {
    local changes
    changes=$(git status --porcelain=v1 --untracked-files=all) || return 1
    if [ -n "$changes" ]; then
        printf '%s\n' 'Repository is dirty; scheduled run stopped.' >&2
        return 1
    fi
}
require_clean_tree && git pull --rebase && require_clean_tree
```

Any failure stops the wrapper before the playbook. If a rebase conflicts, report
it; do not run the playbook, resolve conflicts automatically or discard files.

### Step 2: Run the Playbook

Scheduled playbooks run at the **core** read-scope by default. `BRAIN_READ_SCOPE`
is unset here, so every `run_search.sh` / `run_connections.sh` call inside the
playbook fails closed to `core` (the fingerprint) - which is the intended scope
for incubation-loop, refresh-index, coherence-sweep, gjopen-refresh, and
ai-crystallize. Perception/cross-domain playbooks that legitimately need non-core
content (e.g. **domain-watch**) set a wider `BRAIN_READ_SCOPE=...` inline on their
own search commands; do not widen it here. (Setting `export BRAIN_READ_SCOPE=core`
here would be a redundant fail-safe - the default is already core - and would not
propagate across the separate Bash invocations a playbook makes anyway.)

Invoke the specified playbook using the Skill tool:

```
Skill: $ARGUMENTS
```

Wait for completion.

### Step 3: Check for Changes

```bash
git status --porcelain
```

If no changes, skip to completion.

### Step 4: Commit Only This Playbook's Changes

Compare the complete status and diff with the playbook's actual writes,
including partial output if it failed. Inspect new files as well as tracked
diffs. If an unexpected file or another writer appears, stop Git publication
and report the ambiguity; preserve every file and the index. A clean start is
not proof that every later file belongs to the playbook.

List the exact job-owned file paths, including both paths for a rename and
tracked deletion paths. Stage only that list with literal path handling:

```bash
# Populate this array with the exact verified job-owned files, not a directory
# or a glob. Pass filenames as quoted data.
[ "${#job_paths[@]}" -gt 0 ] || exit 1
git --literal-pathspecs add -- "${job_paths[@]}"
git diff --cached --name-status --no-renames
git diff --cached --binary --full-index
```

Before committing, verify every staged path and byte belongs to that output
list, and that no file changed during inspection. Otherwise stop. Do not use
`git add -A`. Preserve the existing partial-output policy, but never manufacture
missing human approval for an underlying playbook's gated action.

Write the commit message to a temporary file outside the repository. Use the
actual playbook name and current timestamp, not an unexpanded quoted heredoc.
Attribute it to the runtime/model actually executing the task; do not add a
Claude identity to a Codex execution or invent an email/trailer. Then commit:

```bash
git commit --file "$commit_message_file"
```

### Step 5: Push to Remote

```bash
git push
```

## Error Handling

| Error | Recovery |
|-------|----------|
| Pull fails (conflicts) | Abort, log error, do not run playbook |
| Playbook fails | Still attempt commit/push of verified job-owned partial changes, only while the clean-start, sole-writer and approval boundaries hold; otherwise stop and preserve them |
| Push fails | Log error, changes remain local |

## Autonomy Guide

**What should be scheduled (mechanical, no creative decisions):**

| Schedule | Command | Cron (UTC) | Timeout | Purpose |
|----------|---------|------------|---------|---------|
| Incubation Loop | `/scheduled-run incubation-loop` | `0 * * * *` | 45m | Hourly thinking on active topics (self-seeds via starvation floor when empty) — the :00 anchor |
| Domain Watch | `/scheduled-run domain-watch` | `30 */2 * * *` | 30m | Every 2h at :30 — perception layer; auto-activates topics (incl. starvation floor) |
| GJ Open Refresh | `/scheduled-run gjopen-refresh` | `30 1 * * *` | 30m | 01:30 daily — external forecasting data **[disabled]** |
| Refresh Index | `/scheduled-run refresh-index` | `30 3 * * *` | 40m | 03:30 daily — FAISS + BDG bootstrap |
| Coherence Sweep | `/scheduled-run coherence-sweep` | `30 5 * * 1` | 30m | Mon 05:30 — staleness/health briefing **[disabled]** |
| AI Crystallize | `/scheduled-run ai-crystallize` | `30 7 * * 1` | 30m | Mon 07:30 — AI synthesis of converged topics → `AI Crystallizations/` (ai-inferred) |
| Git Sync | (raw git) | `45 */6 * * *` | 10m | :45 every 6h — redundant with scheduled-run git hygiene **[disabled]** |

**Spacing rule:** incubation holds the hourly `:00` slot; every other job runs at `:30` of an **odd** hour (domain-watch only runs even hours), so no two jobs start in the same minute. This does **not** prevent overlap or Git collisions: a 45-minute run can overlap the next half-hour job. The sole-writer check above still applies. Timeouts match each skill's work budget (the 15-min platform default is too short for FAISS rebuilds and multi-domain scans).

**What should NOT be scheduled (requires human judgment):**

| Skill | Why manual |
|-------|-----------|
| `/auto-discovery` | Generates new connections - that's intellectual work |
| `/deep-research` | Creates new content from external sources |
| `/detect-tensions` | Productive contradictions need human interpretation |
| `/compute-lifecycle` | Promotions to framework status need human decision |
| `/integrate-recent-notes` | Integration choices are creative decisions |
| `/analyze-kb` | Useful on-demand, not worth weekly automation |

**The principle:** Automate measurement and maintenance. Never automate creation or judgment *into the endorsed knowledge base*. The refinement (2026-06): autonomous synthesis is permitted when its output is **segregated and tagged `ai-inferred`** - the starvation floor self-seeds topics, and `ai-crystallize` writes AI conclusions to `Brain/05-Meta/AI Crystallizations/` (never `02-Permanent/`). The gate that stays human is the **endorsement act**: only the user promotes an ai-inferred conclusion into permanent, endorsed knowledge via `/manage-thinking-topics crystallize`.

The coherence sweep is the one weekly artifact that earns automation - it's a Monday briefing that says "here's what changed, here's what might be stale, here's what's evolving." You glance at it, act on what matters, ignore the rest.

## Completion Checklist

- [ ] Repository was clean (including untracked files) and sole-writer ownership established
- [ ] Git pull completed successfully
- [ ] Playbook executed
- [ ] Changes detected and committed (if any)
- [ ] Changes pushed to remote
