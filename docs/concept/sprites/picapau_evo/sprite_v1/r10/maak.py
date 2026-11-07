"""r10: tekening.txt = r9/tekening.txt + Swellows bovensnavel (snavel_swellow.txt, rij 8-11) + aanpassing.txt; daarna zet, bouw, controle, diff, platen.
Draaien: python3.11 swellow_snavel.py && python3.11 maak.py"""
import subprocess
sw = [l for l in open('snavel_swellow.txt').read().split('\n') if l and not l.startswith('#')]
boven = [l for l in sw if int(l.split()[0]) <= 11]
t = open('../r9/tekening.txt').read().rstrip('\n') + '\n'
t += '# --- snavel r10: Swellows bovensnavel letterlijk (snavel_swellow.txt, rij 8-11)\n' + '\n'.join(boven) + '\n' + open('aanpassing.txt').read()
open('tekening.txt', 'w').write(t.replace('# Sprite r9 = r7', '# Sprite r10 = r9 met Swellows snavel letterlijk (blok onderaan); r9 = r7', 1))
for cmd in ('zet.py', 'bouw.py', 'controle.py', 'diff.py', 'platen.py'):
    r = subprocess.run(['python3.11', cmd], capture_output=True, text=True)
    print(cmd, (r.stdout + r.stderr).strip().split('\n')[0])
