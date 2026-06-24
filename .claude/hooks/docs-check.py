#!/usr/bin/env python3
"""
Provna documentation consistency checker.

Two modes:

  python3 docs-check.py            # full-tree audit of the public docs; prints a
                                   # report and exits 1 if any error-level finding
                                   # is present, else 0. Used by the `docs-check` skill.

  python3 docs-check.py --hook     # PostToolUse hook mode: reads the tool payload on
                                   # stdin, and if a public .md just gained a reference
                                   # to the gitignored `docs/private/` tree, exits 2 with
                                   # a message so the agent fixes it. Fails OPEN (exit 0)
                                   # on any uncertainty — it never blocks a normal edit.

Enforces the load-bearing rules from CLAUDE.md:
  - Rule #2: no public doc references `docs/private/` (path, filename, or link).
  - Rule #1: English-only public docs (no Turkish `Md.NN` / `madde` leaks).
  - Rule #8: relative links resolve; no YAML front-matter; one H1.
  - Rule #9: Mermaid labels are ASCII-safe.
Stdlib only; no dependencies.
"""

import os
import re
import sys
import json
import glob

# References to the private analysis tree that must never appear in a public doc.
PRIVATE_PATTERNS = [
    r"docs/private",
    r"\.\./private",
    r"provna-cerceve",
    r"initial-report",
    r"capraz-sentez",
    r"rakip-analizi",
]
# Softer leak signals (advisory in full mode; not blocked by the hook).
ADVISORY_PATTERNS = [r"/Users/", r"\bteardown\b"]

# The agent guides legitimately NAME docs/private when stating the rule, so they
# are exempt from the private-ref check (everything else still applies to them).
PRIVATE_REF_EXEMPT = {"CLAUDE.md", "AGENTS.md"}


def repo_root():
    # this file lives at <root>/.claude/hooks/docs-check.py
    env = os.environ.get("CLAUDE_PROJECT_DIR")
    if env and os.path.isdir(env):
        return env
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def is_public_md(path, root):
    rel = os.path.relpath(path, root)
    if rel.startswith(".."):
        return False  # outside the repo
    if not rel.endswith(".md"):
        return False
    if rel.startswith("private/") or "/private/" in rel or rel.startswith("docs/private"):
        return False
    if rel.startswith(".claude/") or "/.claude/" in rel:
        return False  # .claude/ skills+agents legitimately use YAML front-matter
    return True


def inline_code_spans(line):
    return [(m.start(), m.end()) for m in re.finditer(r"`[^`]*`", line)]


# ---------------------------------------------------------------- hook mode
def run_hook():
    # Fail OPEN on anything unexpected: a hook must never wedge a normal edit.
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)
    try:
        tool_input = payload.get("tool_input") or {}
        path = tool_input.get("file_path") or tool_input.get("path")
        if not path:
            sys.exit(0)
        root = repo_root()
        if not os.path.isfile(path) or not is_public_md(path, root):
            sys.exit(0)
        if os.path.basename(path) in PRIVATE_REF_EXEMPT:
            sys.exit(0)
        text = open(path, encoding="utf-8", errors="replace").read()
        hits = []
        for pat in PRIVATE_PATTERNS:
            for m in re.finditer(pat, text, re.I):
                ln = text[: m.start()].count("\n") + 1
                hits.append(f"  {os.path.relpath(path, root)}:{ln}  ->  {m.group(0)}")
        if hits:
            sys.stderr.write(
                "BLOCKED by docs-check: this public doc now references the gitignored "
                "docs/private/ analysis tree.\n"
                "Per CLAUDE.md rule #2, public docs must be self-contained — remove the "
                "reference and restate the fact instead.\n" + "\n".join(hits) + "\n"
            )
            sys.exit(2)
    except Exception:
        sys.exit(0)
    sys.exit(0)


# ---------------------------------------------------------------- full audit
def public_docs(root):
    out = [p for p in glob.glob(os.path.join(root, "**", "*.md"), recursive=True) if is_public_md(p, root)]
    return sorted(out)


