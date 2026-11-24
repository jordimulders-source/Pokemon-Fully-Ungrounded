# Rechtervoet kleiner (Jordi: "akkoord, maar doe het netjes en houd de vorm hetzelfde"):
# binnenrijen van de voet schrappen (x >= 32, onder het lijf), de rest schuift omhoog.
# Niets getekend; alleen rijen weggehaald, zoals het schrappen eerder.
from PIL import Image
import numpy as np
src = Image.open('r2/claydol_eind_r2.png')
pal = src.getpalette(); A = np.array(src)
def schrap(rijen, x0=32, x1=46):
    B = A.copy()
    reg = A[:, x0:x1].copy()
    keep = [y for y in range(64) if y not in rijen]
    sub = reg[keep]
    new = np.zeros_like(reg); new[:len(sub)] = sub
    # alleen onder rij min(rijen) verandert iets
    y0 = min(rijen)
    B[y0:, x0:x1] = new[y0:]
    return B
for naam, rijen in [('1rij', [57]), ('2rijen', [56, 57])]:
    B = schrap(rijen)
    assert (B[:56] == A[:56]).all() or naam == '2rijen'
    assert (B[:, :32] == A[:, :32]).all()
    m = B > 0; seen = np.zeros_like(m); n = 0
    for y0_ in range(64):
        for x0_ in range(64):
            if m[y0_, x0_] and not seen[y0_, x0_]:
                n += 1; st = [(y0_, x0_)]; seen[y0_, x0_] = True
                while st:
                    yy, xx = st.pop()
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            Y, X = yy+dy, xx+dx
                            if 0 <= Y < 64 and 0 <= X < 64 and m[Y, X] and not seen[Y, X]:
                                seen[Y, X] = True; st.append((Y, X))
    print(naam, 'componenten', n, 'gewijzigd', int((B != A).sum()))
    im = Image.fromarray(B.astype(np.uint8), 'P'); im.putpalette(pal)
    im.save(f'r3/claydol_eind_r3_{naam}.png', transparency=0)
    im.convert('RGB').resize((512, 512), Image.NEAREST)
