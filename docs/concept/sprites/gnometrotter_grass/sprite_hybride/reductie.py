# reductie.py: model Grass r4 -> kaal.png (kale reductie, gedeelde geometrie, vlakgemiddelde -> dichtstbijzijnde paletkleur)
# en red.png (technische onderlaag): onderdeel per meerderheid, vlaktint = meerderheidsstem (op helderheid) van de modelvlakpixels,
# buitenlijn 1 px, binnenlijn op de rand van het voorste onderdeel, modelnaden waar de modellijn >= 40 % dekt.
import numpy as np; from PIL import Image
from gemeen import *
from reductie_gedeeld import bron, reduceer, DREMPEL
a=np.asarray(Image.open('../hybride/model_hybride.png').convert('RGB')).astype(float)
f=np.load('model_fam.npz')['f'].astype(int); Z=np.load('model_zone.npz')['z'].astype(int); LUM=0.30*a[...,0]+0.59*a[...,1]+0.11*a[...,2]
gem,dek=reduceer(a)
P=np.array(PAL,float); kaal=np.zeros((64,64),int)
for Y,X in zip(*np.where(dek>=DREMPEL)): kaal[Y,X]=1+np.argmin(((P[1:]-gem[Y,X])**2).sum(1))
opslaan(kaal,'kaal.png')
zone=np.zeros((64,64),int); kl=np.zeros((64,64)); o=np.zeros((64,64),int); oog=np.zeros((64,64),bool)
for Y in range(64):
    for X in range(64):
        tw=0; cov={}; lw=0; ow=0; st=[]
        for u,v,w in bron(X,Y):
            tw+=w
            if f[v,u]:
                cov[Z[v,u]]=cov.get(Z[v,u],0)+w
                if f[v,u]==1:
                    lw+=w
                    if 440<=u<=515 and 160<=v<=200: ow+=w        # donkere strook onder de muts (leest als ogen)
                else: st.append((u,v,w))
        if not cov: continue
        zz=max(cov,key=cov.get); vg=sum(cov.values())/tw
        drempel=0.35 if zz in (11,16) or (zz==15 and X>=51) else DREMPEL   # stok, twijg en twijgblaadjes: dunne delen, anders breken ze (zelfde regel als Rocks stok)
        if vg<drempel: continue
        zone[Y,X]=zz; kl[Y,X]=lw/tw; oog[Y,X]=ow/tw>=0.4
        tone={}
        for u,v,w in st:
            if Z[v,u]!=zz: continue
            k=min(RAMP[zz],key=lambda k:abs(lum(PAL[k])-LUM[v,u])); tone[k]=tone.get(k,0)+w
        o[Y,X]=max(tone,key=tone.get) if tone else RAMP[zz][0]
fg=zone>0; rank={p:i for i,p in enumerate(PRIO)}
OUT=np.zeros((64,64),bool); BIN=np.zeros((64,64),bool)
for Y,X in zip(*np.where(fg)):
    nb=[(Y+dy,X+dx) for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))]
    if any(not(0<=y<64 and 0<=x<64) or not fg[y,x] for y,x in nb): OUT[Y,X]=True; continue
    if any(zone[y,x]!=zone[Y,X] and rank[zone[y,x]]>rank[zone[Y,X]] for y,x in nb): BIN[Y,X]=True
NAAD=fg&~OUT&~BIN&(kl>=0.40)
np.save('zone.npy',zone); np.save('lijnkans.npy',kl); np.save('oog.npy',oog)
np.save('out.npy',OUT); np.save('bin.npy',BIN); np.save('naad.npy',NAAD); np.save('vlak.npy',o)
yy,xx=np.where(fg); print('figuur x%d-%d y%d-%d, %d px; kaal %d px; oogstrook %d px'%(xx.min(),xx.max(),yy.min(),yy.max(),fg.sum(),(kaal>0).sum(),oog.sum()))
