# Hoatzin r1: kale reductie van het natieve model (oppervlakgewogen) -> zones + tonen -> onderlaag.png
import sys, numpy as np; from PIL import Image
N=np.asarray(Image.open('natief.png').convert('RGB')).astype(float); Lum=N.mean(2)
Z=np.load('zones_nat.npy'); fgn=Z!='.'
ys,xs=np.where(fgn); x0,x1,y0,y1=xs.min(),xs.max()+1,ys.min(),ys.max()+1
TH=63; s=(y1-y0)/TH; TW=int(np.ceil((x1-x0)/s))
OX=float(sys.argv[1]) if len(sys.argv)>1 else 0.0; OY=float(sys.argv[2]) if len(sys.argv)>2 else 0.0
def Wm(n0,cnt,off,n):
    M=np.zeros((cnt,n))
    for j in range(cnt):
        a=n0+off+j*s; b=a+s
        for k in range(int(np.floor(a)),int(np.ceil(b))):
            if 0<=k<n: M[j,k]=max(0,min(b,k+1)-max(a,k))
    return M
Wx=Wm(x0,TW,OX,N.shape[1]); Wy=Wm(y0,TH,OY,N.shape[0])
red=lambda m: Wy@m.astype(float)@Wx.T/(s*s)
zl=['K','M','C','F','P','T','S','E','D','W']
fr={z:red(Z==z) for z in zl}; fg=red(fgn)
den={z:np.maximum(Wy@(Z==z).astype(float)@Wx.T,1e-6) for z in zl}
rgb={z:np.stack([(Wy@(N[...,c]*(Z==z))@Wx.T)/den[z] for c in range(3)],2) for z in zl}
import os
DREMPEL={'E':0.22,'K':0.34,'C':float(os.environ.get('DC',0.35)),'F':0.30,'S':0.30,'W':float(os.environ.get('DW',0.22))}
zone=np.full((TH,TW),'.',dtype='<U1'); col=np.zeros((TH,TW,3))
for y in range(TH):
  for x in range(TW):
    if fg[y,x]<0.45: continue
    z=None
    for k in ['E','K','C','F','S','W']:
        if fr[k][y,x]>=DREMPEL[k]: z=k; break
    if z is None:
        c={k:fr[k][y,x] for k in zl if k not in 'KW'}; z=max(c,key=c.get)
    zone[y,x]=z; col[y,x]=rgb[z][y,x]
np.save('zone_t.npy',zone); np.save('col_t.npy',col); np.save('fk_t.npy',fr['K']); np.save('fd_t.npy',fr['D']); np.save('fw_t.npy',fr['W'])
modelcols=np.unique(N[fgn].astype(int),axis=0)
ond=np.zeros((64,64,4),'uint8'); X0=(64-TW)//2; Y0=64-TH
for y in range(TH):
  for x in range(TW):
    if zone[y,x]!='.':
        d=((modelcols-col[y,x])**2).sum(1); ond[Y0+y,X0+x,:3]=modelcols[d.argmin()]; ond[Y0+y,X0+x,3]=255
Image.fromarray(ond,'RGBA').save('onderlaag.png')
Image.fromarray(ond,'RGBA').resize((512,512),Image.NEAREST).save('onderlaag_8x.png')
print('TW',TW,'TH',TH,'s',round(s,3),'X0',X0,'Y0',Y0,'px',(zone!='.').sum(),'oog',(zone=='E').sum())
for y in range(TH): print('%2d '%y+''.join(zone[y]))
