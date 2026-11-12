# Contributing to DevBridge AI

Thank you for considering a contribution! This project is early-stage and welcomes beginner-friendly improvements.

## Getting started

1. Fork the repository after it has been published.
2. Create a branch: `git checkout -b feature/short-description`.
3. Set up Python 3.10+, then run `python -m pip install -e .`.
4. Run `python -m unittest discover -s tests -v`.
5. Make one focused change and add tests where appropriate.
6. Open a pull request explaining the problem, the change, and how you tested it.

## Good first contributions

- Improve error messages and documentation.
- Add focused AST checks with unit tests.
- Add CLI usage examples.
- Improve handling of large files and encoding errors.
- Add a safe, explicit secret-warning step before AI review.

## Guidelines

- Keep the offline checker offline; network calls belong only in explicitly invoked AI commands.
- Never commit API keys, credentials, personal data, or proprietary source code.
- Avoid adding dependencies without a clear reason.
- Be respectful and constructive in issues and reviews.
- Do not claim benchmarks, contributors, adoption, or features that have not been verified.

## Reporting security issues

Do not post working exploits or secrets in public issues. Contact the repository maintainer privately through a contact method they publish after creating the repository.
