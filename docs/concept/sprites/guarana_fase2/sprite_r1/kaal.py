# Kale reductie: per spritepixel de dekking per klasse uit het natieve model; zwart bij >=TK, anders de klasse met de meeste dekking,
# tint = dichtstbijzijnde palettint (binnen die klasse) bij de gemiddelde modelkleur van die klasse onder de pixel. Niets getekend.
import sys, numpy as np; sys.path.insert(0,'sprite_r1')
from klassen2 import klassen; from gemeen2 import *
TK=0.40
a,c,L=klassen(NATIEF)
def tint(cls,col):
    opts={2:ROOD,3:GROEN,4:WIT}[cls]
    return min(opts,key=lambda k:sum((np.array(PAL[k])-col)**2))
# r1b: donkerrood (L<72) in de tros = de modellijnen tussen de vruchten (zoals fase 1 r2); die tellen niet mee in de vultint.
# Pixel met veel zwart+donkerrood (>= TL) en rood als hoofdklasse -> lijnrood 2. Vultint rood uit het aandeel licht/schaduw in het vruchtvlees
# (fase 1 r3: L>=140 licht bij >=30 %, L<100 schaduw bij >=50 %), groen = dichtstbijzijnde groentint bij de gemiddelde groene modelkleur.
TL=0.45
def reductie():
    o=np.zeros((64,64),int); F={}
    for Y in range(64):
        for X in range(64):
            f=np.zeros(5); col=np.zeros((5,3)); rd=0; rf=0; rli=0; rsh=0
            for u,v,w in overlap(X,Y):
                k=c[v,u]; f[k]+=w; col[k]+=w*a[v,u]
                if k==2:
                    if L[v,u]<72: rd+=w
                    else:
                        rf+=w
                        if L[v,u]>=140: rli+=w
                        if L[v,u]<100: rsh+=w
            F[(X,Y)]=(f,col)
            if f[1:].sum()<0.5: continue
            if f[1]>=TK: o[Y,X]=1; continue
            g=2+int(np.argmax(f[2:]))
            if g==2:
                if f[1]+rd>=TL or rf==0: o[Y,X]=2
                else: o[Y,X]=5 if rli/rf>=0.30 else 3 if rsh/rf>=0.50 else 4
            else: o[Y,X]=tint(g,col[g]/f[g])
    return o,F
if __name__=='__main__':
    o,F=reductie(); opslaan(o,'sprite_r1/kaal.png')
    ys,xs=np.where(o>0); print('bbox x',xs.min(),xs.max(),'y',ys.min(),ys.max(), 'kleuren',len(set(o.ravel())))
    rgb(o,(255,255,255)).resize((512,512),0).save('sprite_r1/kaal_8x.png')
