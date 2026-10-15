---
name: learn-new-things
description: Continuous learning heartbeat - autonomously researches, extracts insights, and expands knowledge base
user-invocable: true
disable-model-invocation: true
argument-hint: "[interval-hours] [topic]"
automation: gated
allowed-tools: Task, Read, Write, Bash, Glob, Grep
---

# Learn New Things - Continuous Learning Heartbeat

Autonomous learning loop that periodically expands the knowledge base through research, extraction, and connection discovery. Runs locally using existing skills and sub-agents.

## Overview

This heartbeat skill implements a continuous learning cycle:
1. **Research** - Discover cutting-edge papers and developments
2. **Extract** - Pull unique insights into Document Insights
3. **Connect** - Map discoveries to existing knowledge base
4. **Commit** - Save results to dedicated git branch, return to main
5. **Rest** - Wait for next cycle

Each cycle is a complete learning session. The heartbeat never "completes" - it continuously learns.

**Git Workflow:** Each learning session commits to its own branch (`learning/YYYY-MM-DD-topic-slug`), then returns to `main`. This keeps main clean while preserving all learning for selective merging.

## Dependencies

- **Skills**: `/deep-research`, `/auto-discovery`, `/integrate-recent-notes`, `/refresh-index`
- **Sub-agents**: research-specialist, document-insight-extractor, connection-finder
- **Local Brain Search**: For semantic search and connection discovery

## Usage

```bash
/learn-new-things                    # Default: 8-hour interval, auto-select topic
/learn-new-things 4                  # 4-hour interval
/learn-new-things 8 "multi-agent systems"  # Specific topic
/learn-new-things stop               # Stop the learning loop
```

---

## State Tracking

Track learning progress in `resources/learn-new-things-log.md`:

```yaml
session_id: YYYY-MM-DD-HHMMSS
last_cycle: 2026-02-18T13:15:00
cycles_completed: 0
topics_researched: []
insights_extracted: 0
connections_discovered: 0
consecutive_errors: 0
phase: "running"  # running | paused | error
branches_created: []  # e.g., ["learning/2026-02-18-embodied-cognition"]
```

---

## STEP 1: Read State and Establish Git Ownership

Read existing state without creating or updating it yet:

```bash
cat resources/learn-new-things-log.md 2>/dev/null || echo "No existing state"
```

Parse arguments:
- `$ARGUMENTS[0]` - Interval in hours (default: 8)
- `$ARGUMENTS[1]` - Optional topic (default: auto-select)

If argument is "stop", stop scheduling and report paused; do not modify the
tracked log or switch branches merely to acknowledge stop.

Before any cycle writes (including state, index refresh and research), verify
sole-writer ownership for the entire cycle/publication/return interval using
existing runtime/operator serialization. If uncertain, stop. Require a clean
`main` branch; do not switch away from another branch automatically, stash/pop,
reset, discard, or absorb owner work. Run from the repository root:

```bash
prepare_learning_repository() {
    local changes branch
    changes=$(git status --porcelain=v1 --untracked-files=all) || return 1
    [ -z "$changes" ] || { printf '%s\n' 'Dirty repository; learning stopped.' >&2; return 1; }
    branch=$(git branch --show-current) || return 1
    [ "$branch" = main ] || { printf '%s\n' 'Start learning from clean main.' >&2; return 1; }
    git pull --ff-only origin main || return 1
    changes=$(git status --porcelain=v1 --untracked-files=all) || return 1
    [ -z "$changes" ]
}
prepare_learning_repository
```

Any failure stops before the cycle. Report visible errors without repairing or
suppressing them. Steps 2–3 are read-only until the learning branch is selected.
Keep cycle counters in the current session until Step 7 writes the branch log;
completed branch logs remain the durable record for resuming a selected session.

---

## STEP 2: Pre-Cycle Preparation

### Check Knowledge Base State

Read current analysis:

```bash
head -100 knowledge-base-analysis.md
```

Note:
- Current note counts
- Identified gaps
- Recent research sessions

---

## STEP 3: Topic Selection

### If Topic Provided

Use the provided topic from `$ARGUMENTS[1]`.

### If Auto-Select (Default)

Select topic based on knowledge base gaps and rotation. Use these strategies:

