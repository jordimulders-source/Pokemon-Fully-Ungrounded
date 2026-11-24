# reductie.py A|B : natief (A) of natief met ronder lijf (B) -> sprite-onderlaag.
# Schrijft kaal_X.png (kale reductie: vlakgemiddelde + dichtstbijzijnde modelkleur), red_X.png (zones + lijnen technisch), zone_X.npy
import sys, numpy as np; from PIL import Image
from gemeen import *
var=sys.argv[1]
a,z,lijn=natief()
if var=='B':
    # Ronder lijf: K kolommen invoegen in het lijf rechts van de neus (kolom KX), alleen in de laag zonder muts, rijen >= 47.
    # Alles rechts van KX (lijfhelft, arm R, voet R) schuift onvervormd K naar rechts; muts, neus, arm L en voet L blijven staan.
    K=int(sys.argv[2]) if len(sys.argv)>2 else 4; KX=53
    a2=np.full_like(a,255.); z2=np.zeros_like(z); l2=np.zeros_like(lijn)
    for y in range(100):
        for x in range(100):
            if z[y,x]==1 or y<47: a2[y,x]=a[y,x]; z2[y,x]=z[y,x]; l2[y,x]=lijn[y,x]
    for y in range(47,100):
        for x in range(99,-1,-1):
            if z[y,x] in (0,1): continue
            if x>KX: nx=x+K
            else: nx=x
            if z2[y,nx]!=1: a2[y,nx]=a[y,x]; z2[y,nx]=z[y,x]; l2[y,nx]=lijn[y,x]
        # gat opvullen met kolom KX (lijf), alleen als links en rechts lijf ligt
        if z[y,KX]==3:
            for nx in range(KX+1,KX+K+1):
                if z2[y,nx]!=1: a2[y,nx]=a[y,KX]; z2[y,nx]=3; l2[y,nx]=lijn[y,KX]
    a,z,lijn=a2,z2,l2
    print('B: K',K,'kolommen ingevoegd bij natief x',KX)
    Image.fromarray(a.astype('uint8')).resize((800,800),Image.NEAREST).save('natief_B_8x.png')
np.save('natief_zone_%s.npy'%var,z)
# overlap natief -> sprite
def bron(X,Y):
    ua=CXN+(X-CXS)/S; ub=ua+1/S; va=BOTN-(BOTS-Y)/S; vb=va+1/S
    for v in range(int(np.floor(va)),int(np.ceil(vb))):
        for u in range(int(np.floor(ua)),int(np.ceil(ub))):
            w=max(0,min(ub,u+1)-max(ua,u))*max(0,min(vb,v+1)-max(va,v))
            if w>1e-9 and 0<=u<100 and 0<=v<100: yield u,v,w
P=np.array(PAL,float)
kaal=np.zeros((64,64),int); zone=np.zeros((64,64),int); kl=np.zeros((64,64)); vul=np.full((64,64,3),-1.); donk=np.zeros((64,64,3))
for Y in range(64):
    for X in range(64):
        cov={}; acc=np.zeros(3); tw=0; fgw=0; accv={}; twv={}; lw=0
        for u,v,w in bron(X,Y):
            acc+=w*a[v,u]; tw+=w
            if z[v,u] and (w>0.25) and a[v,u].mean()<donk[Y,X].mean()+(999 if not donk[Y,X].any() else 0): donk[Y,X]=a[v,u]
            if z[v,u]:
                fgw+=w; cov[z[v,u]]=cov.get(z[v,u],0)+w
                if lijn[v,u]: lw+=w
                else: accv[z[v,u]]=accv.get(z[v,u],0)+w*a[v,u]; twv[z[v,u]]=twv.get(z[v,u],0)+w
        if fgw/tw>=0.5:
            m=acc/tw; kaal[Y,X]=1+np.argmin(((P[1:14]-m)**2).sum(1))
            zz=max(cov,key=cov.get); zone[Y,X]=zz; kl[Y,X]=lw/tw
            if zz in twv: vul[Y,X]=accv[zz]/twv[zz]
opslaan(kaal,'kaal_%s.png'%var)
# technische onderlaag: vlakkleur per zone (dichtstbijzijnde zonetint), lijnen volgens regels
o=np.zeros((64,64),int)
for Y,X in zip(*np.where(zone>0)):
    zz=zone[Y,X]; fam=FAM[zz]
    if zz==3: fam=[6,7,8,9] if Y< 47 else [10,11,12]  # lijf: roze boven, blauw onder (grens volgt het model hieronder)
    m=vul[Y,X] if vul[Y,X,0]>=0 else P[kaal[Y,X]]
    if zz==3: fam=[6,7,8,9,10,11,12]
    o[Y,X]=min(fam,key=lambda k:((P[k]-m)**2).sum())
fg=zone>0
def buur4(Y,X): return [(Y+dy,X+dx) for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))]
rank={p:i for i,p in enumerate(PRIO)}
L=np.zeros((64,64),bool)
for Y,X in zip(*np.where(fg)):
    nb=buur4(Y,X)
    if any(not fg[y,x] for y,x in nb): L[Y,X]=True; continue
    # voorste zone krijgt de lijn op haar rand tegen een achterliggende zone
    if any(zone[y,x]!=zone[Y,X] and rank[zone[y,x]]>rank[zone[Y,X]] for y,x in nb): L[Y,X]=True
np.save('zone_%s.npy'%var,zone); np.save('lijnkans_%s.npy'%var,kl); np.save('lijn_%s.npy'%var,L)
# vouwlijnen binnen de muts (modellijn dekt >= 35%)
for Y,X in zip(*np.where((zone==1)&~L&(kl>=0.35))): L[Y,X]=True
# lijnkleur uit het model: donkerste modelpixel in de voetafdruk; bijna zwart -> zwart, anders donkerste zonetint die erop lijkt
for Y,X in zip(*np.where(L)):
    d=donk[Y,X]
    if d.mean()<60: o[Y,X]=1
    else:
        fam=FAM[zone[Y,X]] if zone[Y,X]!=3 else [6,7,10,11]
        o[Y,X]=min(fam,key=lambda k:((P[k]-d)**2).sum())
opslaan(o,'red_%s.png'%var)
yy,xx=np.where(fg); print(var,'figuur x%d-%d y%d-%d (%dx%d)'%(xx.min(),xx.max(),yy.min(),yy.max(),xx.max()-xx.min()+1,yy.max()-yy.min()+1))
CH='.#abcdABCDefgh+'
for Y in range(yy.min(),yy.max()+1): print('%2d '%Y+''.join(CH[v] for v in o[Y,xx.min()-1:xx.max()+2]))
