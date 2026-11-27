# Ronde 1: kale reductie (basis.py) + technische opschoning
#  a) lijnen: rug-detectie op de lijnfractie (1 px dik, zoals de 1-natieve-px-lijn van het model)
#  b) buitenlijn gesloten
import numpy as np
from basis import basis,png,PAL,RAMP
I,MAT,INFO=basis(TH=2.0)   # eerst zonder lijnen: materiaalkleur overal
kf=np.zeros((64,64)); al=np.zeros((64,64))
for (y,x),(a,w) in INFO.items(): kf[y,x]=w.get('K',0); al[y,x]=a
op=I>0
P=np.pad(kf,1)
rugx=(kf>=P[1:-1,:-2])&(kf>=P[1:-1,2:])
rugy=(kf>=P[:-2,1:-1])&(kf>=P[2:,1:-1])
lijn=op&((kf>=0.55)|((kf>=0.25)&(rugx|rugy)))
I[lijn]=1
np.save('r1a_I.npy',I); np.save('r1a_kf.npy',kf)
png(I,'r1a.png'); png(I,'r1a_8x.png',8)
# b) buitenlijn: elke ondoorzichtige pixel die (4-buren) aan transparant grenst wordt lijn,
#    behalve de linkerrand van de stekel (olijf-selout uit r6, index 2 blijft)
op=I>0; P=np.pad(op,1)
rand=op&~(P[:-2,1:-1]&P[2:,1:-1]&P[1:-1,:-2]&P[1:-1,2:])
stekel_links=np.zeros_like(op); stekel_links[5:20,10:16]=True
for y,x in zip(*np.where(rand)):
    if stekel_links[y,x] and MAT[y,x]=='S': I[y,x]=2; continue
    I[y,x]=1
np.save('r1b_I.npy',I); png(I,'r1b.png'); png(I,'r1b_8x.png',8)
# c) benoemde reparaties (elk gemeten op comp_nat)
fix={}
fix[(16,21)]=1      # stekelvoetlijn doorlopend: kfrac 0,44, natief (27,28) zwart
# oog (natief r56-58, x21-25): (24-25,56-57) donker/licht oranje, (21-24,58) oranje
fix[(14,41)]=14; fix[(12,42)]=14; fix[(13,42)]=15; fix[(14,42)]=15
fix[(15,42)]=11     # natief (25,58)=(92,63,61),(26,58)=grijs 64: geen oranje
fix[(55,33)]=13     # staartpunt is grijs steen (r3_3), niet beige
for k,v in fix.items(): I[k[1],k[0]]=v
# d) losse lijnpixels binnen een vlak (geen enkele lijnbuur in 8 richtingen) -> kleur van het materiaal
op=I>0
los=[]
for y in range(1,63):
    for x in range(1,63):
        if I[y,x]==1 and op[y-1:y+2,x-1:x+2].all() and (I[y-1:y+2,x-1:x+2]==1).sum()==1:
            nb=[I[y+dy,x+dx] for dy,dx in ((0,1),(0,-1),(1,0),(-1,0)) if I[y+dy,x+dx]>1]
            v=max(set(nb),key=nb.count); I[y,x]=v; los.append((x,y,v))
print('losse lijnpixels:',los)
# e) selout: buitenlijn van de schildkoepel aan de lichtkant (linksboven) donkerste schildbruin i.p.v. zwart
sel=[]
for y in range(17,36):
    for x in range(0,32):
        if I[y,x]!=1: continue
        boven=y==0 or I[y-1,x]==0; links=x==0 or I[y,x-1]==0
        binnen=[I[y+1,x], I[y,x+1]]
        if (boven or links) and any(v in (6,7) for v in binnen) and not (I[y+1,x]==1 and I[y,x+1]==1):
            I[y,x]=5; sel.append((x,y))
print('selout:',sel)
np.save('r1_I.npy',I); png(I,'r1.png'); png(I,'r1_8x.png',8)
# f) binnenlijnen: zwarte lijnpixel binnen het silhouet met aan alle kanten hetzelfde materiaal = textuurlijn
#    -> donkerste eigen tint (grijs 10, schild/staart 5). Lijnen tussen twee materialen (schildrand over lijf, oog) blijven zwart.
DONKER={'G':10,'T':5}
op=I>0; P=np.pad(op,1)
binnen=op&(P[:-2,1:-1]&P[2:,1:-1]&P[1:-1,:-2]&P[1:-1,2:])
nieuw=I.copy(); tex=[]
for y,x in zip(*np.where(binnen&(I==1))):
    g={MAT[yy,xx] for yy in range(y-1,y+2) for xx in range(x-1,x+2) if I[yy,xx]>1}
    if len(g)==1 and list(g)[0] in DONKER:
        nieuw[y,x]=DONKER[list(g)[0]]; tex.append((x,y))
I=nieuw
print('textuurlijnen naar eigen tint:',len(tex))
np.save('r1_I.npy',I); png(I,'r1.png'); png(I,'r1_8x.png',8)
