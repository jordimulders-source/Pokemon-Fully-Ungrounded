"""r9 = kop van r8 lager + snavel van r7b (vorm en kleuren pixel voor pixel) + een donkere lijn waar de snavel aan het
gezicht vastzit (snavelbasis en mondhoek). Bewijst: oog = r7b, snavelzone tegen r7b alleen de lijnpixels anders."""
import palet
r7b = [l.rstrip('\n') for l in open('../kleur_r7/raster_r7b.txt')][:64]
r8l = [l.rstrip('\n') for l in open('../kleur_r8/raster_lager.txt')][:64]
g = [list(r) for r in r8l]
# snavel van r7b: rijen 14-21, x <= 16 (rij 12-13: alleen x <= 14; het voorhoofd blijft r8 lager, B3)
for y in range(12, 22):
    for x in range(0, 17 if y >= 14 else 15):
        g[y][x] = r7b[y][x]
# de lijn (met de hand): snavelbasis schuin omlaag, mondhoek, en de basis van de ondersnavel
LIJN = {(14, 14): '1', (15, 15): '1', (16, 16): '1', (17, 17): '1', (17, 18): '1', (18, 18): '2', (17, 19): '1', (17, 20): '1'}
for (x, y), c in LIJN.items(): g[y][x] = c
g = [''.join(r) for r in g]
open('raster.txt', 'w').write('\n'.join(g) + '\n')
palet.build('raster.txt', 'kolibrie_pre.png')
zone = [(x, y) for y in range(12, 22) for x in range(0, 19)]
print('snavelzone (x<=18, y12-21) anders dan r7b:', sorted([(x, y, r7b[y][x], g[y][x]) for x, y in zone if r7b[y][x] != g[y][x]], key=lambda t: (t[1], t[0])))
OOG = [(x, y) for y in range(14, 19) for x in range(21, 26) if (x, y) not in ((21, 14), (25, 14), (21, 18), (25, 18))]
print('oogpixels anders dan r7b:', sum(r7b[y][x] != g[y][x] for x, y in OOG))
print('alpha-diff tegen r7b:', [(x, y) for y in range(64) for x in range(64) if (r7b[y][x] != '.') != (g[y][x] != '.')])
d8 = [(x, y) for y in range(64) for x in range(64) if r8l[y][x] != g[y][x] and not (x <= 16 and 12 <= y <= 21)]
print('buiten de snavelzone anders dan r8 lager:', d8, '| px', sum(c != '.' for r in g for c in r))
