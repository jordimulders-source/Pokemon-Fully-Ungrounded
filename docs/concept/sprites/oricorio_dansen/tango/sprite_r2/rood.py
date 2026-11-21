# Rood accent (Jordi: "het rood accent kunnen we in de sprite verwerken"; plek niet gekozen -> 3 varianten, zelfde pixelwerk behalve het rood).
# Rood komt alleen op bestaande vlakken/lijnen; geen nieuwe vormen.
import numpy as np; from lib import I
R,R2=12,13
def varianten():
    o=np.load('tango_kls.npy')
    out={}
    # A: binnenkant van de split (de D1-vulling tussen de jurkranden waar de dij zat)
    a=o.copy(); split=np.load('split_mask.npy')
    a[split&(a==I['D1'])]=R
    out['A']=a
    # B: franjezoom: vulling van de franjestrengen onderaan de jurk (rij >= 44 in werkcoördinaten), donkerste tint -> R2
    b=o.copy(); m=np.zeros_like(o,bool); m[44:,:]=True
    b[m&(b==I['D1'])]=R2; b[m&np.isin(b,[I['D2'],I['D3'],I['D4'],I['D5']])]=R
    out['B']=b
    # C: smal accent bij de knot: de binnenlijn tussen kop en knot (modellijn) -> R
    c=o.copy(); knot=np.load('knot_mask.npy'); c[knot]=R
    out['C']=c
    return out
