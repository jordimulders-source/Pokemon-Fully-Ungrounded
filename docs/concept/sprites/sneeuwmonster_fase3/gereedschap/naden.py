# Duignaden in de emmer meten (natief): houtcellen >=18 donkerder dan het lokale houtgemiddelde (5x5 cellen, ~2 spritepx).
# naad_kaart() -> per spritepixel het aandeel naadcellen en het houtaandeel.
import os, sys, numpy as np
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from gemeen import *; from klassen import klassen
def naad_kaart():
    a,c,L=klassen(); hout=(c==3)
    def box(v,r=2):
        p=np.pad(v.astype(float),r); out=np.zeros(v.shape)
        for dy in range(2*r+1):
            for dx in range(2*r+1): out+=p[dy:dy+v.shape[0],dx:dx+v.shape[1]]
        return out
    mean=box(np.where(hout,L,0))/np.maximum(box(hout),1e-6)
    naad=hout&(L<mean-18)
    idx=spriteindex(); ok=idx>=0; I=idx[ok]; n=np.maximum(np.bincount(I,minlength=4096),1)
    nf=(np.bincount(I,up(naad)[ok].astype(float),minlength=4096)/n).reshape(64,64)
    hf=(np.bincount(I,up(hout)[ok].astype(float),minlength=4096)/n).reshape(64,64)
    return nf,hf
if __name__=='__main__':
    n,h=naad_kaart()
    print('    '+''.join('%-3d'%x for x in range(25,45)))
    for Y in range(11,21): print('%2d  '%Y+''.join(' . ' if h[Y,X]<0.3 else '%2d '%min(99,int(n[Y,X]*100)) for X in range(25,45)))
