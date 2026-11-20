# Gloom r1: model overnemen. Natief raster (149x149, pitch 6,83; figuur 106x102) -> schaal 42/102 (0,412), y11-52, x9-52.
# Verkleinen = oppervlakteweging per spritepixel; gloed wint waar het model een kier/kwijl heeft; daarna alleen technische opschoning, elke stap geteld.
import sys, numpy as np
sys.path.insert(0,'gereedschap'); from klassen import klassen; from gemeen import *
a,c,L=klassen()
TG=float(sys.argv[1]) if len(sys.argv)>1 else 0.25; TK=float(sys.argv[2]) if len(sys.argv)>2 else 0.30
UIT=sys.argv[3] if len(sys.argv)>3 else 'r1'
def toonvan(grp,l,f):
    if grp==2: return 2 if l<52 else 3 if l<88 else 4
    if grp==3: return 5 if l<52 else 6 if l<88 else (8 if f>=0.35 else 7)
    if grp==4: return 9 if l<128 else 10 if l<162 else 11
    if grp==5: return 12 if l<88 else 13 if l<126 else 14
# --- 1. kale reductie ---
o=np.zeros((64,64),int)
for Y in range(0,64):
    for X in range(0,64):
        f=np.zeros(6); lum=np.zeros(6); licht=0
        for u,v,w in overlap(X,Y):
            k=c[v,u]; f[k]+=w; lum[k]+=w*L[v,u]
            if k==3 and L[v,u]>=112: licht+=w
        if f.sum()==0 or f[0]>0.5: continue
        if f[4]>=TG: o[Y,X]=toonvan(4,lum[4]/f[4],0); continue      # gloed wint
        if f[1]>=TK: o[Y,X]=1; continue
        g=2+int(np.argmax(f[2:])); o[Y,X]=toonvan(g,lum[g]/f[g],licht/max(f[3],1e-9))
kaal=o.copy(); opslaan(kaal,UIT+'/kaal.png')
toon(kaal)
print('kleuren',sorted(set(o.ravel())), 'px',(o>0).sum())
