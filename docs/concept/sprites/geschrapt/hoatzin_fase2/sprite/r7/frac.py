# aandeel per spritecel (canvas) van een modelmasker; gebruik als module: frac(masker_natief) -> 64x64
import numpy as np; from PIL import Image
N=np.asarray(Image.open('natief.png').convert('RGB')).astype(float); Ln=N.mean(2)
Zn=np.load('zones_nat.npy'); fgn=Zn!='.'
ys,xs=np.where(fgn); x0,y0=xs.min(),ys.min(); TH=63; s=(ys.max()+1-y0)/TH; TW=51; X0,Y0=6,1
H,W=Ln.shape
def Wm(n0,cnt,n):
    M=np.zeros((cnt,n))
    for j in range(cnt):
        a=n0+j*s; b=a+s
        for k in range(int(np.floor(a)),int(np.ceil(b))):
            if 0<=k<n: M[j,k]=max(0,min(b,k+1)-max(a,k))
    return M
Wx=Wm(x0,TW,W); Wy=Wm(y0,TH,H)
def frac(m):
    o=np.zeros((64,64)); o[Y0:,X0:X0+TW]=Wy@m.astype(float)@Wx.T/(s*s); return o
def mean(v,m):
    o=np.zeros((64,64)); o[Y0:,X0:X0+TW]=(Wy@(v*m)@Wx.T)/np.maximum(Wy@m.astype(float)@Wx.T,1e-6); return o
