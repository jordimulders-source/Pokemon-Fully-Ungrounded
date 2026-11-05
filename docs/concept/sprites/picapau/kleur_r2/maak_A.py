"""Eenmalige hulp: past de handgetekende r2-wijzigingen toe op r1/raster.txt -> raster_A.txt.
Elke regel hieronder is met de hand gekozen (geen automatische vormen)."""
import os
D = os.path.dirname(os.path.abspath(__file__))
rows = [list(r.rstrip('\n')) for r in open(os.path.join(D, '..', 'kleur_r1', 'raster.txt'))][:64]
def zet(y, x0, s):
    for i, c in enumerate(s):
        if c != '_':
            rows[y][x0 + i] = c
# kuiftoppen: zwarte kap 2-4 px breed (zone kuiftoppen, +-1 px)
zet(4, 33, 'kk'); zet(5, 32, 'kek'); zet(6, 31, 'keek')          # punt A
zet(4, 38, 'k'); zet(5, 37, 'kek'); zet(6, 36, 'keek')            # punt B
# snavel: punt donker, aanzet licht en doorlopend in de kop
zet(17, 15, 'k4')
zet(18, 15, 'k34')
zet(19, 16, 'k3412')
zet(20, 17, 'k3112')
zet(21, 17, 'k33112')
zet(22, 18, 'k3342')
zet(23, 19, 'kk3')
# vleugel: schouder lichter (l), drie rijen schubben (1 -> 2 -> 3 naar de punt) met donkere onderkant, slagpennen naar de punt donkerder
zet(25, 35, 'dllbbk')
zet(26, 34, 'dlllbbbk')
zet(27, 34, 'd1ll1bbk')
zet(28, 34, 'db11b11dk')
zet(29, 34, 'dbddbdddk')
zet(30, 35, 'dbbbbbbdk')
zet(31, 35, 'd2bb2bbdk')
zet(32, 35, 'db22b22bdk')
zet(33, 36, 'dddbddbdk')
zet(34, 36, 'dbbbbbbbdk')
zet(35, 37, 'db3bb3bdk')
zet(36, 38, 'db33b33dk')
zet(37, 38, 'dbddbdddk')
zet(38, 39, 'drrrrbbdk')
zet(39, 39, 'drrdrrbdk')
zet(40, 40, 'drrdrbbdk')
zet(41, 40, 'drbdrbbdk')
zet(42, 41, 'drbdbbbdk')
zet(43, 42, 'dbbdbbbdk')
zet(44, 43, 'dbbdbddk')
zet(45, 44, 'dbdbdk')
zet(46, 44, 'dkbddk')
open(os.path.join(D, 'raster_A.txt'), 'w').write('\n'.join(''.join(r) for r in rows) + '\n')
# na controle: mini-clusters weg
rows[22][21] = '3'; rows[33][42] = 'd'; rows[47][47] = 'b'
open(os.path.join(D, 'raster_A.txt'), 'w').write('\n'.join(''.join(r) for r in rows) + '\n')
# snavel: lichte bovenhelft doorgetrokken naar de punt (anders verdwijnt de snavel in de kop)
rows[19][17] = '1'; rows[20][18] = '1'; rows[18][16] = '4'  # punt donker
open(os.path.join(D, 'raster_A.txt'), 'w').write('\n'.join(''.join(r) for r in rows) + '\n')
