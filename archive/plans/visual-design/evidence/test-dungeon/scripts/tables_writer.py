"""Writes a region's tables (Locations, Dressing, Blocks, Connections) from its accepted Design.md, for a test level."""
import sys, re
sys.path.insert(0, '/tmp/claude-0/-home-user-setting-builder/194b492d-8ef5-5235-91e9-0447072bdc6d/scratchpad/repoX/tools')
import maps, tables, space, design, kdl

def write(code, names, ways, stairs=(), height=16):
    """names: {code: name}; ways: {(a,b): dict(type=, secret=bool, locked=bool, width=ft)}; stairs: [(code, to, climb)]."""
    maps.world_for.cache_clear(); maps.built.cache_clear()
    world = maps.world_for(tables.SETTING); r = world.regions[code]
    g = design.groups(r)
    bid = next(iter(g)); gd = g[bid]; node = gd['design']
    members = design.words(node.props['locations'])
    kinds = {}
    for n in gd['lines']:
        if n.name in ('Bind', 'Fill'): kinds.update(design.kinds_of(n))
    d = r.dir
    loc = [f'# Locations of {code}', '', '```kdl']
    for c in members:
        loc.append(f'Location {c} name="{names.get(c, "Room " + c.split(".")[1])}" tags="old, dim, quiet" type="{kinds[c]}"')
    loc.append('```')
    (d / 'Locations.md').write_text("\n".join(loc) + "\n")
    dr = [f'# Dressing of {code}', '', '```kdl']
    for c in members:
        p = gd['places'][c]; o = space.outline_value(p.props['outline']); x, y = space.point_of(p.props['xyz'])[:2]
        w, l = design.box(o)
        line = f'Dressing {c} obvious="A room" width={int(w)} length={int(l)} xyz="{int(x)},{int(y)}" height={height}'
        sh = str(p.props.get('shape', 'rect'))
        if sh != 'rect': line += f' shape="{sh}"'
        if o[0] == 'poly':
            line += ' outline="poly ' + " ".join(f"{px:g},{py:g}" for px, py in o[1]) + '"'
        dr.append(line)
    dr.append('```')
    (d / 'Dressing.md').write_text("\n".join(dr) + "\n")
    outline = node.props.get('outline') or node.props.get('hull')
    (d / 'Blocks.md').write_text(f'# Blocks of {code}\n\n```kdl\nBlock {bid} name="{names.get(bid, bid)}" locations="{", ".join(members)}" outline="{outline}"\n```\n')
    cn = [f'# Connections of {code}', '', '```kdl']
    def conn(a, b, spec):
        t = spec.get('type', 'Open'); extra = ''
        if spec.get('secret'): extra += ' Secret trigger="a hidden catch" tell="a seam in the wall" knows="nobody"'
        if spec.get('locked'): extra += ' Lock key="The Brass Key"'
        wid = f' width={spec["width"]}' if 'width' in spec else ''
        body = f' {{{extra} }}' if extra else ''
        return f'Connection {a} to="{b}" type="{t}"{wid}{body}'
    seen = set()
    for n in gd['links']:
        a, b = str(n.args[0]), str(n.props['to'])
        if frozenset((a, b)) in seen: continue
        seen.add(frozenset((a, b)))
        spec = ways.get((a, b)) or ways.get((b, a)) or {}
        cn.append(conn(a, b, spec)); cn.append(conn(b, a, spec))
    for c, to, climb in stairs:
        cn.append(f'Connection {c} to="{to}" type="Open" climb={climb}')
    cn.append('```')
    (d / 'Connections.md').write_text("\n".join(cn) + "\n")
    maps.world_for.cache_clear()
    return members
