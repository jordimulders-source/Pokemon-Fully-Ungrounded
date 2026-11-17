# r6 = r5 B met de rechte rechterbuitenlijn van de romp (onder de waterval tot het zeefje) als vloeiende curve naar binnen.
# Jordi: "ik vind b beter dan a, maar zou je die rechte lijn nog iets smoother kunnen afkappen, dus dat die iets meer naar binnen komt"
# Per rij: rompdeel rechts van de bombilla wordt korter gemaakt door rompppixels uit het midden (basistint C) weg te
# halen, zodat de schaduwtinten aan de rechterkant met de rand meeschuiven; daarna 1 px omlijning (zwart, schaduwkant)
# op de nieuwe rand. Waterval, zeefje, bombilla's, ventje en alles links: bevroren (assert).
from PIL import Image; import numpy as np
D='docs/concept/sprites/mate_fase2/sprite/'
src=Image.open(D+'r5/mate2_B.png'); a=np.asarray(src).astype(int)
# nieuwe randkolom (x van de omlijning) per rij; rijen 38-42 blijven x60 (waterval hangt eraan)
# trappen in een curvepatroon (lang -> kort), zoals de schuine achtersteven van het model
CURVES={'zacht':{43:59,44:59,45:59,46:58,47:58,48:57,49:57,50:56,51:55,52:54,53:53},   # runs 5,3,2,2,1,1,1,1
        'sterk':{43:59,44:59,45:58,46:58,47:57,48:56,49:55,50:54,51:53,52:52,53:53}}  # runs 5,2,2,1,1,1,1,1
def oude_rand(s,y):
    xs=[x for x in range(44,64) if s[y,x]!=0 and not (13<=s[y,x]<=15)]
    return max(xs)
for naam,cur in CURVES.items():
    s=a.copy(); zone=np.zeros_like(s,bool)
    for y,nx in cur.items():
        ox=oude_rand(s,y)
        sil=[x for x in range(40,ox) if 10<=s[y,x]<=12]
        st=(max(sil)+2) if sil else 44           # na de bombilla en haar omlijning
        while st<ox and s[y,st]==1: st+=1
        if nx<st: nx=st                          # rand mag niet in de bombilla
        seg=list(s[y,st:ox])                     # rompppixels (zonder de oude omlijning)
        # dubbele oude omlijning (2 px dik, rij 46-49): de binnenste lijnpixel wordt rompschaduw (1 px omlijning)
        while seg and seg[-1]==1:
            seg[-1]=next((v for v in reversed(seg) if v!=1),3)
            if len(seg)>=2 and seg[-2]!=1: break
        if len(seg)<nx-st: nx=st+len(seg)        # rand ligt al binnen de curve
        nieuw=nx-st
        while len(seg)>nieuw:
            m=len(seg)/2
            cand=[i for i,v in enumerate(seg) if v==4] or [i for i,v in enumerate(seg) if v!=1] or list(range(len(seg)))
            seg.pop(min(cand,key=lambda i:abs(i-m)))
        rij=s[y].copy()
        rij[st:nx]=seg; rij[nx]=1; rij[nx+1:ox+1]=0
        zone[y,st:ox+1]=True; s[y]=rij
    # rij 54-55: het rompbultje rechts van de bovenkant van het zeefje valt buiten de nieuwe curve -> weg,
    # de omlijning van het zeefje (x54 rij 54, x55 rij 55) wordt daar de rand
    for y,xs in {54:(55,56,57),55:(56,57)}.items():
        for x in xs: zone[y,x]=True; s[y,x]=0
    assert (s[~zone]==a[~zone]).all()
    # geen bombilla/zeefje/waterpixel geraakt
    assert all(not(10<=a[y,x]<=15) or s[y,x]==a[y,x] for y,x in zip(*np.where(zone)))
    print(naam,'pixels gewijzigd:',(s!=a).sum())
    o=Image.fromarray(s.astype('uint8'),'P'); o.putpalette(src.getpalette()); o.save(D+'r6/mate2_%s.png'%naam,transparency=0)
