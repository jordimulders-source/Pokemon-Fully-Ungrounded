"""Controle ronde 4: kleuren, silhouet-diff met ronde 6 (en per afwijking de dekking van het model), open randen,
losse pixels, en het bewijs dat de oogvarianten alleen in de oogzone verschillen.
Draaien: python3 docs/concept/sprites/lama/fase2/kleur/ronde4/bron/controle.py"""
import os
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
R6 = [l.rstrip('\n') for l in open(os.path.join(OUT, '../../silhouet_r6/ronde6.txt'))]
a = np.load(os.path.join(OUT, '../../silhouet_r5/kop_alpha.npy')); k = a.shape[0] // 64
cov = a.reshape(64, k, 64, k).mean((1, 3))
LET = '.kdsblhormnygpuv'
def grid(name):
    im = Image.open(os.path.join(OUT, name)); return im, [[LET[im.getpixel((x, y))] for x in range(64)] for y in range(64)]
im, g = grid('lama.png')
print('lama.png: mode', im.mode, '| transparency', im.info.get('transparency'), '| palet', len(im.getpalette()) // 3,
      '| kleuren gebruikt (incl. transparant):', len({c for r in g for c in r}), '| pixels', sum(c != '.' for r in g for c in r))
plus = [(x, y) for y in range(64) for x in range(64) if g[y][x] != '.' and R6[y][x] != '#']
mins = [(x, y) for y in range(64) for x in range(64) if g[y][x] == '.' and R6[y][x] == '#']
lines = ['Diffkaart kleur ronde 4g t.o.v. silhouet ronde 6 (en de 50%-dekking van het model, silhouet_r5/kop_alpha.npy).',
         'Toegestaan (Claude, 4c): wolomtrek van lijf, hals en borst max. 2 px van het model; elders max. 1 px (glad/staart).',
         f'Silhouet t.o.v. ronde 6: +{len(plus)} / -{len(mins)} px (totaal {len(plus) + len(mins)})']
def afstand(x, y, inside):   # afstand (px) tot de 50%-grens van het model
    best = 9
    for dy in range(-3, 4):
        for dx in range(-3, 4):
            xx, yy = x + dx, y + dy
            if 0 <= xx < 64 and 0 <= yy < 64 and ((cov[yy, xx] >= .5) == inside): best = min(best, max(abs(dx), abs(dy)))
    return best
for sgn, lst in (('+', plus), ('-', mins)):
    for x, y in lst:
        inside = cov[y, x] >= .5
        d = 0 if (sgn == '+') == inside else afstand(x, y, sgn == '+')
        lines.append(f'  {sgn} x{x} y{y}  dekking model {cov[y, x]:.2f}  afwijking van de 50%-grens: {d} px')
print('\n'.join(lines))
OK = set('kdmn')
def at(x, y): return g[y][x] if 0 <= x < 64 and 0 <= y < 64 else '.'
open_ = [(x, y, g[y][x]) for y in range(64) for x in range(64)
         if g[y][x] != '.' and any(at(x + a, y + b) == '.' for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))) and g[y][x] not in OK]
PSEUDO = {(17, 3), (17, 7), (17, 8), (24, 61), (14, 62), (16, 62)}   # §8 pseudo-omlijning: oor van 2 px breed, nagels van 1 px
echt = [o for o in open_ if (o[0], o[1]) not in PSEUDO]
print('open randen (randpixel die geen k/d/m/n is):', len(echt), echt, '| bewuste pseudo-omlijning (§8):', [o for o in open_ if (o[0], o[1]) in PSEUDO])
alone = [(x, y, g[y][x]) for y in range(64) for x in range(64) if g[y][x] not in '.k'
         and all(at(x + a, y + b) != g[y][x] for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)))]
print('losse pixels (geen buur met dezelfde kleur):', len(alone), alone)
from collections import Counter
c = Counter(ch for r in g for ch in r if ch != '.'); tot = sum(c.values())
print('verdeling:', ' '.join(f'{ch}:{c[ch] * 100 // tot}%' for ch in LET[1:] if c[ch]))
R4 = [[LET[c] for c in row] for row in [[Image.open(os.path.join(OUT, '../ronde4f/lama.png')).getpixel((x, y)) for x in range(64)] for y in range(64)]]
d4 = [(x, y) for y in range(64) for x in range(64) if g[y][x] != R4[y][x]]
def tel(x0, y0, x1, y1): return sum(1 for x, y in d4 if x0 <= x <= x1 and y0 <= y <= y1)
print('diff t.o.v. ronde 4f:', len(d4), 'px')
hals = lambda x, y: 14 <= x <= 27 and 20 <= y <= 28
print('  halszone x14-27 y20-28:', sum(1 for p in d4 if hals(*p)), '| daarbuiten:', [p for p in d4 if not hals(*p)])
WAAROM = {(49, 23): 'staart: pluim', (50, 23): 'staart: pluim schuin naar achteren', (51, 24): 'staart: pluim 5 breed', (51, 25): 'staart: idem',
          (46, 25): 'staart: lucht aan de rugzijde', (46, 26): 'staart: lucht aan de rugzijde / wolboog rug', (42, 26): 'wolboog rug (insnoering)',
          (43, 25): 'glad: losse bult weg (r4)', (44, 25): 'glad: idem', (45, 25): 'glad: idem', (51, 26): 'glad: hoek achterwerk (r4)',
          (51, 30): 'wolboog achterwerk', (51, 32): 'wolboog achterwerk', (51, 33): 'wolboog achterwerk', (51, 34): 'wolboog achterwerk',
          (50, 36): 'wolboog achterwerk (insnoering)', (49, 40): 'glad: hoek buik/achterwerk afgerond',
          (13, 34): 'wolboog borst', (13, 35): 'wolboog borst', (13, 36): 'wolboog borst', (13, 37): 'wolboog borst', (13, 41): 'wolboog borst onder',
          (29, 25): 'doek: bovenhoek afgerond', (37, 25): 'doek: bovenhoek afgerond', (49, 59): 'verre achterhoef (eigen hoef)'}
WAAROM.setdefault
lines = [l + ('   <- ' + WAAROM.get((int(l.split()[1][1:]), int(l.split()[2][1:])), 'wolboog (4c lijf / 4e-4g hals, max. 2 px)') if l.startswith('  ') else '') for l in lines]
kaart = ['', 'Kaart y20-42, x38-53 (# beide, + alleen ronde 4, - alleen ronde 6):']
for y in range(20, 43):
    kaart.append(f'y{y:02d} ' + ''.join('+' if (g[y][x] != '.' and R6[y][x] != '#') else '-' if (g[y][x] == '.' and R6[y][x] == '#') else '#' if g[y][x] != '.' else '.' for x in range(38, 54)))
open(os.path.join(OUT, 'diff_silhouet.txt'), 'w').write('\n'.join(lines + kaart) + '\n')
