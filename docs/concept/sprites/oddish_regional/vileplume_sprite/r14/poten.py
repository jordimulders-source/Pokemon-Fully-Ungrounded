# Poten rij voor rij uit het verkleinde model (r1/kaal.py: dekking per modelklasse per spritepixel).
# Per rij en per poot: pixels met >= 40 % modeldekking (geen achtergrond); minder dan 3 -> aanvullen met de buur met de
# meeste dekking (breedte zoals r12/r13-dun: 3 px, lijn - vulling - lijn). Kleur: buitenste pixels = lijn (zwart of
# W0, wat het model meer heeft; W1 van het model telt als W0, het palet heeft geen W1), binnen = meest voorkomende
# vultint (W1 -> W2). Voetkap: rij waar het model zwart heeft onder de poot.
import sys, numpy as np
sys.path.insert(0,'gereedschap'); sys.path.insert(0,'r1')
from kaal import kaal
k_,F=kaal()
def poot(Y,xa,xb):
    cov=[(1-F[Y,X,0]/max(F[Y,X].sum(),1e-9)) if F[Y,X].sum()>0 else 0 for X in range(64)]
    xs=[X for X in range(xa,xb) if cov[X]>=0.4]
    if not xs: return None
    x0,x1=min(xs),max(xs)
    while x1-x0+1<3:
        if cov[x0-1]>=cov[x1+1]: x0-=1
        else: x1+=1
    return x0,x1
def kleur(Y,X,rand):
    f=F[Y,X]
    if rand:
        a=f[6]+f[7]; return 1 if f[1]>a else 6
    v=[f[8]+f[7],f[9],f[10]]; return 8+int(np.argmax(v))
def rij(Y,xa,xb):
    p=poot(Y,xa,xb)
    if p is None: return None
    x0,x1=p
    return x0,[kleur(Y,X,X in (x0,x1)) for X in range(x0,x1+1)]
if __name__=='__main__':
    ch='.K0123abcdeGuomy'
    for Y in range(42,63):
        print(Y,[ (r[0],''.join(ch[v] for v in r[1])) if r else None for r in (rij(Y,19,31),rij(Y,31,46))])
