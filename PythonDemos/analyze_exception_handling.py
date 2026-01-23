### Credits:
# This script was generated using ChatGPT for demo purposes

import ast
import os
from pathlib import Path
from typing import List, Dict, Any


class ExceptionSmellVisitor(ast.NodeVisitor):
    def __init__(self, filename: str):
        self.filename = filename
        self.smells: List[Dict[str, Any]] = []

    def visit_Try(self, node: ast.Try):
        for handler in node.handlers:
            kind, details = self.classify_handler(handler)
            if kind is not None:
                self.smells.append(
                    {
                        "file": self.filename,
                        "lineno": handler.lineno,
                        "kind": kind,
                        "details": details,
                    }
                )

        # Continue walking children
        self.generic_visit(node)

    # ---- Helpers ---------------------------------------------------------

    def classify_handler(self, handler: ast.ExceptHandler):
        """
        Return (kind, details) for a smelly handler, or (None, None) if OK.
        Kinds:
          - 'bare-except'
          - 'empty-handler'
          - 'swallowed-exception'
        """
        # 1) Bare except:
        if handler.type is None:
            return "bare-except", "Catches all exceptions (no specific type)."

        # 2) Empty handler: body empty or only 'pass'
        if self._is_empty_body(handler.body):
            return "empty-handler", "Handler body is empty or only 'pass'."

        # 3) Swallowed exception: only logs/prints and does not re-raise
        if self._is_logging_only(handler.body) and not self._reraises(handler.body):
            return (
                "swallowed-exception",
                "Only logs/prints the error, does not re-raise.",
            )

        return None, None

    @staticmethod
    def _is_empty_body(stmts: List[ast.stmt]) -> bool:
        if not stmts:
            return True
        # All statements are Pass
        return all(isinstance(s, ast.Pass) for s in stmts)

    @staticmethod
    def _is_logging_only(stmts: List[ast.stmt]) -> bool:
        """
        Heuristic: body consists only of Expr(Call(...)) where the call is either:
          - print(...)
          - logging.<something>(...)
        """
        if not stmts:
            return False

        for s in stmts:
            # Allow simple "log only" sequences, not control flow etc.
            if not isinstance(s, ast.Expr) or not isinstance(s.value, ast.Call):
                return False

            call = s.value

            # print(...)
            if isinstance(call.func, ast.Name) and call.func.id == "print":
                continue

            # logging.<level>(...)
            if isinstance(call.func, ast.Attribute) and isinstance(
                call.func.value, ast.Name
            ):
                if call.func.value.id == "logging":
                    continue

            return False

        return True

    @staticmethod
    def _reraises(stmts: List[ast.stmt]) -> bool:
        """
        Detect if there is a 'raise' statement in the body.
        """
        for s in stmts:
            for node in ast.walk(s):
                if isinstance(node, ast.Raise):
                    return True
        return False


def analyze_file(path: Path) -> List[Dict[str, Any]]:
    try:
        source = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return []

    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError:
        return []

    visitor = ExceptionSmellVisitor(str(path))
    visitor.visit(tree)
    return visitor.smells


def analyze_project(root: Path) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            if name.endswith(".py"):
                print(f"Analyzing {name}...")
                file_path = Path(dirpath) / name
                results.extend(analyze_file(file_path))
    return results


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Analyze Python project for exception-handling smells using AST."
    )
    parser.add_argument(
        "path",
        type=str,
        help="Path to project root or single .py file",
    )
    args = parser.parse_args()

    target = Path(args.path)
    if target.is_file() and target.suffix == ".py":
        smells = analyze_file(target)
    else:
        smells = analyze_project(target)

    print(f"{'File':45}  {'Line':4}  {'Kind':20}  Details")
    print("-" * 100)
    for s in smells:
        print(
            f"{s['file'][:45]:45}  "
            f"{s['lineno']:4d}  "
            f"{s['kind'][:20]:20}  "
            f"{s['details']}"
        )


if __name__ == "__main__":
    main()
