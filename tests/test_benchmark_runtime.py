"""Judge transport contracts; subprocess is replaced, no provider calls."""
import importlib.util
import json
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("benchmark_judge", ROOT / ".claude/skills/benchmark-memory/scripts/score_results.py")
judge_module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(judge_module)

class BenchmarkRuntimeTests(unittest.TestCase):
    def test_claude_default_preserves_transport(self):
        with patch.object(judge_module.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, json.dumps({"structured_output": {"score": 3, "reasoning": "match"}}), "")) as run:
            judge = judge_module.LLMJudge()
            result = judge.score("query", "title", "content", retries=1)
        self.assertEqual(result["score"], 3)
        self.assertEqual(run.call_args_list[0].args[0], ["claude", "--version"])
        argv = run.call_args.args[0]
        self.assertEqual(argv[argv.index("--model") + 1], "sonnet")

    def transport(self, output, failure=None, model="test-model", returncode=0):
        calls = []
        def run(argv, **kwargs):
            calls.append((argv, kwargs))
            if argv[-1] == "--version":
                return subprocess.CompletedProcess(argv, 0, "version", "")
            if failure: raise failure
            schema = json.loads(Path(argv[argv.index("--output-schema") + 1]).read_text())
            self.assertFalse(schema["additionalProperties"])
            Path(argv[argv.index("--output-last-message") + 1]).write_text(output)
            return subprocess.CompletedProcess(argv, returncode, '{"type":"thread.started"}\n', "synthetic error" if returncode else "")
        with patch.object(judge_module.subprocess, "run", side_effect=run):
            judge = judge_module.LLMJudge(runtime="codex", model=model)
            result = judge.score("literal $(no) `no`", "title", "content", retries=1)
        return result, calls

    def test_codex_reads_final_file_and_uses_stdin(self):
        result, calls = self.transport('{"score":2,"reasoning":"partial"}')
        self.assertEqual(result, {"score":2,"reasoning":"partial","error":None})
        argv, kwargs = calls[-1]
        self.assertEqual(argv[:2], ["codex", "exec"])
        self.assertIn("--ignore-user-config", argv)
        self.assertIn('web_search="disabled"', argv)
        for feature in judge_module.CODEX_DISABLED_FEATURES:
            self.assertIn(feature, argv)
        self.assertIn("literal $(no) `no`", kwargs["input"])
        self.assertEqual(argv[-1], "-")
        self.assertEqual(kwargs["timeout"], 120)
        self.assertFalse(kwargs.get("shell", False))
        self.assertFalse(Path(argv[argv.index("--output-last-message")+1]).exists())

    def test_codex_requires_explicit_model_before_execution(self):
        with patch.object(judge_module.subprocess, "run") as run:
            with self.assertRaises(ValueError): judge_module.LLMJudge(runtime="codex")
            run.assert_not_called()

    def test_codex_explicit_model(self):
        _, calls = self.transport('{"score":1,"reasoning":"related"}', model="test-model")
        argv = calls[-1][0]
        self.assertEqual(argv[argv.index("--model") + 1], "test-model")

    def test_codex_invalid_output_and_timeout_fail_without_fallback(self):
        for output in ('not json', '{"score":9}', '{"score":true}', '[]'):
            with self.subTest(output=output):
                result, calls = self.transport(output)
                self.assertEqual(result["score"], -1)
                self.assertTrue(result["error"])
                self.assertTrue(all(call[0][0] == "codex" for call in calls))
        result, _ = self.transport("", subprocess.TimeoutExpired("codex",120))
        self.assertEqual(result["score"], -1)
        self.assertIn("Timeout", result["error"])

    def test_codex_nonzero_does_not_accept_output_or_fallback(self):
        result, calls = self.transport('{"score":3,"reasoning":"ignore"}', returncode=1)
        self.assertEqual(result["score"], -1)
        self.assertIn("Codex returned error", result["error"])
        self.assertTrue(all(call[0][0] == "codex" for call in calls))

    def test_invalid_runtime_rejected_before_execution(self):
        with patch.object(judge_module.subprocess, "run") as run:
            with self.assertRaises(ValueError): judge_module.LLMJudge(runtime="other")
            run.assert_not_called()

if __name__ == "__main__": unittest.main()
