"""Execute canonical Git safety recipes against disposable local bare remotes.

These test Git effects, not a model supplying or respecting human approval.
"""
import os
from pathlib import Path
import re
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def recipe(skill, marker):
    text = (ROOT / ".claude/skills" / skill / "SKILL.md").read_text()
    blocks = [block for block in re.findall(r"```bash\n(.*?)```", text, re.S) if marker in block]
    if len(blocks) != 1:
        raise AssertionError("Expected one executable recipe: " + marker)
    return blocks[0]


class GitWorkflowRecipes(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="git workflow ")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.env = dict(os.environ, GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL="/dev/null", GIT_TERMINAL_PROMPT="0")
        self.run_cmd(["git", "init", "--bare", "remote.git"], self.root)
        self.remote = self.root / "remote.git"
        self.run_cmd(["git", "clone", str(self.remote), "work"], self.root)
        self.work = self.root / "work"
        self.git("config", "user.name", "Fixture")
        self.git("config", "user.email", "fixture@example.com")
        for name in ("selected.md", "owner.md", "delete.md"):
            (self.work / name).write_text("baseline\n")
        self.git("add", ".")
        self.git("commit", "-m", "baseline")
        self.git("push", "-u", "origin", "HEAD")

    def run_cmd(self, args, cwd=None, check=True):
        result = subprocess.run(args, cwd=cwd or self.work, env=self.env, capture_output=True, text=True)
        if check:
            self.assertEqual(result.returncode, 0, result.stderr)
        return result

    def git(self, *args, check=True):
        return self.run_cmd(["git", *args], check=check)

    def bash(self, body, paths=()):
        # Positional arguments preserve spaces, newlines, dashes and pathspec text.
        return self.run_cmd(["bash", "-c", 'approved_paths=("$@"); job_paths=("$@");\n' + body, "recipe", *paths], check=False)

    def guard(self, paths):
        return self.bash(recipe("git-commit-push", "python3 -"), paths)

    def remote_paths(self):
        return self.run_cmd(["git", "--git-dir", str(self.remote), "ls-tree", "-r", "--name-only", "HEAD"]).stdout

    def test_learning_dirty_start_preserves_staged_and_working_owner_bytes(self):
        self.git("branch", "-M", "main")
        (self.work / "owner.md").write_text("staged owner\n")
        self.git("add", "owner.md")
        (self.work / "owner.md").write_text("working owner\n")
        before = self.git("ls-files", "--stage", "-z").stdout
        result = self.bash(recipe("learn-new-things", "prepare_learning_repository()"))
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.git("ls-files", "--stage", "-z").stdout, before)
        self.assertEqual((self.work / "owner.md").read_text(), "working owner\n")
        self.assertEqual(self.git("stash", "list").stdout, "")

    def test_learning_clean_branch_selected_before_output_and_collision_stops(self):
        self.git("branch", "-M", "main")
        self.git("push", "-u", "origin", "main")
        self.assertEqual(self.bash(recipe("learn-new-things", "prepare_learning_repository()")).returncode, 0)
        self.env["BRANCH_NAME"] = "learning/synthetic-cycle"
        create = recipe("learn-new-things", "git switch -c")
        self.assertEqual(self.bash(create).returncode, 0)
        self.assertEqual(self.git("branch", "--show-current").stdout.strip(), "learning/synthetic-cycle")
        self.git("switch", "main")
        self.assertNotEqual(self.bash(create).returncode, 0)
        self.assertEqual(self.git("branch", "--show-current").stdout.strip(), "main")

    def test_learning_exact_output_guard_preserves_late_owner(self):
        (self.work / "selected.md").write_text("owned partial\n")
        (self.work / "owner.md").write_text("staged owner\n")
        self.git("add", "owner.md")
        before = self.git("ls-files", "--stage", "-z").stdout
        guard = recipe("learn-new-things", "python3 -")
        self.assertNotEqual(self.bash(guard, ["selected.md"]).returncode, 0)
        self.assertEqual(self.git("ls-files", "--stage", "-z").stdout, before)
        self.git("restore", "--staged", "--worktree", "owner.md")
        (self.work / "late-owner.txt").write_text("untracked owner\n")
        self.assertNotEqual(self.bash(guard, ["selected.md"]).returncode, 0)
        self.assertEqual(self.git("diff", "--cached").stdout, "")

    def test_learning_owned_partial_literal_paths_can_publish(self):
        name = ":(glob) learning result.md"
        (self.work / name).write_text("owned partial\n")
        guard = recipe("learn-new-things", "python3 -")
        self.assertEqual(self.bash(guard, [name]).returncode, 0)
        self.assertEqual(self.bash(recipe("learn-new-things", "git --literal-pathspecs add"), [name]).returncode, 0)
        self.assertEqual(self.bash(guard, [name]).returncode, 0)
        message = self.root / "message"; message.write_text("Learning partial result\n")
        self.env["commit_message_file"] = str(message)
        self.assertEqual(self.bash(recipe("learn-new-things", "git commit --file")).returncode, 0)
        self.git("push")
        self.assertEqual(self.git("show", "HEAD:" + name).stdout, "owned partial\n")

    def test_scheduled_rejects_each_dirty_state_without_pull_or_playbook(self):
        for kind in ("untracked", "unstaged", "staged"):
            with self.subTest(kind=kind):
                # Fixture restoration only, never part of the workflow recipe.
                self.git("reset", "--hard", "HEAD")
                extra = self.work / "untracked owner.txt"
                if extra.exists(): extra.unlink()
                target = extra if kind == "untracked" else self.work / "owner.md"
                target.write_text("owner work\n")
                if kind == "staged": self.git("add", "owner.md")
                old_head = self.git("rev-parse", "HEAD").stdout
                result = self.bash(recipe("scheduled-run", "require_clean_tree()") + " && touch playbook-ran")
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse((self.work / "playbook-ran").exists())
                self.assertEqual(target.read_text(), "owner work\n")
                # git status can refresh index stat metadata; compare staged objects.
                self.assertEqual(self.git("rev-parse", "HEAD").stdout, old_head)
                self.assertIn("owner", self.git("status", "--porcelain").stdout)

    def test_clean_scheduled_pull_and_no_change(self):
        result = self.bash(recipe("scheduled-run", "require_clean_tree()"))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.git("status", "--porcelain").stdout, "")

    def test_pull_conflict_stops_before_playbook_and_preserves_conflict(self):
        self.run_cmd(["git", "clone", str(self.remote), "other"], self.root)
        other = self.root / "other"
        self.run_cmd(["git", "config", "user.name", "Other Fixture"], other)
        self.run_cmd(["git", "config", "user.email", "other@example.com"], other)
        (other / "selected.md").write_text("remote conflicting edit\n")
        self.run_cmd(["git", "commit", "-am", "remote update"], other)
        self.run_cmd(["git", "push"], other)
        (self.work / "selected.md").write_text("local conflicting edit\n")
        self.git("commit", "-am", "local update")
        result = self.bash(recipe("scheduled-run", "require_clean_tree()") + " && touch playbook-ran")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.work / "playbook-ran").exists())
        self.assertTrue(self.git("ls-files", "--unmerged").stdout)
        content = (self.work / "selected.md").read_text()
        self.assertIn("local conflicting edit", content)
        self.assertIn("remote conflicting edit", content)

    def test_empty_job_selection_does_not_stage_anything(self):
        (self.work / "owner.md").write_text("unrelated unstaged work\n")
        result = self.bash(recipe("scheduled-run", 'git --literal-pathspecs add'))
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.git("diff", "--cached").stdout, "")

    def test_selection_rejects_unrelated_staged_owner_content(self):
        (self.work / "owner.md").write_text("staged owner\n")
        self.git("add", "owner.md")
        (self.work / "owner.md").write_text("different unstaged owner\n")
        before = self.git("ls-files", "--stage", "-z").stdout
        result = self.guard(["selected.md"])
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.git("ls-files", "--stage", "-z").stdout, before)
        self.assertEqual((self.work / "owner.md").read_text(), "different unstaged owner\n")
        self.assertEqual(self.git("show", "HEAD:owner.md").stdout, "baseline\n")

    def test_selection_guard_rechecks_late_staged_path(self):
        self.assertEqual(self.guard(["selected.md"]).returncode, 0)
        (self.work / "owner.md").write_text("late owner\n")
        self.git("add", "owner.md")
        self.assertNotEqual(self.guard(["selected.md"]).returncode, 0)

    def test_literal_new_deleted_and_staged_only_paths(self):
        names = [":(glob)*.md", "-option name.md", "line\nbreak.md", "delete.md", "selected.md"]
        for name in names[:3]: (self.work / name).write_text("reviewed new file\n")
        (self.work / "delete.md").unlink()
        (self.work / "selected.md").write_text("selected staged change\n")
        self.git("add", "selected.md")
        (self.work / "owner.md").write_text("unselected owner work\n")
        self.assertEqual(self.guard(names).returncode, 0)
        result = self.bash(recipe("git-commit-push", 'git --literal-pathspecs add'), names)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.guard(names).returncode, 0)
        message = self.root / "message.txt"; message.write_text("Reviewed files\n")
        self.env["commit_message_file"] = str(message)
        result = self.bash(recipe("git-commit-push", 'git commit --file'))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.git("push")
        self.assertEqual(self.git("show", "HEAD:owner.md").stdout, "baseline\n")
        self.assertEqual((self.work / "owner.md").read_text(), "unselected owner work\n")
        for name in names[:3]: self.assertEqual(self.git("show", "HEAD:" + name).stdout, "reviewed new file\n")
        self.assertNotEqual(self.git("cat-file", "-e", "HEAD:delete.md", check=False).returncode, 0)

    def test_push_failure_preserves_commit_and_remote(self):
        original_remote = self.run_cmd(["git", "--git-dir", str(self.remote), "rev-parse", "HEAD"]).stdout
        (self.work / "selected.md").write_text("verified partial output\n")
        self.assertEqual(self.bash(recipe("scheduled-run", 'git --literal-pathspecs add'), ["selected.md"]).returncode, 0)
        message = self.root / "message.txt"; message.write_text("Partial job output\n")
        self.env["commit_message_file"] = str(message)
        self.assertEqual(self.bash(recipe("scheduled-run", 'git commit --file')).returncode, 0)
        local_head = self.git("rev-parse", "HEAD").stdout
        self.git("remote", "set-url", "origin", str(self.root / "missing.git"))
        self.assertNotEqual(self.git("push", check=False).returncode, 0)
        self.assertEqual(self.git("rev-parse", "HEAD").stdout, local_head)
        self.assertEqual(self.run_cmd(["git", "--git-dir", str(self.remote), "rev-parse", "HEAD"]).stdout, original_remote)


if __name__ == "__main__":
    unittest.main()
