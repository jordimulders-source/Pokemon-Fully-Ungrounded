# r5: zelfde als r4/bouw4.py, maar op het model met alleen de 2 halskolommen geschrapt (72 breed); geen plaatsing
# r4: geschrapt model (64x48, r4/schrap4.py); zelfde opbouw als r1+r2+r3, lokale x-zones +2 (2 halskolommen minder geschrapt)
# r1: geschrapt model -> geindexeerde 64x64 frontsprite.
# Alle pixels komen uit het model; alleen: kleurgroepen kwantiseren naar modeltinten (mediaan per cluster),
# kano/yerba-textuur gladgestreken via toonkaart (gladde luminantie van het model), losse pixels weg.
from PIL import Image; import numpy as np
D='docs/concept/sprites/mate_fase2/sprite/r1/'
a=np.asarray(Image.open(D+'../r5/geschrapt72.png').convert('RGB')).astype(int)
H,W,_=a.shape
L=.3*a[...,0]+.59*a[...,1]+.11*a[...,2]
mx=a.max(2); mn=a.min(2)
# achtergrond = lichte pixels verbonden met de rand
light=mn>235
bg=np.zeros((H,W),bool); st=[(y,x) for y in range(H) for x in range(W) if (y in(0,H-1) or x in(0,W-1)) and light[y,x]]
for p in st: bg[p]=True
while st:
    y,x=st.pop()
    for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
        v,u=y+dy,x+dx
        if 0<=v<H and 0<=u<W and light[v,u] and not bg[v,u]: bg[v,u]=True; st.append((v,u))
cls=np.full((H,W),'.',dtype='<U1')
r,g,b=a[...,0],a[...,1],a[...,2]
for y in range(H):
    for x in range(W):
        if bg[y,x]: continue
        if L[y,x]<55: c='#'
        elif b[y,x]>r[y,x]+15 and b[y,x]>=g[y,x]: c='w'
        elif mx[y,x]-mn[y,x]<30 or mn[y,x]>200: c='s'
        elif g[y,x]>=r[y,x]: c='g'
        else: c='b'
        cls[y,x]=c
np.save(D+'../r5/cls.npy',cls)
def km1(v,k,it=50):
    c=np.quantile(v,np.linspace(.1,.9,k))
    for _ in range(it):
        lab=np.abs(v[:,None]-c[None]).argmin(1)
        c=np.array([v[lab==i].mean() if (lab==i).any() else c[i] for i in range(k)])
    return np.sort(c)
def blur(m,v,s=1.0):
    R=int(3*s); k=np.exp(-np.arange(-R,R+1)**2/(2*s*s)); 
    def cv(z):
        z=np.pad(z,R); 
        z=np.array([np.convolve(row,k,'valid') for row in z]); z=np.array([np.convolve(col,k,'valid') for col in z.T]).T
        return z
    num=cv(np.where(m,v,0.)); den=cv(m.astype(float)); return num/np.maximum(den,1e-6)
pal=[(0,0,0)]; idx=np.zeros((H,W),int)
def addtones(mask,k,c=None):
    v=L[mask]; c=km1(v,k) if c is None else np.array(c,float); start=len(pal)
    lab=np.abs(L[...,None]-c[None,None]).argmin(2)
    for i in range(k):
        sel=mask&(lab==i); pal.append(tuple(int(t) for t in np.median(a[sel],axis=0)))
    return start,c
