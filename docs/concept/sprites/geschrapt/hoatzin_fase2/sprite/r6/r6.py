# Hoatzin r6: "blurry" oplossen op r5 (silhouet, vormen, onderdelen bevroren), niets getekend.
# 1 palet: buik D, grotere toonstappen (±35 helderheid, zoals Taillow/Swellow)
# 2 mauve vulling (lijf/vleugels, niet staart/strepen/lijnen) opnieuw uit een gladde toonkaart van het model,
#   drempels = 1D-k-means (3 klassen) op de eigen toonverdeling
# 3 zwarte lijnen die door de reductie 2 px dik zijn: per 2x2-blok de lichtste modelcel naar de vlaktint (simple point)
# 4 vlekjes < 6 px (mauve en buik) samenvoegen met de buurtint
import os, sys, json, numpy as np; from PIL import Image
N=np.asarray(Image.open('natief.png').convert('RGB')).astype(float); Ln=N.mean(2)
Zn=np.load('zones_nat.npy'); fgn=Zn!='.'
LIJN=np.load('../r4/lijn_nat.npy'); STREEP=np.load('../r4/streep_nat.npy')
Zt=np.load('../r4/zone_t.npy'); TH,TW=Zt.shape; X0=(64-TW)//2; Y0=64-TH
Z=np.full((64,64),'.',dtype='<U1'); Z[Y0:,X0:X0+TW]=Zt
src=Image.open('r5.png'); S=np.array(src).astype(int); R5=S.copy()
ys,xs=np.where(fgn); x0,y0=xs.min(),ys.min(); s=(ys.max()+1-y0)/TH
H,W=Ln.shape
def Wm(n0,cnt,n):
    M=np.zeros((cnt,n))
    for j in range(cnt):
        a=n0+j*s; b=a+s
        for k in range(int(np.floor(a)),int(np.ceil(b))):
            if 0<=k<n: M[j,k]=max(0,min(b,k+1)-max(a,k))
    return M
Wx=Wm(x0,TW,W); Wy=Wm(y0,TH,H)
def boxmean(a,m,r):
    P=np.pad(a*m,r); Q=np.pad(m.astype(float),r); sm=np.zeros_like(a); c=np.zeros_like(a)
    for dy in range(-r,r+1):
        for dx in range(-r,r+1):
            sm+=P[r+dy:r+dy+H,r+dx:r+dx+W]; c+=Q[r+dy:r+dy+H,r+dx:r+dx+W]
    return sm/np.maximum(c,1e-6)
def canvas(t):
    o=np.zeros((64,64)); o[Y0:,X0:X0+TW]=t; return o
# celmediaan zonder lijnen/strepen (voor het verdunnen van lijnen)
cel=np.full((64,64),255.)
for y in range(TH):
  for x in range(TW):
    a=y0+y*s; b=x0+x*s; sl=(slice(int(a),int(np.ceil(a+s))),slice(int(b),int(np.ceil(b+s))))
    m=fgn[sl]
    if m.any(): cel[y+Y0,x+X0]=Ln[sl][m].mean()
# ---- 1 palet ----
PAL=[(152,208,160),(30,18,32),(56,34,54),(102,70,96),(146,112,138),(196,166,188),(100,52,32),(172,96,50),
     (52,62,144),(98,116,214),(208,52,76),(0x4C,0x28,0x60),(0x7C,0x44,0x98),(0xB4,0x7C,0xD6),(70,66,90),(134,130,152)]
PAL=[tuple(int(v) for v in os.environ.get('P%d'%i,','.join(map(str,c))).split(',')) for i,c in enumerate(PAL)]
lum=lambda c: 0.299*c[0]+0.587*c[1]+0.114*c[2]
log={}
def zet(y,x,v,regel):
    if S[y,x]!=v:
        log[regel]=log.get(regel,0)+1; S[y,x]=v
fg=S!=0
pad=np.pad(fg,1); rand=fg&~(pad[:-2,1:-1]&pad[2:,1:-1]&pad[1:-1,:-2]&pad[1:-1,2:])
N4=((-1,0),(1,0),(0,-1),(0,1)); N8=[(i,j) for i in (-1,0,1) for j in (-1,0,1) if i or j]
ok=lambda y,x: 0<=y<64 and 0<=x<64
# ---- 2 mauve vulling uit de gladde toonkaart ----
mm=np.isin(Zn,['M','W'])&~LIJN&~STREEP
R=int(os.environ.get('R',4))
T=canvas((Wy@(boxmean(Ln,mm,R)*mm)@Wx.T)/np.maximum(Wy@mm.astype(float)@Wx.T,1e-6))
VUL=np.isin(S,[2,3,4])&~rand&(Z!='D')&np.isin(Z,['M','W','K'])
v=T[VUL]
c=np.percentile(v,[20,55,85])
for _ in range(50):
    k=np.argmin(abs(v[:,None]-c[None]),1); c=np.array([v[k==i].mean() for i in range(3)])
