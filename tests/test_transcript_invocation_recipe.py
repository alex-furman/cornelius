"""Check wrapper dispatch only; the production transcript helper is not shipped."""
import os
from pathlib import Path
import re
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class TranscriptInvocationTests(unittest.TestCase):
    def run_recipe(self, provide_fixture):
        text = (ROOT / ".claude/skills/get-youtube-transcript/SKILL.md").read_text()
        command = re.findall(r"```bash\n(.*?)```", text, re.S)[0]
        with tempfile.TemporaryDirectory(prefix="transcript recipe ") as tmp:
            root = Path(tmp) / "checkout with spaces"
            root.mkdir()
            capture = root / "arguments.txt"
            if provide_fixture:
                helper = root / "scripts/utilities/yt-transcript.sh"
                helper.parent.mkdir(parents=True)
                helper.write_text('#!/bin/bash\nprintf "%s\\n" "$#" "$1" > "$ARGUMENT_CAPTURE"\n')
                helper.chmod(0o755)
            url = "https://example.invalid/watch?v=literal&x=$(touch injected)"
            env = dict(os.environ, video_url=url, ARGUMENT_CAPTURE=str(capture))
            env.pop("PROJECT_ROOT", None)
            result = subprocess.run(["bash", "-c", command], cwd=root,
                                    env=env, capture_output=True, text=True)
            self.assertFalse((root / "injected").exists())
            if provide_fixture:
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(capture.read_text(), "1\n" + url + "\n")
            else:
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertIn("Transcript helper unavailable", result.stderr)
                self.assertFalse(capture.exists())

    def test_missing_helper_stops_with_dependency_message(self):
        self.run_recipe(False)

    def test_configured_helper_receives_literal_url_from_spaced_checkout(self):
        self.run_recipe(True)


if __name__ == "__main__":
    unittest.main()
