#!/usr/bin/env python3
"""Run the repository's lightweight verification checks."""
from __future__ import annotations

import py_compile
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PYTHON_DIRS = [ROOT / "scripts"]


def iter_python_files() -> list[Path]:
    files: list[Path] = []
    for path in PYTHON_DIRS:
        files.extend(sorted(path.glob("*.py")))
    return files


def compile_python_files() -> None:
    for path in iter_python_files():
        py_compile.compile(str(path), doraise=True)


def run_unittests() -> bool:
    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return result.wasSuccessful()


def main() -> None:
    compile_python_files()
    ok = run_unittests()
    if not ok:
        sys.exit(1)
    print("checks passed")


if __name__ == "__main__":
    main()