**Strategy A: Gap-Filling**
Choose from underrepresented domains in knowledge-base-analysis.md:
- Systems thinking & complexity science (12 notes - gap)
- Embodiment & interoception (14 notes - gap)
- Creativity neuroscience
- Memory consolidation
- Collective intelligence

**Strategy B: Depth-Building**
Extend existing strong domains:
- AI agent architectures (latest 2025-2026 developments)
- Neuroscience of decision-making
- Buddhism-neuroscience bridges
- Identity and belief systems

**Strategy C: Emerging Trends**
Research cutting-edge developments:
- Latest AI safety research
- New consciousness research
- Recent dopamine/motivation findings
- Multi-agent coordination

**Rotation Logic:**
```
cycle_num = cycles_completed % 3
if cycle_num == 0: Strategy A (gap-filling)
if cycle_num == 1: Strategy B (depth-building)
if cycle_num == 2: Strategy C (emerging)
```

Document selected topic and rationale.

### Select the Learning Branch Before Any Writes

Build `BRANCH_NAME` as `learning/YYYY-MM-DD-topic-slug` using a sanitized topic
slug. If that branch already exists, stop and report; never reuse/reset it or
continue on main. A new explicitly selected unique suffix can identify another
cycle. Recheck clean main, then create the branch before initializing state,
refreshing the index, or producing research:

```bash
[ -n "$BRANCH_NAME" ] || exit 1
git check-ref-format --branch "$BRANCH_NAME" >/dev/null || exit 1
case "$BRANCH_NAME" in learning/*) ;; *) exit 1 ;; esac
[ "$(git branch --show-current)" = main ] || exit 1
changes=$(git status --porcelain=v1 --untracked-files=all) || exit 1
[ -z "$changes" ] || exit 1
git switch -c "$BRANCH_NAME"
```

Stop on any failure. Once on this branch, initialize the cycle state as needed.
Track exact files written by each phase, including partial outputs. Keep a
separate list of ignored generated search/graph/cache files touched by the cycle;
these are derived local state, not publishable cycle files. Their contents still follow each underlying skill's approval gates;
this autonomous publication workflow cannot approve endorsed knowledge edits.

### Ensure Index is Fresh

Check when index was last updated:

```bash
ls -la resources/local-brain-search/data/brain.faiss
```

If older than 24 hours, refresh:

```bash
resources/local-brain-search/run_index.sh
```



---

## STEP 4: Execute Deep Research

Launch the deep-research skill with selected topic:

Use Task tool with subagent_type='research-specialist':

```
TOPIC: [Selected topic]

Conduct comprehensive research on [topic] focusing EXCLUSIVELY on the most recent research and developments (2025-2026).

SEARCH STRATEGY:
- Prioritize papers from last 12-18 months
- Search for "2025", "2026", "recent", "latest" in queries
- Check arXiv preprints, major conferences (NeurIPS, ICML, ICLR)
- Look for industry whitepapers and blog posts

OUTPUT REQUIREMENTS:
- 15-25 major papers/developments
- Full citations with DATES
- Key findings and novel contributions
- Save to: resources/[Topic-Slug]-Research-YYYY-MM-DD.md
```

**On Success:** Continue to Step 5
**On Failure:** Log error, increment `consecutive_errors`, check threshold

---

## STEP 5: Extract Insights

### Create Session Folder

Format: `YYYY-MM-DD [Topic Description]`

```bash
date '+%Y-%m-%d'
# Create: Brain/Document Insights/YYYY-MM-DD [Topic]/
```

### Launch Document Insight Extractor

Use Task tool with subagent_type='document-insight-extractor':

```
Extract unique insights from the research report for the knowledge base.

SOURCE DOCUMENT: [Path to research report from Step 4]
SESSION FOLDER: [Session folder name]

EXTRACTION GUIDELINES:
1. Focus on novel insights (paradigm shifts, counter-intuitive findings)
2. Bridge to existing hubs: Consciousness, Dopamine, Decision-Making, Identity, AI Agents, Flow
3. Quality > Quantity: 15-25 high-value insights
4. ALWAYS search for duplicates before creating notes
5. Create changelog in session folder
```

