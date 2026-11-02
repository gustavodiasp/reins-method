#!/usr/bin/env python3
"""
Validates check_adapter_stack_overlaps() (bin/reins), wired into `reins doctor`.

Found while deciding whether to chase full multi-agent conflict resolution
(rejected — no real runtime boundary to enforce it, and two earlier attempts
at enforcement, MCP tool-gating and a Claude Code mod hook, were already
abandoned as bypassable/incomplete). This is the one piece of that discussion
that was real, small, and deterministic: `config_add_adapter()`/
`cmd_new_adapter()` never validate ADAPTER.md's `stacks:` field, so two
configured adapters that both claim the same stack load together silently —
nothing today tells the user their own floor.md files might disagree. This
test is about that syntactic overlap (plain comma list comparison), not about
judging whether two floor.md files' prose actually conflicts — that is
explicitly out of scope, per the function's own docstring in bin/reins.

Verification:
  1. Two configured adapters whose `stacks:` lists share a stack -> `reins
     doctor` prints a warning naming both adapters and the shared stack.
  2. Two configured adapters with disjoint stacks -> no such warning (no
     false positive).

Run with: python3 tools/tests/adapter_stack_overlap_test.py
"""
import os
import shutil
import subprocess
import sys
import tempfile

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REINS_BIN = os.path.join(REPO_ROOT, "bin", "reins")


def _make_fixture(overlap: bool) -> str:
    home = tempfile.mkdtemp(prefix="reins-adapter-overlap-")
    reins_home = os.path.join(home, ".reins")
    user_dir = os.path.join(reins_home, "user")
    adapters_dir = os.path.join(user_dir, "adapters")
    os.makedirs(adapters_dir)
    os.makedirs(os.path.join(reins_home, "core"))

    second_stack = "node" if overlap else "python"
    for name, stack in (("adapter-a", "node"), ("adapter-b", second_stack)):
        adapter_dir = os.path.join(adapters_dir, name)
        os.makedirs(os.path.join(adapter_dir, "standards"))
        with open(os.path.join(adapter_dir, "ADAPTER.md"), "w") as f:
            f.write(
                f"---\nname: {name}\nstacks: [{stack}]\n"
                "author: test\nversion: 0.1.0\n---\n"
            )

    with open(os.path.join(user_dir, "config.yaml"), "w") as f:
        f.write("adapters:\n  - adapter-a\n  - adapter-b\n")

    return home


def _run_doctor(home: str) -> str:
    env = dict(os.environ)
    env["HOME"] = home
    env["REINS_HOME"] = os.path.join(home, ".reins")
    result = subprocess.run(
        ["bash", REINS_BIN, "doctor"],
        env=env,
        capture_output=True,
        text=True,
        timeout=15,
    )
    return result.stdout + result.stderr


def test_overlapping_stacks_warn() -> bool:
    home = _make_fixture(overlap=True)
    try:
        output = _run_doctor(home)
    finally:
        shutil.rmtree(home)

    ok = "adapter-a" in output and "adapter-b" in output and "both declare stack" in output and '"node"' in output
    print(f"[overlap] warning naming both adapters + shared stack present: {ok}")
    if not ok:
        print(output)
    return ok


def test_non_overlapping_stacks_silent() -> bool:
    home = _make_fixture(overlap=False)
    try:
        output = _run_doctor(home)
    finally:
        shutil.rmtree(home)

    ok = "both declare stack" not in output
    print(f"[no overlap] no false-positive warning: {ok}")
    if not ok:
        print(output)
    return ok


if __name__ == "__main__":
    r1 = test_overlapping_stacks_warn()
    r2 = test_non_overlapping_stacks_silent()

    print("\n=== Summary ===")
    print(f"overlapping adapter stacks -> warned:      {r1}")
    print(f"disjoint adapter stacks -> stayed silent:  {r2}")

    if not (r1 and r2):
        print("\nFAIL: adapter stack overlap detection does not hold.")
        sys.exit(1)
    print("\nPASS: reins doctor warns on overlapping adapter stacks only.")
    sys.exit(0)
