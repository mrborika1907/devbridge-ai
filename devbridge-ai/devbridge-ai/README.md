# DevBridge AI

[![Tests](https://img.shields.io/badge/tests-unverified-lightgrey)](#testing)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

**A small, open-source, privacy-first developer CLI for Python code checks and optional AI code review.**

> Status: early-stage prototype (v0.1.0). No claims of production readiness, users, contributors, or adoption.

## Why this exists

Code review and debugging can be intimidating for beginners. DevBridge AI provides basic, explainable checks that run locally, plus an **optional** integration with an OpenAI-compatible chat completions endpoint for richer feedback.

## Features

- Offline checks for Python syntax errors, bare `except`, `eval()` calls, and missing public-function docstrings.
- Human-readable or JSON results.
- Optional AI review of a single `.py` file via a user-configured endpoint (including locally hosted compatible servers).
- No required external Python dependencies at runtime.
- Unit tests and GitHub Actions CI.

**Limitations:** The checks are intentionally small and heuristic. They do not prove that code is safe or correct. AI feedback can be wrong. This tool does not execute the files being reviewed.

## Installation

Requires Python 3.10+.

```bash
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
python -m pip install -e .
```

## Local review (offline)

```bash
devbridge check src/
devbridge check my_script.py --json
```

Exit codes: `0` no findings, `1` findings present, `2` usage/IO/API error.

## Optional AI review

Configure an **OpenAI-compatible** `/v1/chat/completions` endpoint (the provider/model must support this format). The default endpoint targets a local server at `http://localhost:1234/v1/chat/completions`; you must start and configure your own compatible server first.

```bash
# Local model server, if available:
devbridge review example.py --model your-local-model

# Remote provider (example: replace with YOUR provider URL and model):
export DEVBRIDGE_ENDPOINT="https://your-provider.example/v1/chat/completions"
export DEVBRIDGE_MODEL="your-model"
export DEVBRIDGE_API_KEY="your-key"
devbridge review example.py
```

For Windows PowerShell, set environment variables with `$env:DEVBRIDGE_ENDPOINT="..."` etc.

**Privacy:** `check` is fully offline. `review` transmits the entire selected file to the configured endpoint. Do not review secrets, private code, or personal data without permission. Remote providers may charge fees. DevBridge AI does **not** provide free Claude access, Anthropic credits, or any subscription bypass.

## Testing

```bash
python -m unittest discover -s tests -v
```

## Roadmap

- [x] Initial CLI and offline checks
- [x] Optional AI endpoint integration
- [x] Unit tests and CI configuration
- [ ] Add configurable rules and ignore patterns
- [ ] Add secure redaction checks before AI requests
- [ ] Add multi-file summarization with explicit opt-in
- [ ] Add structured output for AI feedback
- [ ] Gather real user feedback and external contributions

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Issues and PRs are welcome after the repository is published.

## Project background

See [PROJECT_STORY.md](PROJECT_STORY.md) for a transparent project narrative and a draft of how this work could be described in a future open-source program application. Publishing this project does not establish eligibility for any third-party program.

## License

MIT — see [LICENSE](LICENSE).
