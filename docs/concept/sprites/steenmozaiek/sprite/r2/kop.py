# r2 kop (j11-24, i3-24): per cel de meerderheidstint van de vlakpixels van het model (voegpixels tellen niet mee),
# zwart stuk alleen waar >= 2 van de 4 modelpixels bij een zwart stuk horen. Rand = zwarte omlijning (uit r2-basis).
import sys, numpy as np
sys.argv = ['x', '../natief_zonder_wangoog.png', '/dev/null', '0', '0']
src = open('reduceer.py').read().split('# --- reductie')[0]
exec(src)
CHR = {'B0': 'a', 'B1': 'b', 'B2': 'c', 'R0': 'r', 'R1': 'R', 'R2': 'p', 'C0': 'e', 'C1': 'f', 'C2': 'h', 'W': 'w'}
def kopcel(j, i):
    s = (slice(2 * j, 2 * j + 2), slice(2 * i, 2 * i + 2))
    if blk[s].sum() >= 2: return 'x'
    c = [v for v, l in zip(cls[s].ravel(), line[s].ravel() | blk[s].ravel()) if not l and v in CHR]
    if not c: return None
    v, n = np.unique(c, return_counts=True)
    best = n.max(); cand = [x for x, k in zip(v, n) if k == best]
    # gelijkspel: lichtste tint wint (grote lichte vlakken van het model)
    order = ['W', 'C2', 'B2', 'C1', 'R2', 'B1', 'R1', 'C0', 'B0', 'R0']
    return CHR[sorted(cand, key=order.index)[0]]
if __name__ == '__main__':
    rows = [list(l.rstrip('\n')) for l in open(sys.argv_in if False else 'scriptreductie.txt')]
