# Kale reductie: natief 128x144 -> 55x62 met oppervlakteweging; per spritepixel de meest voorkomende modelklasse
# (lijnklassen K/R0/W0 winnen vanaf 30 % dekking). Palet = mediaan van de modelpixels per klasse. Niets getekend.
import sys, numpy as np
sys.path.insert(0,'gereedschap'); from klassen import klassen, NAMEN; from gemeen import *
a,c,L=klassen()
PAL=[(0,0,0)]*16
for k in range(1,16): PAL[k]=tuple(int(v) for v in np.median(a[c==k],axis=0))
PAL[0]=(152,208,160)

def kaal():
    o=np.zeros((64,64),int); F=np.zeros((64,64,16))
    for Y in range(64):
        for X in range(64):
            for u,v,w in overlap(X,Y): F[Y,X,c[v,u]]+=w
            f=F[Y,X]
            if f.sum()==0 or f[0]>0.5: continue
            if f[1]>=0.3: o[Y,X]=1; continue
            g={'R':f[[2,3,4,5]].sum(),'W':f[[6,7,8,9,10]].sum(),'K':f[[11,12,13,14,15]].sum()}
            G=max(g,key=g.get)
            if G=='R': o[Y,X]=2 if f[2]>=0.3 else 2+int(np.argmax(f[[2,3,4,5]]))
            elif G=='W': o[Y,X]=6 if f[6]>=0.3 else 6+int(np.argmax(f[[6,7,8,9,10]]))
            else: o[Y,X]=11+int(np.argmax(f[[11,12,13,14,15]]))
            if g[G]<f[1]: o[Y,X]=1
    return o,F
if __name__=='__main__':
    o,F=kaal(); opslaan(o,PAL,'r1/kaal.png')
    for k in range(16): print(NAMEN[k],PAL[k],(o==k).sum())
    ys,xs=np.where(o>0); print('bbox',xs.min(),xs.max(),ys.min(),ys.max())
    ch='.K0123abcdeGuomy'
    print('   '+''.join(str(x%10) for x in range(64)))
    for y in range(64): print('%2d '%y+''.join(ch[v] for v in o[y]))
