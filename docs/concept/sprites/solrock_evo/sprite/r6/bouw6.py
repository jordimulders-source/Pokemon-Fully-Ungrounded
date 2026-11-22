# r6: gezichtszone opnieuw uit het natieve raster.
#  vlak : plaattint per spritepixel = meerderheid van de niet-lijn plaatklassen (A/a/b) in de pixel, daarna vlekjes < 3 px weg
#  lijnen: alleen de doorlopende modellijnen (8-componenten op het natieve raster): neuslijn+onderste barsten links (comp rood),
#          barsten rechtsonder (groen), Y-barst midden-boven (blauw); natieve lijnpixel -> spritepixel (skelet, 1 px)
#  rand : zwart alleen waar >=3 van de ±5 natieve pixels zwart zijn (dunne randen blijven dun)
#  ogen : 2x2-blokken uit het natieve raster (lid, contour, iris), fase gekozen per oog; correcties per pixel benoemd
import numpy as np, sys; from scipy import ndimage as nd
from klas import *
sys.path.insert(0,'..'); from npy2png import save
r5=np.load('../r5/sprite.npy'); o=r5.copy()
K=np.load('K.npy'); lab=np.load('lab.npy')
ZX,ZY=(14,37),(21,47)
LIJNCOMP=[int(a) for a in sys.argv[1].split(',')] if len(sys.argv)>1 else [30,37,18,22,24]
cnt={}
for j in range(199):
    for i in range(199):
        x,y=int(sx(i)),int(sy(j))
        if ZX[0]<=x<ZX[1] and ZY[0]<=y<ZY[1]: cnt.setdefault((y,x),[]).append((K[j,i],lab[j,i]))
binnen=lambda x,y:(x+0.5-31.1)**2+(y+0.5-34)**2<16.0**2
PT={'A':13,'a':7,'b':8}
KERNTINT={}
_acc={}
for j in range(199):
    for i in range(199):
        x,y=int(sx(i)),int(sy(j))
        if ZX[0]<=x<ZX[1] and ZY[0]<=y<ZY[1] and K[j,i] in 'gw': _acc.setdefault((y,x),[]).append(N[j,i].mean())
for k,v in _acc.items():
    L=np.mean(v); KERNTINT[k]=2 if L<36 else (3 if L<75 else 4)
for (y,x),lst in cnt.items():
    if not binnen(x,y): continue
    ks=[k for k,_ in lst]
    nk=ks.count('K'); ng=sum(k in 'gw' for k in ks); npl=sum(k in 'aAbcL' for k in ks); nr=sum(k in 'rR' for k in ks)
    if nr>=2: continue                          # ogen komen uit de oogblokken
    if ng>npl and ng>=nk:
        # kern naast de plaat: zwart alleen bij >=3 zwarte natieve pixels, anders kerngrijs naar modelhelderheid
        if not (39<=y<=43 and 15<=x<=22): o[y,x]=r5[y,x] if r5[y,x] in (1,2,3,4) else 3
        elif nk>=3: o[y,x]=1
        else:
            Ls=[N[j,i].mean() for j in range(199) for i in range(199) if False]
            o[y,x]=KERNTINT[(y,x)]
        continue
    if nk>=3: o[y,x]=1; continue
    if npl==0 and nk>0: o[y,x]=1; continue
    pl=[k for k in ks if k in 'Aab']
    if not pl: pl=['b']
    # A alleen bij meerderheid
    t=max(set(pl),key=pl.count)
    o[y,x]=PT[t]
# vlekjes < 3 px in het vlak -> buurtint
def buur(o,j,i,ok):
    v=[o[y,x] for y in range(j-1,j+2) for x in range(i-1,i+2) if (y,x)!=(j,i) and o[y,x] in ok]
    return max(set(v),key=v.count) if v else None
Z=np.zeros((64,64),bool); Z[ZY[0]:ZY[1],ZX[0]:ZX[1]]=True
for _ in range(2):
    for t in (13,7,8):
        l,n=nd.label((o==t)&Z)
        for k in range(1,n+1):
            m=l==k
            if m.sum()<3:
                for j,i in zip(*np.where(m)):
                    b=buur(o,j,i,[v for v in (13,7,8) if v!=t])
                    if b: o[j,i]=b
# lijnen op de skeletpixels
from skimage.morphology import skeletonize
LM=np.isin(lab,LIJNCOMP)
# snoeien tot ±4 doorlopende lijnen (opdracht): zijtak linksonder van de neuslijn (natief x<70, y>100) en de linkertak van de barst rechtsonder (comp 37, x<92) vallen weg
JJ,II=np.mgrid[0:199,0:199]
LM&=~((lab==30)&(II<70)&(JJ>100)); LM&=~((lab==37)&(II<92))
sk=skeletonize(LM)
LIDCOMP=[22,24]; sklid=skeletonize(np.isin(lab,LIDCOMP))           # modelskelet op het natieve raster
sl=np.zeros((64,64),bool)
for j,i in zip(*np.where(sk)): sl[int(sy(j)),int(sx(i))]=True
sl=skeletonize(sl)                               # 1 px op spriteschaal
nl=0
for y,x in zip(*np.where(sl)):
    if o[y,x] in (13,7,8): o[y,x]=9; nl+=1
# ooglidcontour (model: donkerbruin) in P4
for j,i in zip(*np.where(sklid)):
    y,x=int(sy(j)),int(sx(i))
    if o[y,x] in (13,7,8,9): o[y,x]=10
# ogen
from oog2x import red
M={'K':1,'R':12,'r':11,'a':7,'b':8,'c':9,'L':10,'A':13}
OOG={'L':(61,84,8,9,1,1),'R':(84,86,9,10,0,0)}
pos={}
for k,(x0,y0,w,h,fx,fy) in OOG.items():
    b=red(x0+fx,y0+fy,w,h)
    X=int(round(sx(x0+fx+w)-w/2)); Y=int(round(sy(y0+fy+h)-h/2)); pos[k]=(X,Y)
    for j,row in enumerate(b):
        for i,c in enumerate(row):
            if c in 'KRr': o[Y+j,X+i]=M[c]      # alleen lid (zwart) en iris; plaat en lidcontour komen uit vlak/lijnkaart
np.save('basis6.npy',o); print('oogblokken',pos,'lijnpixels gezet',nl)
