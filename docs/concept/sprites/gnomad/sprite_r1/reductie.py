# reductie.py: natief model -> kaal.png (kale reductie: vlakgemiddelde + dichtstbijzijnde paletkleur)
# en red.png (technische onderlaag: zone per meerderheid, vlaktint = meerderheidstoon van de modelvlakpixels, lijnen 1 px volgens regels), zone.npy, lijn.npy
import numpy as np; from PIL import Image
from gemeen import *
a=np.asarray(Image.open('natief.png')).astype(float)
fam=np.load('natief_fam.npy'); z=np.load('natief_zone.npy')
lijn=fam==1
def bron(X,Y):
    ua=CXN+(X-CXS)/S; ub=ua+1/S; va=BOTN-(BOTS-Y)/S; vb=va+1/S
    for v in range(int(np.floor(va)),int(np.ceil(vb))):
        for u in range(int(np.floor(ua)),int(np.ceil(ub))):
            w=max(0,min(ub,u+1)-max(ua,u))*max(0,min(vb,v+1)-max(va,v))
            if w>1e-9 and 0<=u<100 and 0<=v<100: yield u,v,w
P=np.array(PAL,float)
kaal=np.zeros((64,64),int); zone=np.zeros((64,64),int); kl=np.zeros((64,64)); o=np.zeros((64,64),int); donk=np.full((64,64),999.)
for Y in range(64):
    for X in range(64):
        acc=np.zeros(3); tw=0; fgw=0; cov={}; lw=0; tone={}
        for u,v,w in bron(X,Y):
            acc+=w*a[v,u]; tw+=w
            if z[v,u]:
                fgw+=w; cov[z[v,u]]=cov.get(z[v,u],0)+w
                if lijn[v,u]:
                    lw+=w
                    if w>0.2: donk[Y,X]=min(donk[Y,X],a[v,u].mean())
        if tw==0 or fgw/tw<0.5: continue
        m=acc/tw; kaal[Y,X]=1+np.argmin(((P[1:]-m)**2).sum(1))
        zz=max(cov,key=cov.get); zone[Y,X]=zz; kl[Y,X]=lw/tw
        # meerderheidstoon: elke vlakpixel van deze zone stemt op de dichtstbijzijnde zonetint
        for u,v,w in bron(X,Y):
            if z[v,u]==zz and not lijn[v,u]:
                k=min(FAMZ[zz],key=lambda k:((P[k]-a[v,u])**2).sum()); tone[k]=tone.get(k,0)+w
        if tone: o[Y,X]=max(tone,key=tone.get)
        else: o[Y,X]=min(FAMZ[zz],key=lambda k:((P[k]-m)**2).sum())
opslaan(kaal,'kaal.png')
fg=zone>0; rank={p:i for i,p in enumerate(PRIO)}
L=np.zeros((64,64),bool)
for Y,X in zip(*np.where(fg)):
    nb=[(Y+dy,X+dx) for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))]
    if any(not fg[y,x] for y,x in nb): L[Y,X]=True; continue
    # voorste onderdeel krijgt de lijn op zijn rand tegen een achterliggend onderdeel (broek/lijf: geen lijn, alleen kleurgrens)
    if any(zone[y,x]!=zone[Y,X] and rank[zone[y,x]]>rank[zone[Y,X]] and not {zone[y,x],zone[Y,X]}<= {5,8} for y,x in nb): L[Y,X]=True
OUT=L.copy()
# vouwlijnen binnen onderdelen waar de modellijn >= 40% dekt
VOUW=(fg&~L&(kl>=0.40))
L|=VOUW
for Y,X in zip(*np.where(L)):
    o[Y,X]=1 if donk[Y,X]<70 or OUT[Y,X] else FAMZ[zone[Y,X]][0]
np.save('zone.npy',zone); np.save('lijn.npy',L); np.save('lijnkans.npy',kl)
opslaan(o,'red.png')
yy,xx=np.where(fg); print('figuur x%d-%d y%d-%d (%dx%d)'%(xx.min(),xx.max(),yy.min(),yy.max(),xx.max()-xx.min()+1,yy.max()-yy.min()+1))
CH='.#abcdRST123CDbr'
for Y in range(yy.min(),yy.max()+1): print('%2d '%Y+''.join(CH[v] for v in o[Y,xx.min()-1:xx.max()+2]))
