# r8: probeersels van het MODELOOG (geen oog uit een andere sprite). Zelfde reductie als r5/r7: elke pixel in de oogzone wordt
# opnieuw op het model gemeten (kop-vervorming 115% + extra oogvergroting), met de r5-regels (lijn >= 38% of bruine
# natieve groep >= 50% -> 2; de lichte modeldriehoek -> binnenkant 13; rode streep -> 11; creme naar de modelmediaan).
# Oogvergroting: factor F rond O; met BOVEN=1 alleen naar boven en opzij (onder de onderste ooglijn factor 1), zodat de
# mondlijn op rij 25 blijft staan. Zone: afstand tot O < RV1 (factor vloeiend van F binnen RV0 naar 1 bij RV1).
# Opties per probeersel: DICHT (gesloten omlijning in modelbruin 2 rond binnenkant+pupil, 8-buren), PUPIL 'h'/'v' (2 px
# bijna-zwart 1 op de donkerste modelplek in het oog, r4 (13,8;22,05), horizontaal of verticaal), GLANS (1 px lichtste
# creme 5 linksboven naast de pupil, in de binnenkant).
# Basis: ../r7/sprite_geel.png met de oogzone eerst teruggezet naar r5 (dus het r7-oog vervalt) en de vlamtong van vlam8.
import sys, json, numpy as np; from PIL import Image
PAL=json.load(open('palet.json')); SCHAAL,AX,AY,R=1.15,22.0,18.0,7.0
M=np.asarray(Image.open('../../referenties/model_v14.png').convert('RGB')).astype(float)
fg=np.load('../r4/model_fg.npz')['fg']; lum=M@[0.299,0.587,0.114]; pink=(M[...,0]-M[...,1])>90; line=(lum<125)&~pink
K=np.load('../r5/klassen.npz'); KL={n:np.unpackbits(K[n])[:1024*1024].reshape(1024,1024).astype(bool) for n in K.files}
def kop_inv(u,v):
    d=AX-u; t=np.clip(d/R,0,1); w=t*t*(3-2*t); s=1+(SCHAAL-1)*w
    return AX-d/s, AY+(v-AY)/s, s
def oogwit(u,v):
    A,B,C=(12.6,22.4),(15.3,20.2),(15.1,22.6)
    def kant(p,q,r): return (q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])
    k=[kant(A,B,(u,v)),kant(B,C,(u,v)),kant(C,A,(u,v))]; return all(x>=0 for x in k) or all(x<=0 for x in k)
def bouw(O,F,RV0,RV1,BOVEN,DICHT,PUPIL,GLANS,basis):
    O=np.array(O)
    def mfac(rho):
        t=np.clip((rho-RV0)/(RV1-RV0),0,1); w=t*t*(3-2*t); return F+(1-F)*w
    def inv(u,v):
        p=np.array((u,v)); m=mfac(np.linalg.norm(p-O)); dx=(p[0]-O[0])/m; dy=(p[1]-O[1])/m if (p[1]<O[1] or not BOVEN) else p[1]-O[1]
        up,vp,s=kop_inv(O[0]+dx,O[1]+dy); return up,vp,s*m
    def meet(i,j):
        u,v,s=inv(i+0.5,j+0.5); b=12/s; cx=106+12*u; cy=120+12*v
        sl=(slice(int(round(cy-b/2)),int(round(cy+b/2))),slice(int(round(cx-b/2)),int(round(cx+b/2)))); f=fg[sl]; n=f.size
        cr=f&~pink[sl]&~line[sl]
        return dict(u=u,v=v,lijn=(line[sl]&f).sum()/n,rood=KL['rood'][sl].sum()/n,goud=KL['goud'][sl].sum()/n,
                    bruin=KL['bruin'][sl].sum()/n,med=np.median(lum[sl][cr]) if cr.sum()>3 else 0)
    a=basis.copy(); Z=[]
    for j in range(12,30):
        for i in range(4,22):
            if np.linalg.norm(np.array((i+0.5,j+0.5))-O)>=RV1 or basis[j,i] in (0,6,7,8): continue
            if any(basis[j+dy,i+dx]==0 for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))): continue
            m=meet(i,j); Z.append((i,j))
            if m['rood']>=0.08 and 9<=m['u']<=13 and 19<=m['v']<=24: a[j,i]=11
            elif m['lijn']>=0.38 or m['bruin']>=0.5: a[j,i]=2
            elif oogwit(m['u'],m['v']): a[j,i]=13
            else:
                t=5 if m['med']>=218 else (4 if m['med']>=195 else 3)
                if m['goud']>=0.73: t=3
                elif m['goud']>=0.365 and t==5: t=4
                a[j,i]=t
    # pupil: binnenkantpixel het dichtst bij de donkerste modelplek + buur (horizontaal of verticaal)
    best=None
    for v in np.arange(16,28,0.02):
        for u in np.arange(8,19,0.02):
            x,y,_=inv(u,v); e=(x-13.8)**2+(y-22.05)**2
            if best is None or e<best[0]: best=(e,u,v)
    pu,pv=best[1],best[2]
    BK=[(i,j) for (i,j) in Z if a[j,i]==13]
    p1=min(BK,key=lambda p:(p[0]+0.5-pu)**2+(p[1]+0.5-pv)**2)
    nbs=[q for q in (((p1[0]-1,p1[1]),(p1[0]+1,p1[1])) if PUPIL=='h' else ((p1[0],p1[1]-1),(p1[0],p1[1]+1))) if q in BK]
    PUP=[p1]+([min(nbs,key=lambda p:(p[0]+0.5-pu)**2+(p[1]+0.5-pv)**2)] if nbs else [])
    for (x,y) in PUP: a[y,x]=1
    GL=[]
    if GLANS:
        kand=[(x-1,y-1) for (x,y) in PUP]+[(x-1,y) for (x,y) in PUP]+[(x,y-1) for (x,y) in PUP]
        kand=[k for k in kand if a[k[1],k[0]]==13]
        if kand: GL=[kand[0]]; a[GL[0][1],GL[0][0]]=5
    RING=[]
    if DICHT:
        I={(x,y) for y in range(64) for x in range(64) if a[y,x] in (13,1) or (x,y) in GL}
        I={p for p in I if p in Z or p in PUP or p in GL}
        for (x,y) in list(I):
            for dy in (-1,0,1):
                for dx in (-1,0,1):
                    q=(x+dx,y+dy)
                    if q not in I and a[q[1],q[0]] not in (2,1,11,0): RING.append(q); a[q[1],q[0]]=2
    return a,dict(zone=len(Z),binnenkant=int(sum(1 for (i,j) in Z if a[j,i]==13)),pupil=PUP,glans=GL,ring=sorted(set(RING)))
