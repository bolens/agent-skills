import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "skills/evaluate-agent-workflows/scripts/summarize-codex-trace.py"
)


class AgentWorkflowTrace(unittest.TestCase):
    def test_only_successful_entrypoint_reads_are_observed(self):
        heading = "---\nname: {}\ndescription: fixture\n---\n"
        events = [
            ("failed-read", "cat .agents/skills/blocked/SKILL.md", 1, heading.format("blocked") + "# Blocked"),
            ("listed", "rg --files -g SKILL.md", 0, ".agents/skills/listed/SKILL.md"),
            ("metadata-only", "head -4 .agents/skills/metadata/SKILL.md", 0, heading.format("metadata")),
            ("composite", "cat notes.md; test -f skills/other/SKILL.md", 0, heading.format("other") + "# Notes"),
            ("mismatched", "cat skills/foo/SKILL.md", 0, heading.format("unrelated") + "# Unrelated"),
            (
                "crlf-read",
                '/bin/bash -lc "sed -n \'1,20p\' skills/windows/SKILL.md"',
                0,
                (heading.format("windows") + "# Windows\n").replace("\n", "\r\n"),
            ),
            (
                "batched-read",
                "cat .agents/skills/{header,one,two}/SKILL.md",
                0,
                heading.format("header") + heading.format("one") + "\n# One\n" + heading.format("two") + "\n# Two\n",
            ),
        ]
        with tempfile.TemporaryDirectory() as directory:
            trace = Path(directory) / "case.jsonl"
            with trace.open("w", encoding="utf-8") as stream:
                for identifier, command, status, output in events:
                    event = {
                        "type": "item.completed",
                        "item": {
                            "id": identifier, "type": "command_execution",
                            "command": command, "exit_code": status, "aggregated_output": output,
                        },
                    }
                    stream.write(json.dumps(event) + "\n")
                stream.write('{"type":"turn.completed","usage":{"output_tokens":100}}\n')
            result = subprocess.run([sys.executable, str(SCRIPT), str(trace)], capture_output=True, text=True,
                                    check=True, timeout=10)

        self.assertEqual(
            {
                "turn_status": "completed",
                "skill_reads": {"one": "batched-read", "two": "batched-read", "windows": "crlf-read"},
                "usage": {"output_tokens": 100},
            },
            json.loads(result.stdout),
        )
