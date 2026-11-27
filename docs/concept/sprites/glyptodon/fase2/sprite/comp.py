# Natieve compositie (100x100) voor de sprite: model_nat als plaatsing, plaknaden vervangen door scherpe bronpixels.
# Herkomst: 4=r4, 6=r6 (stekel/band/strepen), 3=r3_3 (staart), ?=gevuld in model.png.
# Naad-regel: elke '?'-cel (mediaan-vulling of vlakvulling onder de oude stekel) krijgt de schildpixel uit r6
# (zelfde relatieve rij-afbeelding als de strepen in model_natief.py, anders r6 op de stekelverschuiving -4,-1);
# alleen bruine schildcellen worden overgenomen, lijnen/strepen niet. Getekende schildrand (zwart) blijft zoals model.png.
import sys; sys.path.insert(0,'../gereedschap')
import numpy as np
from kaart import klasse
m=np.load('model_nat.npy').astype(int); H=np.load('herkomst.npy')
r6=np.load('r6_nat.npy').astype(int)
out=m.copy(); bron=H.copy()
def rand(img,y):
    row=[klasse(img[y,x]) for x in range(100)]
    xs=[x for x in range(100) if row[x]!='.']
    if not xs: return None
    l=xs[0]; r=l
    while r+1<100 and row[r+1]!='.': r+=1
    return l,r
DL=np.array([-5,-4,-2])   # r6-bruin iets lichter dan r4-bruin: naar r4 verschuiven
for y in range(100):
    for x in range(100):
        if H[y,x]!='?': continue
        if klasse(m[y,x])=='K' and y<=33: continue   # getekende schildrand bovenop: model
        kand=[]
        e4=rand(m,y); e6=rand(r6,y+1) if y+1<100 else None
        if e4 and e6:
            e6=(e6[0],min(e6[1],76))
            X6=e6[1]-(e4[1]-x) if x>(e4[0]+e4[1])/2 else e6[0]+(x-e4[0])
            if 0<=X6<100: kand.append((r6[y+1,X6],'r'))
        if 0<=y+1<100 and 0<=x+4<100: kand.append((r6[y+1,x+4],'s'))
        for c,k in kand:
            if klasse(c)=='B': out[y,x]=np.clip(c+DL,0,255); bron[y,x]=k; break
        else: bron[y,x]='m'
np.save('comp_nat.npy',out); np.save('comp_bron.npy',bron)
print('naadcellen:',(H=='?').sum(),' r6 relatief:',(bron=='r').sum(),' r6 verschoven:',(bron=='s').sum(),' model gehouden:',(bron=='m').sum())
