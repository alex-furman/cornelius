"""Execute image recipes offline; these checks do not qualify generation."""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ".claude/skills/nano-banana-image-generator/scripts/generate_image.py"


class ImageInvocationTests(unittest.TestCase):
    def exercise(self, skill, with_key):
        source = ROOT / ".claude/skills" / skill / "SKILL.md"
        blocks = re.findall(r"```bash\n(.*?)```", source.read_text(), re.S)
        commands = [block for block in blocks if "generate_image.py" in block]
        self.assertTrue(commands, "Document a repository-local Python generation command")
        with tempfile.TemporaryDirectory(prefix="image recipe ") as tmp:
            root = Path(tmp) / "checkout with spaces"
            script = root / SCRIPT
            script.parent.mkdir(parents=True)
            shutil.copy2(ROOT / SCRIPT, script)
            bin_dir = Path(tmp) / "bin"
            bin_dir.mkdir()
            # Execute the actual CLI and parser, replacing only credential lookup
            # outside the fixture and HTTP transport. No requests dependency needed.
            shim = bin_dir / "python3"
            shim.write_text(
                f"#!{sys.executable}\n"
                "import json, os, pathlib, runpy, sys, types\n"
                "from unittest.mock import patch\n"
                "def post(url, json):\n"
                "    if not os.environ.get('GOOGLE_API_KEY'):\n"
                "        raise AssertionError('HTTP attempted without key')\n"
                "    pathlib.Path(os.environ['REQUEST_CAPTURE']).write_text(\n"
                "        __import__('json').dumps({'payload': json, 'argv': sys.argv[1:]}))\n"
                "    return types.SimpleNamespace(json=lambda: {'error': {'message': 'offline fixture'}})\n"
                "sys.modules['requests'] = types.SimpleNamespace(post=post)\n"
                "sys.argv = sys.argv[1:]\n"
                "with patch.object(pathlib.Path, 'home', return_value=pathlib.Path(os.environ['FIXTURE_HOME'])):\n"
                "    runpy.run_path(sys.argv[0], run_name='__main__')\n"
            )
            shim.chmod(0o755)
            capture = Path(tmp) / "request.json"
            output = Path(tmp) / "output images" / "chosen image.png"
            prompt = 'A "quoted" label; $(touch injected) `touch injected` $USER'
            env = dict(os.environ)
            env.pop("GOOGLE_API_KEY", None)
            env.pop("GEMINI_API_KEY", None)
            env.update(PATH=str(bin_dir) + os.pathsep + env["PATH"],
                       FIXTURE_HOME=str(Path(tmp) / "empty home"),
                       REQUEST_CAPTURE=str(capture), PYTHONDONTWRITEBYTECODE="1",
                       image_prompt=prompt, image_output=str(output), image_ratio="16:9")
            if with_key:
                env["GOOGLE_API_KEY"] = "synthetic-not-a-credential"
            result = subprocess.run(["bash", "-c", commands[0]], cwd=root,
                                    env=env, capture_output=True, text=True)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertFalse(output.exists())
            self.assertFalse((root / "injected").exists())
            if with_key:
                self.assertTrue(capture.exists(), result.stdout + result.stderr)
                captured = json.loads(capture.read_text())
                self.assertEqual(captured["argv"],
                                 [prompt, str(output), "--aspect-ratio", "16:9"])
                payload = captured["payload"]
                self.assertEqual(payload["contents"][0]["parts"][0]["text"], prompt)
                self.assertEqual(payload["generationConfig"]["imageConfig"]["aspectRatio"], "16:9")
                self.assertIn("offline fixture", result.stdout)
            else:
                self.assertIn("No API key found", result.stdout)
                self.assertFalse(capture.exists())

    def test_nano_recipe_transports_quoted_arguments(self):
        self.exercise("nano-banana-image-generator", True)

    def test_explanatory_recipe_transports_quoted_arguments(self):
        self.exercise("create-explanatory-image", True)

    def test_missing_key_stops_before_http_or_artifacts(self):
        for skill in ("nano-banana-image-generator", "create-explanatory-image"):
            with self.subTest(skill=skill):
                self.exercise(skill, False)

    def test_final_copy_and_cleanup_preserve_unrelated_images(self):
        source = ROOT / ".claude/skills/create-explanatory-image/SKILL.md"
        blocks = re.findall(r"```bash\n(.*?)```", source.read_text(), re.S)
        copy = next(block for block in blocks if "cp --" in block)
        cleanup = next(block for block in blocks if "rm --" in block)
        with tempfile.TemporaryDirectory(prefix="image cleanup ") as tmp:
            root = Path(tmp)
            selected = root / "variant [1].png"
            rejected = root / "variant 2.png"
            unrelated = root / "variant old.png"
            final = root / "final chosen.png"
            selected.write_bytes(b"selected fixture")
            rejected.write_bytes(b"rejected fixture")
            unrelated.write_bytes(b"owner fixture")
            # Shell arguments supply exact filenames, never interpolated code.
            command = 'best_image="$1"; final_image="$2"; intermediate_images=("$1" "$3")\n'
            result = subprocess.run(
                ["bash", "-e", "-c", command + copy + cleanup, "recipe",
                 str(selected), str(final), str(rejected)], cwd=root,
                capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(final.read_bytes(), b"selected fixture")
            self.assertEqual(unrelated.read_bytes(), b"owner fixture")
            self.assertFalse(selected.exists())
            self.assertFalse(rejected.exists())


if __name__ == "__main__":
    unittest.main()
