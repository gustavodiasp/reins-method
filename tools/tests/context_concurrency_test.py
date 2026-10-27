#!/usr/bin/env python3
"""
Validates the mkdir()-lock + targeted-edit convention that
core/workflow/3_implement.md's "After confirmation — update the context file"
step prescribes for concurrent sessions updating a shared contexts/<type>_<slug>.md
file (see core/templates/context.md's "## Current step" multi-component format).

This is a real, persisted repo artifact (not a one-off scratch script) per the
project's own standards.md rule #1/#5. History: a prior version of this test
was run manually and discarded (code review flagged the gap); the first
persisted version used "optimistic concurrency" (re-stat right before
writing, retry on mismatch) and was re-reviewed as passing — but re-testing
at a stricter standard found it still produced a real, measured 1/20 silent
double-success collision, because the final stat-check and the rename() are
two separate syscalls with a real gap between them. This version replaces
that with an actual mkdir()-based mutex (atomic on every POSIX filesystem,
no extra binary required) and keeps the insufficient optimistic version
alongside it, under a new name, specifically so this regression stays
provable instead of silently reverified away.

Harness hardening (round-3 code review — three independent reviewers all ran
this script and found it crashed or produced false-positive "corruption"
verdicts, especially when run from a sandboxed Bash call, which is the exact
tool class an agent would actually use):
  - The file path is unique per process (tempdir + pid), not a shared fixed
    `/tmp/...` path — the old fixed path meant two invocations running close
    together (e.g. two reviewers independently told to "run this yourself")
    could stomp on each other's file, producing failures that had nothing to
    do with the lock's actual correctness.
  - Every variable the worker processes need (file path, lock dir path) is
    passed as an explicit argument, never read off a module-level global —
    `multiprocessing` defaults to the "spawn" start method on macOS, which
    re-imports this module fresh in each child process; a global reassigned
    at runtime in the parent (e.g. inside `if __name__ == "__main__":`) is
    NOT visible to a spawned child, only the value present at import time is.
  - `naive_edit`'s read and `worker_different_lines`' recovery read are both
    now guarded against `FileNotFoundError` (a real possibility: another
    process's write can make the file briefly absent during its own
    replace), and the recovery path's `int(line.split()[1])` no longer
    crashes the whole script on a malformed/unexpected line — it raises a
    clear, caught error instead.
  - Each scenario run is wrapped so an unexpected crash in one variant (most
    likely `naive`, which is deliberately unprotected — that's the point of
    the baseline) is reported as a failure for that run instead of killing
    the process before the other variants get to report their own results.

Run with: python3 tools/tests/context_concurrency_test.py

Three variants compared head to head:
  1. "naive" — read, locate target line, replace in memory, write the whole
     file back, with NO check that the file changed since the read. The
     original pre-fix behavior. Expected: lost updates under real
     concurrency (proves the bug is real, not hypothetical).
  2. "unsafe_optimistic" — re-stat immediately before writing, retry on a
     detected change. The first fix attempted. Expected: fixes the common
     (different-line) case, but can still produce a rare silent
     double-success collision on the deliberate same-line conflict case —
     this run quantifies how rare.
  3. "safe (mkdir lock)" — a real short-lived mutex around the whole
     read-modify-write. Expected: zero lost updates AND zero silent
     collisions, because no other process can be inside the critical
     section at all while one holds the lock.
"""
import os
import sys
import time
import random
import tempfile
import multiprocessing

N_ITERATIONS = 200


def make_file(file_path):
    lines = [
        "---\n",
        "type: chore\n",
        "status: active\n",
        "branches: { backend: b, frontend: f }\n",
        "---\n",
        "\n",
        "## Current step\n",
        "(backend) 00 — start\n",
        "(frontend) 00 — start\n",
    ]
    with open(file_path, "w") as f:
        f.writelines(lines)


def naive_edit(file_path, old_string, new_string):
    """Pre-fix behavior: read, replace in memory, write whole file. No check
    that the file is still what we think it is. Deliberately unprotected —
    that's what makes it the broken baseline — but a transient
    FileNotFoundError (the file briefly absent mid-write by the OTHER
    process) is still reported as a normal "couldn't apply, caller should
    retry" condition rather than an uncaught crash that would kill the whole
    test run before safer variants get to report their own results."""
    try:
        with open(file_path, "r") as f:
            content = f.read()
    except FileNotFoundError:
        raise RuntimeError(f"file transiently absent while reading: {file_path}")
    if content.count(old_string) != 1:
        raise RuntimeError(f"old_string not found exactly once: {old_string!r}")
    new_content = content.replace(old_string, new_string, 1)
    # Simulate real-world latency between "decide the edit" and "write it" —
    # an LLM agent's tool-call round trip is not instantaneous. Without this,
    # two processes on a fast loopback would rarely interleave at all.
    time.sleep(random.uniform(0, 0.003))
    with open(file_path, "w") as f:
        f.write(new_content)


