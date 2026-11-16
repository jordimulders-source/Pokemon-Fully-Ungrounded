# r5 punt 1: KOP GROTER, dezelfde reductieketen als r4 (kop4.py), alleen met een kleinere verkleiningsfactor in de kopzone.
# Vervorming (anker op de aansluiting met de hals): spritepixel (u,v) van r5 -> r4-coordinaat (u',v'):
#   d = AX-u ; w = smoothstep(d/R) (0 bij de hals, 1 vanaf R px links ervan) ; s = 1+(SCHAAL-1)*w
#   u' = AX - d/s ; v' = AY + (v-AY)/s     (rechts van AX: s=1, identiek aan r4)
# r4-coordinaat -> model: (106+12u', 120+12v'); blok = 12/s modelpx. Per blok dezelfde metingen als r4 (meet4.py) +
# aandelen van de natieve groepen (klassen.npz). Kleurregels = kop4.py (r4): dekking >= 0,35 (dunne delen 0,22),
# roze streep -> 7 (rand 6), lijn -> 2, creme naar de modelmediaan (5/4/3) + goud/tan-strengen, rand = selout van het blok.
# Gezicht: lijnen uit de lijnmeting (geen r3-V-lijst meer: die past niet op de grotere kop), pupil = rood uit het model.
# Bevroren: alles buiten de kopzone van r4, de hals rechts van AX, het lijf linksonder van de hals, de twinkels.
import sys, json, numpy as np; from PIL import Image
from scipy import ndimage
SCHAAL=float(sys.argv[1]); AX,AY,R=22.0,18.0,7.0
LB=int(sys.argv[2]) if len(sys.argv)>2 and sys.argv[2].isdigit() else 2   # min. natieve lijnpixels voor een binnenlijn
PAL=json.load(open('palet.json')); P=np.array(PAL,float)
r4=np.asarray(Image.open('../r4/sprite.png')).astype(int); kop3=np.load('../r3/r3_kop_V.npy'); r3=np.asarray(Image.open('../r3/sprite.png')).astype(int)
M=np.asarray(Image.open('../../referenties/model_v14.png').convert('RGB')).astype(float)
fg=np.load('../r4/model_fg.npz')['fg']; lum=M@[0.299,0.587,0.114]; pink=(M[...,0]-M[...,1])>90; line=(lum<125)&~pink
K=np.load('klassen.npz'); KL={n:np.unpackbits(K[n])[:1024*1024].reshape(1024,1024).astype(bool) for n in K.files}
H=W=64; Y,X=np.mgrid[:H,:W]
KZ=(X<26)&(Y<31)&~((X>=22)&(Y>=24))
SPIK=r3!=kop3                                   # spikkels B (worden opnieuw geplaatst, spikkels5.py)
TWC=[(8,6),(5,9),(29,18),(20,26),(16,29)]
TW=np.zeros((H,W),bool)
for cx,cy in TWC:
    for dx,dy in ((0,0),(1,0),(-1,0),(0,1),(0,-1)): TW[cy+dy,cx+dx]=1
BEV=(~KZ)|((X>=18)&(Y>=24))                     # bevroren in r4-termen: lijf/lijnen/pijl, lijf linksonder de hals, twinkels
def inv(u,v):
    d=AX-u; t=np.clip(d/R,0,1); w=t*t*(3-2*t); s=1+(SCHAAL-1)*w
    return AX-d/s, AY+(v-AY)/s, s
def meet(i,j):
    u,v,s=inv(i+0.5,j+0.5); b=12/s; cx=106+12*u; cy=120+12*v
    x0,x1=int(round(cx-b/2)),int(round(cx+b/2)); y0,y1=int(round(cy-b/2)),int(round(cy+b/2))
    sl=(slice(max(0,y0),y1),slice(max(0,x0),x1)); f=fg[sl]; n=f.size
    r={'u':u,'v':v,'cov':f.mean(),'lijn':(line[sl]&f).sum()/n}
    for g in KL: r[g]=KL[g][sl].sum()/n
    cr=f&~pink[sl]&~line[sl]
    r['med']=np.median(lum[sl][cr]) if cr.sum()>3 else 0
    if f.sum()>3:
        l=lum[sl][f]; r['md']=M[sl][f][l<=np.percentile(l,30)].mean(0)
    else: r['md']=np.array([255.,255,255])
    return r
# lijnkaarten (zoals ../r3/lijnkaart.py): elke natieve pixel van een groep zet de r5-spritepixel waarin zijn middelpunt
# valt (heen-afbeelding van de vervorming numeriek omgekeerd). Zo blijven dunne lijnen/strepen 1 px breed en aaneengesloten.
from PIL import Image as _I
q=np.asarray(_I.open('../r3/natief_q_dg.png')).astype(int)
def _comp(m):
    lab,n=ndimage.label(m,np.ones((3,3))); gr=np.bincount(lab.ravel()); return m&(gr[lab]>=3)
dd=np.linspace(0,60,6001); t=np.clip(dd/R,0,1); sdd=1+(SCHAAL-1)*t*t*(3-2*t); dpr=dd/sdd
def heen(up,vp):                                  # r4-coordinaat -> r5-coordinaat
    dp=AX-up
    if dp<=0: return up,vp
    d=np.interp(dp,dpr,dd); t_=min(1,d/R); s=1+(SCHAAL-1)*t_*t_*(3-2*t_)
    return AX-d, AY+(vp-AY)*s
