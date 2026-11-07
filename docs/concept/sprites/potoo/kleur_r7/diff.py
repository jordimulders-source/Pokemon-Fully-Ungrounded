"""Bewijs: pixeldiff r7 t.o.v. r6 buiten de reparatiezones = 0."""
import os, runpy
H = os.path.dirname(os.path.abspath(__file__)); W = runpy.run_path(os.path.join(H, 'wijzig_r7.py'))
a = [l.rstrip('\n') for l in open(os.path.join(H, '../kleur_r6/raster.txt'))]; b = [l.rstrip('\n') for l in open(os.path.join(H, 'raster.txt'))]
inz = lambda x, y: any(x0 <= x <= x1 and y0 <= y <= y1 for x0, y0, x1, y1 in W['ZONES']) or (x, y) in W['KUIF']
d = [(x, y) for y in range(64) for x in range(64) if a[y][x] != b[y][x]]
buiten = [p for p in d if not inz(*p)]
print(f'gewijzigd t.o.v. r6: {len(d)} px; buiten de zones: {len(buiten)} {buiten}')
