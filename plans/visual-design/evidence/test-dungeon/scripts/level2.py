from features import *
src = f'{R}/setting/region/Y/Y.a.json'
m = json.load(open(src)); F = facts(src)
rooms = room_boxes(m)
m['title'] = 'Level 2 - The Three Roads'; m['legend'] = True; m['compass'] = True; m['scaleBar'] = True
m['furniture'] = {'place': 'outside'}
# every door kind: the passages' ends in turn, double doors on the great hall's ways, and kinds on the core's shared walls
kinds = ['door', 'arch', 'double', 'locked', 'secret', 'portcullis', None]
hall_ways = {c['index'] for c in F['corridors'] if 'Y-3' in (c['from'].get('room'), c['to'].get('room'))}
n = 0
for c in F['corridors']:
    i = c['index']; ds = m['corridors'][i]['doors']
    for k in (0, 1):
        if ds[k] is None and i % 3: continue
        ds[k] = 'double' if i in hall_ways else kinds[n % len(kinds)]; n += 1
for j, con in enumerate(m['connections']):
    con['kind'] = ['door', 'double', 'portcullis', 'arch', 'locked', 'open', 'secret'][j % 7]
    con['weight'] = 0.8 if j % 2 else 1.4
if m['connections']:                       # an illusory wall: open floor behind a dashed line
    m['connections'][-1].update(kind='open', line='dashed', width=2)
for r in m['rooms']:
    if r['label'] in ('Y.18', 'Y.19', 'Y.20'): r['partition'] = 0.6
# the wide hall: a fountain, statues round it, two rows of pillars, wavy drapery along its north wall
r3 = rooms['Y.3']; cx, cy = centre(r3)
sym(m, 'fountain', cx, cy, scale=2)
for i in range(6):
    sym(m, 'statue', r3['x'] + 2 + i * (r3['w'] - 4) / 5, r3['y'] + 1.5)
    sym(m, 'statue', r3['x'] + 2 + i * (r3['w'] - 4) / 5, r3['y'] + r3['h'] - 1.5)
for i in range(1, 4):
    sym(m, 'pillar', cx - 5 + 0, cy - 3 + (i - 2) * 2.5) if False else None
for dx in (-6, -3, 3, 6): sym(m, 'pillar', cx + dx, cy - 3); sym(m, 'pillar', cx + dx, cy + 3)
r3['edge'] = 'wavy'; r3['edgeSides'] = ['n']
# the trapped lane: traps down its length, a pit and a skull at its far end
r2 = rooms['Y.2']; lx, ly = centre(r2)
for i in range(9): sym(m, 'trap', lx + (-0.7 if i % 2 else 0.7), r2['y'] + 1.5 + i * (r2['h'] - 3) / 8)
sym(m, 'pit', lx, r2['y'] + r2['h'] - 1); sym(m, 'skull', lx, r2['y'] + 0.8)
# furnishings round the level: one of each, so the symbol set is drawn
def at(code, kind, dx=0, dy=0, **kw): sym(m, kind, *(c + d for c, d in zip(centre(rooms[code]), (dx, dy))), **kw)
at('Y.10', 'altar'); at('Y.7', 'pool'); at('Y.5', 'web'); at('Y.27', 'bones'); at('Y.25', 'chest'); at('Y.22', 'coffin')
at('Y.20', 'barrel', -0.8); at('Y.20', 'crate', 0.8); at('Y.19', 'bed', -1); at('Y.19', 'table', 1); at('Y.18', 'throne')
at('Y.9', 'curtain'); at('Y.8', 'fire'); at('Y.4', 'rubble'); at('Y.6', 'ladder'); at('Y.21', 'dais'); at('Y.26', 'pit-filled'); at('Y.24', 'pool-filled')
at('Y.16', 'spiral-stair'); at('Y.15', 'arch-stair'); at('Y.14', 'curved-arrow', sweep=120, angle=200)
# rings: an illusory circle round the gate room and a poly ring over bare rock
gx, gy = centre(rooms['Y.10'])
m['rings'] = [{'id': 'r1', 'shape': 'circle', 'at': [round(gx, 1), round(gy, 1)], 'r': 6, 'line': 'dashed'}]
# labels
label(m, 'THE GREAT HALL', cx, r3['y'] - 1.2); label(m, 'THE TRAPPED LANE', lx + 3, ly, angle=90)
label(m, 'THE CORE', *centre(rooms['Y.17']), kind='note')
finish('level2', m)
