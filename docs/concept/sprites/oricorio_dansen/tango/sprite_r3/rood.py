# Rood accent (Jordi: "het rood accent kunnen we in de sprite verwerken"; plek niet gekozen -> 3 varianten, zelfde pixelwerk behalve het rood).
# Rood komt alleen op bestaande vlakken/lijnen; geen nieuwe vormen.
import numpy as np; from lib import I
R,R2=12,13
# bovenrand van het rood per kolom (werkcoördinaten): golvend, zoals een vallende zoom; links en rechts verschillend
TOP={12:45,13:44,14:44,15:43,16:43,17:44,18:45,19:45,20:44,21:43,22:43,23:44,24:45,25:46,
     28:45,29:44,30:43,31:43,32:44,33:45,34:45,35:44,36:45,37:46,38:46}
from lib import comps
def varianten():
    # r3: alleen B (Jordi: "kleur 2"). Rood = vulling van de franje onder een golvende bovenrand (Jordi: "de franje aan de bovenkant niet 1 rechte lijn").
    o=np.load('tango_kls.npy'); b=o.copy(); poot=np.load('poot_mask.npy')
    VUL=[I['D2'],I['D3'],I['D4'],I['D5']]
    for x,t in TOP.items():
        for y in range(t,o.shape[0]):
            if poot[y,x]: continue
            if o[y,x]==I['D1']: b[y,x]=R2
            elif o[y,x] in VUL: b[y,x]=R
    # netheid: losse rode pixel -> terug; losse zwarte vulpixel tussen rood -> rood
    for pts in comps(np.isin(b,[R,R2])):
        if len(pts)<2:
            for p in pts: b[p]=o[p]
    for pts in comps(np.isin(b,VUL+[I['D1']])&(np.arange(b.shape[0])[:,None]>=43)):
        if len(pts)<2:
            y,x=pts[0]
            if any(b[y+dy,x+dx] in (R,R2) for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))): b[y,x]=R2 if o[y,x]==I['D1'] else R
    return {'B':b}
