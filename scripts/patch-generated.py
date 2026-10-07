#!/usr/bin/env python3
"""Patch the residual REX_FATAL stubs in the generated recomp code.

Run AFTER `rexglue codegen` and BEFORE building:

    python3 scripts/patch-generated.py [generated-dir]

Why this exists: after the config hint rounds (see re_cherry_config.toml),
8 REX_FATAL stubs remained. Inspection of the generated code (2026-10-07)
showed every one is a case where the codegen analyzer failed to wire a
target it had in fact emitted:

* Two are conditional branches whose target label EXISTS in the same
  generated function (a self-loop to the function's own entry in
  sub_82848550 - this is the crash hit when starting attacks in game -
  and a forward branch to loc_82BE7C7C in three TUs holding copies of a
  shared body). The correct emission is a plain goto.
* Four are unconditional tail branches (`b`, annotated "no CallTarget in
  FunctionNode") to functions that ARE defined (they came from the
  round-1 hints). The generated line is already followed by `return;`,
  i.e. codegen produced the standard tail-call idiom minus the call
  itself; inserting the direct call restores it exactly.

Each replacement is an exact-string match with an asserted count, so a
codegen change that alters any site fails loudly instead of patching
the wrong thing.
"""

import pathlib
import sys

# (fatal string, replacement, expected count across all generated .cpp)
PATCHES = [
    # Self-loop inside sub_82848550: branch back to the function's own
    # entry label (loop over the items it walks). Crash site from real
    # gameplay: FATAL fired when the player started attacking.
    ('REX_FATAL("Unresolved branch from 0x82848B28 to 0x82848550")',
     "goto loc_82848550", 1),
    # Forward conditional branch; label exists in the same function in
    # each of the three TUs that hold a copy of this shared body.
    ('REX_FATAL("Unresolved branch from 0x82BE7C58 to 0x82BE7C7C")',
     "goto loc_82BE7C7C", 3),
    # Tail branches to hint-defined functions (call + existing return).
    ('REX_FATAL("Unresolved call from 0x82BE7C1C to 0x82BE7B04");',
     "sub_82BE7B04(ctx, base);", 1),
    ('REX_FATAL("Unresolved call from 0x82BD3F58 to 0x82BD3EA0");',
     "sub_82BD3EA0(ctx, base);", 1),
    ('REX_FATAL("Unresolved call from 0x82BE7BDC to 0x82BE7B20");',
     "sub_82BE7B20(ctx, base);", 1),
    ('REX_FATAL("Unresolved call from 0x82BE48D8 to 0x82BE484C");',
     "sub_82BE484C(ctx, base);", 1),
]


def main() -> int:
    gen = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "generated/default")
    files = sorted(gen.glob("*.cpp"))
    if not files:
        print(f"no generated .cpp files under {gen}", file=sys.stderr)
        return 1

    totals = {old: 0 for old, _, _ in PATCHES}
    for path in files:
        text = path.read_text()
        new = text
        for old, repl, _ in PATCHES:
            n = new.count(old)
            if n:
                totals[old] += n
                new = new.replace(old, repl)
        if new != text:
            path.write_text(new)
            print(f"patched {path.name}")

    bad = False
    for old, _, expected in PATCHES:
        got = totals[old]
        status = "ok" if got == expected else "MISMATCH"
        if got != expected:
            bad = True
        print(f"{status}: {got}/{expected} x {old[:70]}")
    if bad:
        return 1

    remaining = sum(p.read_text().count('REX_FATAL("Unresolved')
                    for p in files)
    print(f"remaining unresolved REX_FATAL stubs: {remaining}")
    return 0 if remaining == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
