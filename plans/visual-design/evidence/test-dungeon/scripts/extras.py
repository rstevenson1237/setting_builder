from features import *
base = json.load(open(f'{OUT}/level2.json'))
rooms = {r['label']: r for r in base['rooms']}
def trial(name, fn):
    m = copy.deepcopy(base)
    try:
        fn(m)
    except Exception as e:
        print(f'{name:34s} could not be set up: {e}'); return
    f = f'{OUT}/extra-{name}.json'
    json.dump(m, open(f, 'w'))
    chk = json.loads(art('dungeon', 'check', '--file', f, '--json').stdout or '{}')
    new = collections.Counter(x.get('id', 'schema') for x in chk.get('errors', []) + chk.get('warnings', []))
    r = art('dungeon', 'render', '--file', f, '--format', 'svg', '--fit', '900x900px', '--out', OUT + '/extras')
    print(f'{name:34s} check ok={chk.get("ok")} findings={dict(new)} render rc={r.returncode}', (r.stderr.strip()[:90] if r.returncode else ''))
os.makedirs(OUT + '/extras', exist_ok=True)
H, W = base['rows'], base['cols']
print('Level 2 file:', W, 'x', H, 'cells;', len(base['rooms']), 'rooms;', len(base['corridors']), 'corridors')
trial('walls-round-the-core', lambda m: m.__setitem__('walls', [{'id': 'w1', 'rooms': [f'Y-{i}' for i in range(17, 24)], 'thickness': 1, 'inset': 1,
        'towers': {'shape': 'round', 'size': 3}, 'gates': [{'at': list(centre(rooms['Y.17'])), 'kind': 'gate', 'room': 'Y-17', 'width': 2}]}]))
trial('void-area-in-the-rock', lambda m: m.__setitem__('areas', [{'points': [2, H - 12, 12, H - 12, 12, H - 3, 2, H - 3], 'kind': 'void', 'label': 'a collapsed shaft'}]))
trial('rock-area', lambda m: m.__setitem__('areas', [{'points': [W - 14, H - 14, W - 4, H - 14, W - 4, H - 4, W - 14, H - 4], 'kind': 'rock', 'label': 'solid'}]))
trial('explicit-bounds', lambda m: m.__setitem__('bounds', [1, 1, W - 1, 1, W - 1, H - 1, 1, H - 1]))
trial('block-split-rooms', lambda m: m.__setitem__('blocks', [{'id': 'b1', 'shape': 'rect', 'x': 2, 'y': H - 14, 'w': 14, 'h': 10, 'split': {'mode': 'grid', 'min': 4, 'seed': 3}, 'doors': 0.5}]))
trial('exit-arrow-with-angle', lambda m: rooms['Y.27'].setdefault('exits', []).append({'kind': 'arrow', 'side': 's', 'angle': 100, 'text': 'a way on'}) or None)
trial('corridor-exit-fade', lambda m: m['corridors'].append({'from': {'room': 'Y-25', 'side': 'e'}, 'to': {'at': [centre(rooms['Y.25'])[0] + 9, centre(rooms['Y.25'])[1]], 'exit': {'text': 'a passage that leads on', 'fade': 4}}, 'width': 1, 'route': 'straight'}))
trial('corridor-joins-corridor', lambda m: m['corridors'].append({'id': 'j', 'from': {'corridor': m['corridors'][0].get('id') or 'c0', 'near': list(centre(rooms['Y.17']))}, 'to': {'room': 'Y-21'}, 'width': 1}) if m['corridors'][0].setdefault('id', 'c0') else None)
trial('diagonal-passage', lambda m: m['corridors'].append({'from': {'room': 'Y-4'}, 'to': {'room': 'Y-24'}, 'route': 'straight', 'width': 1, 'doors': ['door', 'door']}))
trial('door-square-mark', lambda m: m['style'].__setitem__('doors', 'square'))
trial('numbers-plain-on', lambda m: (m.__setitem__('numbers', True), m['style'].__setitem__('numbers', 'plain')))
trial('room-fill-building-yard-cellar', lambda m: [rooms[c].__setitem__('fill', k) for c, k in (('Y.18', 'building'), ('Y.19', 'yard'), ('Y.20', 'cellar'))])
trial('hexagon-pointy-octagon-cut', lambda m: [rooms['Y.14'].__setitem__('orient', 'pointy'), rooms['Y.11'].__setitem__('cut', 0.2)])
trial('label-href-and-labelAt', lambda m: (rooms['Y.3'].__setitem__('labelAt', 'n'), m['overlay']['labels'].append({'text': 'link', 'x': 5, 'y': 5, 'kind': 'note', 'href': '#anchor'})))
trial('scale-symbol-stretch', lambda m: sym(m, 'stairs', 10, 10, scaleX=0.8, scaleY=4))
trial('grid-everywhere', lambda m: m['grid'].update({'clip': 'all', 'sub': True}))
trial('palette-blueprint-preset', lambda m: m['style'].update({'preset': 'blueprint', 'palette': {'wall': '#ffffff'}}))