def check_private_refs(path, text, root):
    if os.path.basename(path) in PRIVATE_REF_EXEMPT:
        return [], []
    errs, warns = [], []
    rel = os.path.relpath(path, root)
    for pat in PRIVATE_PATTERNS:
        for m in re.finditer(pat, text, re.I):
            ln = text[: m.start()].count("\n") + 1
            errs.append(f"{rel}:{ln}  private-ref  '{m.group(0)}'")
    for pat in ADVISORY_PATTERNS:
        for m in re.finditer(pat, text, re.I):
            ln = text[: m.start()].count("\n") + 1
            warns.append(f"{rel}:{ln}  leak?  '{m.group(0)}'")
    return errs, warns


def check_front_matter(path, text, root):
    rel = os.path.relpath(path, root)
    stripped = text.lstrip()
    if stripped.startswith("---"):
        return [f"{rel}:1  front-matter  starts with YAML front-matter; use an H1 + bold metadata"]
    if not stripped.startswith("# "):
        return [f"{rel}:1  no-h1  does not start with a single H1 heading"]
    return []


def check_language(path, text, root):
    rel = os.path.relpath(path, root)
    errs = []
    for m in re.finditer(r"Md\.\d", text):
        ln = text[: m.start()].count("\n") + 1
        errs.append(f"{rel}:{ln}  lang-leak  'Md.' (use 'Article')")
    for m in re.finditer(r"\bmadde\b", text, re.I):
        ln = text[: m.start()].count("\n") + 1
        errs.append(f"{rel}:{ln}  lang-leak  Turkish 'madde' in a public doc")
    return errs


def check_mermaid(path, text, root):
    rel = os.path.relpath(path, root)
    errs = []
    for m in re.finditer(r"```mermaid\n(.*?)```", text, re.S):
        block = m.group(1)
        first = block.strip().splitlines()[0] if block.strip() else ""
        base_ln = text[: m.start()].count("\n") + 1
        if "'" in block:
            errs.append(f"{rel}:{base_ln}  mermaid  apostrophe in a label (breaks strict renderers)")
        if "\\n" in block:
            errs.append(f"{rel}:{base_ln}  mermaid  literal backslash-n in a label (use <br/>)")
        if first.startswith("sequenceDiagram") and ("<br/>" in block or '"' in block or ";" in block):
            errs.append(f"{rel}:{base_ln}  mermaid  sequenceDiagram note has <br/> / quote / ';'")
        if first.startswith("quadrantChart") and '"' in block:
            errs.append(f"{rel}:{base_ln}  mermaid  quadrantChart label is quoted (use plain text)")
    return errs


def check_links(path, text, root):
    rel = os.path.relpath(path, root)
    errs = []
    d = os.path.dirname(path)
    in_fence = False
    for i, line in enumerate(text.split("\n"), 1):
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        spans = inline_code_spans(line)
        for m in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", line):
            if any(s <= m.start() < e for s, e in spans):
                continue  # illustrative link inside an inline-code span
            tgt = m.group(1).strip().split("#")[0]
            if not tgt or tgt.startswith(("http://", "https://", "mailto:")):
                continue
            if not os.path.exists(os.path.normpath(os.path.join(d, tgt))):
                errs.append(f"{rel}:{i}  broken-link  '{m.group(1)}'")
    return errs


def run_full():
    root = repo_root()
    files = public_docs(root)
    errs, warns = [], []
    for p in files:
        text = open(p, encoding="utf-8", errors="replace").read()
        e, w = check_private_refs(p, text, root)
        errs += e
        warns += w
        errs += check_front_matter(p, text, root)
        errs += check_language(p, text, root)
        errs += check_mermaid(p, text, root)
        errs += check_links(p, text, root)

    print(f"docs-check — {len(files)} public docs scanned\n")
    print(f"ERRORS ({len(errs)}):" if errs else "ERRORS: none")
    for e in errs:
        print("  " + e)
    if warns:
        print(f"\nWARNINGS ({len(warns)}) — review, may be legitimate:")
        for w in warns:
            print("  " + w)
    print("\nRESULT:", "FAIL" if errs else "PASS")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    if "--hook" in sys.argv[1:]:
        run_hook()
    else:
        run_full()
