# Hummlet r1: kale reductie (onderlaag) -> palet (stap A) -> technisch opschonen (B) -> Gen 3-licht (C)
import numpy as np; from PIL import Image
N=np.asarray(Image.open('natief.png').convert('RGB')).astype(float); Lum=N.mean(2)
Z=np.load('zones_nat.npy')
TW=40; x0,x1,y0,y1=12,89,19,86; s=(x1-x0)/TW; TH=int(round((y1-y0)/s)); OX=OY=-0.5; LT=0.28
def W(n0,cnt,off,n):
    M=np.zeros((cnt,n))
    for j in range(cnt):
        a=n0+off+j*s; b=a+s
        for k in range(int(np.floor(a)),int(np.ceil(b))):
            if 0<=k<n: M[j,k]=max(0,min(b,k+1)-max(a,k))
    return M
Wx=W(x0,TW,OX,100); Wy=W(y0,TH,OY,100)
red=lambda m: Wy@m.astype(float)@Wx.T/(s*s)
zl=['K','L','W','P','V','F','Y','S','E']
fr={z:red(Z==z) for z in zl}; fg=red(Z!='.')
mean={z:(Wy@(Lum*(Z==z))@Wx.T)/np.maximum(Wy@(Z==z).astype(float)@Wx.T,1e-6) for z in zl}
rgb={z:np.stack([(Wy@(N[...,c]*(Z==z))@Wx.T)/np.maximum(Wy@(Z==z).astype(float)@Wx.T,1e-6) for c in range(3)],2) for z in zl}
zone=np.full((TH,TW),'.',dtype='<U1'); tone=np.zeros((TH,TW))
col=np.zeros((TH,TW,3))
for y in range(TH):
  for x in range(TW):
    if fg[y,x]<0.45: continue
    if fr['E'][y,x]>=0.3: z='E'
    elif fr['K'][y,x]>=LT: z='K'
    elif fr['Y'][y,x]>=0.12: z='Y'
    else:
        c={k:fr[k][y,x] for k in zl if k!='K'}
        z=max(c,key=c.get)
        if z=='W' and fr['P'][y,x]>=0.25*fg[y,x]: z='P'
        if z=='P' and fr['P'][y,x]<0.25*fg[y,x]: z='W'
    zone[y,x]=z; tone[y,x]=mean[z][y,x]; col[y,x]=rgb[z][y,x] if z!='K' else (12,10,20)
np.save('zone_t.npy',zone); np.save('tone_t.npy',tone)
# onderlaag: kale reductie in modelkleuren (gemiddelde van de zone in de cel, dichtstbijzijnde natieve modelkleur)
modelcols=np.unique((N[Z!='.']).astype(int),axis=0)
ond=np.zeros((TH,TW,4),'uint8')
for y in range(TH):
  for x in range(TW):
    if zone[y,x]!='.':
        d=((modelcols-col[y,x])**2).sum(1); ond[y,x,:3]=modelcols[d.argmin()]; ond[y,x,3]=255
Image.fromarray(ond,'RGBA').save('onderlaag.png')
# stap A: zones/tonen op het oude palet
def pal(z,l,y=0):
    if z=='K': return 1
    if z=='L': return 5 if l>=178 else 4 if l>=(148 if y<9 else 138) else 3 if l>=110 else 2
    if z=='W': return 6 if l>=212 else 5
    if z=='P': return 3 if l<140 else 4
    if z=='V': return 8 if l>=90 else 10
    if z=='S': return 3 if l>=100 else 2
    if z=='F': return 13 if l>=128 else 9 if l>=85 else 15
    if z=='Y': return 12
    if z=='E': return 1 if l<70 else 14 if l<170 else 7
A=np.zeros((TH,TW),int)
for y in range(TH):
  for x in range(TW):
    if zone[y,x]!='.': A[y,x]=pal(zone[y,x],tone[y,x],y)
np.save('stapA.npy',A)
print(TW,TH,(A>0).sum())
for y in range(TH): print('%2d '%y+''.join('.' if v==0 else '0123456789abcdef'[v] for v in A[y]),'  ',''.join(zone[y]))
