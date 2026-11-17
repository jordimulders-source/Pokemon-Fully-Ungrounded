# r8 = r7 met de hele rechterbuitenlijn (rij 42 onder de waterval -> aansluiting op het zeefje, rij 54 x54) op één boog:
#   x(y) = 60 - c*(y-y0)^p, afgerond (floor(x+0.5)); x(42)=60 (vast, waterval), x(54)=54 = omlijning zeefje.
#   A: p=1,7 y0=41,5 c=0,0754 -> trappen (vanaf rij 43) x60:2 59:3 58:2 57:2 56:1 55:1 54:1
#   B: p=1,7 y0=39,5 c=0,0600 -> trappen 59:4 58:2 57:2 56:2 55:1 54:1
# Per rij wordt het rompdeel rechts van de bombilla korter (basistint C uit het midden weg) of langer (schaduwtint aan
# de rand verdubbeld), zodat de schaduwband meeschuift; 1 px zwarte omlijning op de nieuwe rand.
# Bevroren (assert): waterval, bombilla's, zeefje, alles links van de bombilla en buiten rij 43-53.
from PIL import Image; import numpy as np
D='docs/concept/sprites/mate_fase2/sprite/'
src=Image.open(D+'r7/mate2.png'); a=np.asarray(src).astype(int)
pal=np.array(src.getpalette()[:48]).reshape(16,3)
VAR={'A':(1.7,41.5,0.0754),'B':(1.7,39.5,0.0600)}
def maak(naam,p,y0,c):
    xs={y:int(np.floor(60-c*max(0,y-y0)**p+0.5)) for y in range(42,55)}
    assert xs[42]==60 and xs[54]==54
    s=a.copy(); zone=np.zeros_like(s,bool)
    for y in range(43,54):
        nx=xs[y]
        ox=max(x for x in range(44,64) if s[y,x]!=0 and not 13<=s[y,x]<=15)
        sil=[x for x in range(40,ox) if 10<=s[y,x]<=12]
        st=max(sil)+2
        while s[y,st]==1: st+=1
        seg=list(s[y,st:ox])
        while seg and seg[-1]==1: seg.pop()
        while len(seg)>nx-st:
            m=len(seg)/2; cand=[i for i,v in enumerate(seg) if v==4] or list(range(len(seg)))
            seg.pop(min(cand,key=lambda i:abs(i-m)))
        while len(seg)<nx-st: seg.append(seg[-1] if seg[-1]!=2 else 3)
        rij=s[y].copy(); rij[st:nx]=seg; rij[nx]=1; rij[nx+1:max(ox,nx)+2]=0
        zone[y,st:max(ox,nx)+2]=True; s[y]=rij
    assert (s[~zone]==a[~zone]).all()
    assert all(not(10<=a[y,x]<=15) or s[y,x]==a[y,x] for y,x in zip(*np.where(zone)))
    # geen dubbele hoekpixels: per rij precies 1 omlijningspixel rechts van de romp
    for y in range(43,54): assert sum(1 for x in range(st,64) if s[y,x]==1 and x>=xs[y]-1 and s[y,x-1] not in(1,10,11,12))<=1
    runs=[]; prev=None
    for y in range(43,55):
        if xs[y]==prev: runs[-1][1]+=1
        else: runs.append([xs[y],1]); prev=xs[y]
    print(naam,'rand per rij',xs,'trappen',runs,'gewijzigd',(s!=a).sum())
    o=Image.fromarray(s.astype('uint8'),'P'); o.putpalette(src.getpalette()); o.save(D+'r8/mate2_%s.png'%naam,transparency=0)
    # hulpbeeld zonder bombilla (zelfde regels als r7)
    rgb=np.where(s[...,None]==0,np.array([235,240,235]),pal[s]).astype('uint8')
    zil=(s>=10)&(s<=12); msk=zil.copy()
    for y,x in np.argwhere(s==1):
        if any(zil[y+dy,x+dx] for dy in(-1,0,1) for dx in(-1,0,1) if 0<=y+dy<64 and 0<=x+dx<64): msk[y,x]=True
    msk[:40]=False; msk[:, :40]=False
    for x in (48,49,50): msk[58,x]=False
    rgb[msk]=(255,205,215)
    for x,y in [(53,55),(52,56),(51,57)]: rgb[y,x]=(220,30,30)
    Image.fromarray(rgb).save(D+'r8/hulp_%s.png'%naam)
for k,v in VAR.items(): maak(k,*v)
