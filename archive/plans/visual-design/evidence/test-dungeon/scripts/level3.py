from features import *
src = f'{R}/setting/region/Z/Z.a.json'
m = json.load(open(src)); F = facts(src)
rooms = room_boxes(m)
m['title'] = 'Level 3 - The Spiral Deep'; m['legend'] = True; m['compass'] = False; m['scaleBar'] = True
m['furniture'] = {'place': 'outside'}
# a dark look: the preset fills what the file leaves, with walls set apart from the rock
m['style'] = {'preset': 'dark', 'palette': {'wall': '#d9c9a3', 'floor': '#5a4b3a', 'ink': '#e9dcc0', 'grid': '#7d6a50', 'rock': '#1d1a1a'}}
# natural passages, curved through their bends, in place of built ones
for i, c in enumerate(m['corridors']):
    c['style'] = 'natural'; c['seed'] = 7 + i; c['route'] = 'around'; c['curve'] = 'smooth'
    c['doors'] = [None, None]
# organic rooms: a wavy rubble margin on every second cave
for i, r in enumerate(m['rooms']):
    if i % 2 == 0: r['edge'] = 'wavy'
# the way inward: curved arrows along the spiral, then the final chamber's dressing
pts = [centre(rooms[f'Z.{i}']) for i in range(1, 15)]
for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]):
    sym(m, 'curved-arrow', (x0 + x1) / 2, (y0 + y1) / 2, sweep=60, angle=round(math.degrees(math.atan2(y1 - y0, x1 - x0))), scale=0.7)
fx, fy = centre(rooms['Z.14'])
sym(m, 'altar', fx, fy); sym(m, 'throne', fx, fy - 3)
for dx, dy in ((-3, -3), (3, -3), (-3, 3), (3, 3)): sym(m, 'fire', fx + dx, fy + dy, scale=0.8)
sym(m, 'skull', fx + 5, fy); sym(m, 'bones', fx - 5, fy + 2); sym(m, 'coffin', fx, fy + 4)
for code, kind in (('Z.2', 'bones'), ('Z.3', 'web'), ('Z.4', 'rubble'), ('Z.5', 'pit-filled'), ('Z.6', 'pool-filled'), ('Z.7', 'skull'),
                   ('Z.8', 'web'), ('Z.9', 'bones'), ('Z.10', 'rubble'), ('Z.11', 'pit'), ('Z.12', 'spiral-stair'), ('Z.13', 'pool')):
    sym(m, kind, *centre(rooms[code]))
# a ring of dashes round the final chamber, and a void of rock the passages must not take
m['rings'] = [{'id': 'seal', 'shape': 'circle', 'at': [round(fx, 1), round(fy, 1)], 'r': 7, 'line': 'dashed', 'width': 0.2}]
label(m, 'THE SPIRAL', *centre(rooms['Z.9']), kind='area', angle=0) if False else None
label(m, 'THE FINAL CHAMBER', fx, fy - 5.5, kind='name')
finish('level3', m)
