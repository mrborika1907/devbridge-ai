"""Command-line entry point."""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
from .analyzer import analyze_path
from .ai import review_with_ai


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="devbridge", description="Privacy-first developer review CLI")
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("check", help="Run local Python code checks (no network)")
    check.add_argument("path", type=Path)
    check.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    review = sub.add_parser("review", help="Opt-in AI review of one Python file")
    review.add_argument("path", type=Path)
    review.add_argument("--model", default=os.environ.get("DEVBRIDGE_MODEL", "local-model"))
    review.add_argument("--endpoint", default=os.environ.get("DEVBRIDGE_ENDPOINT", "http://localhost:1234/v1/chat/completions"))
    args = parser.parse_args(argv)
    try:
        if args.command == "check":
            findings = analyze_path(args.path)
            if args.json:
                print(json.dumps([f.to_dict() for f in findings], indent=2))
            else:
                for f in findings:
                    print(f"{f.file}:{f.line}: {f.code}: {f.message}")
                print(f"{len(findings)} finding(s)")
            return 1 if findings else 0
        if not args.path.is_file() or args.path.suffix != ".py":
            raise ValueError("AI review requires an existing .py file")
        print("Notice: this command sends the selected file to your configured AI endpoint.", flush=True)
        result = review_with_ai(args.path.read_text(encoding="utf-8"), model=args.model, endpoint=args.endpoint)
        print(result)
        return 0
    except (OSError, ValueError, RuntimeError) as exc:
        parser.exit(2, f"Error: {exc}\n")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
