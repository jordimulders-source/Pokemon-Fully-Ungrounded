# r2 kale reductie. Per spritepixel de dekking per klasse uit het natieve model (klassen2.py). Nieuw t.o.v. r1:
#  - vruchtvlees (rood L>=72) en groen per natieve pixel ingedeeld bij de modeltint (k-means-mediaan, zie gemeen2.py); de spritepixel krijgt de tint
#    met de meeste dekking (geen gemiddelde kleur), rood hooglicht (249,144,112) al bij >= 25 % (glans, zoals fase 1 r3).
#  - vrucht-id per spritepixel: samenhangende stukken vruchtvlees in het natieve model (4-buren) = vruchten; FID = vrucht met de meeste dekking.
#  - LD = dekking door modellijn (zwart + donkerrood L<72) per spritepixel.
import sys, numpy as np; sys.path.insert(0,'sprite_r2')
from klassen2 import klassen; from gemeen2 import *
TK=0.40; TL=0.45; RFT=0.30
a,c,L=klassen(NATIEF)
H,W=c.shape
RT={3:(178,54,47),4:(223,86,59),12:(236,113,79),5:(249,144,112)}
GT={6:(55,87,45),7:(76,115,67),13:(105,148,89),8:(123,167,101)}
def nearest(col,T): return min(T,key=lambda k:sum((np.array(T[k])-col)**2))
T=np.zeros((H,W),int)
for y in range(H):
    for x in range(W):
        if c[y,x]==2 and L[y,x]>=72: T[y,x]=nearest(a[y,x],RT)
        elif c[y,x]==3: T[y,x]=nearest(a[y,x],GT)
# vruchten
VM=(c==2)&(L>=72); VL=np.zeros((H,W),int); n=0
for y,x in zip(*np.where(VM)):
    if VL[y,x]: continue
    n+=1; st=[(y,x)]; VL[y,x]=n
    while st:
        cy,cx=st.pop()
        for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
            yy,xx=cy+dy,cx+dx
            if 0<=yy<H and 0<=xx<W and VM[yy,xx] and not VL[yy,xx]: VL[yy,xx]=n; st.append((yy,xx))
GROOT=set(i for i in range(1,n+1) if (VL==i).sum()>=25)
def reductie():
    o=np.zeros((64,64),int); F={}; FID=np.zeros((64,64),int); LD=np.zeros((64,64))
    for Y in range(64):
        for X in range(64):
            f=np.zeros(5); col=np.zeros((5,3)); t={}; rd=0; fr={}
            for u,v,w in overlap(X,Y):
                k=c[v,u]; f[k]+=w; col[k]+=w*a[v,u]
                if T[v,u]: t[T[v,u]]=t.get(T[v,u],0)+w
                if k==1 or (k==2 and L[v,u]<72): rd+=w
                if VL[v,u] in GROOT: fr[VL[v,u]]=fr.get(VL[v,u],0)+w
            F[(X,Y)]=(f,col); LD[Y,X]=rd
            if fr: FID[Y,X]=max(fr,key=fr.get)
            if f[1:].sum()<0.5: continue
            rt={k:v for k,v in t.items() if k in RT}; rf=sum(rt.values())
            # r2: in de tros wint het vruchtvlees al bij >= RFT dekking (ook als er een modellijn door de pixel loopt): de lijnen
            # tussen de vruchten komen daarna 1 px dik uit de vrucht-id's (bouw.py stap 1b), niet uit elke pixel met wat zwart erin.
            if f[2]>=f[3] and rf>=RFT:
                o[Y,X]=5 if rt.get(5,0)>=0.25*rf else max(rt,key=rt.get); continue
            if f[1]>=TK: o[Y,X]=1; continue
            g=2+int(np.argmax(f[2:]))
            if g==2:
                if f[1]+f[2]-rf>=TL or not rt: o[Y,X]=2
                elif rt.get(5,0)>=0.25*sum(rt.values()): o[Y,X]=5
                else: o[Y,X]=max(rt,key=rt.get)
            elif g==3:
                gt={k:v for k,v in t.items() if k in GT}
                o[Y,X]=max(gt,key=gt.get) if gt else 6
            else: o[Y,X]=10
    return o,F,FID,LD
if __name__=='__main__':
    o,F,FID,LD=reductie(); opslaan(o,'sprite_r2/kaal.png')
    ys,xs=np.where(o>0); print('bbox x',xs.min(),xs.max(),'y',ys.min(),ys.max(),'kleuren',len(set(o.ravel())),'vruchten natief',len(GROOT))
    rgb(o,(255,255,255)).resize((512,512),0).save('sprite_r2/kaal_8x.png')
