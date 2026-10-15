"""Exercise real runner/metrics/CSV/resume; stub only provider and search."""
import contextlib
import csv
import importlib.util
import io
from pathlib import Path
import sys
import tempfile
import unittest
from types import ModuleType
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / ".claude/skills/benchmark-memory/scripts"
SPEC = importlib.util.spec_from_file_location("benchmark_runner", SCRIPTS / "run_benchmark.py")
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)


class BenchmarkFailureResumeTests(unittest.TestCase):
    def setUp(self):
        # Only aggregate_metrics needs numpy; this suite exercises the real
        # per-query metrics, which are stdlib-only. An inert import placeholder
        # keeps that unused dependency optional and fails on any attempted use.
        modules = patch.dict(sys.modules, {"numpy": ModuleType("numpy")})
        modules.start()
        self.addCleanup(modules.stop)

    def test_failure_is_excluded_and_resume_retries(self):
        for failure in ({"score": -1, "error": "synthetic auth failure"},
                        {"score": 2, "error": "synthetic auth failure"},
                        {"score": -1}):
            with self.subTest(failure=failure), tempfile.TemporaryDirectory() as temp:
                output = Path(temp) / "results.csv"
                queries = {"queries": [{"id": q, "query": q, "category": "test"}
                                        for q in ("good", "retry")]}
                calls = []
                broken = True
                class Judge:
                    def __init__(self, **kwargs): pass
                    def score(self, query, note_title, **kwargs):
                        calls.append(query)
                        if broken and query == "retry" and note_title == "second":
                            return failure
                        return {"score": 3, "reasoning": "match", "error": None}
                def execute(resume=False):
                    return runner.run_benchmark(
                        [{"name": "test"}], queries, Path(temp), output,
                        judge_model="test", judge_runtime="codex", delay=0, resume=resume)
                search = {"results": [{"title": t, "content": "excerpt"}
                                      for t in ("first", "second")]}
                with patch.object(sys, "path", [str(SCRIPTS)] + sys.path), patch("score_results.LLMJudge", Judge), patch.object(runner, "run_search", return_value=search), contextlib.redirect_stdout(io.StringIO()):
                    with self.assertRaisesRegex(RuntimeError, "test.*retry"):
                        execute()
                    before = output.read_text()
                    rows = list(csv.DictReader(io.StringIO(before)))
                    self.assertEqual([r["query_id"] for r in rows], ["good"])
                    broken = False
                    calls.clear()
                    execute(resume=True)
                    self.assertEqual(calls, ["retry", "retry"])
                    self.assertTrue(output.read_text().startswith(before))
                    rows = list(csv.DictReader(io.StringIO(output.read_text())))
                    self.assertEqual([r["query_id"] for r in rows], ["good", "retry"])
                    self.assertEqual(float(rows[1]["avg_score"]), 3)

    def test_legacy_failure_is_refused_without_modifying_csv(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "results.csv"
            legacy = "config_name,query_id,result_1_score,avg_score\ntest,old,-1,-1\n"
            output.write_text(legacy)
            with patch.object(sys, "path", [str(SCRIPTS)] + sys.path), patch("score_results.LLMJudge"), contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaisesRegex(ValueError, "negative.*new output"):
                    runner.run_benchmark([], {"queries": []}, Path(temp), output, resume=True)
            self.assertEqual(output.read_text(), legacy)

if __name__ == "__main__":
    unittest.main()
