# Palpaca r1 stap 1: oppervlakgewogen reductie van het natieve model (zones_nat.npy) naar ±48 px hoog.
# Uit: onderlaag.png (kale reductie in modelkleuren, dichtstbijzijnde natieve modelkleur), zone_t.npy, tone_t.npy, rgb_t.npy
import numpy as np; from PIL import Image
N=np.asarray(Image.open('natief.png').convert('RGB')).astype(float); Lum=N.mean(2)
Z=np.load('zones_nat.npy'); H0,W0=Z.shape
fgn=Z!='.'; ys,xs=np.nonzero(fgn)
x0,x1,y0,y1=xs.min(),xs.max()+1,ys.min(),ys.max()+1
TH=48; s=(y1-y0)/TH; TW=int(np.ceil((x1-x0)/s))
OX=-((TW*s-(x1-x0))/2); OY=0.0
def Wm(n0,cnt,off,n):
    M=np.zeros((cnt,n))
    for j in range(cnt):
        a=n0+off+j*s; b=a+s
        for k in range(int(np.floor(a)),int(np.ceil(b))):
            if 0<=k<n: M[j,k]=max(0,min(b,k+1)-max(a,k))
    return M
Wx=Wm(x0,TW,OX,W0); Wy=Wm(y0,TH,OY,H0)
red=lambda m: Wy@m.astype(float)@Wx.T/(s*s)
zl=['K','W','D','G','T','P','C','E']
fr={z:red(Z==z) for z in zl}; fg=red(fgn)
# lijnkaart: modellijnen (K-componenten >= 8 natieve px) als dunne lijn: cel is lijn als hij op de lijn het maximum is (niet-maximum-onderdrukking)
from scipy import ndimage
lab,n=ndimage.label(Z=='K',structure=np.ones((3,3))); sz=ndimage.sum(Z=='K',lab,range(1,n+1))
Kl=np.isin(lab,1+np.where(sz>=8)[0]); kf=red(Kl); np.save('kf.npy',kf)
pad=np.pad(kf,1)
nms=((kf>=pad[:-2,1:-1])&(kf>=pad[2:,1:-1]))|((kf>=pad[1:-1,:-2])&(kf>=pad[1:-1,2:]))
lijn=(kf>=0.2)&nms
def zmean(arr,z):
    m=(Z==z).astype(float); return (Wy@(arr*m)@Wx.T)/np.maximum(Wy@m@Wx.T,1e-6)
tone={z:zmean(Lum,z) for z in zl}
rgbz={z:np.stack([zmean(N[...,c],z) for c in range(3)],2) for z in zl}
zone=np.full((TH,TW),'.',dtype='<U1'); T=np.zeros((TH,TW)); C=np.zeros((TH,TW,3))
for y in range(TH):
  for x in range(TW):
    if fg[y,x]<(0.40 if (x>=22 and y<=22) else 0.45): continue  # staartpluim: 0.40 houdt de ronde bovenkant van het model (vak 25,20 = 0.42)
    if fr['E'][y,x]>=0.3: z='E'
    elif lijn[y,x] or fr['K'][y,x]>=0.34: z='K'
    else:
        c={k:fr[k][y,x] for k in zl if k not in('K','E')}; z=max(c,key=c.get)
        if fr['C'][y,x]>=0.25: z='C'
    zone[y,x]=z; T[y,x]=tone[z][y,x]; C[y,x]=rgbz[z][y,x]
np.save('zone_t.npy',zone); np.save('tone_t.npy',T); np.save('rgb_t.npy',C)
np.save('fg_t.npy',fg)
mc=np.unique(N[fgn].astype(int),axis=0)
ond=np.zeros((TH,TW,4),'uint8')
for y in range(TH):
  for x in range(TW):
    if zone[y,x]!='.':
        d=((mc-C[y,x])**2).sum(1); ond[y,x,:3]=mc[d.argmin()]; ond[y,x,3]=255
Image.fromarray(ond,'RGBA').save('../onderlaag.png')
print('doel',TW,'x',TH,'schaal',round(s,3))
for y in range(TH): print('%2d '%y+''.join(zone[y]))