# omlijning
out=cls=='#'; pal.append(tuple(int(t) for t in np.median(a[out],axis=0))); idx[out]=1
# bruin 4, groen 4, zilver 3, water 2
yy,xx=np.mgrid[0:H,0:W]
B=cls=='b'; G=cls=='g'; S=cls=='s'; Wt=cls=='w'
DX=2
VENT=G&((xx>=29+DX)|(yy<=17))
sb,cb=addtones(B,4,[60,86,120,172])  # toppen van het bruine histogram van het model
sg,cg=addtones(G,4); ss,cs=addtones(S,3); sw,cw=addtones(Wt,2)
def toon(mask,start,c,sig,lijn=None,lijnabs=-1):
    sm=blur(mask,L,sig)
    lab=np.abs(sm[...,None]-c[None,None]).argmin(2)
    if lijn is not None:  # modellijnen (donker in het model zelf, of veel donkerder dan omgeving) -> donkerste tint
        lab=np.where((L<sm-lijn)|(L<lijnabs),0,lab)
    idx[mask]=(start+lab)[mask]
toon(B,sb,cb,0.7,40,75)
toon(G&~VENT,sg,cg,0.6,30,70)
labv=np.abs(L[...,None]-cg[None,None]).argmin(2); idx[VENT]=(sg+labv)[VENT]
FACEm=(yy>=10)&(yy<=17)&(xx>=31+DX)&(xx<=47+DX)
_keep=idx.copy(); toon(VENT&~FACEm,sg,cg,0.6,30,70); idx[FACEm]=_keep[FACEm]  # (r3) bladkop/lijf ventje via gladde toonkaart, gezicht bevroren
# r4 punt 3: bruine pixels op de buitenrand krijgen hun eigen modeltoon (dichtstbijzijnde bruine tint op L), niet de geblurde
rand=np.zeros((H,W),bool)
for y in range(H):
    for x in range(W):
        if B[y,x] and any(not(0<=y+dy<H and 0<=x+dx<W) or bg[y+dy,x+dx] for dy,dx in((1,0),(-1,0),(0,1),(0,-1))): rand[y,x]=True
labr=np.abs(L[...,None]-cb[None,None]).argmin(2); idx[rand]=(sb+labr)[rand]; print('randtoon bruin',rand.sum())
labs=np.abs(L[...,None]-cs[None,None]).argmin(2); idx[S]=(ss+labs)[S]
labw=np.abs(L[...,None]-cw[None,None]).argmin(2); idx[Wt]=(sw+labw)[Wt]
# losse pixels: vulpixel zonder 4-buur met dezelfde index -> meest voorkomende buur binnen dezelfde groep
grp={1:'#'}; 
for i in range(4): grp[sb+i]='b'; grp[sg+i]='g'
for i in range(3): grp[ss+i]='s'
for i in range(2): grp[sw+i]='w'
for _ in range(2):
    n2=idx.copy()
    for y in range(H):
        for x in range(W):
            i=idx[y,x]
            if i<=1 or grp[i] in 'sw': continue
            nb=[idx[y+dy,x+dx] for dy,dx in((1,0),(-1,0),(0,1),(0,-1)) if 0<=y+dy<H and 0<=x+dx<W]
            if i in nb: continue
            if VENT[y,x] and 5<=y<=14 and 33+DX<=x<=47+DX: continue   # gezicht ventje bevroren
            # lijnpixels (donkerste bruin/groen) die aan andere lijnpixels raken blijven staan
            if i in (sb,sg) and any(idx[y+dy,x+dx] in (1,sb,sg) for dy in(-1,0,1) for dx in(-1,0,1) if (dy or dx) and 0<=y+dy<H and 0<=x+dx<W): continue
            same=[j for j in nb if j>1 and grp.get(j)==grp[i]]
            if same: n2[y,x]=max(set(same),key=same.count)
    idx=n2
# --- bombilla's (Jordi: "de verre bombilla moet echt duidelijk een bombilla blijven, 1 pixel wordt te dun, 3 minimaal nodig")
# Model heeft al 3-4 px (grijs/zwart - licht - zwart); alleen de kern consequent licht maken:
# eerste lichte pixel na de linkerrand = wit (W), verdere kernpixels = midden (M), water/donkerzilver in de kern -> W/M.
SD,SM,SW_=ss,ss+1,ss+2
gewijzigd=[]
def zet(y,x,v):
    if idx[y,x]!=v: gewijzigd.append((y,x,int(idx[y,x]),v)); idx[y,x]=v
