"""Test route-transities: bouwt een test-ROM met per plek een warp-script (slots 1..7) en in slot 8 een wild gevecht,
en maakt per plek een strook frames van de transitie.
Gebruik: python3 tools/grounded/maptools/transtest.py <uitmap> "MAP_X, x, y" ["MAP_Y, x, y" ...]
Uitvoer: <uitmap>/trans_<n>.png (12 frames, 8 frames uit elkaar)."""
import os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
out, spots = sys.argv[1], sys.argv[2:]
BADGES = '; '.join('setflag FLAG_BADGE0%d_GET' % i for i in range(1, 9))
ARCEUS = 'givemon SPECIES_ARCEUS, 100, move1=MOVE_DARK_PULSE, move2=MOVE_PSYCHIC, move3=MOVE_THUNDERBOLT, move4=MOVE_ICE_BEAM'
scripts = ['%s; %s; warp %s; waitstate' % (BADGES, ARCEUS, s) for s in spots]
scripts += [''] * (7 - len(scripts)) + ['setwildbattle SPECIES_ZIGZAGOON, 5; dowildbattle']
subprocess.run([sys.executable, os.path.join(HERE, 'testrom.py'), out] + scripts, check=True)
sys.path.insert(0, HERE)
from emu import Emu, load, debug_script
from PIL import Image
for n in range(1, len(spots) + 1):
    e = Emu(os.path.join(out, 'test.gba')); load(e, os.path.join(out, 'intro.bin'))
    debug_script(e, n)
    debug_script(e, 8, settle=0)
    shots = []
    for i in range(12):
        e.run(8); shots.append(e.img.to_pil().convert('RGB'))
    W = Image.new('RGB', (240 * 4, 160 * 3))
    for i, im in enumerate(shots): W.paste(im, ((i % 4) * 240, (i // 4) * 160))
    W.save(os.path.join(out, 'trans_%d.png' % n))
print('klaar')
