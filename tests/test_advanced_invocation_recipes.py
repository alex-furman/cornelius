"""Execute skill command recipes with fixture wrappers, without models or engines."""
import json
import argparse
import ast
import os
from pathlib import Path
import re
import subprocess
import tempfile
import unittest
ROOT = Path(__file__).resolve().parents[1]

def blocks(skill):
    return re.findall(r"```bash\n(.*?)```", (ROOT / ".claude/skills" / skill / "SKILL.md").read_text(), re.S)

class InvocationRecipes(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="recipe space ")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.log = self.root / "calls.jsonl"
        self.env = dict(os.environ, RECIPE_LOG=str(self.log))
        self.env.pop("PROJECT_ROOT", None)
        for rel in ("local-brain-search/run_search.sh", "local-brain-search/run_index.sh", "local-brain-search/run_connections.sh", "brain-graph/run_brain_graph.sh"):
            p = self.root / "resources" / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text('#!/usr/bin/env python3\nimport os,sys,json\nwith open(os.environ["RECIPE_LOG"],"a") as f: f.write(json.dumps({"argv":sys.argv[1:],"scope":os.environ.get("BRAIN_READ_SCOPE"),"tool":sys.argv[0]})+"\\n")\n')
            p.chmod(0o755)

    def run_block(self, block):
        result = subprocess.run(["bash", "-e", "-c", block],cwd=self.root,env=self.env,capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
        return [json.loads(x) for x in self.log.read_text().splitlines()]

    def test_thinking_searches_use_wrapper_and_preserve_flags(self):
        for skill in ("think-about-it", "incubation-loop", "manage-thinking-topics"):
            with self.subTest(skill=skill):
                selected=[b for b in blocks(skill) if "--mode spreading" in b]
                self.assertTrue(selected)
                for b in selected:
                    calls=self.run_block(b)
                    for call in calls:
                        self.assertIn("run_search.sh",call["tool"])
                        self.assertIn("--limit",call["argv"])
                    if skill in ("think-about-it","incubation-loop"):
                        self.assertIn("--no-track",calls[-1]["argv"])
                    if skill=="think-about-it": self.assertEqual(calls[-1]["scope"],"core,Books,document-insights")

    def test_graph_blocks_run_independently_from_root_with_spaces(self):
        for skill in ("coherence-sweep","compute-lifecycle","detect-tensions","propagate-change"):
            for block in blocks(skill):
                if "cli.py" in block or "run_brain_graph.sh" in block:
                    with self.subTest(skill=skill,block=block):
                        calls=self.run_block(block)
                        self.assertIn("run_brain_graph.sh",calls[-1]["tool"])

    def test_failed_search_remains_visible_and_stops_recipe(self):
        wrapper = self.root / "resources/local-brain-search/run_search.sh"
        wrapper.write_text('#!/bin/sh\necho "fixture search unavailable" >&2\nexit 9\n')
        for skill in ("think-about-it", "incubation-loop", "manage-thinking-topics"):
            block = next(b for b in blocks(skill) if "--mode spreading" in b)
            result = subprocess.run(["bash", "-e", "-c", block], cwd=self.root,
                                    env=self.env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 9)
            self.assertIn("fixture search unavailable", result.stderr)

    def test_learning_index_uses_existing_wrapper(self):
        block=next(b for b in blocks("learn-new-things") if "run_reindex.sh" in b or "run_index.sh" in b)
        self.assertIn("run_index.sh",self.run_block(block)[-1]["tool"])

    def test_diagnostic_dependency_check_preserves_cwd(self):
        agent=self.root/".claude/agents/diagram-generator.md"
        agent.parent.mkdir(parents=True);agent.write_text("fixture")
        block=next(b for b in blocks("self-diagnostic") if "import sqlite3" in b)
        result=subprocess.run(["bash","-c",block+'\ntest -f .claude/agents/diagram-generator.md'],cwd=self.root,env=self.env,capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)

    def test_diagnostic_direct_retrieval_does_not_track(self):
        block=next(b for b in blocks("self-diagnostic") if '"consciousness"' in b)
        tree = ast.parse((ROOT / "resources/local-brain-search/connections.py").read_text())
        main = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "main")
        # Execute the actual parser declarations without importing engine dependencies.
        declarations = []
        for statement in main.body:
            if isinstance(statement, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "args" for t in statement.targets):
                break
            declarations.append(statement)
        namespace = {"argparse": argparse}
        exec(compile(ast.Module(body=declarations, type_ignores=[]), "connections-parser", "exec"), namespace)
        for call in self.run_block(block):
            if call["tool"].endswith("run_search.sh"):
                self.assertIn("--no-track", call["argv"])
            else:
                namespace["parser"].parse_args(call["argv"])

if __name__=="__main__": unittest.main()
