from features import *
src = f'{R}/setting/region/X/X.a.json'
m = json.load(open(src)); F = facts(src)
rooms = room_boxes(m)
# classic look: black and white, hatched rock, plain walls
m['style'] = {'hatch': 'full', 'wall': 2.5}
m['title'] = 'Level 1 - The Looping Vaults'; m['legend'] = True; m['compass'] = True; m['scaleBar'] = True
m['furniture'] = {'place': 'outside'}
# the hub: four pillars; the entry: statues; the gallery: an altar; dead ends: chests; the stair room: a brazier
cx, cy = centre(rooms['X.1'])
for dx, dy in ((-2, -2), (2, -2), (-2, 2), (2, 2)): sym(m, 'pillar', cx + dx, cy + dy)
for c in ('X.17', 'X.16', 'X.20', 'X.21', 'X.22'): sym(m, 'chest', *centre(rooms[c]))
x, y = centre(rooms['X.14']); sym(m, 'altar', x, y)
x, y = centre(rooms['X.13']); sym(m, 'statue', x - 1.5, y); sym(m, 'statue', x + 1.5, y)
x, y = centre(rooms['X.12']); sym(m, 'fire', x, y + 0.5)
# traps and rubble along the passages: every third passage at its middle, longer ones at a third and two thirds
longp = []
for c in F['corridors']:
    if c['index'] % 3 == 0: sym(m, 'trap', *along(c['path'], 0.5)[:2])
    if c['index'] % 7 == 2: sym(m, 'rubble', *along(c['path'], 0.4)[:2])
    if c['length']['map'] > 7: longp.append(c['index'])
# doors standing in the run itself: a portcullis in the middle of the two longest passages
for i in sorted(longp, key=lambda i: -F['corridors'][i]['length']['map'])[:2]:
    m['corridors'][i].setdefault('midDoors', []).append({'at': round(F['corridors'][i]['length']['map'] / 2, 1), 'kind': 'portcullis'})
# area labels over each loop
ax, ay = centre(rooms['X.3']); bx, by = centre(rooms['X.9'])
label(m, 'THE LEFT LOOP', ax - 1, ay + 5); label(m, 'THE RIGHT LOOP', bx, by + 6)
label(m, 'secret ways marked S', *centre(rooms['X.4']), kind='note') if False else None
finish('level1', m)