**On Success:** Count insights extracted, continue to Step 6
**On Failure:** Log error, continue to Step 6 (partial success is OK)

---

## STEP 6: Discover Connections

### Launch Connection Finder

Use Task tool with subagent_type='connection-finder':

```
Discover connections between newly extracted insights and existing knowledge base.

STARTING POINTS: All notes in session folder: [Session folder path]

CONNECTION DISCOVERY GOALS:
1. Bridge to existing 530+ permanent notes
2. Link to 6 primary thematic hubs
3. Find cross-domain consilience opportunities
4. Similarity thresholds: 0.65-0.85

OUTPUT:
- Connection map for new insights
- Synthesis opportunities identified
- Changelog: CHANGELOG - Connection Discovery Session YYYY-MM-DD.md in Brain/05-Meta/Changelogs/
```

**On Success:** Count connections, continue to Step 7
**On Failure:** Log error, continue to Step 7

---

## STEP 7: Update State & Log

### Update State File

Write to `resources/learn-new-things-log.md`:

```markdown
# Learn New Things - Session Log

**Session ID:** [session_id]
**Last Updated:** [timestamp]
**Phase:** running

## Statistics
- Cycles completed: [N]
- Topics researched: [list]
- Total insights extracted: [N]
- Total connections discovered: [N]
- Consecutive errors: [N]

## Latest Cycle
- **Started:** [timestamp]
- **Topic:** [topic]
- **Research report:** [path]
- **Session folder:** [path]
- **Insights extracted:** [N]
- **Connections found:** [N]
- **Status:** [success/partial/error]

## Cycle History
| Date | Topic | Insights | Connections | Status |
|------|-------|----------|-------------|--------|
| YYYY-MM-DD | [topic] | [N] | [N] | [status] |
```

### Log to Master Changelog

Add entry to `Brain/CHANGELOG.md`:

```markdown
## YYYY-MM-DD - Learning Heartbeat Cycle [N]

- **Topic:** [topic]
- **Insights extracted:** [N]
- **Connections discovered:** [N]
- **Session folder:** [[Document Insights/YYYY-MM-DD Topic]]
```

---

## STEP 8: Git Commit & Branch Management

The learning branch was selected before any writes. Never stash/pop or move
unfinished results onto main. Complete the cycle log (including branch name and
success/partial/error outcome) before staging. Inspect all tracked diffs and
full new-file contents against actual phase writes. Only known cycle-owned
outputs may be published, including verified partial outputs after a phase
failure. If ownership, writer exclusion, or an underlying approval is unclear,
stop publication and preserve every file and the index on this branch.

### Stage Exact Verified Outputs

Populate `job_paths` with exact verified file paths, including deleted paths and
both sides of a rename. Exclude ignored generated data (including
`resources/local-brain-search/data/` and `resources/brain-graph/data/`); never
force-add it. No directory selection, wildcard changelogs, or blanket
index-data staging. Run this guard before staging and again before committing;
it rejects any changed or staged file outside that selection without altering
owner work:

```bash
python3 - "${job_paths[@]}" <<'PY_GIT'
import os
import subprocess
import sys
selected = {os.fsencode(path) for path in sys.argv[1:]}
if not selected or len(selected) != len(sys.argv) - 1:
    raise SystemExit("Expected a nonempty unique list of cycle-owned paths")
def paths(*args):
    return set(filter(None, subprocess.check_output(["git", *args]).split(b"\0")))
changed = paths("diff", "HEAD", "--name-only", "--no-renames", "-z")
staged = paths("diff", "--cached", "--name-only", "--no-renames", "-z")
untracked = paths("ls-files", "--others", "--exclude-standard", "-z")
if (changed | staged | untracked) - selected:
    raise SystemExit("Unexpected owner paths; preserve state and stop publication")
PY_GIT
```

A successful path guard does not establish ownership of bytes: compare the
fresh full contents/diff and file modes with the retained inspected output,
including any staged versus working differences. Any change requires another
inspection; never overwrite an owner's staged version to make a check pass.
After the guard and content check succeed:

```bash
[ "${#job_paths[@]}" -gt 0 ] || exit 1
git --literal-pathspecs add -- "${job_paths[@]}"
git diff --cached --binary --full-index
```