def unsafe_optimistic_edit(file_path, old_string, new_string, max_retries=40):
    """FIRST fix attempted: re-read immediately before the edit, re-check the
    file hasn't changed right before the write, retry on a detected change —
    "optimistic concurrency" with no real lock. Kept here (renamed, not
    deleted) because empirical re-testing found it INSUFFICIENT: stat_final
    and os.rename() are two separate syscalls, not one atomic operation —
    another process can complete an entire read-modify-write cycle in the
    gap between this process's last stat check and its rename. Measured:
    roughly 1/20 to 2/20 runs under this test's stress load produced a
    genuine silent double-success collision (both processes "succeeded",
    only one write survived) — small, but real, not theoretical. This
    confirms the instruction this function embodies was not sufficient on
    its own and needed the real lock in safe_edit() below."""
    for attempt in range(max_retries):
        try:
            stat_before = os.stat(file_path)
            with open(file_path, "r") as f:
                content = f.read()
        except FileNotFoundError:
            time.sleep(0.0005 * (attempt + 1))
            continue
        count = content.count(old_string)
        if count == 0:
            time.sleep(0.0005 * (attempt + 1))
            continue
        if count > 1:
            raise RuntimeError(f"old_string not unique ({count}x): {old_string!r}")
        new_content = content.replace(old_string, new_string, 1)
        time.sleep(random.uniform(0, 0.003))  # same simulated latency
        try:
            stat_now = os.stat(file_path)
        except FileNotFoundError:
            time.sleep(0.0005 * (attempt + 1))
            continue
        if (stat_now.st_mtime_ns, stat_now.st_size) != (stat_before.st_mtime_ns, stat_before.st_size):
            time.sleep(0.0005 * (attempt + 1))
            continue
        tmp = f"{file_path}.tmp.{os.getpid()}.{attempt}"
        with open(tmp, "w") as f:
            f.write(new_content)
        try:
            stat_final = os.stat(file_path)
        except FileNotFoundError:
            os.remove(tmp)
            time.sleep(0.0005 * (attempt + 1))
            continue
        if (stat_final.st_mtime_ns, stat_final.st_size) != (stat_before.st_mtime_ns, stat_before.st_size):
            os.remove(tmp)
            time.sleep(0.0005 * (attempt + 1))
            continue
        os.rename(tmp, file_path)  # atomic, but the CHECK before it is not atomic with it
        return
    raise RuntimeError(f"max retries exceeded for edit {old_string!r} -> {new_string!r}")


def acquire_lock(lock_dir, max_wait_s=5.0):
    """mkdir() is the one filesystem operation POSIX guarantees is atomic
    without any extra tooling (no flock binary needed — portable to macOS,
    Linux, WSL2, anywhere this repo's own install.sh already targets): it
    either creates the directory and returns, or fails with FileExistsError
    if another process already holds it. That's a real mutex, not a
    heuristic. Stale-lock recovery (a crashed holder) is deliberately out of
    scope for this test — see the note added to 3_implement.md."""
    deadline = time.monotonic() + max_wait_s
    while True:
        try:
            os.mkdir(lock_dir)
            return
        except FileExistsError:
            if time.monotonic() > deadline:
                raise RuntimeError(f"timed out waiting for lock {lock_dir}")
            time.sleep(0.0005)


def release_lock(lock_dir):
    os.rmdir(lock_dir)


def safe_edit(file_path, old_string, new_string, lock_dir=None):
    """REAL fix: a short-lived mkdir()-based lock around the entire
    read-modify-write — not optimistic re-checking, an actual mutex. While
    held, no other process can be inside this function at all, so there is
    no gap for another writer to land in between this process's check and
    its write. Nothing to retry against once the lock is held — the file
    cannot have changed since we acquired exclusive access to it."""
    if lock_dir is None:
        lock_dir = file_path + ".lock"
    acquire_lock(lock_dir)
    try:
        with open(file_path, "r") as f:
            content = f.read()
        count = content.count(old_string)
        if count == 0:
            raise RuntimeError(f"old_string not found (already applied by a prior holder?): {old_string!r}")
        if count > 1:
            raise RuntimeError(f"old_string not unique ({count}x): {old_string!r}")
        new_content = content.replace(old_string, new_string, 1)
        time.sleep(random.uniform(0, 0.003))  # same simulated latency, now safely inside the lock
        tmp = f"{file_path}.tmp.{os.getpid()}"
        with open(tmp, "w") as f:
            f.write(new_content)
        os.rename(tmp, file_path)  # atomic, and nobody else can be mid-edit while we hold the lock
    finally:
        release_lock(lock_dir)


