"""Diffkaart ronde 1 tegen het model (50%-dekking): X = beide, + = alleen ronde 1, - = alleen model. Plus afstandscheck,
componenten en gaten. Draaien: python3 diff_model.py > diff_model.txt"""
import os
import numpy as np
def dil(m):
    P = np.pad(m, 1); o = np.zeros_like(m)
    for dy in range(3):
        for dx in range(3): o |= P[dy:dy+64, dx:dx+64]
    return o
def label(m):  # 8-buur componenten
    lab = np.zeros(m.shape, int); n = 0
    for y0, x0 in zip(*np.nonzero(m)):
        if lab[y0, x0]: continue
        n += 1; st = [(y0, x0)]; lab[y0, x0] = n
        while st:
            y, x = st.pop()
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    v, u = y + dy, x + dx
                    if 0 <= v < 64 and 0 <= u < 64 and m[v, u] and not lab[v, u]: lab[v, u] = n; st.append((v, u))
    return lab, n
HERE = os.path.dirname(os.path.abspath(__file__))
a = np.load(os.path.join(HERE, 'alpha.npy')); k = a.shape[0] // 64
cov = a.reshape(64, k, 64, k).mean((1, 3)); M = cov >= 0.5
S = np.array([[c == '#' for c in l.rstrip('\n')] for l in open(os.path.join(HERE, 'ronde1.txt')) if l.strip()])
plus, minus = S & ~M, M & ~S
print(f'model (50%): {int(M.sum())} px | ronde 1: {int(S.sum())} px | alleen ronde 1 (+): {int(plus.sum())} | alleen model (-): {int(minus.sum())}')
# afstand: + moet grenzen (8-buur) aan model-pixel, - aan niet-model-pixel
dM = dil(M); dN = dil(~M)
far = (plus & ~dM) | (minus & ~dN)
print(f'afwijkingen > 1 px van de 50%-grens: {int(far.sum())}')
for y, x in zip(*np.nonzero(plus | minus)):
    print(f'   {"+" if plus[y, x] else "-"} x{x} y{y}  dekking {cov[y, x]:.2f}')
lab, n = label(S)
E = np.pad(~S, 1, constant_values=True)
bg = np.zeros((66, 66), bool); st = [(0, 0)]; bg[0, 0] = True
while st:  # achtergrond vanaf de rand, 4-buur
    y, x = st.pop()
    for v, u in ((y+1, x), (y-1, x), (y, x+1), (y, x-1)):
        if 0 <= v < 66 and 0 <= u < 66 and E[v, u] and not bg[v, u]: bg[v, u] = True; st.append((v, u))
holes = E & ~bg
print(f'componenten: {n} | losse px: {int((S & (dil(S) & ~S | True) & np.array([[S[max(0,y-1):y+2, max(0,x-1):x+2].sum() == 1 for x in range(64)] for y in range(64)])).sum())} | gaten: {int(holes.sum())}')
print('\n     ' + ''.join(str(x // 10) for x in range(64)) + '\n     ' + ''.join(str(x % 10) for x in range(64)))
for y in range(64):
    print(f'y{y:02d}  ' + ''.join('X' if S[y, x] and M[y, x] else '+' if S[y, x] else '-' if M[y, x] else '.' for x in range(64)))
