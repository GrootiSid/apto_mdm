"""Shared helpers for AptoMDM doc-set maintenance scripts.

Standard library only, deliberately. A maintenance script that needs a virtualenv
stops getting run, and then the doc set drifts.

Nothing in this module deletes or truncates a file. Writes go through
`write_text_atomic`, which refuses to replace existing content with something
shorter unless explicitly allowed.
"""

from __future__ import annotations

import os
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator

# --------------------------------------------------------------------------
# Layout
# --------------------------------------------------------------------------

#: Number of phases planned (Bible v1.2, Section 7).
PHASE_COUNT = 16

#: Total modules planned (Bible v1.2, Section 7).
MODULE_COUNT = 73

DOCS_DIRNAME = "AptoMDM_Docs"
MODULES_DIRNAME = "Modules"

#: Directories that hold documents, relative to the repo root.
DOC_DIRS = (
    DOCS_DIRNAME,
    MODULES_DIRNAME,
    "Development_Docs",
    "QA",
    "UIUX",
)

#: Never walked when discovering documents.
SKIP_DIRS = frozenset(
    {".git", ".claude", "__pycache__", ".venv", "venv", "node_modules", ".idea", ".vscode"}
)

MODULE_FILE_RE = re.compile(
    r"^AptoMDM_Module_(?P<phase>\d+)_(?P<seq>\d+(?:_\d+)?)_(?P<name>.+)\.md$"
)

PHASE_DIR_RE = re.compile(r"^Phase_(?P<num>\d{2})$")

#: Markers that identify a document as a scaffold rather than authored content.
SCAFFOLD_MARKERS = ("status: scaffold", "**status: scaffold", "_(to define)_", "_(none yet)_")


def repo_root(start: Path | str | None = None) -> Path:
    """Walk upward from *start* to the repo root.

    Identified by containing the docs directory, or failing that a .git directory,
    so the scripts work from any subdirectory.
    """
    here = Path(start or __file__).resolve()
    if here.is_file():
        here = here.parent
    for candidate in (here, *here.parents):
        if (candidate / DOCS_DIRNAME).is_dir() or (candidate / ".git").is_dir():
            return candidate
    raise RuntimeError(
        f"Could not locate the apto_mdm repo root walking up from {here}. "
        f"Expected a directory containing {DOCS_DIRNAME}/ or .git/."
    )


def docs_dir(root: Path | None = None) -> Path:
    return (root or repo_root()) / DOCS_DIRNAME


def modules_dir(root: Path | None = None) -> Path:
    return (root or repo_root()) / MODULES_DIRNAME


def phase_dir(phase: int, root: Path | None = None) -> Path:
    """Path to a phase folder, zero-padded: phase 1 -> Modules/Phase_01."""
    if not 1 <= phase <= PHASE_COUNT:
        raise ValueError(f"phase must be 1..{PHASE_COUNT}, got {phase!r}")
    return modules_dir(root) / f"Phase_{phase:02d}"


# --------------------------------------------------------------------------
# Document discovery
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class DocFile:
    """A markdown document in the repo."""

    path: Path
    root: Path

    @property
    def rel(self) -> str:
        return self.path.relative_to(self.root).as_posix()

    @property
    def is_module(self) -> bool:
        return MODULE_FILE_RE.match(self.path.name) is not None

    @property
    def module_number(self) -> str | None:
        """Dotted module number, e.g. '1.1' or '1.6.2'. None if not a module doc."""
        m = MODULE_FILE_RE.match(self.path.name)
        if not m:
            return None
        return f"{m.group('phase')}." + m.group("seq").replace("_", ".")

    @property
    def module_title(self) -> str | None:
        m = MODULE_FILE_RE.match(self.path.name)
        return m.group("name").replace("_", " ") if m else None

    @property
    def phase(self) -> int | None:
        m = MODULE_FILE_RE.match(self.path.name)
        return int(m.group("phase")) if m else None

    def text(self) -> str:
        return self.path.read_text(encoding="utf-8")

    @property
    def lines(self) -> int:
        return sum(1 for _ in self.path.open(encoding="utf-8"))

    @property
    def words(self) -> int:
        return len(self.text().split())

    @property
    def is_scaffold(self) -> bool:
        """True if the document still advertises itself as a scaffold."""
        head = self.text()[:4000].lower()
        return any(marker in head for marker in SCAFFOLD_MARKERS)


def iter_docs(root: Path | None = None, dirs: Iterable[str] | None = None) -> Iterator[DocFile]:
    """Yield every markdown document under the doc directories, sorted by path."""
    root = root or repo_root()
    found: list[Path] = []
    for name in dirs or DOC_DIRS:
        base = root / name
        if not base.is_dir():
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
            for fn in sorted(filenames):
                if fn.lower().endswith(".md"):
                    found.append(Path(dirpath) / fn)
    for p in sorted(found, key=lambda p: p.as_posix()):
        yield DocFile(path=p, root=root)


def iter_module_docs(root: Path | None = None) -> Iterator[DocFile]:
    for doc in iter_docs(root, dirs=(MODULES_DIRNAME,)):
        if doc.is_module:
            yield doc


def module_filename(phase: int, seq: str, name: str) -> str:
    """Build a conforming module filename.

    >>> module_filename(1, "1", "Tenant & Organization Setup")
    'AptoMDM_Module_1_1_Tenant_Organization_Setup.md'
    """
    return f"AptoMDM_Module_{phase}_{seq}_{slug(name)}.md"


def slug(name: str) -> str:
    """Underscore_Title_Case token suitable for a filename."""
    decomposed = unicodedata.normalize("NFKD", name)
    ascii_only = decomposed.encode("ascii", "ignore").decode("ascii")
    words = re.findall(r"[A-Za-z0-9]+", ascii_only)
    return "_".join(words)


# --------------------------------------------------------------------------
# Markdown table helpers
# --------------------------------------------------------------------------


def parse_table_row(line: str) -> list[str] | None:
    """Split a markdown table row into stripped cells, or None if not a row."""
    s = line.strip()
    if not s.startswith("|") or not s.endswith("|") or len(s) < 2:
        return None
    return [c.strip() for c in s[1:-1].split("|")]


def is_table_divider(line: str) -> bool:
    cells = parse_table_row(line)
    if cells is None:
        return False
    return bool(cells) and all(re.fullmatch(r":?-{2,}:?", c) for c in cells)


def format_table_row(cells: Iterable[str]) -> str:
    return "| " + " | ".join(str(c).strip() for c in cells) + " |"


# --------------------------------------------------------------------------
# Safe writes
# --------------------------------------------------------------------------


def write_text_atomic(path: Path, text: str, *, allow_shrink: bool = False) -> None:
    """Write *text* to *path* via a temp file in the same directory, then replace.

    Guards against the two ways doc-maintenance scripts destroy work: a partial
    write leaving a truncated file, and a logic bug silently replacing a long
    document with a short one. Pass ``allow_shrink=True`` only when a reduction in
    size is genuinely intended.
    """
    path = Path(path)
    if path.exists() and not allow_shrink:
        old = len(path.read_text(encoding="utf-8"))
        if len(text) < old * 0.9:
            raise ValueError(
                f"Refusing to shrink {path.name} from {old} to {len(text)} chars. "
                f"Pass allow_shrink=True if this is intended."
            )
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)  # atomic on the same filesystem


if __name__ == "__main__":  # pragma: no cover
    import doctest

    root = repo_root()
    failures, tests = doctest.testmod()
    print(f"repo root: {root}")
    print(f"doctests:  {tests - failures}/{tests} passed")
    print(f"documents: {sum(1 for _ in iter_docs(root))}")
