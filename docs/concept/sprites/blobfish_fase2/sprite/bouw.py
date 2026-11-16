# r1: kale reductie (kaal.npy) -> technisch opschonen. Niets getekend: alleen
#  (1) buitenlijn 1 px: randpixels worden zwart (schaduwkant) of selout = donkerste tint van hun eigen kleurgroep (lichtkant, licht linksboven)
#  (2) ruis: tintvlakjes < 3 px nemen de meest voorkomende buurtint uit dezelfde kleurgroep (glans en zwart uitgezonderd)
import json, sys; import numpy as np; from PIL import Image
o=np.load('kaal.npy').copy(); P=json.load(open('kaal_palet.json')); cols=P['cols']; grp={int(k):v for k,v in P['grp'].items()}
G=np.full(len(cols),-1); [G.__setitem__(v,g) for g,vs in grp.items() for v in vs]
SEL={0:9,1:12,2:15}                     # selout per groep = donkerste paletkleur van die groep (uit het model)
DREMPEL=float(sys.argv[1]) if len(sys.argv)>1 else 0.3
kaal=o.copy(); op=o>0
# (1) buitenlijn
p=np.pad(op,1); rand=op&~(p[:-2,1:-1]&p[2:,1:-1]&p[1:-1,:-2]&p[1:-1,2:])
af=np.pad(op.astype(float),3); k=np.ones((7,7))
def gem(a):
    s=np.zeros((64,64))
    for dy in range(7):
        for dx in range(7): s+=a[dy:dy+64,dx:dx+64]
    return s/49
# normaal naar buiten = -gradiënt van de vervaagde dekking
f=gem(af); fp=np.pad(f,1,mode='edge'); gx=(fp[1:-1,2:]-fp[1:-1,:-2]); gy=(fp[2:,1:-1]-fp[:-2,1:-1])
nx,ny=-gx,-gy; nn=np.hypot(nx,ny)+1e-9; ux,uy=nx/nn,ny/nn; licht=np.where((uy<-0.4)&(ux<0.75),1.0,-ux)   # >drempel = rand kijkt naar boven (niet sterk rechts) of naar links (licht linksboven)
for y,x in zip(*np.where(rand)):
    g=G[o[y,x]] if o[y,x]>1 else None
    if g is None:   # was al zwart: groep van de buren
        b=[G[o[yy,xx]] for yy,xx in ((y-1,x),(y+1,x),(y,x-1),(y,x+1),(y-1,x-1),(y+1,x+1),(y-1,x+1),(y+1,x-1)) if 0<=yy<64 and 0<=xx<64 and o[yy,xx]>1]
        g=max(set(b),key=b.count) if b else 0
    o[y,x]=SEL[g] if licht[y,x]>DREMPEL else 1
# (1b) binnenlijnen pixel-perfect: een hoekpixel (lijnburen links/rechts én boven/onder, diagonaal ertussen geen lijn) valt weg -> vulkleur van de kale reductie
C=np.load('kaal_rgb.npy'); Pc=np.array(cols,float)
def feat(X): return np.c_[X@[.299,.587,.114], 2.0*(X[:,0]-X[:,1]), 2.0*(X[:,2]-X[:,1])]
LB=np.load('label.npy')
def vul(y,x):
    ix=grp[LB[y-17,x-1]]; return ix[int(np.argmin(((feat(Pc[ix])-feat(C[y-17,x-1][None]))**2).sum(1)))]
nh=0
for lijn in (1,9):
    for _ in range(3):
        L=(o==lijn)
        for y,x in zip(*np.where(L&~rand)):
            if not L[y,x]: continue
            for dy in (-1,1):
                for dx in (-1,1):
                    if L[y+dy,x] and L[y,x+dx] and not L[y+dy,x+dx] and L[y,x]:
                        L[y,x]=False; o[y,x]=vul(y,x); nh+=1
print('hoekpixels weg',nh)
# (2) ruis
def ruis(o):
    n=0
    for c in range(2,len(cols)):
        if c in (2,9): continue                          # glans mag klein; 9 = donkere binnenlijn uit het model
        m=o==c; seen=np.zeros_like(m)
        for y,x in zip(*np.where(m)):
            if seen[y,x]: continue
            st=[(y,x)]; cl=[]; seen[y,x]=1
            while st:
                a,b=st.pop(); cl.append((a,b))
                for aa,bb in ((a-1,b),(a+1,b),(a,b-1),(a,b+1)):
                    if 0<=aa<64 and 0<=bb<64 and m[aa,bb] and not seen[aa,bb]: seen[aa,bb]=1; st.append((aa,bb))
            if len(cl)<3:
                buur=[o[aa,bb] for a,b in cl for aa,bb in ((a-1,b),(a+1,b),(a,b-1),(a,b+1)) if 0<=aa<64 and 0<=bb<64 and o[aa,bb]>1 and o[aa,bb]!=c and G[o[aa,bb]]==G[c] and (aa,bb) not in cl]
                if buur:
                    v=max(set(buur),key=buur.count)
                    for a,b in cl: o[a,b]=v; n+=1
    return n
binnen=~rand
o2=o.copy(); n=ruis(o2); o2[rand]=o[rand]; o=o2
np.save('r1.npy',o)
def opslaan(o,naam):
    im=Image.fromarray(o.astype(np.uint8),'P'); pl=sum(cols,[]); im.putpalette(pl); im.save(naam,transparency=0)
    rgb=np.array(cols,'uint8')[o]; rgb[o==0]=255; Image.fromarray(rgb).resize((512,512),Image.NEAREST).save(naam.replace('.png','_8x.png'))
opslaan(o,'r1.png')
z=(rand&(o==1)).sum()/rand.sum()
print('rand',rand.sum(),'zwart %.0f%%'%(100*z),'ruis-px',n,'afwijkend van kaal',(o!=kaal).sum(),'buitenlijn',(rand&(o!=kaal)).sum())
