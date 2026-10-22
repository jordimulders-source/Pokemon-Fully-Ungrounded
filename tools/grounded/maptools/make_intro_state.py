"""Maakt een savestate na de (korte) intro, voor emulatortests. Een nieuw spel start in StartTown (9, 12).
Gebruik: python3 tools/grounded/maptools/make_intro_state.py pokeemerald.gba <uit.bin> [pokeemerald.map]
Drukt A tot de speler in de overworld staat (gMain.callback2 == CB2_Overworld, adressen uit pokeemerald.map van
dezelfde build) en meldt de kaart. Let op: een savestate is ongeldig na elke rebuild; maak hem dan opnieuw."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from emu import Emu
REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
rom, out = sys.argv[1], sys.argv[2]
mapfile = sys.argv[3] if len(sys.argv) > 3 else os.path.join(REPO, 'pokeemerald.map')


def sym(name):
    for l in open(mapfile):
        m = re.match(r'\s+0x([0-9a-f]+)\s+' + name + r'$', l)
        if m:
            return int(m.group(1), 16)


e = Emu(rom); e.run(600)
overworld = sym('CB2_Overworld') if os.path.exists(mapfile) else None
for i in range(80):
    e.press('A', after=40)
    if i >= 20 and overworld and (e.core.memory.u32[sym('gMain') + 4] & ~1) == overworld:
        e.run(120)
        break
if overworld:
    sb1 = e.core.memory.u32[sym('gSaveBlock1Ptr')]
    print('intro klaar: kaart %d.%d, positie (%d, %d)' % (e.core.memory.u8[sb1 + 4], e.core.memory.u8[sb1 + 5],
                                                        e.core.memory.s16[sb1], e.core.memory.s16[sb1 + 2]))
open(out, 'wb').write(bytes(e.core.save_raw_state()))
