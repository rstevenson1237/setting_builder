#!/usr/bin/env python3
"""The draw: whether a rated Spec line fires for this location, and which item a
draw gives it, both by arithmetic rather than by choice.

A generator deciding for itself whether a 30% line fires decides yes whenever
the room feels thin, and one picking its own item from `{a | b | c}` picks the
first plausible one. Both are drift toward the average room. This derives each
answer from the location's own code, so the same code always draws the same
answer and two codes rarely draw the same one - and neither is anyone's
judgement. `tools/context.py` resolves a whole class contract this way.

Usage: python3 tools/draw.py CODE SLOT [SLOT ...] [--reroll N]

  CODE    a location code (`C.5`), which is the whole of the seed
  SLOT    one of
            NN%          a rate, resolved to drawn or not drawn
            a|b|c        a draw over those items; an item may carry its own
                         weight, `table roll 55%|key 20%|lore 20%|unique 5%`
          and any slot may carry an `@key` suffix - `40%@gate` - so one
          location resolves the same rate or draw more than once without
          getting the same answer each time.
  --reroll N  re-resolve against an Nth seeding
"""
from __future__ import annotations

import hashlib
import re
import sys

WEIGHT_RE = re.compile(r'^(.*?)\s+(\d+)%$')
RATE_SLOT_RE = re.compile(r'^(?P<pct>\d+)%(?:@(?P<key>.+))?$')


def roll(code: str, key: str) -> int:
    """A stable 64-bit integer for this location and this draw.

    blake2b rather than hash(): the built-in is salted per process, so a draw
    made in one session would not reproduce in the next.
    """
    digest = hashlib.blake2b(f"{code}\x00{key}".encode(), digest_size=8).digest()
    return int.from_bytes(digest, "big")


def seed(key: str, reroll: int) -> str:
    return key if reroll == 0 else f"{key}#{reroll}"


def fires(code: str, pct: int, key: str, reroll: int = 0) -> tuple[bool, int]:
    """Whether a rated line appears here, and the value it rolled (0-99)."""
    value = roll(code, seed(f"{pct}%@{key}", reroll)) % 100
    return value < pct, value


def items_of(text: str) -> list[tuple[str, int | None]]:
    """`a | b 20% | c` as (item, weight or None), in its own order."""
    out = []
    for raw in text.split("|"):
        item = " ".join(raw.split())
        w = WEIGHT_RE.match(item)
        out.append((w.group(1), int(w.group(2))) if w else (item, None))
    return [(i, w) for i, w in out if i]


def pick(code: str, key: str, items: list[tuple[str, int | None]],
         reroll: int = 0, exclude: set | None = None) -> str:
    """One item, drawn evenly unless every item carries a weight.

    Items already `exclude`d are drawn around, so a second draw of the same set
    in one room is a second thing rather than the first one twice.
    """
    pool = [(i, w) for i, w in items if not exclude or i.lower() not in exclude] or items
    value = roll(code, seed(f"{key}~pick", reroll))
    weights = [w for _, w in pool]
    if all(w is not None for w in weights) and sum(weights):
        value %= sum(weights)
        for item, w in pool:
            if value < w:
                return item
            value -= w
    return pool[value % len(pool)][0]


def ladder(code: str, key: str, rungs: list[tuple[str, int | None]], reroll: int = 0) -> str:
    """The first rung that hits, and nothing below it - a rung without a rate is
    the floor it lands on when none above hits."""
    for i, (item, pct) in enumerate(rungs):
        if pct is None:
            return item
        if fires(code, pct, f"{key}.{i}", reroll)[0]:
            return item
    return rungs[-1][0]


def format_slot(code: str, slot: str, reroll: int = 0) -> str:
    rate = RATE_SLOT_RE.match(slot)
    if rate:
        hit, value = fires(code, int(rate.group("pct")), rate.group("key") or "", reroll)
        return f"{slot:28s} {'drawn' if hit else 'not drawn':>9s}  (rolled {value})"
    body, _, key = slot.partition("@")
    items = items_of(body)
    if len(items) < 2:
        raise ValueError(f"{slot}: not a rate, and not a draw of two or more items")
    return f"{slot:28s} -> {pick(code, key or body, items, reroll)}"


def main(argv: list[str]) -> int:
    reroll, args = 0, []
    i = 0
    while i < len(argv):
        if argv[i] == "--reroll" and i + 1 < len(argv) and argv[i + 1].isdigit():
            reroll = int(argv[i + 1])
            i += 2
            continue
        args.append(argv[i])
        i += 1
    if len(args) < 2:
        print(__doc__)
        return 1
    try:
        for slot in args[1:]:
            print(f"{args[0]}  {format_slot(args[0], slot, reroll)}")
    except ValueError as e:
        print(f"draw.py: {e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
