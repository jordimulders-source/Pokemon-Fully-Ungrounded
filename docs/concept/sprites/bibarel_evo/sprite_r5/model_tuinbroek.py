# model_tuinbroek.py: crème borststuk/bandjes en zaklijn uit het model (r10_k8, natief) gemeten en verkleind naar het spriteraster
# (oppervlakteaandeel per spritepixel, zelfde afbeelding als toon.npy). Uitvoer: bib_frac.npy, zak_frac.npy
import numpy as np; from PIL import Image
a=np.asarray(Image.open('model/r10_k8.png').convert('RGB')).astype(float); fig=np.load('sprite_r1/masker.npy')
yy,xx=np.where(fig); x0,y0=xx.min(),yy.min(); x1,y1=xx.max()+1,yy.max()+1
crop=a[y0:y1,x0:x1]; m=fig[y0:y1,x0:x1].astype(float)
R,G,B=crop[...,0],crop[...,1],crop[...,2]; Lu=crop@[0.299,0.587,0.114]
creme=(Lu>=200)&(B>=150)&(R>=G)&(G>=B)&(R-B<=90)          # licht crème
tan=(Lu>=125)&(Lu<200)&(R>G)&(G>B)&(R-B>=50)&(R-B<=110)&(B>=75)   # zandkleurige lijnen in het borststuk
H0,W0=m.shape; s=64/W0; H=round(H0*s); oy=64-H
def wmat(N0,N):
    M=np.zeros((N,N0)); e=N0/N
    for i in range(N):
        lo,hi=i*e,(i+1)*e
        for j in range(int(lo),min(N0,int(np.ceil(hi)))): M[i,j]=max(0,min(hi,j+1)-max(lo,j))
    return M
Wy,Wx=wmat(H0,H),wmat(W0,64); den=Wy@np.ones_like(m)@Wx.T
def red(k): out=np.zeros((64,64)); out[oy:]=Wy@(k*m)@Wx.T/den; return out
# alleen het borststukgebied (natief: y 40-62, x 26-60) — buiten dat zijn crème pixels potlood/oogband
reg=np.zeros_like(m); reg[40-y0:62-y0,26-x0:60-x0]=1
bc=red(creme*reg); tc=red(tan*reg)
np.save('sprite_r5/bib_frac.npy',bc+tc); np.save('sprite_r5/zak_frac.npy',tc)
if __name__=='__main__':
    for y in range(26,46):
        print('%2d '%y+''.join('#' if bc[y,x]+tc[y,x]>=0.5 and tc[y,x]>=0.3 else ('o' if bc[y,x]+tc[y,x]>=0.5 else ('.' if bc[y,x]+tc[y,x]>=0.3 else ' ')) for x in range(14,46)))