Re-run the guard and verify that the cached patch matches exactly the inspected
cycle output and no writer has intervened. Write the actual topic/cycle summary
and runtime attribution to a temporary message file outside the repository:

```bash
git commit --file "$commit_message_file"
```

If no changes exist, report that and skip commit/PR creation. If commit fails,
stop and retain partial output/index on the learning branch. After a successful
commit, push only this branch:

```bash
git push -u origin "$BRANCH_NAME"
```

If push fails, stop on the learning branch, report the local commit and failed
publication, and do not continue into another cycle or pretend it was pushed.

### Create Pull Request

Create a PR for review and selective merging:

```bash
gh pr create --title "Learning: [Topic] - Cycle [N]" --body "$(cat <<'EOF'
## Learning Session Summary

**Topic:** [topic]
**Date:** YYYY-MM-DD
**Cycle:** [N]

### Research Results
- Papers analyzed: [N]
- Insights extracted: [N]
- Connections discovered: [N]

### Files Added
- Research report: `resources/[filename]`
- Session folder: `Brain/Document Insights/[Session-Folder]/`
- Changelogs updated

### Key Discoveries
1. [Most significant insight]
2. [Cross-domain connection found]
3. [Synthesis opportunity identified]

### Review Checklist
- [ ] Insights are high quality and non-redundant
- [ ] Connections to existing notes are valid
- [ ] No sensitive or incorrect information

---
🤖 Generated by `/learn-new-things` heartbeat
EOF
)"
```

Report the actual PR URL and publication outcome in the cycle response. Do not
modify the tracked state file after committing merely to record the URL or
future checkout status: that would dirty main or create uncommitted carryover.
The committed cycle log remains on the learning branch; use its branch/commit
reference when resuming rather than assuming it has been merged into main.

If PR creation fails, report that the branch was pushed but no PR was created.
Do not automatically retry or start another cycle. A clean return to main may
still proceed, but the learning loop stays paused until that outcome is handled.

### Return to Main Only with Clean State

```bash
changes=$(git status --porcelain=v1 --untracked-files=all) || exit 1
[ -z "$changes" ] || exit 1
git switch main || exit 1
changes=$(git status --porcelain=v1 --untracked-files=all) || exit 1
[ -z "$changes" ] || exit 1
```

Git cleanliness does not prove ignored derived data matches main: caches built
on the learning branch survive checkout. Report that a refresh against main is
needed before reusing affected search/graph state or starting the next cycle.
When authorized, use the existing `/refresh-index` procedure and its completion,
graph and daemon freshness checks; verify the Git tree remains clean afterward.
Otherwise pause and leave the derived-state limitation explicit. Do not
force-add, silently delete, or claim branch-derived caches represent main.
No new cross-branch refresh/recovery service is introduced here.

Any unexpected dirty state or checkout failure pauses the loop immediately.
Preserve the branch, partial outputs and index for review; do not auto-stash,
reset, discard, or continue on main after a failed branch creation. Report
actual local branch/commit, remote publication and return status separately.

---

## STEP 9: Error Handling

### Check Error Threshold

If `consecutive_errors >= 3` OR any Git ownership/preflight/publication/return gate failed:

```markdown
## LEARNING HEARTBEAT PAUSED

**Error:** 3 consecutive cycles failed
**Last topic:** [topic]
**Last error:** [error description]

Manual intervention required. Check:
1. Network connectivity for research
2. Local Brain Search index health
3. Disk space for new notes

To resume: `/learn-new-things`
```

Report phase `error` and stop. Preserve Git-failure state without new log writes;
record non-Git phase failures in Step 7 before publication.

### Reset on Success

Finalize these counters in Step 7 before publication; do not write them on main
after returning. If cycle completes successfully:
- Set `consecutive_errors = 0`
- Increment `cycles_completed`
- Add topic to `topics_researched`

---

## STEP 10: Cycle Summary

Display cycle summary:

