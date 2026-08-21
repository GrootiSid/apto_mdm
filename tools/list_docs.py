#!/usr/bin/env python3
"""List every document in the AptoMDM repo.

Replaces a hand-maintained file list, which cannot survive 73 modules without
going stale. This reads the filesystem, so it is always current.

    python tools/list_docs.py            # every document, grouped by folder
    python tools/list_docs.py --modules  # module design docs only
    python tools/list_docs.py --check    # flag scaffold-only and empty documents
    python tools/list_docs.py --paths    # bare paths, for piping into other tools

Read-only. This script never writes, moves or removes anything.
"""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _lib import (  # noqa: E402
    MODULE_COUNT,
    PHASE_COUNT,
    DocFile,
    iter_docs,
    iter_module_docs,
    repo_root,
)


def _group(docs: list[DocFile]) -> dict[str, list[DocFile]]:
    groups: dict[str, list[DocFile]] = defaultdict(list)
    for doc in docs:
        parent = doc.path.parent.relative_to(doc.root).as_posix()
        groups[parent].append(doc)
    return dict(sorted(groups.items()))


def cmd_list(docs: list[DocFile]) -> int:
    if not docs:
        print("No documents found.")
        return 0
    for folder, items in _group(docs).items():
        print(f"\n{folder}/")
        for doc in items:
            flag = "  [scaffold]" if doc.is_scaffold else ""
            print(f"  {doc.path.name:<62} {doc.lines:>5} lines{flag}")
    total_words = sum(d.words for d in docs)
    print(f"\n{len(docs)} document(s), {total_words:,} words total.")
    return 0


def cmd_modules(root: Path) -> int:
    mods = sorted(
        iter_module_docs(root),
        key=lambda d: [int(p) for p in (d.module_number or "0").split(".")],
    )
    if not mods:
        print(f"No module documents yet. {MODULE_COUNT} planned across {PHASE_COUNT} phases.")
        return 0
    for doc in mods:
        state = "scaffold" if doc.is_scaffold else "authored"
        print(f"  {doc.module_number:<8} {doc.module_title:<48} {state:<9} {doc.rel}")
    pct = len(mods) / MODULE_COUNT * 100
    print(f"\n{len(mods)} of {MODULE_COUNT} modules have documents ({pct:.0f}%).")
    return 0


def cmd_check(docs: list[DocFile]) -> int:
    empty = [d for d in docs if d.words < 20]
    scaffolds = [d for d in docs if d.is_scaffold and d not in empty]

    if empty:
        print("Empty or near-empty (under 20 words):")
        for doc in empty:
            print(f"  {doc.rel}  ({doc.words} words)")
        print()

    if scaffolds:
        print("Scaffolds awaiting content:")
        for doc in scaffolds:
            print(f"  {doc.rel}")
        print()

    authored = len(docs) - len(empty) - len(scaffolds)
    print(f"{authored} authored, {len(scaffolds)} scaffold, {len(empty)} empty.")
    # Scaffolds are an expected state, not an error — exit 0 either way.
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--modules", action="store_true", help="module design docs only")
    g.add_argument("--check", action="store_true", help="flag scaffold and empty docs")
    g.add_argument("--paths", action="store_true", help="bare paths, one per line")
    args = ap.parse_args(argv)

    try:
        root = repo_root()
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.modules:
        return cmd_modules(root)

    docs = list(iter_docs(root))

    if args.paths:
        for doc in docs:
            print(doc.rel)
        return 0
    if args.check:
        return cmd_check(docs)
    return cmd_list(docs)


if __name__ == "__main__":
    raise SystemExit(main())
