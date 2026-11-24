#!/usr/bin/env python3
"""One-Sentence Absurd Invention Pitch — entry point.

Reads entry.txt (shipped in this repo), validates the house gate
(1-220 UTF-8 characters, one sentence, not only whitespace),
and writes the exact bytes to /output/entry.txt for the grader.

Deterministic: the same entry.txt always produces the same
/output/entry.txt, byte for byte. No network, no secrets, no
files outside this repository.
"""

import os
import sys

MAX_CHARS = 220
TERMINATORS = ".!?"


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    entry_path = os.path.join(here, "entry.txt")
    with open(entry_path, "r", encoding="utf-8") as f:
        entry = f.read().strip()

    # Gate 1: 1-220 characters, not only whitespace.
    if not entry:
        print("FAIL: entry is empty", file=sys.stderr)
        return 1
    if len(entry) > MAX_CHARS:
        print(
            f"FAIL: entry is {len(entry)} chars, max {MAX_CHARS}",
            file=sys.stderr,
        )
        return 1

    # Gate 2: exactly one sentence — a single terminal mark, at the end.
    if sum(entry.count(t) for t in TERMINATORS) != 1:
        print("FAIL: entry is not exactly one sentence", file=sys.stderr)
        return 1
    if entry[-1] not in TERMINATORS:
        print("FAIL: entry does not end with terminal punctuation", file=sys.stderr)
        return 1
    if "\n" in entry:
        print("FAIL: entry spans more than one line", file=sys.stderr)
        return 1

    # Gate 3: the sentence must say something — at least one letter.
    if not any(ch.isalpha() for ch in entry):
        print("FAIL: entry has no letters", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(entry)

    # Read-back: the grader must see exactly the validated bytes.
    with open(out_path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != entry:
        print("FAIL: read-back mismatch on /output/entry.txt", file=sys.stderr)
        return 1

    print(entry)
    print(f"OK: {len(entry)} chars, 1 sentence -> {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
