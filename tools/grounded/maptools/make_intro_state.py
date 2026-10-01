"""Maakt een savestate na de (korte) intro, voor emulatortests.
Gebruik: python3 tools/grounded/maptools/make_intro_state.py pokeemerald.gba <uit.bin>
Let op: een savestate is ongeldig na elke rebuild; maak hem dan opnieuw."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from emu import Emu
rom, out = sys.argv[1], sys.argv[2]
e = Emu(rom); e.run(600)
for i in range(40):
    e.press('A', after=40)
open(out, 'wb').write(bytes(e.core.save_raw_state()))
