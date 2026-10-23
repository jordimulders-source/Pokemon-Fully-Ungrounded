"""patch.py basis.txt patches.txt uit.txt
patches.txt: blokken
  @ frame x0 y0
  rijen (teken per pixel; '_' = laten staan, '.' = transparant)
"""
import sys
CH = '.123456789abcdef'


def read_frames(path):
    frames, cur = [], None
    for line in open(path).read().split('\n'):
        if line.startswith('== '):
            cur = []; frames.append(cur); continue
        if cur is not None and len(cur) < 64 and line:
            cur.append(list(line[:64].ljust(64, '.')))
    return frames


base, pf, out = sys.argv[1:4]
fr = read_frames(base)
cur = None
for line in open(pf).read().split('\n'):
    if line.startswith('#') or not line.strip():
        continue
    if line.startswith('='):
        _, dst, src = line.split()
        fr[int(dst) - 1] = [list(r) for r in fr[int(src) - 1]]
        continue
    if line.startswith('!'):
        # ! frame y x tekens  (losse plaatsing; '_' = laten staan)
        _, k, yy, xx, st = line.split()
        for i, ch in enumerate(st):
            if ch != '_':
                assert ch in CH, (line, ch)
                fr[int(k) - 1][int(yy)][int(xx) + i] = ch
        continue
    if line.startswith('@'):
        _, k, x0, y0 = line.split()
        cur = [int(k) - 1, int(x0), int(y0), 0, None]
        continue
    k, x0, y0, j, w = cur
    if w is None:
        cur[4] = w = len(line.rstrip())
    if len(line.rstrip()) != w:
        print('LET OP breedte %d i.p.v. %d: frame %d y %d: %s' % (len(line.rstrip()), w, k + 1, y0 + j, line))
    for i, ch in enumerate(line.rstrip()):
        if ch == '_':
            continue
        assert ch in CH, (line, ch)
        fr[k][y0 + j][x0 + i] = ch
    cur[3] += 1
with open(out, 'w') as f:
    for k, rows in enumerate(fr):
        f.write('== frame %d\n' % (k + 1))
        for r in rows:
            f.write(''.join(r) + '\n')
