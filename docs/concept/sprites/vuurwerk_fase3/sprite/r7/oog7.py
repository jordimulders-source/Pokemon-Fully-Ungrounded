# r7: alleen het OOG groter (±1,5x), op r5 115% (geel en goud). Zelfde reductieketen als r5 (kop5.py), alleen in de oogzone
# een extra vergroting rond het oogmidden E (r5-coord.): binnen RV0 factor OOGF, vloeiend naar 1 bij RV1. Elke pixel in de
# oogzone wordt opnieuw gemeten op het model (r5-kop-vervorming + oogvergroting) met de r5-regels: lijn >= 38% donkere
# modelpixels -> 2, oogwit = de lichte driehoek van het model (zelfde driehoek als r5) -> binnenkleur, rode streep -> 11,
# creme naar de modelmediaan (5/4/3) + goudstrengen. Buiten de oogzone: r5, pixel voor pixel.
# Pupil: 1 (bijna-zwart) op de donkerste plek binnen het modeloog (gemeten op 1024 px, >= 0,3 van de ooglijnen af):
# r4-coordinaat (13,8; 22,05), lum 188 tegen 230 gemiddeld; 2 px (de pupilplek en de pixel ernaast met het meeste aandeel).
import sys, json, numpy as np; from PIL import Image
PAL=json.load(open('palet.json')); SCHAAL,AX,AY,R=1.15,22.0,18.0,7.0
E=np.array([float(v) for v in (sys.argv[1] if len(sys.argv)>1 else "13.0,22.0").split(",")]); OOGF,RV0,RV1=[float(v) for v in (sys.argv[2] if len(sys.argv)>2 else "1.5,2.0,3.2").split(",")]
M=np.asarray(Image.open('../../referenties/model_v14.png').convert('RGB')).astype(float)
fg=np.load('../r4/model_fg.npz')['fg']; lum=M@[0.299,0.587,0.114]; pink=(M[...,0]-M[...,1])>90; line=(lum<125)&~pink
K=np.load('../r5/klassen.npz'); KL={n:np.unpackbits(K[n])[:1024*1024].reshape(1024,1024).astype(bool) for n in K.files}
def mfac(rho):
    t=np.clip((rho-RV0)/(RV1-RV0),0,1); w=t*t*(3-2*t); return OOGF+(1-OOGF)*w
def kop_inv(u,v):
    d=AX-u; t=np.clip(d/R,0,1); w=t*t*(3-2*t); s=1+(SCHAAL-1)*w
    return AX-d/s, AY+(v-AY)/s, s
def inv(u,v):                                   # r7 -> r4-coordinaat, met totale schaal
    p=np.array((u,v)); rho=np.linalg.norm(p-E); m=mfac(rho); q=E+(p-E)/m
    up,vp,s=kop_inv(*q); return up,vp,s*m
def heen(up,vp):                                # r4 -> r7 (numeriek, voor de pupilplek)
    best=None
    for v in np.arange(15,28,0.02):
        for u in np.arange(8,19,0.02):
            a,b,_=inv(u,v); e=(a-up)**2+(b-vp)**2
            if best is None or e<best[0]: best=(e,u,v)
    return best[1],best[2]
def oogwit(u,v):
    A,B,C=(12.6,22.4),(15.3,20.2),(15.1,22.6)
    def kant(p,q,r): return (q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])
    k=[kant(A,B,(u,v)),kant(B,C,(u,v)),kant(C,A,(u,v))]; return all(x>=0 for x in k) or all(x<=0 for x in k)
def meet(i,j):
    u,v,s=inv(i+0.5,j+0.5); b=12/s; cx=106+12*u; cy=120+12*v
    sl=(slice(int(round(cy-b/2)),int(round(cy+b/2))),slice(int(round(cx-b/2)),int(round(cx+b/2)))); f=fg[sl]; n=f.size
    cr=f&~pink[sl]&~line[sl]
    return dict(u=u,v=v,cov=f.mean(),lijn=(line[sl]&f).sum()/n,rood=KL['rood'][sl].sum()/n,goud=KL['goud'][sl].sum()/n,
                roze=KL['roze'][sl].sum()/n,bruin=KL['bruin'][sl].sum()/n,med=np.median(lum[sl][cr]) if cr.sum()>3 else 0)
def maak(naam,OOG):
    r5=np.asarray(Image.open('../r5/sprite_115_%s.png'%naam)).astype(int); a=r5.copy(); Z=[]
    for j in range(14,30):
        for i in range(5,21):
            if np.linalg.norm(np.array((i+0.5,j+0.5))-E)>=RV1 or r5[j,i] in (0,6,7,8): continue   # alleen binnen de kop, roze strepen blijven
            if any(r5[j+dy,i+dx]==0 for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))): continue        # rand blijft r5
            m=meet(i,j); Z.append((i,j))
            if m['rood']>=0.08 and 9<=m['u']<=13 and 19<=m['v']<=24: a[j,i]=11
            elif m['lijn']>=0.38 or m['bruin']>=0.5: a[j,i]=2
            elif oogwit(m['u'],m['v']): a[j,i]=OOG
            else:
                t=5 if m['med']>=218 else (4 if m['med']>=195 else 3)
                if m['goud']>=0.73: t=3
                elif m['goud']>=0.365 and t==5: t=4
                a[j,i]=t
    pu,pv=heen(13.8,22.05)
    # pupil: de binnenkantpixel waarvan het midden het dichtst bij de donkerste modelplek ligt, plus zijn horizontale buur
    # (de donkere plek in het model is horizontaal: u 13,5-14,1 bij v 22,0-22,2) die er het dichtst bij ligt
    BK=[(i,j) for (i,j) in Z if a[j,i]==OOG]
    p1=min(BK,key=lambda p:(p[0]+0.5-pu)**2+(p[1]+0.5-pv)**2)
    nbs=[q for q in ((p1[0]-1,p1[1]),(p1[0]+1,p1[1])) if q in BK]
    PUP=[p1]+([min(nbs,key=lambda p:(p[0]+0.5-pu)**2+(p[1]+0.5-pv)**2)] if nbs else [])
    for (x,y) in PUP: a[y,x]=1
    im=Image.fromarray(a.astype('uint8'),'P'); im.putpalette(sum(PAL,[])+[0]*(768-48)); im.save('sprite_%s.png'%naam,transparency=0)
    d=a!=r5; print(naam,'pupil r7-coord (%.2f,%.2f) ->'%(pu,pv),PUP,'| oogzone',len(Z),'px, gewijzigd',int(d.sum()),
          '| binnenkant',len([1 for (i,j) in Z if a[j,i]==OOG]),'px (oud',len([1 for (i,j) in Z if r5[j,i]==OOG]),')')
    return a,r5
if __name__=='__main__':
    HX='.123456789ABCDEF'
    for naam,o in (('geel',13),('goud',14)):
        a,r5=maak(naam,o)
    if "stil" not in sys.argv:
      for y in range(16,27): print('%2d'%y,''.join(HX[v] for v in r5[y,4:20]),'  ',''.join(HX[v] for v in a[y,4:20]))
