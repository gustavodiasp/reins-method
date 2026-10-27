#!/usr/bin/env python3
"""
Validates step-05's actual guarantee (see
~/.reins/user/projects/reins-method/specs/chore_v1-stabilization/step-05-spec.md
"Verification" section) — NOT the same thing as context_concurrency_test.py in
this same directory, which validates a different, later-discovered fix for the
shared contexts/<type>_<slug>.md file. This one is about
specs/<type>_<slug>_<component>.md: once a task is multi-component, each
component's spec file is a *different path* than its siblings', so there is
nothing to coordinate — isolation by construction, no lock needed. Code review
(Oscar) found that step-05's own spec'd test was never actually written: an
earlier manual run was done once and discarded, and the test that was later
persisted (context_concurrency_test.py) answers a different question. This
file closes that real gap.

Verification per the SPEC:
  1. Two processes concurrently append synthetic steps to their own
     `_backend.md`/`_frontend.md` paths in a loop. Assert two separate files
     exist, never one shared file touched by both.
  2. Closing one mid-test (deleting its file) affects only that file — assert
     the sibling's content is byte-identical before and after.

Run with: python3 tools/tests/spec_file_isolation_test.py
"""
import os
import sys
import time
import random
import hashlib
import multiprocessing

DIR = "/tmp/reins-spec-isolation-test"
BACKEND_FILE = os.path.join(DIR, "chore_x_backend.md")
FRONTEND_FILE = os.path.join(DIR, "chore_x_frontend.md")
N_STEPS = 50


def setup():
    os.makedirs(DIR, exist_ok=True)
    for f in (BACKEND_FILE, FRONTEND_FILE):
        if os.path.exists(f):
            os.remove(f)


def teardown():
    for f in (BACKEND_FILE, FRONTEND_FILE):
        if os.path.exists(f):
            os.remove(f)
    if os.path.isdir(DIR):
        os.rmdir(DIR)


def append_step(path, n):
    """Mirrors 3_implement.md Step 1: create the file if this is the first
    step for that component, otherwise append a new '## Step NN' section —
    this component's own file only, never touching a sibling's path."""
    mode = "a" if os.path.exists(path) else "w"
    with open(path, mode) as f:
        f.write(f"## Step {n:02d}\n\n### SPEC\nsynthetic step {n}\n\n### PLAN\nok\n\n")


def worker_append_loop(path, n_steps):
    for n in range(1, n_steps + 1):
        time.sleep(random.uniform(0, 0.002))  # simulated interleaving with the sibling process
        append_step(path, n)
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def file_hash(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def test_concurrent_append_never_cross_writes():
    """Guarantee 1: two components' processes appending concurrently never
    produce a shared file, and each file contains only its own component's
    steps."""
    setup()
    with multiprocessing.Pool(2) as pool:
        pool.starmap(worker_append_loop, [(BACKEND_FILE, N_STEPS), (FRONTEND_FILE, N_STEPS)])

    backend_exists = os.path.exists(BACKEND_FILE)
    frontend_exists = os.path.exists(FRONTEND_FILE)
    are_different_paths = os.path.abspath(BACKEND_FILE) != os.path.abspath(FRONTEND_FILE)

    with open(BACKEND_FILE) as f:
        backend_content = f.read()
    with open(FRONTEND_FILE) as f:
        frontend_content = f.read()

    backend_step_count = backend_content.count("## Step ")
    frontend_step_count = frontend_content.count("## Step ")
    no_cross_contamination = (
        "frontend" not in backend_content.replace(".md", "")  # sanity: component name never leaks across
        and "backend" not in frontend_content.replace(".md", "")
    )

    ok = (
        backend_exists
        and frontend_exists
        and are_different_paths
        and backend_step_count == N_STEPS
        and frontend_step_count == N_STEPS
        and no_cross_contamination
    )
    print(f"[concurrent append] backend: {backend_step_count}/{N_STEPS} steps, "
          f"frontend: {frontend_step_count}/{N_STEPS} steps -> {'PASS' if ok else 'FAIL'}")
    return ok


def test_closing_one_leaves_sibling_byte_identical():
    """Guarantee 2: deleting one component's file mid-task (closing it)
    never touches the sibling's content — assert byte-identical before/after."""
    setup()
    append_step(BACKEND_FILE, 1)
    append_step(FRONTEND_FILE, 1)
    append_step(FRONTEND_FILE, 2)

    frontend_hash_before = file_hash(FRONTEND_FILE)

    # Close the backend component: delete only its file (4_close_task.md Step 9).
    os.remove(BACKEND_FILE)

    backend_gone = not os.path.exists(BACKEND_FILE)
    frontend_still_exists = os.path.exists(FRONTEND_FILE)
    frontend_hash_after = file_hash(FRONTEND_FILE)
    byte_identical = frontend_hash_before == frontend_hash_after

    ok = backend_gone and frontend_still_exists and byte_identical
    print(f"[close one component] backend deleted: {backend_gone}, "
          f"frontend untouched (byte-identical): {byte_identical} -> {'PASS' if ok else 'FAIL'}")
    teardown()
    return ok


if __name__ == "__main__":
    r1 = test_concurrent_append_never_cross_writes()
    teardown()
    r2 = test_closing_one_leaves_sibling_byte_identical()

    print("\n=== Summary ===")
    print(f"concurrent append, no cross-writes:        {r1}")
    print(f"closing one leaves sibling byte-identical:  {r2}")

    if not (r1 and r2):
        print("\nFAIL: per-component spec file isolation does not hold as specified.")
        sys.exit(1)
    print("\nPASS: per-component spec files are isolated by construction, as step-05 specified.")
    sys.exit(0)
