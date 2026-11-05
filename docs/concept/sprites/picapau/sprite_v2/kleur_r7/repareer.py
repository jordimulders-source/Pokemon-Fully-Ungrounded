"""r7 = r6 + Jordi's punten over r6 (5 nov), door Claude toegepast met controle op de oude waarde:
1 staartpunt: inkeping op rij 51 dicht, zodat de rechterrand van de punt doorloopt uit de knobbel (zoals de render);
2 buik: de losse lichtvlek op de buik (rij 39-43) weg ("willekeurige cirkels op de buik");
3 palet: geel 1/2/3 donkerder, niet lichter dan Pikachu ("hoofd en de buik wat tinten te licht");
4 vleugel: de fellere stip linksboven gelijk aan de andere ("1 stip op de vleugel is opeens veel lichter");
5 kuif: lichte kant van beide kegels (reparatie 6 uit kleur_r5/KEURING.md, toonkaart toon 4; Jordi: "kuif mag je zijn suggestie doen")."""
R = [l.rstrip('\n') for l in open('../kleur_r6/raster.txt')][:64]
g = [list(r) for r in R]; log, mis = [], []
def zet(x, y, oud, nieuw, rep):
    if g[y][x] != oud: mis.append((rep, x, y, g[y][x], oud)); return
    g[y][x] = nieuw; log.append((rep, x, y, oud, nieuw))
zet(49, 51, 'k', 'b', 1); zet(50, 51, '.', 'k', 1)
for y in range(38, 45):
    for x in range(26, 40):
        if g[y][x] == '1': zet(x, y, '1', '2', 2)
for x, y in [(35, 27), (36, 27), (35, 28), (36, 28)]: zet(x, y, 'h', 'g', 4)
for x, y in [(35, 9), (33, 10), (34, 10), (32, 11), (33, 11), (31, 12), (32, 12), (33, 12), (31, 13), (32, 13), (31, 9), (30, 10), (30, 11)]:
    zet(x, y, '2', '1', 5)
open('raster.txt', 'w').write('\n'.join(''.join(r) for r in g) + '\n')
print('toegepast', len(log), [l for l in log if l[0] == 2]); print('NIET toegepast:', mis)
# 5b opruimen (geen tintclusters < 3 px in de kuif): voorste kegel lichte kant als één vlak, losse pixel achterste kegel terug
R = [l.rstrip('\n') for l in open('raster.txt')][:64]; g = [list(r) for r in R]; log, mis = [], []
zet(31, 10, '2', '1', '5b'); zet(32, 9, '2', '1', '5b'); zet(35, 9, '1', '2', '5b')
open('raster.txt', 'w').write('\n'.join(''.join(r) for r in g) + '\n'); print('5b', log, mis)
# 5c (35,9) '2' -> '3' (de r2-waarde; sluit aan op de schaduw van de achterste kegel)