def kaart(ks):
    m=_comp(np.isin(q,ks)); k=np.zeros((H,W),int)
    for yy,xx in zip(*np.where(m)):
        mx=(xx+1)*5.12+4.25; my=(yy+1)*5.12+4.25; u,v=heen((mx-106)/12,(my-120)/12)
        i,j=int(np.floor(u)),int(np.floor(v))
        if 0<=i<W and 0<=j<H: k[j,i]+=1
    return k
KR=kaart([6,7,8,9,10,11,12]); KB=kaart([1,2]); KG=kaart([3,14])
# twinkels (sterretjes uit het model rond de kop) schuiven mee met de vervorming: nieuw middelpunt = de r5-pixel waarvan
# het r4-punt het dichtst bij het oude middelpunt ligt. De vorm (plusje van 5 px) en kleuren blijven die van r4.
TWN={}
for cx,cy in TWC:
    best=min(((inv(i+0.5,j+0.5)[0]-cx-0.5)**2+(inv(i+0.5,j+0.5)[1]-cy-0.5)**2,(i,j)) for j in range(H) for i in range(W))[1]
    TWN[(cx,cy)]=best
TW5=np.zeros((H,W),bool)
for (cx,cy),(nx,ny) in TWN.items():
    for dx,dy in ((0,0),(1,0),(-1,0),(0,1),(0,-1)): TW5[ny+dy,nx+dx]=1
# kopzone in r5: pixels waarvan het r4-punt in de r4-kopzone (en niet bevroren) ligt en links van de hals
Z=np.zeros((H,W),bool); MS={}
for j in range(H):
    for i in range(W):
        if i+0.5>=AX: continue
        u,v,_=inv(i+0.5,j+0.5); iu,iv=int(np.floor(u)),int(np.floor(v))
        if 0<=iu<W and 0<=iv<H and KZ[iv,iu] and not BEV[iv,iu] and not (BEV[j,i] and not KZ[j,i]) and not TW5[j,i] and not ((i>=18)&(j>=24)):
            Z[j,i]=1; MS[(j,i)]=meet(i,j)
a=r4.copy(); a[SPIK]=0
a[Z]=0; a[TW&~TW5]=0
for (cx,cy),(nx,ny) in TWN.items():
    for dx,dy in ((0,0),(1,0),(-1,0),(0,1),(0,-1)): a[ny+dy,nx+dx]=r4[cy+dy,cx+dx]
print('twinkels', TWN)
sil=np.zeros((H,W),bool)
for (j,i),m in MS.items(): sil[j,i]=m['cov']>=0.35
def n4(y,x): return [(y+dy,x+dx) for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)) if 0<=y+dy<H and 0<=x+dx<W]
vast=(a>0)&~SPIK&~TW5
for _ in range(2):
    for (j,i),m in MS.items():
        if not sil[j,i] and m['cov']>=0.22 and m['u']<14 and any(sil[q] or vast[q] for q in n4(j,i)): sil[j,i]=1
alles=sil|vast; lab,_=ndimage.label(alles); sil&=lab==lab[20,40]
def rand(y,x): return any(not(sil[q] or vast[q]) or TW5[q] for q in n4(y,x))
# oogwit: binnenkant van het oog = de lichte driehoek in het model (r4-coordinaten, gemeten op 60x: binnenrand van de
# bovenleden (12,6;22,4)-(15,3;20,2) en de rechter/onderkant (15,1;22,6)). OOG = kleur van de binnenkant (punt 2, varianten).
OOG=int(sys.argv[3]) if len(sys.argv)>3 and sys.argv[3].isdigit() else 5
def oogwit(u,v):
    A,B,C=(12.6,22.4),(15.3,20.2),(15.1,22.6)
    def kant(p,q,r): return (q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])
    k1,k2,k3=kant(A,B,(u,v)),kant(B,C,(u,v)),kant(C,A,(u,v))
    return (k1>=0 and k2>=0 and k3>=0) or (k1<=0 and k2<=0 and k3<=0)
for (j,i),m in MS.items():
    if not sil[j,i]: continue
    rd=rand(j,i)
    if m['rood']>=0.08 and 9<=m['u']<=13 and 19<=m['v']<=24: a[j,i]=11; continue          # pupil (rode streep in het model)
    if KR[j,i]>=2: a[j,i]=6 if rd else 7; continue
    if rd:
        ks=[2,3,14,6,7]; a[j,i]=2 if m['lijn']>=0.2 else ks[int(((P[ks]-m['md'])**2).sum(1).argmin())]; continue
    if m['lijn']>=0.38 or KB[j,i]>=3: a[j,i]=2; continue           # binnenlijn: >= 38% donkere modelpixels in het blok
    if oogwit(m['u'],m['v']): a[j,i]=OOG; continue
    t=5 if m['med']>=218 else (4 if m['med']>=195 else 3)
    if KG[j,i]>=4: t=3
    elif KG[j,i]>=2 and t==5: t=4
    a[j,i]=t
np.save('kop5_%d_%d.npy'%(round(SCHAAL*100),OOG),a); np.save('zone5_%d.npy'%round(SCHAAL*100),Z)
import pickle; pickle.dump(MS,open('meting5_%d.pkl'%round(SCHAAL*100),'wb'))
HX='.123456789ABCDEF'
if 'stil' not in sys.argv:
    for y in range(32): print('%2d'%y,''.join(HX[v] for v in a[y,:30]))
