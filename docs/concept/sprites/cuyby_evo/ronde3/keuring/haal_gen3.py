"""Haalt de echte Gen 3-sprites (anim_front_gba.png + normal_gba.pal) uit de git-geschiedenis (commit 358c0d0699,
'Added back GBA sprites via config') naar keuring/gen3/<naam>/. In de huidige graphics/pokemon/ staan de
nieuwere expansion-sprites. Vanuit de repo-root: python3 docs/concept/sprites/cuyby_evo/ronde3/keuring/haal_gen3.py
"""
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '../../../../../..'))
COMMIT = '358c0d0699'
NAMEN = ['mareep', 'swinub', 'piloswine', 'linoone', 'furret', 'teddiursa', 'ninetales', 'vulpix',
         'eevee', 'skitty', 'zigzagoon', 'whismur', 'swablu', 'mawile']
for n in NAMEN:
    d = os.path.join(HERE, 'gen3', n)
    os.makedirs(d, exist_ok=True)
    for f in ('anim_front_gba.png', 'normal_gba.pal'):
        data = subprocess.run(['git', '-C', REPO, 'show', '%s:graphics/pokemon/%s/%s' % (COMMIT, n, f)],
                              capture_output=True, check=True).stdout
        open(os.path.join(d, f), 'wb').write(data)
print('ok', len(NAMEN))
