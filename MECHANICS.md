# Mechanics

The ruleset is the mold. This file is the negative of it, and it is the only
file in this repository that maps a mechanical token to a system. Swap this
file and the whole setting retargets.

**Prose never states a mechanical value.** A feature reads as fiction and
carries its mechanic beside it as a bracketed token. `{TEST: Sanity}` survives
a system change. "Roll your Magic die" does not.

**Tokens are referee-facing.** A token never appears in player-facing text.

## Token vocabulary

`validate.py` reads the Token, Form and Values columns of this table (M21).

| Token | Form | Values | Carried by |
| :--- | :--- | :--- | :--- |
| `TEST` | enum | Constitution, Sanity, Fate | Traps, hazards, forced dangers |
| `WOUND` | enum | Piercing, Crushing, Poison, Fire, Frost, Blast | Anything that can cause a Wound |
| `CONDITION` | parts:3 | name / effect / duration | Any Test of Fate |
| `AD` | ad | count, then a modifier from -2 to +6 | Every creature and NPC |
| `TYPE` | enum | Men, Humanoid, Beast, Fantasy, Undead, Construct, Horror, Wyrm, Fey, Fiend, Giant | Every creature |
| `VALUE` | value | a count of `cn`, silver standard | Every treasure entry |
| `WT` | int | slots, where 100 coins is one slot | Every treasure entry |
| `QUALITY` | enum | Cursed, Poor, Fine, Masterwork, Artifact | Treasure and equipment |
| `OUTCOME` | enum | Success, Complication, Failure | Every `T-PRC` entry, all three lines |

**Forms.** `enum` takes one listed value. `parts:3` takes three free-form parts
separated by `/`, all three required. `ad` takes `n, mod`. `value` takes `n cn`.
`int` takes a bare integer.

## Written forms

```
{TEST: Sanity}
{WOUND: Frost}
{CONDITION: Bell-struck / cannot speak above a whisper / until a full rest}
{AD: 2, +1}
{TYPE: Undead}
{VALUE: 400 cn}
{WT: 1}
{QUALITY: Fine}
{OUTCOME: Complication}
```

## Bare values

A bare value is a mechanic written as a number instead of as a token. These
patterns are system vocabulary, and `validate.py` reports any of them found in
prose (M24). Retargeting the setting means rewriting this list.

| Pattern | Catches |
| :--- | :--- |
| `\b\d*d\d+\b` | `d20`, `2d6`, `1d8` |
| `\bDC\s*\d+` | `DC 15` |
| `\bAC\s*\d+` | `AC 14` |
| `\b\d+\s*(?:hp\|HP)\b` | `12 hp` |
| `\b(?:hp\|HP)\s*\d+` | `HP 12` |
| `\bTHAC0\b` | `THAC0` |
| `\bsav(?:e\|ing throw)\s+(?:vs\.?\|against)\b` | `save vs. poison` |
| `[+-]\d+\s+to\s+(?:hit\|damage\|save)\b` | `+2 to hit` |
| `\broll\s+(?:a\|your\|an)\b` | `roll a d6`, `roll your Magic die` |
| `\b\d+\s*(?:points?\s+of\s+)?damage\b` | `6 damage`, `6 points of damage` |
