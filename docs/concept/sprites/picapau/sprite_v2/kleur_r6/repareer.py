"""r6 = r5 + reparaties 1-5 uit kleur_r5/KEURING.md (exacte pixeltabel, door Claude toegepast met controle op de oude waarde).
Reparatie 6 (kuifkegels, Jordi's zone kop rechts) niet uitgevoerd."""
R = [l.rstrip('\n') for l in open('../kleur_r5/raster.txt')][:64]
g = [list(r) for r in R]
log, mis = [], []
def zet(x, y, oud, nieuw, rep):
    if g[y][x] != oud: mis.append((rep, x, y, g[y][x], oud, nieuw)); return
    g[y][x] = nieuw; log.append((rep, x, y, oud, nieuw))
def rij(y, xs, oud, nieuw, rep):
    for x in xs: zet(x, y, oud, nieuw, rep)
# 1 gezichtslicht
for y, rs in {16: [(25, 29)], 17: [(22, 30)], 18: [(20, 23), (28, 30)], 19: [(21, 23), (28, 29)], 20: [(22, 23), (28, 29)],
              21: [(22, 23), (28, 28)], 22: [(24, 27)], 23: [(24, 24)]}.items():
    for a, b in rs: rij(y, range(a, b + 1), '2', '1', 1)
for x, y in [(22, 22), (23, 22), (22, 23), (23, 23)]: zet(x, y, '3', '1', 1)
for x, y in [(24, 18), (27, 18), (24, 21), (27, 21)]: zet(x, y, '3', '2', 1)
# 2 kopschaduw als sikkel
for x, y in [(32, 20), (31, 21), (30, 22), (31, 22), (29, 23), (30, 23), (29, 24), (22, 24), (23, 24), (21, 25), (22, 25), (23, 25)]: zet(x, y, '3', '2', 2)
for x, y in [(33, 16), (33, 17)]: zet(x, y, '2', '3', 2)
# 3 snavel
for x, y in [(18, 20), (19, 20), (20, 20), (19, 21), (20, 21)]: zet(x, y, 'h', 'g', 3)
for x, y in [(19, 22), (20, 22), (19, 23), (20, 23)]: zet(x, y, 'g', 'G', 3)
# 4 vleugelstippen + schoudervoorrand
for x, y in [(39, 26), (40, 26), (40, 27), (36, 31), (37, 31), (36, 32), (37, 32), (42, 35), (43, 35)]: zet(x, y, 'h', 'g', 4)
for x, y in [(34, 29), (35, 29), (34, 30)]: zet(x, y, 'b', 'l', 4)
# 5 halsplooi
zet(24, 30, '4', '.', 5); zet(25, 30, '2', '4', 5)
open('raster.txt', 'w').write('\n'.join(''.join(r) for r in g) + '\n')
print('toegepast', len(log)); print('NIET toegepast (oude waarde klopt niet):', mis)
