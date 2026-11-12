"""Deterministic, local Python checks. No files leave the computer."""
from __future__ import annotations
import ast
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class Finding:
    file: str
    line: int
    code: str
    message: str

    def to_dict(self) -> dict:
        return asdict(self)


def analyze_source(source: str, filename: str = "<input>") -> list[Finding]:
    findings: list[Finding] = []
    try:
        tree = ast.parse(source, filename=filename)
    except SyntaxError as exc:
        return [Finding(filename, exc.lineno or 1, "SYNTAX", exc.msg)]
    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler) and node.type is None:
            findings.append(Finding(filename, node.lineno, "BARE_EXCEPT", "Avoid bare except; catch specific exceptions."))
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and len(node.body) > 0:
            if ast.get_docstring(node) is None and not node.name.startswith("_"):
                findings.append(Finding(filename, node.lineno, "DOCSTRING", "Consider documenting this public function."))
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "eval":
            findings.append(Finding(filename, node.lineno, "EVAL", "Review use of eval(); it can execute untrusted code."))
    return sorted(findings, key=lambda f: (f.line, f.code))


def analyze_path(path: Path) -> list[Finding]:
    path = path.resolve()
    if not path.exists():
        raise FileNotFoundError(f"Path does not exist: {path}")
    if not path.is_dir() and path.suffix != ".py":
        raise ValueError("Provide a Python .py file or directory")
    files = [path] if path.is_file() else sorted(p for p in path.rglob("*.py") if not any(part.startswith(".") or part in {".venv", "venv", "node_modules", "__pycache__"} for part in p.relative_to(path).parts))
    results: list[Finding] = []
    for file in files:
        try:
            content = file.read_text(encoding="utf-8")
        except (UnicodeError, OSError) as exc:
            results.append(Finding(str(file), 1, "READ_ERROR", str(exc)))
            continue
        results.extend(analyze_source(content, str(file)))
    return results