def worker_different_lines(edit_fn, file_path, component, n):
    """Each process only ever edits its OWN component's line — the common
    case: two sessions, two different lines, same shared file. Mirrors the
    actual instruction given to an agent in 3_implement.md: on a failed/
    conflicting edit, re-read and retry THE SAME increment — never abandon
    it and move on, which would just be giving up on recording a real,
    already-decided state transition."""
    current = 0
    while current < n:
        old = f"({component}) {current:02d} — start\n" if current == 0 else f"({component}) {current:02d} — step\n"
        new = f"({component}) {current + 1:02d} — step\n"
        try:
            edit_fn(file_path, old, new)
            current += 1
        except RuntimeError:
            # Re-read what's actually on disk for this component and retry
            # from there — the increment is not abandoned, just re-attempted
            # against fresh content. Both the read and the parse are guarded:
            # the file can be transiently absent (another writer mid-replace),
            # and a line that doesn't match the expected "NN — step" shape
            # (e.g. leftover content from an unrelated scenario, if paths were
            # ever accidentally shared) must not crash the whole script.
            try:
                with open(file_path, "r") as f:
                    content = f.read()
            except FileNotFoundError:
                time.sleep(0.001)
                continue
            found = False
            for line in content.splitlines():
                if line.startswith(f"({component}) "):
                    parts = line.split()
                    if len(parts) >= 2 and parts[1].isdigit():
                        current = int(parts[1])
                        found = True
                    break
            if not found:
                # Could not determine current state from disk — treat as a
                # transient read, not a fatal error. Retry the same increment.
                time.sleep(0.001)
    return current


def run_different_lines_scenario(edit_fn, label, file_path, lock_dir):
    make_file(file_path)
    try:
        with multiprocessing.Pool(2) as pool:
            pool.starmap(
                worker_different_lines,
                [
                    (edit_fn, file_path, "backend", N_ITERATIONS),
                    (edit_fn, file_path, "frontend", N_ITERATIONS),
                ],
            )
        with open(file_path, "r") as f:
            content = f.read()
        backend_final = next(l for l in content.splitlines() if l.startswith("(backend)"))
        frontend_final = next(l for l in content.splitlines() if l.startswith("(frontend)"))
        backend_ok = backend_final == f"(backend) {N_ITERATIONS:02d} — step"
        frontend_ok = frontend_final == f"(frontend) {N_ITERATIONS:02d} — step"
        print(f"[{label}] backend line: {backend_final!r} (expected step {N_ITERATIONS}) -> {'PASS' if backend_ok else 'FAIL — LOST UPDATE(S)'}")
        print(f"[{label}] frontend line: {frontend_final!r} (expected step {N_ITERATIONS}) -> {'PASS' if frontend_ok else 'FAIL — LOST UPDATE(S)'}")
        return backend_ok and frontend_ok
    except Exception as e:
        # A crash in one variant (most likely `naive`, deliberately
        # unprotected) must not prevent the other variants from running and
        # reporting their own results.
        print(f"[{label}] CRASHED: {e!r} -> FAIL")
        return False


def worker_same_line_collision(edit_fn, file_path, result_queue, label):
    try:
        edit_fn(file_path, "(backend) 00 — start\n", f"(backend) WON-BY-{label}\n")
        result_queue.put((label, "succeeded"))
    except RuntimeError as e:
        result_queue.put((label, f"failed loudly: {e}"))
    except Exception as e:
        result_queue.put((label, f"failed loudly (unexpected): {e!r}"))


def run_collision_scenario(edit_fn, label, file_path, lock_dir):
    make_file(file_path)
    try:
        q = multiprocessing.Queue()
        p1 = multiprocessing.Process(target=worker_same_line_collision, args=(edit_fn, file_path, q, "A"))
        p2 = multiprocessing.Process(target=worker_same_line_collision, args=(edit_fn, file_path, q, "B"))
        p1.start()
        p2.start()
        p1.join()
        p2.join()
        outcomes = [q.get(), q.get()]
        with open(file_path, "r") as f:
            content = f.read()
        print(f"[{label}] collision outcomes: {outcomes}")
        print(f"[{label}] final file state: {[l for l in content.splitlines() if 'backend' in l]}")
        # The real safety property: it must never be the case that BOTH sides
        # report "succeeded" when only one write can actually be reflected in a
        # single-line collision — that combination is exactly silent corruption
        # (both callers believe their change landed; only one did; no error told
        # anyone). Zero or one reported success is safe either way: zero means
        # both failed loudly (no one assumed their write landed when it didn't);
        # one means the winner's belief matches reality and the loser was told
        # it didn't land.
        succeeded = [o for o in outcomes if o[1] == "succeeded"]
        no_silent_corruption = len(succeeded) <= 1
        if len(succeeded) == 1:
            # The one reported success must match what's actually on disk.
            winner_label = succeeded[0][0]
            no_silent_corruption = f"WON-BY-{winner_label}" in content
        return no_silent_corruption
    except Exception as e:
        print(f"[{label}] CRASHED: {e!r} -> FAIL")
        return False


