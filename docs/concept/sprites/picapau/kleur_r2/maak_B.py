"""Variant B (voorstel voor Jordi): raster_A.txt + met de hand gekozen silhouetwijzigingen -> raster_B.txt.
Snavel aan de basis dikker, pootjes uit elkaar (verre poot 1 px hoger en naar achteren, kolom 33 lucht), buikonderkant rond."""
import os
D = os.path.dirname(os.path.abspath(__file__))
rows = [list(r.rstrip('\n')) for r in open(os.path.join(D, 'raster_A.txt'))][:64]
def zet(y, x0, s):
    for i, c in enumerate(s):
        if c != '_':
            rows[y][x0 + i] = c
# snavel: basis 1 px dikker boven (18,18) en onder (17,22), (18,23)
zet(18, 15, 'k444')
zet(19, 16, 'k1112')
zet(22, 17, 'k33332')
zet(23, 18, 'kkk3')
# poten + ronde buik
zet(45, 30, 'kgkkkGk33334kk')
zet(46, 27, 'kkgggk.kGGGk44k..')
zet(47, 26, 'kkggkgk..kkk.kk')
zet(48, 34, '.')
open(os.path.join(D, 'raster_B.txt'), 'w').write('\n'.join(''.join(r) for r in rows) + '\n')
rows[45][36] = 'G'  # verre poot 2 px breed (geen losse zwarte pixel)
open(os.path.join(D, 'raster_B.txt'), 'w').write('\n'.join(''.join(r) for r in rows) + '\n')
