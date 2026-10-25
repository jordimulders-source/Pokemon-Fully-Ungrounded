"""Silhouet ronde 8 = ronde 7 (Jordi's gum, 6g) met:
- staande verre voorpoot: onderpoot loopt schuin naar achter tot de hiel (x 27 eraf op y 57-58, x 32 erbij op y 57-60);
- hangende klauwen gladder: (16,58) eraf (klauw A loopt gelijkmatiger), (23,57) eraf (klauw B taps)."""
import os
H = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(H, '../../../silhouet')
sil = [list(l.rstrip('\n')) for l in open(os.path.join(S, 'ronde7.txt')) if l.strip()]
ERAF = [(27, 57), (27, 58), (16, 58), (23, 57)]
ERBIJ = [(32, 57), (32, 58), (32, 59), (32, 60)]
for x, y in ERAF: assert sil[y][x] == '#'; sil[y][x] = '.'
for x, y in ERBIJ: assert sil[y][x] == '.'; sil[y][x] = '#'
open(os.path.join(S, 'ronde8.txt'), 'w').write('\n'.join(''.join(r) for r in sil) + '\n')
print('ronde8.txt:', sum(r.count('#') for r in sil), 'px (-%d +%d)' % (len(ERAF), len(ERBIJ)))