def cleanup(file_path, lock_dir):
    if os.path.exists(file_path):
        os.remove(file_path)
    if os.path.isdir(lock_dir):
        os.rmdir(lock_dir)
    parent = os.path.dirname(file_path)
    prefix = os.path.basename(file_path) + ".tmp."
    for f in os.listdir(parent):
        if f.startswith(prefix):
            os.remove(os.path.join(parent, f))


if __name__ == "__main__":
    COLLISION_RUNS = 20  # the double-success failure mode is rare (~1/20) — run enough times to catch it

    # Unique per-process working directory: avoids any cross-run interference
    # if this script is invoked more than once around the same time (e.g. by
    # more than one reviewer independently told to run it).
    run_dir = tempfile.mkdtemp(prefix="reins-ctx-test-")
    FILE = os.path.join(run_dir, "context-concurrency-test.md")
    LOCK_DIR = FILE + ".lock"

    print("=== Scenario 1: different-line concurrent edits (the common case) ===")
    naive_ok = run_different_lines_scenario(naive_edit, "naive whole-file write", FILE, LOCK_DIR)
    cleanup(FILE, LOCK_DIR)
    unsafe_ok = run_different_lines_scenario(unsafe_optimistic_edit, "unsafe optimistic (re-stat, no lock)", FILE, LOCK_DIR)
    cleanup(FILE, LOCK_DIR)
    safe_ok = run_different_lines_scenario(safe_edit, "safe (mkdir lock)", FILE, LOCK_DIR)
    cleanup(FILE, LOCK_DIR)

    print(f"\n=== Scenario 2: same-line collision (deliberate conflict), {COLLISION_RUNS} repeated runs per variant ===")
    naive_corrupted = 0
    unsafe_corrupted = 0
    safe_corrupted = 0
    for i in range(COLLISION_RUNS):
        if not run_collision_scenario(naive_edit, f"naive run {i+1}/{COLLISION_RUNS}", FILE, LOCK_DIR):
            naive_corrupted += 1
        cleanup(FILE, LOCK_DIR)
        if not run_collision_scenario(unsafe_optimistic_edit, f"unsafe_optimistic run {i+1}/{COLLISION_RUNS}", FILE, LOCK_DIR):
            unsafe_corrupted += 1
        cleanup(FILE, LOCK_DIR)
        if not run_collision_scenario(safe_edit, f"safe (mkdir lock) run {i+1}/{COLLISION_RUNS}", FILE, LOCK_DIR):
            safe_corrupted += 1
        cleanup(FILE, LOCK_DIR)

    os.rmdir(run_dir)

    print("\n=== Summary ===")
    print(f"naive:             different-line lost updates? {'YES' if not naive_ok else 'no'}  |  silent collisions: {naive_corrupted}/{COLLISION_RUNS}")
    print(f"unsafe_optimistic: different-line lost updates? {'YES' if not unsafe_ok else 'no'}  |  silent collisions: {unsafe_corrupted}/{COLLISION_RUNS}")
    print(f"safe (mkdir lock): different-line lost updates? {'YES' if not safe_ok else 'no'}  |  silent collisions: {safe_corrupted}/{COLLISION_RUNS}")

    failures = []
    if not safe_ok:
        failures.append("different-line case still lost updates under the mkdir-lock fix")
    if safe_corrupted > 0:
        failures.append(f"same-line collision produced silent corruption {safe_corrupted}/{COLLISION_RUNS} times under the mkdir-lock fix")

    if failures:
        print("\nFAIL: " + "; ".join(failures))
        sys.exit(1)
    print("\nPASS: the mkdir-lock fix eliminates lost updates on the different-line case, "
          f"and produced zero silent collisions across {COLLISION_RUNS} same-line collision runs "
          "(unsafe_optimistic and naive results above are the baseline this fix had to beat, not a pass/fail gate).")
    sys.exit(0)
