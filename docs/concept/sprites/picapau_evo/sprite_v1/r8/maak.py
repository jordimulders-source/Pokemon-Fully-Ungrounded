"""r8: tekening_<V>.txt = basis.txt (r7 zonder snavel) + snavel_<V>.txt (met de hand), daarna zet, bouw, controle en diff.
Draaien: python3.11 maak.py A B"""
import sys, subprocess
for V in sys.argv[1:]:
    open(f'tekening_{V}.txt', 'w').write(open('basis.txt').read() + open(f'snavel_{V}.txt').read())
    for cmd in (['zet.py', V], ['bouw.py', f'raster_{V}.txt', f'picapau_evo_{V}.png'], ['controle.py', V], ['diff.py', V]):
        r = subprocess.run(['python3.11'] + cmd, capture_output=True, text=True)
        print(f'[{V}] {cmd[0]}:', (r.stdout + r.stderr).strip().split('\n')[0] if cmd[0] != 'zet.py' else (r.stdout + r.stderr).strip())