t1,t2=(c[0]+c[1])/2,(c[1]+c[2])/2
D1=float(os.environ.get('D1',0)); D2=float(os.environ.get('D2',0)); t1+=D1; t2+=D2
print('toonkaart k-means centra',c.round(1),'drempels',round(t1,1),round(t2,1))
for y,x in zip(*np.where(VUL)):
    zet(y,x,2 if T[y,x]<t1 else 3 if T[y,x]<t2 else 4,'2 mauve vulling uit toonkaart')
VAST=np.zeros((64,64),bool)
# ---- 3 dikke zwarte lijnen verdunnen (binnen de figuur, niet in snavel/oog/gezicht/poten) ----
VRIJ=~np.isin(Z,['S','E','F','T'])
def simple(y,x):
    # p mag weg als de zwarte 8-buren na verwijderen 1 samenhangende groep blijven
    nb=[(d,e) for d,e in N8 if ok(y+d,x+e) and S[y+d,x+e]==1]
    if len(nb)<=1: return False
    st=[nb[0]]; seen={nb[0]}
    while st:
        d,e=st.pop()
        for f,g in nb:
            if (f,g) not in seen and max(abs(f-d),abs(g-e))<=1: seen.add((f,g)); st.append((f,g))
    return len(seen)==len(nb)
def buurtoon(y,x):
    nb=[S[y+d,x+e] for d,e in N8 if ok(y+d,x+e) and S[y+d,x+e] not in (0,1,5)]
    return max(set(nb),key=nb.count) if nb else 2
for it in range(6):
    ver=False
    for y in range(63):
      for x in range(63):
        blk=[(y,x),(y,x+1),(y+1,x),(y+1,x+1)]
        if all(S[q]==1 for q in blk):
            kand=[q for q in blk if not rand[q] and VRIJ[q] and simple(*q)]
            if kand:
                q=max(kand,key=lambda q:cel[q]); zet(q[0],q[1],buurtoon(*q),'3 2px-lijn -> 1 px (lichtste modelcel naar vlaktint)'); ver=True
    if not ver: break
# lijnstukken binnen de figuur waar het model niet donker is (cel > 70) en die nergens aan vastzitten
for y,x in zip(*np.where((S==1)&~rand&VRIJ)):
    if cel[y,x]>float(os.environ.get('LK',70)) and simple(y,x):
        zet(y,x,buurtoon(y,x),'3 zwart waar het model niet donker is (> 70)')
# ---- 4 vlekjes < 6 px samenvoegen (mauve 2-4 en buik 11-13, per tint, 4-verbonden) ----
MIN=int(os.environ.get('MIN',6))
GR={2:(2,3,4),3:(2,3,4),4:(2,3,4),11:(11,12,13),12:(11,12,13),13:(11,12,13)}
for it in range(4):
    seen=np.zeros((64,64),bool); n=0
    for y in range(64):
      for x in range(64):
        t=S[y,x]
        if t not in GR or seen[y,x] or VAST[y,x]: continue
        st=[(y,x)]; comp=[]; seen[y,x]=1
        while st:
            a,b=st.pop(); comp.append((a,b))
            for d,e in N4:
                q,r=a+d,b+e
                if ok(q,r) and not seen[q,r] and S[q,r]==t: seen[q,r]=1; st.append((q,r))
        if len(comp)>=MIN: continue
        if t in (2,3,4) and all(Z[q]=='D' for q in comp): continue
        nb=[S[a+d,b+e] for a,b in comp for d,e in N4 if ok(a+d,b+e) and S[a+d,b+e] in GR[t] and S[a+d,b+e]!=t]
        if not nb: continue
        # rand-selout (buitenkant) niet veranderen
        nt=max(set(nb),key=nb.count)
        for q in comp:
            if not rand[q]: zet(q[0],q[1],nt,'4 vlekje < %d px -> buurtint'%MIN); n+=1
    if not n: break
# ---- uitvoer ----
assert ((S!=0)==(R5!=0)).all(), 'silhouet veranderd'
im=Image.fromarray(S.astype('uint8'),'P'); flat=[v for c in PAL for v in c]; im.putpalette(flat+[0]*(768-len(flat)))
im.save('hoatzin.png',transparency=0)
with open('normal.pal','w') as f:
    f.write('JASC-PAL\n0100\n16\n'+''.join('%d %d %d\n'%c for c in PAL))
print(json.dumps(log,indent=1,ensure_ascii=False))
print('palet L:',[int(lum(c)) for c in PAL])
print('px anders dan r5:',int((S!=R5).sum()))
