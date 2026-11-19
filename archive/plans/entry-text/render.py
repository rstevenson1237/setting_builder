"""Experiment for review item 1: region K's write-ups rendered from its tables plus one capped sentence an entry.
The sentences below were written from K's tables alone, before K's existing write-ups were read.
A citation is `{}` in a sentence: the renderer fills it from the entry. usage: render.py OUTDIR"""
import re, sys
from pathlib import Path
sys.path.insert(0, "tools")
import dungeon, maps, tables

CAP = {"seen": 40, "note": 45, "text": 28}
# location -> seen, note, then (entry, name, text): entry is Kind#n at that location, a way's child as Way:TO
K = {
 "K.1": ("A short landing at the stair's foot, the air thick and dim. A **wraith** in a king's robe stands where it opens west, and no footfall sounds.",
         "A landing 10 feet by 20 and 10 high. The wraith is the level's door: it lets pass whoever draws no steel.",
         [("Dressing", "The Black Hand", "Painted in ash on the wall beside the west opening, palm out."),
          ("Way:K.2", "The Wraith", "Stands in the west opening in a king's robe {}; it wants no steel drawn, and falls on the first bared blade.")]),
 "K.2": ("A long cold hall, smoke hanging in thick air that carries a faint wailing. A **black altar** is cut into one wall under a painted **black hand**, and shapes crouch beyond the light.",
         "A hall 60 feet by 40 and 10 high. Flames burn low here and lower toward the south arch (K.3). (The Demon Is Invited)",
         [("Dressing", "The Black Altar", "Cut from the wall's own basalt, its top stained and dry, a black hand painted above it."),
          ("Encounter#1", "The Ghouls", "Crouch at the hall's far end, wailing low {}; they rush a light."),
          ("Sign:K.3", "The South Arch", "Flames lean toward it and gutter; the air beyond is harder to draw.")]),
 "K.3": ("A low wide hall, bone dust over the floor and the air too thick to fill a chest; a heartbeat sounds loud in it. An **iron gate** stands in the east wall, and stone **figures** line the others.",
         "A hall 50 feet square and 10 high, the antechamber. Each hour lingered here costs a Test of Sanity, 1d. The cult breathe shallow through their masks. (The Demon Is Invited)",
         [("Hazard#1", "The Air", "Flames gutter in it. Whoever breathes deep - to shout, run or fight - takes in the demon's breath {}."),
          ("Encounter#1", "The Figures", "Gargoyles stand against the walls among carved ones {}; they move when a hand touches the gate."),
          ("Reward#1", "The Gate Niche", "A niche in the gate's frame holds what the cult leaves for the hall beyond {}."),
          ("Dressing", "The Gate", "Iron, a black hand on each leaf, and a black altar cut into its sill."),
          ("Sign:K.8", "The Bone Dust", "Lies deepest at the arch to the kneeling hall, scuffed by knees.")]),
 "K.4": ("Bronze **masks** hang dusty on hooks along all four walls, eyeless and mouthless. Four **robed figures** stand among them drawing their own masks tight.",
         "A store 40 feet square and 10 high. The cultists reach an alarm anywhere on the level in 1 turn.",
         [("Encounter#1", "The Cultists", "Four in black cloth tighten their mask straps {}; one whose mask is torn screams, and the level hears."),
          ("Reward#1", "The Hollow Mask", "One mask hangs heavier than the rest, a folded writing pushed into its hollow {}."),
          ("Dressing", "The Black Hand", "Painted on the lintel of each door."),
          ("Way:K.7", "The Wooden Door", "Sweet smoke seeps under it; opened, the censers' smoke rolls out over whoever stands there {}."),
          ("Sign:K.3", "The Padded Masks", "Each is packed thick over nose and mouth, the newest thickest.")]),
 "K.5": ("A square room, warm, with a deep hum in the stone. A carved **iron door** fills the east wall, and a tall **mirror** glows dimly beside it.",
         "A room 30 feet square and 10 high, the last before the demon's hall; the stair beyond the door runs 30 feet down to L.1. The air thickens here by the hour. (The Demon Is Invited)",
         [("Dressing", "The Iron Door", "Carved with the demon's face, unscraped, a black hand at its centre; warm to the hand, it opens on the stair down."),
          ("Mystery#1", "The Mirror", "Whoever looks into its glow sees the demon's hall, and what is fed there {}."),
          ("Reward#1", "Behind the Mirror", "The mirror swings on a pin; a recess behind it holds the threshold's offerings {}.")]),
 "K.6": ("A round room whose **ribbed walls** swell and sink like a chest, slowly. Air whistles through **vents** overhead with each swell.",
         "A round room 30 feet across and 10 high, once the level's bellows. A held breath outlasts the swell; the cult know it.",
         [("Hazard#1", "The Ribs", "As they swell the air goes thin, and whoever is breathing it chokes {}."),
          ("Dressing", "The Vents", "Slots in the ceiling, too narrow for a hand."),
          ("Sign:K.8", "The Bone Dust", "Drifted against the arch to the kneeling hall, pressed in two rows by knees.")]),
 "K.7": ("A small room thick with sweet smoke. **Censers** hiss in a row along a stone ledge, and a bench faces them.",
         "A room 30 feet square and 10 high, where the cult keeps its censers lit.",
         [("Dressing", "The Censers", "Bronze bowls on chains, smoking; with all of them put out the room clears in a turn."),
          ("Reward#1", "The Cold Censer", "One bowl is unlit, and something is packed under its ash {}.")]),
 "K.8": ("A long silent hall. **Skeletons** kneel in rows across it, every skull bowed south toward a carved **door** with offerings heaped at its foot.",
         "A hall 40 feet square and 10 high. The dead answer an alarm on the level in 1 turn. (The Demon Is Invited)",
         [("Encounter#1", "The Kneeling Dead", "Rows of them, bone settling as a party passes {}; they rise only behind a turned back."),
          ("Reward#1", "The Offerings", "Bowls, rings and cut stones heaped at the carved door's foot {}."),
          ("Dressing", "The Carved Door", "Cut in relief in the south wall under a black altar, with no hinge or handle: stone behind it.")]),
}
MAKE = {"Open": "an open passage", "Archway": "an archway", "Iron": "an iron door", "Stone": "a stone door", "Wooden": "a wooden door"}
TESTS = {"Nuisance": 1, "Damaging": 2, "Lethal": 3}

