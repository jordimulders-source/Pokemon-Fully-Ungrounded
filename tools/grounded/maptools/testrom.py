"""Bouwt een test-ROM met tijdelijke debug-scripts en zet data/scripts/debug.inc daarna terug.
Gebruik: python3 tools/grounded/maptools/testrom.py <uitmap> "regels voor script 1" ["regels voor script 2" ...]
Regels scheiden met ';', bijv.:
  testrom.py /tmp/x "givemon SPECIES_LAPRAS, 50, move1=MOVE_SURF; warp MAP_ROUTE136_GROTTO, 15, 19; waitstate"
Maakt <uitmap>/test.gba en <uitmap>/intro.bin (savestate na de intro). Starten in de emulator:
  e=Emu(rom); load(e,intro); debug_script(e,1)   (zie emu.py)"""
import os, sys, shutil, subprocess
REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
out, scripts = sys.argv[1], sys.argv[2:]
os.makedirs(out, exist_ok=True)
p = os.path.join(REPO, 'data/scripts/debug.inc')
orig = open(p).read()
s = orig
for i, body in enumerate(scripts, 1):
    lines = ''.join(f'\t{l.strip()}\n' for l in body.split(';') if l.strip())
    s = s.replace(f'Debug_EventScript_Script_{i}::\n\trelease\n\tend', f'Debug_EventScript_Script_{i}::\n{lines}\trelease\n\tend', 1)
try:
    open(p, 'w').write(s)
    r = subprocess.run(['make', '-j4'], cwd=REPO, capture_output=True, text=True)
    if r.returncode:
        print(r.stdout[-2000:], r.stderr[-2000:]); sys.exit(1)
    shutil.copy(os.path.join(REPO, 'pokeemerald.gba'), os.path.join(out, 'test.gba'))
finally:
    open(p, 'w').write(orig)
subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'make_intro_state.py'),
                os.path.join(out, 'test.gba'), os.path.join(out, 'intro.bin')], check=True)
print('klaar:', os.path.join(out, 'test.gba'), '(debug.inc is teruggezet; pokeemerald.gba bevat nog de testscripts, bouw opnieuw voor een schone ROM)')
