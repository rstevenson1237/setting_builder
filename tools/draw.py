#!/usr/bin/env python3
"""The draw: which entry a genre list gives this location, and whether a rated
Spec line fires here, both by arithmetic rather than by choice.

A generator that picks its own entry from a list picks the first plausible one,
and a generator that decides for itself whether a 30% line fires decides yes
whenever the room feels thin. Both are drift toward the average room. This
derives each answer from the location's own code, so the same code under the
same pack always draws the same entry and two different codes rarely draw the
same one - and neither is anyone's judgement.

What it draws from is the pack `tools/validate_setting.py` selects, per STEPS.md
step 1b; what it is drawn for is `tools/context.py`, which resolves a whole class
contract this way and prints the result.

Usage: python3 tools/draw.py CODE SLOT [SLOT ...] [--reroll N]

  CODE    a location code (`D.5`), which is the whole of the seed
  SLOT    one of
            name          a genre list in the selected pack
            name:facet    a faceted list, filtered to the entries carrying that
                          facet, and numbered as the list itself numbers them
            NN%           a rated Spec line, resolved to yes or no
          and any slot may carry an `@key` suffix - `doors@D.2`, `40%@gate` -
          which is how one location draws the same list, or resolves the same
          rate, more than once without drawing the same entry twice.
  --reroll N  move a list draw on by N entries, and re-resolve a rate against
              an Nth seeding. A reroll on a list is a step rather than a
              reseed, so `--reroll 1` always moves; a reroll on a rate has
              nowhere to step to, so it reseeds.

Exits 1 if a slot names no list in the pack, or a facet no entry carries.
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from validate_setting import rel, selected_pack  # noqa: E402

ENTRY_RE = re.compile(r'^\s*(\d+)\.\s+(.*\S)\s*$')
FACET_RE = re.compile(r'^([a-z][a-z0-9 -]*?)\s+-\s+(.*)$')
SLOT_RE = re.compile(r'^(?P<name>[^:@%]+)(?::(?P<facet>[^@]+))?(?:@(?P<key>.+))?$')
RATE_SLOT_RE = re.compile(r'^(?P<pct>\d+)%(?:@(?P<key>.+))?$')


class DrawError(Exception):
    pass


def roll(code: str, key: str) -> int:
    """A stable 64-bit integer for this location and this draw.

    blake2b rather than hash(): the built-in is salted per process, so a draw
    made in one session would not reproduce in the next, and reproducibility is
    the whole point.
    """
    digest = hashlib.blake2b(f"{code}\x00{key}".encode(), digest_size=8).digest()
    return int.from_bytes(digest, "big")


def list_entries(path: Path) -> list[str]:
    """A list's entries, in its own order. Index 0 is its entry 1."""
    return [m.group(2) for m in
            (ENTRY_RE.match(line) for line in path.read_text().splitlines()) if m]


def facet_of(entry: str) -> tuple[str | None, str]:
    """A faceted entry's facet and its text, per patterns/SPEC.md's list format."""
    m = FACET_RE.match(entry)
    return (m.group(1), m.group(2)) if m else (None, entry)


def list_path(name: str, pack: Path | None = None) -> Path:
    pack = pack or selected_pack()
    if pack is None:
        raise DrawError("genre/ holds no pack with a lists/ directory, or holds several "
                        "and GENRE.md names none - see STEPS.md step 1b")
    path = pack / "lists" / f"{name}.md"
    if not path.exists():
        raise DrawError(f"{name}: no such list in {rel(pack)}")
    return path


def draw(code: str, name: str, facet: str | None = None, key: str | None = None,
         reroll: int = 0, pack: Path | None = None) -> tuple[int, int, str]:
    """(entry number, list length, entry text) for this location's draw.

    The entry number is the list's own numbering even under a facet, so a draw
    can be read straight against the list file.
    """
    entries = list_entries(list_path(name, pack))
    if not entries:
        raise DrawError(f"{name}: holds no numbered entries")
    pool = [(i, text) for i, text in enumerate(entries, 1)]
    if facet:
        pool = [(i, body) for i, (f, body) in
                ((i, facet_of(text)) for i, text in pool) if f == facet]
        if not pool:
            raise DrawError(f"{name}: no entry carries the facet {facet!r}")
    seed = f"{name}:{facet}" if facet else name
    if key:
        seed = f"{seed}@{key}"
    index = (roll(code, seed) + reroll) % len(pool)
    number, text = pool[index]
    return number, len(entries), text


def fires(code: str, pct: int, key: str, reroll: int = 0) -> tuple[bool, int]:
    """Whether a rated Spec line appears in this location, and the value it rolled.

    A reroll reseeds rather than steps: a rate has no neighbouring entry to move
    on to, and stepping a percentile by one would leave all but one reroll in a
    hundred resolving the same way.
    """
    seed = f"{pct}%@{key}" if reroll == 0 else f"{pct}%@{key}#{reroll}"
    value = roll(code, seed) % 100
    return value < pct, value


def format_draw(code: str, slot: str, reroll: int = 0, pack: Path | None = None) -> str:
    rate = RATE_SLOT_RE.match(slot)
    if rate:
        key = rate.group("key") or ""
        hit, value = fires(code, int(rate.group("pct")), key, reroll)
        return f"{slot:28s} {'drawn' if hit else 'not drawn':>9s}  (rolled {value})"
    m = SLOT_RE.match(slot)
    if not m or not m.group("name").strip():
        raise DrawError(f"{slot}: not a list name, a name:facet, or a rate")
    number, total, text = draw(code, m.group("name").strip(),
                               (m.group("facet") or "").strip() or None,
                               m.group("key"), reroll, pack)
    return f"{slot:28s} {f'{number}/{total}':>9s}  {text}"


def main(argv: list[str]) -> int:
    reroll = 0
    args: list[str] = []
    i = 0
    while i < len(argv):
        if argv[i] == "--reroll":
            if i + 1 >= len(argv) or not argv[i + 1].lstrip("-").isdigit():
                print("--reroll takes a number")
                return 1
            reroll = int(argv[i + 1])
            i += 2
            continue
        args.append(argv[i])
        i += 1
    if len(args) < 2:
        print(__doc__)
        return 1
    code, slots = args[0], args[1:]
    try:
        for slot in slots:
            print(f"{code}  {format_draw(code, slot, reroll)}")
    except DrawError as e:
        print(f"draw.py: {e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
