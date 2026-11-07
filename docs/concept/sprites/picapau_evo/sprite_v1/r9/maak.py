"""r9: tekening.txt = basis.txt (r7 zonder snavel en oren) + kop.txt (kop, snavel, oren met de hand), daarna zet, bouw, controle, diff.
Draaien: python3.11 maak.py"""
import subprocess
open('tekening.txt', 'w').write(open('basis.txt').read() + open('kop.txt').read())
for cmd in (['zet.py'], ['bouw.py'], ['controle.py'], ['diff.py']):
    r = subprocess.run(['python3.11'] + cmd, capture_output=True, text=True)
    print(f'{cmd[0]}:', '\n'.join(l for l in (r.stdout + r.stderr).strip().split('\n') if 'regel' not in l))
