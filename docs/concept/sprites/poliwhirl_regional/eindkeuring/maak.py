import numpy as np, sys
from PIL import Image
from lijn import *
im,a=laad(); F=bevroren(a); L=np.load('ylum.npy')
def stap_lijn(a):
    o=a.copy(); n=0
    for x,y,nx,ny,own,m in analyse(a):
        if F[y,x] or not licht(nx,ny): continue
        if own=='Y': o[y,x]=7; n+=1
        elif own=='I': o[y,x]=11; n+=1
    return o
def schaduw(o,var):
    s=o.copy(); Y=np.isin(a,YEL)&~F&(a!=7)
    for y in range(64):
        for x in range(64):
            if not Y[y,x]: continue
            l=L[y,x]
            if np.isnan(l): continue
            if var=='V2':
                s[y,x]=5 if l>=214 else 6 if l>=196 else 7
            elif var=='V1':
                if l<176: s[y,x]=7
    return s
if __name__=='__main__':
    o=stap_lijn(a)
    for v in ('V1','V2'):
        s=schaduw(o,v); np.save(v+'.npy',s)
    np.save('V0.npy',o)
def v3(o):
    """lit/shade uit het model blijven 5/6 zoals r6; binnen de modelschaduwzone (<196) wordt de pixel die aan de
    schaduwkant (rechts, onder, rechtsonder) grenst aan zwart/donker patroon 7: sikkel langs de vorm, geen band."""
    s=o.copy(); Y=np.isin(a,(5,6))&~F
    for y in range(1,63):
        for x in range(1,63):
            if not Y[y,x] or np.isnan(L[y,x]) or L[y,x]>=196: continue
            # rechts: zwarte lijn of donker patroon (schaduwflank); onder/rechtsonder: alleen de zwarte buitenlijn
            # (niet het patroon onder de mond: dat is een kleurgrens, geen vormschaduw -> zou een rechte band geven)
            if o[y,x+1] in (1,2,3) or o[y+1,x]==1 or o[y+1,x+1]==1: s[y,x]=7
    return s
if __name__=='__main__':
    np.save('V3.npy',v3(np.load('V0.npy')))
    # Eindversie: V3 + (20,48): enige zwarte pixel tussen twee 7-lijnpixels op de linkerrand van het linkerbeen
    # (holle knie; normaal-regel gaf 'zwart'), om zwart/donkergeel om-en-om te voorkomen (Gnomad r10-regel).
    ek=np.load('V3.npy'); ek[48,20]=7
    p=Image.fromarray(ek.astype('uint8'),'P'); p.putpalette(im.getpalette()); p.save('poliwhirl_regional_ek.png',transparency=0)
