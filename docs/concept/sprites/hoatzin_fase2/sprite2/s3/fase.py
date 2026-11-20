# fase.py: probeer rasterfases (DX, DY in spritepx) en meet hoeveel modeldetail overblijft in de sprite:
# rood in het oog, kuif-pixels (licht/donker), licht grijs in de snavel, vleugel-lijnpixels (ruis) en zuiverheid.
import subprocess, os, numpy as np
FASES = [(dx, dy) for dx in (-0.5, -0.25, 0, 0.25, 0.5) for dy in (-0.5, -0.25, 0, 0.25, 0.5)]
res = []
for dx, dy in FASES:
    env = dict(os.environ, DX=str(dx), DY=str(dy))
    out = subprocess.run('python3 reduceer.py && python3 lijnen.py && python3 bouw.py', shell=True, env=env, capture_output=True, text=True).stdout
    pur = float([l for l in out.split('\n') if l.startswith('zuiverheid')][0].split()[1])
    S = np.load('hoatzin.npy')
    ck = subprocess.run('python3 ../../sprite/r11/check.py hoatzin.png; python3 ../../sprite/r23/barcode.py hoatzin.png', shell=True, capture_output=True, text=True).stdout
    fout = sum(int(l.split()[1]) if l.startswith(('dambord', 'om-en', 'barcode')) else int(l.split()[3]) if l.startswith('zwarte') else 0 for l in ck.split('\n') if l)
    r = dict(dx=dx, dy=dy, pur=pur, rood=int((S == 14).sum()), kuif=int(np.isin(S, (10, 11)).sum()),
             snavel=int((S[26:40, 0:9] == 15).sum()), fout=fout)
    res.append(r); print(r)
best = max(res, key=lambda r: (r['fout'] == 0, r['rood'] >= 3, r['snavel'] + r['kuif'] / 4 + r['rood']))
print('beste', best)
open('fase_keuze.txt', 'w').write('%s %s\n' % (best['dx'], best['dy']))