world = maps.world_for(tables.SETTING)
region = world.regions["K"]
names = {c: str(n.props["name"]) for r in world.regions.values() for c, n in r.locations().items()}
fields = {m.group(1): m.group(2).split(",")[0].strip() for m in re.finditer(r"^### (.+)\n(?:.*\n)*?Fields: (.+)$", (tables.SETTING / "Factions.md").read_text(), re.M)}
walks = dungeon.walks("K")


def cite(n) -> str:
    if n.name == "Encounter":
        who = n.children[0]
        if who.name == "Creature":
            return f"({n.props['reaction']}, {who.props['count']}, Bestiary : {who.props['bestiary']})"
        if who.name == "Faction":
            return f"({n.props['reaction']}, {who.props['present']}, Bestiary : {fields[str(who.props['faction'])]})"
    if n.name in ("Hazard", "Mystery"):
        d, t = TESTS[str(n.props["damage"])], str(n.props["test"])
        return {"Constitution": f"(Test of Constitution, {d}d, {n.props.get('wound')})", "Sanity": f"(Test of Sanity, {d}d)",
                "Fate": f"(Test of Fate, {n.props.get('condition')})"}[t]
    if n.name == "Reward":
        c = str(n.props["contents"])
        return f"({c}, d20)" if c.startswith("Treasure") else f"({c})"
    return ""


def entry(code: str, ref: str):
    if ref.startswith("Way:"):
        way = next(n for n in region.files["Connections"] if str(n.args[0]) == code and str(n.props["to"]) == ref[4:])
        return way.children[0]
    if "#" in ref:
        kind, k = ref.split("#")
        pool = region.files["Rewards" if kind == "Reward" else "Challenges"]
        return [n for n in pool if n.name == kind and str(n.args[0]) == code][int(k) - 1]
    return None


out = Path(sys.argv[1])
loc = region.locations()
over = []
for code, (seen, note, feats) in K.items():
    n = loc[code]
    for what, text in (("seen", seen), ("note", note)):
        if len(text.split()) > CAP[what]:
            over.append(f"{code} {what}: {len(text.split())} words")
    lines = [f"{code} **{n.props['name']}** ({n.props['type']}) - *{n.props['tags']}*", "", seen, "", f"*{note}*", ""]
    for ref, name, text in feats:
        if len(text.replace("{}", "").split()) > CAP["text"]:
            over.append(f"{code} {name}: {len(text.split())} words")
        e = entry(code, ref)
        lines.append(f"**{name}:** " + text.replace("{}", cite(e) if e is not None else ""))
    exits = []
    for w in [x for x in region.files["Connections"] if str(x.args[0]) == code]:
        to = str(w.props["to"])
        if "climb" in w.props:
            exits.append(f"{'up' if int(w.props['climb']) > 0 else 'down'} a stair -> {to} {names[to]}")
        else:
            side = walks.get((code, to), ("",))[0]
            exits.append(f"{MAKE[str(w.props['type'])]} {side} -> {to} {names[to]}".replace("  ", " "))
    lines += ["", "**Exits:** " + ", ".join(sorted(exits, key=lambda e: "stair" in e))]
    (out / f"{code.split('.')[1]}.md").write_text("\n".join(lines) + "\n")
print("over cap:", over or "none")
