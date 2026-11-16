# r3 = r2 (bevroren) + vin rechts opnieuw uit het model + 4 losse vulpixels in de mond. Buiten de zones diff 0.
import numpy as np
from zone import *
r2=np.load('r2.npy'); o=r2.copy()
op=r2>0; p=np.pad(op,1); RAND=op&~(p[:-2,1:-1]&p[2:,1:-1]&p[1:-1,:-2]&p[1:-1,2:])
KAND=[c for c in GRP if c!=9]
def dekking(i,j,M):
    tw=0; s=0
    for y,x,w in cellen(i,j,0,0): tw+=w; s+=w*M[y,x]
    return s/tw
# 1. vin rechts (x 51-60, y 36-46): buitenlijn zwart waar het model zwart heeft (>=25% van het blok), binnen: zwart bij >=40% modelzwart, anders mediaan van het modelblok (vlakcellen)
L9=lijnkaart(D9,0,0)   # donkere binnenlijnen (vinstralen) van het model, middelpunt-regel
Zv=np.zeros((64,64),bool); Zv[36:47,51:61]=True; Zv&=op
for j,i in zip(*np.where(Zv)):
    z=dekking(i,j,ZW)
    if RAND[j,i]:
        if z>=0.25: o[j,i]=1
        continue
    if z>=0.4: o[j,i]=1; continue
    if (j,i) in L9: o[j,i]=9; continue
    ST=[RGB[y,x] for y,x,w in cellen(i,j,0,0) if AL[y,x] and not ZW[y,x] and LUM[y,x]<125 and (int((y+0.5-Y0)//F)+17,int((x+0.5-X0)//F)+1)==(j,i)]
    if ST: o[j,i]=9; continue     # vinstreep (donkere modelcel, middelpunt-regel) = binnenlijn in de donkere oudroze tint
    X=[RGB[y,x] for y,x,w in cellen(i,j,0,0) for _ in range(int(round(w*4))) if AL[y,x] and not ZW[y,x] and not D9[y,x]]
    if X: o[j,i]=dichtst(np.median(np.array(X),0),KAND)
# 2. vier losse vulpixels in de mond: kleur van een buurgroep (zwart, 9, lip) die het model daar het meest heeft
Zm=np.zeros((64,64),bool); MAAT={1:ZW,9:D9,5:LIP,7:LIP}
for x,y in [(7,42),(8,43),(16,43),(7,44)]:
    kand={o[y+dy,x+dx] for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))} & set(MAAT)
    sc={c:dekking(x,y,MAAT[c]) for c in kand}; c=max(sc,key=sc.get)
    if c in (5,7):
        X=[RGB[yy,xx] for yy,xx,w in cellen(x,y,0,0) if LIP[yy,xx]]; c=dichtst(np.mean(X,0),[5,7]) if X else c
    print('mondpixel',(x,y),'dekking',{k:round(v,2) for k,v in sc.items()},'->',c); o[y,x]=c; Zm[y,x]=True
np.save('r3.npy',o); opslaan(o,'r3.png')
alle=Zv|Zm
print('vin: gewijzigd',((o!=r2)&Zv).sum(),'van',Zv.sum(),'| mond:',((o!=r2)&Zm).sum())
print('gewijzigd BUITEN de zones:',((o!=r2)&~alle).sum(),'| silhouet gelijk:',((o>0)==(r2>0)).all())
