"""The feature pass for the test dungeon: takes each level's map as built from its tables and adds what the design
does not state - symbols, door kinds, rings, wavy edges, natural passages, labels - then checks and renders it."""
import sys, json, subprocess, math, collections, copy
R = '/tmp/claude-0/-home-user-setting-builder/194b492d-8ef5-5235-91e9-0447072bdc6d/scratchpad/repoX'
OUT = '/tmp/claude-0/-home-user-setting-builder/194b492d-8ef5-5235-91e9-0447072bdc6d/scratchpad/full'
ART = [ 'node', f'{R}/tools/artgen/artgen-maps.js' ]

def art(*a):
    return subprocess.run(ART + list(a), capture_output=True, text=True)

def facts(path):
    return json.loads(art('dungeon', 'facts', '--file', path, '--json').stdout)

def room_boxes(m):
    return {r['label']: r for r in m['rooms']}

def centre(r):
    return r['x'] + r['w'] / 2, r['y'] + r['h'] / 2

def sym(m, kind, x, y, **kw):
    m['overlay']['symbols'].append({'kind': kind, 'x': round(x, 2), 'y': round(y, 2), **kw})

def label(m, text, x, y, kind='area', **kw):
    m['overlay']['labels'].append({'text': text, 'x': round(x, 2), 'y': round(y, 2), 'kind': kind, **kw})

def along(path, t):
    pts = list(zip(path[::2], path[1::2]))
    seg = [math.dist(a, b) for a, b in zip(pts, pts[1:])]
    total = sum(seg); goal = total * t
    for (a, b), s in zip(zip(pts, pts[1:]), seg):
        if goal <= s or s == 0:
            f = goal / s if s else 0
            return a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f, math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
        goal -= s
    return pts[-1][0], pts[-1][1], 0

def finish(name, m, fit=1400):
    f = f'{OUT}/{name}.json'
    json.dump(m, open(f, 'w'), indent=1)
    chk = json.loads(art('dungeon', 'check', '--file', f, '--json').stdout or '{}')
    found = collections.Counter(x.get('id', 'schema') for x in chk.get('errors', []) + chk.get('warnings', []))
    errs = [x for x in chk.get('errors', [])]
    r = art('dungeon', 'render', '--file', f, '--format', 'both', '--fit', f'{fit}x{fit}px', '--out', OUT)
    print(f'{name}: ok={chk.get("ok")} errors={len(errs)} findings={dict(found)} render rc={r.returncode} {r.stderr.strip()[:200]}')
    for e in errs[:8]:
        print('   ERROR', e.get('id'), e.get('path'), e['message'][:150])
    return chk

import os
os.makedirs(OUT, exist_ok=True)
