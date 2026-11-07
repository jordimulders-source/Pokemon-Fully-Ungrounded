"""Close-up kop op 16x: r7 en r6 (kop met snavel en beide krullen) naast de snavelreferenties op 16x (Fearow, Pidgeot, Staraptor, Picapau).
Draaien: python3.11 kop_closeup.py"""
from ref_snavels import SNAVELS, vel
kies = dict((t, (t, f, c)) for t, f, c in SNAVELS)
items = [('kop r7', 'picapau_evo.png', (4, 0, 48, 18)), ('kop r6', '../r6/picapau_evo.png', (4, 0, 48, 18))] + \
        [kies[n] for n in ('Fearow', 'Pidgeot', 'Staraptor', 'Picapau')]
vel(items, 16, 'kop_closeup.png')
