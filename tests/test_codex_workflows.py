"""Execute documented workflow recipes; model approval behavior is tested live."""
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ReferenceScopeRecipeTests(unittest.TestCase):
    def run_recipe(self, scope, link_target=None):
        guide = (ROOT / "docs/CODEX.md").read_text()
        recipes = re.findall(r"```bash\n(.*?)```", guide, re.S)
        matches = [r for r in recipes if '"$REFERENCE_SCOPE"' in r]
        self.assertEqual(len(matches), 1, "Reference scope recipe is missing")
        with tempfile.TemporaryDirectory(prefix="reference vault ") as tmp:
            vault = Path(tmp) / "Brain with spaces"
            for name in ["Company/people/Person.md", "Company/orgs/Org.md",
                         "DemoCRM/people/Person.md", "Thinkers/Person.md",
                         "02-Permanent/Core.md"]:
                note = vault / name
                note.parent.mkdir(parents=True, exist_ok=True)
                note.write_text("fixture", encoding="utf-8")
            if link_target:
                target = Path(tmp) / "Outside.md" if link_target == "outside" else vault / "02-Permanent/Core.md"
                if link_target == "outside":
                    target.write_text("outside fixture", encoding="utf-8")
                (vault / "Company/people/Linked.md").symlink_to(target)
            result = subprocess.run(
                ["bash", "-c", matches[0]], cwd=ROOT, capture_output=True,
                text=True, env=dict(os.environ, BRAIN_PATH=str(vault),
                                    REFERENCE_SCOPE=scope))
            if result.returncode:
                return result.returncode, result.stderr
            paths = json.loads(result.stdout)
            return 0, {Path(x).relative_to(vault).as_posix() for x in paths}

    def test_family_child_does_not_read_siblings(self):
        self.assertEqual(self.run_recipe("Company/people"),
                         (0, {"Company/people/Person.md"}))

    def test_non_company_family_and_flat_reference_scope(self):
        self.assertEqual(self.run_recipe("DemoCRM"),
                         (0, {"DemoCRM/people/Person.md"}))
        self.assertEqual(self.run_recipe("thinkers"),
                         (0, {"Thinkers/Person.md"}))

    def test_unknown_core_and_mixed_write_targets_are_rejected(self):
        for scope in ["typo", "core", "core,Company", "Company,DemoCRM",
                      "../Company", "Company/../../02-Permanent", ""]:
            with self.subTest(scope=scope):
                status, _ = self.run_recipe(scope)
                self.assertNotEqual(status, 0)

    def test_symlink_cannot_widen_selected_scope(self):
        for target in ["outside", "core"]:
            with self.subTest(target=target):
                status, _ = self.run_recipe("Company/people", target)
                self.assertNotEqual(status, 0)


class NonTrackingRecipeTests(unittest.TestCase):
    def run_search_recipes(self, skill, selector):
        text = (ROOT / f".claude/skills/{skill}/SKILL.md").read_text()
        blocks = re.findall(r"```bash\n(.*?)```", text, re.S)
        recipes = [b for b in blocks if selector in b]
        self.assertTrue(recipes)
        with tempfile.TemporaryDirectory(prefix="search recipe ") as tmp:
            root = Path(tmp)
            search = root / "resources/local-brain-search/run_search.sh"
            search.parent.mkdir(parents=True)
            # The fixture records actual argv/env received by the shell recipe.
            # It does not simulate model approval or prove engine learning behavior.
            search.write_text(
                "#!/usr/bin/env python3\nimport json,os,sys\n"
                "with open(os.environ['RECIPE_LOG'],'a') as f:\n"
                " f.write(json.dumps({'args':sys.argv[1:],"
                "'scope':os.environ.get('BRAIN_READ_SCOPE')})+'\\n')\n"
                "print(json.dumps({'results':[]}))\n")
            search.chmod(0o755)
            log = root / "calls.jsonl"
            for recipe in recipes:
                result = subprocess.run(["bash", "-c", recipe], cwd=root,
                                        env=dict(os.environ, RECIPE_LOG=str(log)),
                                        capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
            return [json.loads(line) for line in log.read_text().splitlines()]

    def test_first_run_smoke_search_does_not_train_learning(self):
        calls = self.run_search_recipes("first-run", "decision under uncertainty")
        self.assertEqual(len(calls), 1)
        self.assertIn("--no-track", calls[0]["args"])

    def test_interview_search_uses_supported_limit_and_core_scope(self):
        calls = self.run_search_recipes("insight-interview", "--mode spreading")
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0]["scope"], "core")
        self.assertEqual(calls[0]["args"], ["[topic]", "--limit", "15", "--mode", "spreading"])

    def test_reference_bridge_searches_are_nontracking(self):
        calls = self.run_search_recipes("ref-bridge", "--mode static")
        self.assertEqual(len(calls), 2)
        self.assertEqual({c["args"][c["args"].index("--mode") + 1]
                          for c in calls}, {"static", "spreading"})
        for call in calls:
            self.assertEqual(call["scope"], "core")
            self.assertIn("--no-track", call["args"])


class BrainMergeRefreshRecipeTests(unittest.TestCase):
    def test_each_agent_refreshes_from_its_own_quoted_root(self):
        skill = (ROOT / ".claude/skills/brain-merge/SKILL.md").read_text()
        section = skill.split("#### Step 4: Refresh indexes in both agents", 1)[1]
        recipe = re.search(r"```bash\n(.*?)```", section, re.S).group(1)
        with tempfile.TemporaryDirectory(prefix="merge roots ") as tmp:
            roots = [Path(tmp) / "target agent", Path(tmp) / "source agent"]
            log = Path(tmp) / "refresh.log"
            for root in roots:
                script = root / "resources/local-brain-search/run_index.sh"
                script.parent.mkdir(parents=True)
                script.write_text('#!/bin/sh\npwd >> "$REFRESH_LOG"\n')
                script.chmod(0o755)
            recipe = recipe.replace("[TARGET_AGENT_ROOT]", str(roots[0]))
            recipe = recipe.replace("[SOURCE_AGENT_ROOT]", str(roots[1]))
            result = subprocess.run(["bash", "-c", recipe], cwd=ROOT,
                                    env=dict(os.environ, REFRESH_LOG=str(log)),
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(log.read_text().splitlines(), list(map(str, roots)))


if __name__ == "__main__":
    unittest.main()
