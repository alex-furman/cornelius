"""Execute the skill's event inspection recipe against real JSONL records."""
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class MemorySystemRecipeTests(unittest.TestCase):
    def test_event_inspection_reads_each_record_without_mutating_history(self):
        skill = (ROOT / ".claude/skills/test-memory-system/SKILL.md").read_text()
        block = next(b for b in re.findall(r"```bash\n(.*?)```", skill, re.S)
                     if "# Verify event structure" in b)
        command = block.split("# Verify event structure", 1)[1].strip()
        command = command.replace("python ", f'"{sys.executable}" ')
        with tempfile.TemporaryDirectory(prefix="memory recipe ") as tmp:
            history = Path(tmp) / "data/usage_history.jsonl"
            history.parent.mkdir()
            events = [{"note_id": f"02-Permanent/Note {i}.md",
                       "position_in_results": i, "event_type": "retrieved"}
                      for i in range(7)]
            original = "".join(json.dumps(e) + "\n" for e in events)
            history.write_text(original)
            result = subprocess.run(["bash", "-c", command], cwd=tmp,
                                    text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual([json.loads(line) for line in result.stdout.splitlines()],
                             events[-5:])
            self.assertEqual(history.read_text(), original)


if __name__ == "__main__":
    unittest.main()
