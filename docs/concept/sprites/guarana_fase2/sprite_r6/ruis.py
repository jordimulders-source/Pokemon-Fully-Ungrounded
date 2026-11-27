# ruis.py SPRITE...: losse pixels (geen 4-buur met dezelfde index) per index, buiten pupil/oogwit, en tintvlakjes < 3 px (vulling)
import sys; sys.path.insert(0,'sprite_r6'); import numpy as np; from PIL import Image; from hulp import *
for f in sys.argv[1:]:
    o=np.array(Image.open(f)).astype(int); los={}; lp=[]
    for y,x in zip(*np.where(o>0)):
        k=o[y,x]
        if k in (1,10,11): continue
        if not any(ok(y+dy,x+dx) and o[y+dy,x+dx]==k for dy,dx in N4):
            los[k]=los.get(k,0)+1; lp.append((x,y,k))
    vul=np.isin(o,[3,4,5,7,8,9,12,13,14,15]); lab,n=label(vul&False)
    klein=0
    for k in (3,4,5,7,8,9,12,13,14,15):
        L,nn=label(o==k); sz=np.bincount(L.ravel())[1:]; klein+=int((sz<3).sum())
    print(f.split('/')[-1],'losse px per index',dict(sorted(los.items())),'totaal',sum(los.values()),' vulvlakjes<3px',klein)
