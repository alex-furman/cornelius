#!/usr/bin/env python3
"""
LLM-as-Judge scoring using Claude Code (default) or Codex workstation CLI.

Usage:
    python score_results.py --query "What is dopamine?" --note "Dopamine.md" --content "..."
    python score_results.py --batch results.json --output scored_results.json

Scoring scale (0-3):
- 0: Irrelevant - No connection to query
- 1: Tangential - Loosely related
- 2: Relevant - Addresses the query
- 3: Highly Relevant - Directly answers the query

Uses the selected CLI's existing authentication; no separate API key is required.
Agent turns must use their native delegation channel, not these subprocesses.
"""
import argparse
import json
import subprocess
import sys
import time
import tempfile
from pathlib import Path
from typing import Optional

SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
CONFIGS_DIR = SKILL_DIR / "configs"

# Load judge prompt template
JUDGE_PROMPT_PATH = CONFIGS_DIR / "judge_prompt.txt"

# Disable effectful built-ins and integrations for untrusted note excerpts.
# Verified against Codex 0.147.0; unknown flags fail rather than weakening this.
CODEX_DISABLED_FEATURES = (
    "shell_tool", "multi_agent", "multi_agent_v2", "apps", "plugins", "hooks",
    "remote_plugin", "browser_use", "browser_use_external", "computer_use",
    "view_image", "image_generation", "workspace_dependencies", "goals",
    "skill_search", "tool_suggest", "code_mode_host", "shell_snapshot",
)

# JSON schema for structured output
SCORE_SCHEMA = {
    "type": "object",
    "properties": {
        "reasoning": {
            "type": "string",
            "description": "Brief explanation of the score (1-2 sentences)"
        },
        "score": {
            "type": "integer",
            "minimum": 0,
            "maximum": 3,
            "description": "Relevance score: 0=irrelevant, 1=tangential, 2=relevant, 3=highly relevant"
        }
    },
    "required": ["reasoning", "score"]
}


def load_judge_prompt() -> str:
    """Load the judge prompt template."""
    if JUDGE_PROMPT_PATH.exists():
        return JUDGE_PROMPT_PATH.read_text()
    else:
        # Fallback template
        return """You are evaluating the relevance of a retrieved note for a knowledge base search query.

## Query
{query}

## Query Intent
{intent}

## Retrieved Note
Title: {note_title}
Content (excerpt):
{note_content_excerpt}

## Scoring Instructions

Rate the relevance on a 0-3 scale:
0 = IRRELEVANT: No connection to query
1 = TANGENTIAL: Loosely related
2 = RELEVANT: Addresses the query
3 = HIGHLY RELEVANT: Directly answers the query

## Response Format
Return JSON only:
{{"reasoning": "Brief explanation (1-2 sentences)", "score": <0-3>}}"""


