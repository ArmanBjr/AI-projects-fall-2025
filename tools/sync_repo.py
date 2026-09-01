#!/usr/bin/env python3
"""Prepare AI course repo at Code/ root: merge nested git content and normalize layout."""
from __future__ import annotations

import shutil
from pathlib import Path

CODE = Path(r"E:\University\University_Subjects\5th\Artificial_Intelligence\Code")
NESTED = CODE / "Artificial_Intelligence-Course"

SKIP_TOP = {
    "Expect",
    "expected",
    "strawberry",
    "Artificial_Intelligence-Course",
    "tools",
    "Codes.zip",
    "StrawberryProlog_3_0_Beta4.exe",
    "Prolog-1.ppt",
    "Prolog-2.ppt",
    "Prolog-3.ppt",
    ".gitkeep",
}

RENAME = {
    "SESSION7": "session7",
    "Session8": "session8",
    "Session-10": "session10",
    "Session3": "session3",
    "Prolog": "prolog",
}


def rm_tree(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)


def copy_tree(src: Path, dst: Path) -> None:
    if dst.exists():
        rm_tree(dst)
    shutil.copytree(
        src,
        dst,
        ignore=shutil.ignore_patterns(
            "__pycache__",
            "__MACOSX",
            ".DS_Store",
            "*.pyc",
            ".git",
        ),
    )


def main() -> None:
    # Move nested repo-only paths to Code root
    for name in ("AI-graphicSearch", "view"):
        src = NESTED / name
        dst = CODE / name
        if src.exists():
            copy_tree(src, dst)
            print(f"merged {name}/")

    # Prefer nested session4 (includes report) and session5 (canonical CSP)
    for name in ("session4", "session5"):
        src = NESTED / name
        dst = CODE / name
        if src.exists():
            copy_tree(src, dst)
            print(f"merged {name}/")

    # Normalize folder names
    for old, new in RENAME.items():
        src = CODE / old
        dst = CODE / new
        if src.exists() and not dst.exists():
            src.rename(dst)
            print(f"renamed {old} -> {new}")
        elif src.exists() and dst.exists() and old == "Session-10":
            rm_tree(CODE / "session10")
            src.rename(dst)
            print("replaced session10 with Session-10")

    # Remove duplicate session2 (same topic as AI-graphicSearch)
    rm_tree(CODE / "session2")
    print("removed duplicate session2/")

    print("done")


if __name__ == "__main__":
    main()