```markdown
## Learning Cycle [N] Complete

**Topic:** [topic]
**Duration:** [time]

### Results
- Research papers analyzed: [N]
- Unique insights extracted: [N]
- Connections discovered: [N]

### Key Discoveries
1. [Most significant insight]
2. [Cross-domain connection]
3. [Synthesis opportunity]

### Files Created
- Research report: `resources/[filename]`
- Session folder: `Brain/Document Insights/[folder]`
- Changelogs updated

### Git
- **Branch:** `learning/YYYY-MM-DD-topic-slug`
- **Pushed to remote:** yes
- **Pull Request:** [PR URL]
- **Returned to main:** yes

### Next Cycle
- Scheduled in: [interval] hours
- Suggested topic: [next topic based on rotation]
```

---

## STEP 11: Schedule Next Cycle

**Codex:** Completing one cycle does not schedule another. Use an existing,
configured native or platform scheduling interface only when available and
authorized, and require its successful confirmation before reporting the next
cycle scheduled. Otherwise report the completed cycle and that continuation is
unscheduled. Do not use a detached shell sleep or another provider CLI as a
scheduler substitute. A confirmed schedule is not evidence that a future cycle
has run; report actual delivery separately. Preserve the cycle's Git ownership,
publication and human-decision gates on every later execution.

**Claude Code timer path:** Set timer for next learning cycle:

```bash
INTERVAL_HOURS=${1:-8}
INTERVAL_SECONDS=$((INTERVAL_HOURS * 3600))
sleep $INTERVAL_SECONDS && echo "HEARTBEAT: learn-new-things ready for next cycle"
```

Run with `run_in_background: true`.

**Important:** The heartbeat only continues if you respond to "HEARTBEAT: learn-new-things" prompt.

---

## Stopping the Loop

**Automatic pause:**
- 3+ consecutive errors

**Manual stop:**
- Run `/learn-new-things stop`
- Don't respond to "HEARTBEAT:" prompts
- Say "stop learning"

**Resume:**
- Run `/learn-new-things` again

---

## Configuration

### Modifiable Parameters

Edit this skill to adjust:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `interval_hours` | 8 | Hours between cycles |
| `max_errors` | 3 | Consecutive errors before pause |
| `insights_per_cycle` | 15-25 | Target insight count |
| `connection_threshold` | 0.65-0.85 | Similarity range |

### Topic Rotation

The rotation pattern can be customized:

```
Cycle 0, 3, 6, 9... → Gap-filling (underrepresented domains)
Cycle 1, 4, 7, 10... → Depth-building (strong domains)
Cycle 2, 5, 8, 11... → Emerging trends (cutting-edge)
```

---

## Examples

### Example 1: Start with Defaults

```
/learn-new-things

→ Runs a learning cycle with an 8-hour continuation interval
→ Auto-selects topic based on gaps
→ Runs research → extract → connect
→ Reports next cycle scheduled only after the Step 11 scheduling confirmation
→ Otherwise reports continuation unscheduled
```

### Example 2: Specific Topic, Faster Cycle

```
/learn-new-things 4 "embodied cognition"

→ 4-hour interval
→ Researches embodied cognition specifically
→ Useful for filling known gap quickly
```

### Example 3: Check Status

```
# Set learning_ref to the branch or commit reported by the latest cycle.
git show "${learning_ref}:resources/learn-new-things-log.md"

→ See cycles completed, topics covered
→ Review error history
→ Check the cycle response or configured scheduler for confirmed next execution
```

### Example 4: Stop Learning

```
/learn-new-things stop

→ Pauses the heartbeat
→ Preserves state for later resume
→ No new cycles scheduled
```

---

## Managing Learning Branches & Pull Requests

Each learning cycle creates a branch (`learning/YYYY-MM-DD-topic-slug`) and opens a Pull Request. This provides a formal review workflow for learning results.

### List Open Learning PRs

```bash
gh pr list --search "Learning:" --state open
```

### Review a Learning PR

```bash
# View PR details
gh pr view [PR-NUMBER]

# See files changed
gh pr diff [PR-NUMBER]

# View in browser
gh pr view [PR-NUMBER] --web
```

### Merge Valuable Learning

When learning results look good:

```bash
# Merge via CLI
gh pr merge [PR-NUMBER] --merge

# Or merge via GitHub web interface for more control
gh pr view [PR-NUMBER] --web
```

### Close Without Merging

If a learning session produced low-quality results:

```bash
# Close PR without merging
gh pr close [PR-NUMBER]

# Optionally delete the branch too
gh pr close [PR-NUMBER] --delete-branch
```

### Bulk Operations

```bash
# List all open learning PRs
gh pr list --search "Learning:" --state open

# List all learning branches (including those without PRs)
git branch -r | grep "learning/"

# Delete all merged learning branches (cleanup)
git branch -r --merged main | grep "learning/" | xargs -I {} git push origin --delete {}
```

### Why This Pattern?

- **Formal review**: PRs provide structured review with descriptions and checklists
- **Main stays clean**: Learning only enters main after explicit approval
- **Easy comparison**: GitHub diff view shows exactly what was learned
- **Discussion**: Can comment on specific insights or flag issues
- **Audit trail**: PR history shows decisions about what was accepted/rejected
- **Notifications**: Get notified when learning sessions complete

---

## Integration with Other Skills

| Skill | Relationship |
|-------|--------------|
| `/deep-research` | Core research engine (called each cycle) |
| `/auto-discovery` | Can run separately for connection-only cycles |
| `/integrate-recent-notes` | Runs after learning to connect new notes |
| `/refresh-index` | Called before each cycle |
| `/analyze-kb` | Run periodically to update gap analysis |

---

## The Learning Pattern

```
┌────────────────────────────────────────────────────────────────────────────┐
│                          LEARNING HEARTBEAT                                 │
│                                                                             │
│  ┌────────┐   ┌────────┐   ┌────────┐   ┌────────┐   ┌─────────┐   ┌─────┐ │
│  │ SELECT │──▶│RESEARCH│──▶│EXTRACT │──▶│CONNECT │──▶│ COMMIT  │──▶│ PR  │ │
│  │ TOPIC  │   │ PAPERS │   │INSIGHTS│   │ TO KB  │   │ BRANCH  │   │     │ │
│  └────────┘   └────────┘   └────────┘   └────────┘   └─────────┘   └──┬──┘ │
│       │                                                               │     │
│       │                                                       ┌───────▼───┐ │
│       │                                                       │ RETURN TO │ │
│       │                                                       │   MAIN    │ │
│       │                                                       └─────┬─────┘ │
│       │                                                             │       │
│       └──────────────────CONFIRMED NEXT CYCLE──────────────────────┘       │
│                                                                             │
└────────────────────────────────────────────────────────────────────────────┘

Each cycle:
1. Check gaps in knowledge base
2. Select topic (gap-fill / depth / emerging)
3. Research latest papers (15-25)
4. Extract unique insights (15-25)
5. Discover connections to existing notes
6. Commit to learning/YYYY-MM-DD-topic branch
7. Push branch, create Pull Request
8. Return to main; confirm scheduling or report continuation unscheduled

Continuous learning → Ever-expanding knowledge base
PRs enable formal review → Selective merging via GitHub
```

---

## Completion Checklist

Each cycle should complete:

- [ ] Topic selected with rationale
- [ ] Research report generated (15-25 papers)
- [ ] Session folder created in Document Insights
- [ ] Insights extracted with deduplication
- [ ] Connections discovered to existing notes
- [ ] State file updated with cycle results
- [ ] Master changelog updated
- [ ] Learning branch created and pushed
- [ ] Pull request created
- [ ] Returned to main branch
- [ ] Next cycle scheduled (if continuing)

---

## State Dependencies

| Source | Location | Read | Write | Description |
|--------|----------|------|-------|-------------|
| State file | `resources/learn-new-things-log.md` | ✓ | ✓ | Cycle tracking |
| KB analysis | `knowledge-base-analysis.md` | ✓ | | Gap identification |
| Research reports | `resources/` | | ✓ | Generated reports |
| Document Insights | `Brain/Document Insights/` | | ✓ | Extracted insights |
| Changelogs | `Brain/05-Meta/Changelogs/` | | ✓ | Session logs |
| Master changelog | `Brain/CHANGELOG.md` | ✓ | ✓ | Summary entries |
| Local Brain Search | `resources/local-brain-search/` | ✓ | | Index, search |

---

**Remember:** This is a continuous learning engine. Each cycle makes the knowledge base smarter. The goal is not completion - it's perpetual growth and integration.