class LLMJudge:
    """Relevance judge using the selected authenticated workstation CLI."""

    def __init__(
        self,
        model: Optional[str] = None,
        runtime: str = "claude",
    ):
        """Initialize the LLM judge.

        Args:
            model: Runtime model; defaults to sonnet for Claude, explicit model required for Codex.
            runtime: Workstation CLI, claude (default) or codex.
        """
        if runtime not in ("claude", "codex"):
            raise ValueError("runtime must be claude or codex")
        if runtime == "codex" and not (model and model.strip()):
            raise ValueError("Codex judging requires an explicit --model")
        self.runtime = runtime
        self.model = model or ("sonnet" if runtime == "claude" else None)
        self.prompt_template = load_judge_prompt()

        # Verify the selected binary is available (not an authentication check)
        try:
            result = subprocess.run(
                [self.runtime, "--version"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            if result.returncode != 0:
                raise RuntimeError(f"{self.runtime} CLI not available")
        except FileNotFoundError:
            raise RuntimeError(f"{self.runtime} CLI not found")

    def score(
        self,
        query: str,
        note_title: str,
        note_content: str,
        intent: str = "conceptual",
        max_content_length: int = 500,
        retries: int = 3,
        delay: float = 1.0,
    ) -> dict:
        """Score a single result's relevance to a query.

        Returns:
            dict with 'score' (0-3), 'reasoning', and 'error' (if any)
        """
        # Truncate content for consistent scoring
        content_excerpt = note_content[:max_content_length]
        if len(note_content) > max_content_length:
            content_excerpt += "..."

        # Format prompt
        prompt = self.prompt_template.format(
            query=query,
            intent=intent,
            note_title=note_title,
            note_content_excerpt=content_excerpt,
        )

        for attempt in range(retries):
            try:
                if self.runtime == "codex":
                    # Workstation only: agent runtimes use native child delegation.
                    with tempfile.TemporaryDirectory(prefix="benchmark-judge-") as directory:
                        schema_path = Path(directory) / "schema.json"
                        output_path = Path(directory) / "result.json"
                        schema_path.write_text(json.dumps({**SCORE_SCHEMA, "additionalProperties": False}))
                        command = [
                            "codex", "exec", "--ephemeral", "--ignore-user-config",
                            "--sandbox", "read-only", "-c", 'web_search="disabled"',
                            "--skip-git-repo-check", "--output-schema", str(schema_path),
                            "--output-last-message", str(output_path), "--json",
                        ]
                        for feature in CODEX_DISABLED_FEATURES:
                            command.extend(["--disable", feature])
                        if self.model:
                            command.extend(["--model", self.model])
                        command.append("-")
                        result = subprocess.run(
                            command, input=prompt, capture_output=True, text=True,
                            timeout=120, cwd=directory,
                        )
                        if result.returncode != 0:
                            raise RuntimeError(f"Codex returned error: {result.stderr}")
                        output = json.loads(output_path.read_text())
                else:
                    # Call Claude Code in headless mode with JSON schema for structured output
                    # Note: --json-schema requires 2+ turns, so we don't use --max-turns 1
                    schema_json = json.dumps(SCORE_SCHEMA)
                    result = subprocess.run(
                        [
                            "claude",
                            "-p", prompt,
                            "--model", self.model,
                            "--output-format", "json",
                            "--json-schema", schema_json,
                        ],
                        capture_output=True,
                        text=True,
                        timeout=120,
                    )

                    if result.returncode != 0:
                        raise RuntimeError(f"Claude returned error: {result.stderr}")

                    # Parse JSON response
                    response = json.loads(result.stdout)

                    # Extract structured output from response
                    if "structured_output" in response:
                        output = response["structured_output"]
                    elif "result" in response:
                        # Try parsing result as JSON (may be wrapped in markdown code fences)
                        result_text = response["result"]
                        # Strip markdown code fences if present
                        if result_text.startswith("```"):
                            lines = result_text.split("\n")
                            # Remove first line (```json) and last line (```)
                            lines = [l for l in lines if not l.startswith("```")]
                            result_text = "\n".join(lines)
                        try:
                            output = json.loads(result_text)
                        except json.JSONDecodeError:
                            raise ValueError(f"Could not parse result: {response['result'][:100]}")
                    else:
                        raise ValueError(f"Unexpected response format: {list(response.keys())}")

                # Validate score
                score = output.get("score")
                if score is None or type(score) is not int or score < 0 or score > 3:
                    raise ValueError(f"Invalid score: {score}")

                return {
                    "score": score,
                    "reasoning": output.get("reasoning", ""),
                    "error": None,
                }

            except subprocess.TimeoutExpired:
                if attempt < retries - 1:
                    time.sleep(delay)
                    continue
                return {
                    "score": -1,
                    "reasoning": "",
                    "error": f"Timeout waiting for {self.runtime} response",
                }
            except json.JSONDecodeError as e:
                if attempt < retries - 1:
                    time.sleep(delay)
                    continue
                return {
                    "score": -1,
                    "reasoning": "",
                    "error": f"JSON parse error: {e}",
                }
            except Exception as e:
                if attempt < retries - 1:
                    time.sleep(delay)
                    continue
                return {
                    "score": -1,
                    "reasoning": "",
                    "error": str(e),
                }

        return {
            "score": -1,
            "reasoning": "",
            "error": "Max retries exceeded",
        }

    def score_batch(
        self,
        items: list[dict],
        delay: float = 0.5,
        progress_callback: Optional[callable] = None,
    ) -> list[dict]:
        """Score a batch of query-result pairs.

        Args:
            items: List of dicts with 'query', 'note_title', 'note_content', 'intent'
            delay: Delay between API calls
            progress_callback: Optional callback(current, total)

        Returns:
            List of score results
        """
        results = []
        total = len(items)

        for i, item in enumerate(items):
            if progress_callback:
                progress_callback(i + 1, total)

            result = self.score(
                query=item["query"],
                note_title=item["note_title"],
                note_content=item["note_content"],
                intent=item.get("intent", "conceptual"),
            )

            results.append({
                **item,
                **result,
            })

            if i < total - 1:
                time.sleep(delay)

        return results


def estimate_cost(num_scores: int, model: str = "haiku") -> dict:
    """Estimate API cost for scoring.

    Haiku pricing (as of 2024):
    - Input: $0.25 / million tokens
    - Output: $1.25 / million tokens

    Sonnet pricing:
    - Input: $3.00 / million tokens
    - Output: $15.00 / million tokens
    """
    # Estimated tokens per score
    input_tokens_per_score = 400
    output_tokens_per_score = 50

    total_input = num_scores * input_tokens_per_score
    total_output = num_scores * output_tokens_per_score

    if "haiku" in model.lower():
        input_cost = (total_input / 1_000_000) * 0.25
        output_cost = (total_output / 1_000_000) * 1.25
    else:  # sonnet
        input_cost = (total_input / 1_000_000) * 3.00
        output_cost = (total_output / 1_000_000) * 15.00

    return {
        "model": model,
        "num_scores": num_scores,
        "input_tokens": total_input,
        "output_tokens": total_output,
        "input_cost": input_cost,
        "output_cost": output_cost,
        "total_cost": input_cost + output_cost,
    }


def main():
    parser = argparse.ArgumentParser(
        description="LLM-as-Judge scoring using a workstation CLI"
    )
    parser.add_argument(
        "--query",
        help="Query to score against",
    )
    parser.add_argument(
        "--note",
        help="Note title",
    )
    parser.add_argument(
        "--content",
        help="Note content",
    )
    parser.add_argument(
        "--intent",
        default="conceptual",
        choices=["factual", "conceptual", "synthesis", "temporal"],
        help="Query intent",
    )
    parser.add_argument(
        "--batch",
        type=Path,
        help="Batch input file (JSON)",
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        help="Output file for batch results",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Judge model (Claude default: sonnet; Codex: explicit model required)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.5,
        help="Delay between scoring calls",
    )
    parser.add_argument(
        "--estimate",
        type=int,
        metavar="NUM_SCORES",
        help="Estimate cost for N scores",
    )

    parser.add_argument("--runtime", choices=["claude", "codex"], default="claude",
                        help="Workstation judge CLI (default: claude)")
    args = parser.parse_args()

    if args.runtime == "codex" and args.estimate:
        parser.error("Cost estimates are not available for Codex")

    if args.runtime == "codex" and not args.model:
        parser.error("Codex judging requires --model")

    # Cost estimation
    if args.estimate:
        cost = estimate_cost(args.estimate, args.model or "sonnet")
        print(f"Cost estimate for {cost['num_scores']} scores using {cost['model']}:")
        print(f"  Input tokens:  {cost['input_tokens']:,}")
        print(f"  Output tokens: {cost['output_tokens']:,}")
        print(f"  Input cost:    ${cost['input_cost']:.2f}")
        print(f"  Output cost:   ${cost['output_cost']:.2f}")
        print(f"  Total cost:    ${cost['total_cost']:.2f}")
        return

    # Initialize judge
    try:
        judge = LLMJudge(model=args.model, runtime=args.runtime)
    except RuntimeError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Single scoring
    if args.query and args.note and args.content:
        result = judge.score(
            query=args.query,
            note_title=args.note,
            note_content=args.content,
            intent=args.intent,
        )
        print(json.dumps(result, indent=2))
        return

    # Batch scoring
    if args.batch:
        with open(args.batch) as f:
            items = json.load(f)

        print(f"Scoring {len(items)} items with {args.runtime} ({judge.model or 'configured model'})...")

        def progress(current, total):
            pct = (current / total) * 100
            print(f"\r  Progress: {current}/{total} ({pct:.1f}%)", end="", flush=True)

        results = judge.score_batch(items, delay=args.delay, progress_callback=progress)
        print()  # Newline after progress

        if args.output:
            with open(args.output, "w") as f:
                json.dump(results, f, indent=2)
            print(f"Results saved to: {args.output}")
        else:
            print(json.dumps(results, indent=2))
        return

    # Show help if no action specified
    parser.print_help()


if __name__ == "__main__":
    main()