def kern(y,x0,x1,linksgrijs=True):
    run=[x for x in range(x0,x1+1) if idx[y,x]>0]
    if not run: return
    # rechterrand = eerste omlijning na de kern
    xs=[x for x in run]
    l=xs[0]; r=[x for x in xs if idx[y,x]==1 and x>l]
    if not r: return
    r=r[0]; k=list(range(l+1,r))
    if not k: return
    if linksgrijs and idx[y,l]!=1: zet(y,l,SD)
    for j,x in enumerate(k): zet(y,x,SW_ if j==0 else SM)
# verre bombilla: schacht rij 3-12 (boven de hand), x 21-32
for y in range(3,13): kern(y,21+DX,32+DX)
# nabije bombilla: schacht rij 19-23 (in de handen) en 28-37 (onder de rand), zoek de run rond de diagonaal
for y in list(range(19,24))+list(range(28,42)):   # r4: geen rijen meer geschrapt, schacht loopt tot rij 41
    xs=[x for x in range(30+DX,56+DX) if idx[y,x]==1]
    # kies het paar omlijningspixels met 1-2 kernpixels ertussen waarvan de kern zilver/water is
    for i in range(len(xs)-1):
        a_,b_=xs[i],xs[i+1]
        if 2<=b_-a_<=3 and all(grp.get(idx[y,x]) in ('s','w') for x in range(a_+1,b_)):
            for j,x in enumerate(range(a_+1,b_)): zet(y,x,SW_ if j==0 else SM)
print('bombilla-kern gewijzigd',len(gewijzigd),gewijzigd)
# --- selout: buitenlijn aan de lichtkant (achtergrond boven of links) wordt de donkerste tint van het vlak eronder
selout=0
n2=idx.copy()
for y in range(H):
    for x in range(W):
        if idx[y,x]!=1: continue
        def isbg(v,u): return not(0<=v<H and 0<=u<W) or idx[v,u]==0
        if not(isbg(y-1,x) or isbg(y,x-1)) or isbg(y+1,x) or isbg(y,x+1): continue
        if VENT[y,x] and 5<=y<=14 and 33+DX<=x<=47+DX: continue
        bin_=[idx[y+dy,x+dx] for dy,dx in((1,0),(0,1),(1,1)) if y+dy<H and x+dx<W]
        gs=[grp.get(j) for j in bin_ if j>1]
        if gs and all(g_=='b' for g_ in gs): n2[y,x]=sb; selout+=1
        elif gs and all(g_=='g' for g_ in gs): n2[y,x]=sg; selout+=1
idx=n2; print('selout',selout)
# eilandjes van 1 px (ook diagonaal geen gelijke buur) in bruin/groen, buiten het gezicht: buurtint uit dezelfde groep
FACE=lambda y,x: 10<=y<=17 and 31+DX<=x<=47+DX
nweg=0
for _ in range(2):
    n2=idx.copy()
    for y in range(H):
        for x in range(W):
            i=idx[y,x]
            if i<=1 or grp[i] not in 'bg' or FACE(y,x): continue
            n8=[idx[y+dy,x+dx] for dy in(-1,0,1) for dx in(-1,0,1) if (dy or dx) and 0<=y+dy<H and 0<=x+dx<W]
            if i in n8: continue
            n4=[idx[y+dy,x+dx] for dy,dx in((1,0),(-1,0),(0,1),(0,-1)) if 0<=y+dy<H and 0<=x+dx<W]
            same=[j for j in n4 if j>1 and grp.get(j)==grp[i]] or [j for j in n8 if j>1 and grp.get(j)==grp[i]]
            if same: n2[y,x]=max(set(same),key=same.count); nweg+=1
    idx=n2
print('eilandjes weg',nweg)
np.save(D+'../r5/idx72.npy',idx)
print(len(pal),pal)
# in 64x64: onderaan gecentreerd