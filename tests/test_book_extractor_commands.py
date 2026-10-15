"""Exercise documented command paths/quoting, not extraction dependencies."""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class BookExtractorCommandTests(unittest.TestCase):
    def check_command(self, skill, script, extension):
        source = ROOT / ".claude" / "skills" / skill
        blocks = re.findall(r"```bash\n(.*?)```", (source / "SKILL.md").read_text(), re.S)
        command = next(block for block in blocks if script in block and "uv run" in block)
        with tempfile.TemporaryDirectory(prefix="book commands ") as tmp:
            root = Path(tmp) / "vault with spaces"
            destination = root / ".claude" / "skills" / skill
            destination.mkdir(parents=True)
            shutil.copy2(source / script, destination / script)
            books = Path(tmp) / "input books"
            books.mkdir()
            book = books / ("sample book." + extension)
            book.write_text("command transport fixture")
            output = Path(tmp) / "output chapters"
            command = command.replace(f"/path/to/book.{extension}", str(book))
            command = command.replace("[output_dir]", '"' + str(output) + '"')
            command = command.replace("/path/to/output folder", str(output))
            bin_dir = Path(tmp) / "bin"
            bin_dir.mkdir()
            uv = bin_dir / "uv"
            uv.write_text(
                "#!/usr/bin/env python3\n"
                "import json, os, pathlib, sys\n"
                "args = sys.argv[sys.argv.index('python') + 1:]\n"
                "script = pathlib.Path(args[0]).resolve(strict=True)\n"
                "pathlib.Path(os.environ['INVOCATION']).write_text(\n"
                "    json.dumps([str(script), *args[1:]]))\n"
            )
            uv.chmod(0o755)
            invocation = Path(tmp) / "invocation.json"
            env = dict(os.environ, HOME=str(Path(tmp) / "empty home"),
                       PROJECT_ROOT=str(root), INVOCATION=str(invocation),
                       PATH=str(bin_dir) + os.pathsep + os.environ["PATH"])
            result = subprocess.run(["bash", "-c", command], cwd=root, env=env,
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(invocation.read_text()),
                             [str(destination / script), str(book), str(output)])

    def test_epub_command_uses_bundled_script_and_quoted_paths(self):
        self.check_command("epub-chapter-extractor", "extract_chapters.py", "epub")

    def test_pdf_command_uses_bundled_script_and_quoted_paths(self):
        self.check_command("multi-format-book-extractor", "extract_book.py", "pdf")


if __name__ == "__main__":
    unittest.main()
