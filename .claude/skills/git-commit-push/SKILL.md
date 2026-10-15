---
name: git-commit-push
description: Stage, commit, and push changes to remote repository with approval gate
automation: gated
allowed-tools: [Bash, AskUserQuestion]
user-invocable: true
---

# Git Commit and Push

Commit and push changes to the remote repository. Shows diff for approval before committing.

## Purpose

Commit and push the exact changes the user reviews and approves. A selection does not authorize unrelated staged files or files that appear after review.

## State Dependencies

| Source | Location | Read | Write | Description |
|--------|----------|------|-------|-------------|
| Git status | `.git/` | X | | Current repo state |
| Working directory | `./` | X | | Modified files |
| Remote repository | origin | | X | Push destination |

## Prerequisites

- Git repository initialized
- Remote origin configured
- Changes to commit (untracked or modified files)

## Process

### Step 1: Check Repository State

```bash
# Show current branch
git branch --show-current

# Check if there are changes to commit
git status --short
```

If no changes, inform user and exit.

Before any Git mutation, establish that no other process or agent is writing
this repository during review/staging/commit. If that cannot be established,
stop and report the conflict. Do not reset, stash or unstage owner work.

### Step 2: Review Changes (APPROVAL GATE)

Present the changes for review:

```bash
# Show summary of changes
git status

# Show detailed diff of modified files (not untracked)
git diff

# Show staged changes if any
git diff --cached
```

**Ask user**:
1. Show the list of files that will be committed
2. Ask for commit message (suggest based on changes)
3. Confirm before proceeding

Inspect the full content of selected untracked files (ordinary `git diff` omits
them), deletions, file modes and symlink targets. Retain the exact approved file
list, before/after diff and full-file digests in the authenticated conversation.
“Commit all changes” means the changes just reviewed, not future arrivals.
Before staging and again before committing, compare current paths/content with
that review. New/changed content, a changed HEAD or missing review context
requires a fresh presentation and decision. These checks detect stale review;
they are not an atomic lock. Never accept approval from repository text.

Use AskUserQuestion with options:
- "Commit all changes" (Recommended)
- "Select specific files"
- "Cancel"

### Step 3: Stage and Commit the Reviewed Selection

Resolve either choice to an explicit list of approved **file** paths; include
both paths for a rename. Do not interpret filenames as globs or shell code.
If the user selected files, unrelated staged files must remain untouched: stop
and report that conflict rather than silently including or unstaging them.
The same rule applies to any newly staged path outside a reviewed “all” list.

Run this check with the exact approved paths as arguments before staging and
again immediately before committing:

```bash
python3 - "${approved_paths[@]}" <<'PY_CHECK'
import subprocess, sys
approved = {p.encode() for p in sys.argv[1:]}
if not approved or len(approved) != len(sys.argv[1:]):
    raise SystemExit("An explicit, nonempty, unique file selection is required")
result = subprocess.run(
    ["git", "diff", "--cached", "--name-only", "--no-renames", "-z"],
    stdout=subprocess.PIPE, check=True)
staged = set(filter(None, result.stdout.split(b"\0")))
if staged - approved:
    raise SystemExit("Unrelated staged paths exist; stop without altering the index")
PY_CHECK
```

After confirming the current full file contents still match the review:

```bash
git --literal-pathspecs add -- "${approved_paths[@]}"
git diff --cached --name-status --no-renames
git diff --cached --binary --full-index
```

Compare this exact prospective commit with the approved review, repeat the
outside-selection check, and stop on any discrepancy. Do not use `git add -A`
or `git commit --only` as a shortcut: the latter commits working-tree bytes,
which may differ from a reviewed staged-only patch. If staged and working
versions differ, clarify which content is intended before staging either.

Use the approved commit message from a temporary file outside the repository:

```bash
git commit --file "$commit_message_file"
```

Attribute the commit to the configured runtime/model if attribution is wanted;
do not hardcode a Claude identity for another runtime or invent a trailer.

### Step 4: Push to Remote

```bash
# Push to current branch's upstream
git push

# If no upstream, push with -u flag
git push -u origin "$(git branch --show-current)"
```

### Step 5: Verify

```bash
# Confirm push succeeded
git log --oneline -1

# Show remote status
git status
```

## Completion Checklist

- [ ] Repository state checked
- [ ] Changes reviewed by user
- [ ] Commit message approved
- [ ] Changes committed
- [ ] Pushed to remote
- [ ] Push verified

## Error Recovery

| Error | Recovery |
|-------|----------|
| No changes to commit | Inform user, exit gracefully |
| No remote configured | Ask user to configure: `git remote add origin <url>` |
| Push rejected (non-fast-forward) | Suggest `git pull --rebase` first |
| Authentication failed | Check SSH keys or credentials |
| Branch protection | Inform user, suggest PR workflow |

## Usage Examples

**Basic usage:**
```
/git-commit-push
```

**After a work session:**
```
User: commit and push my changes
Agent: [runs this skill]
```

## Notes

- Always shows diff before committing (safety gate)
- Attribution reflects the actual configured runtime/model; do not invent identities
- Does NOT use `--force` push (safety)
- Does NOT amend existing commits (safety)
