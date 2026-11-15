# frac.py x0 x1 y0 y1 : per spritecel aandeel modelpixels per groep (D=donker lum<95, L=lila, C=creme) als cijfer 0-9
import sys, numpy as np
from PIL import Image
from reduceer import fig, X0,X1,Y0,Y1, wts, W, H
x0,x1,y0,y1=map(int,sys.argv[1:5]); tw=50; th=45
Wx=wts(X0,X1,tw)[:, :W]; Wy=wts(Y0,Y1,th)[:, :H]
Wx=np.pad(Wx,((0,0),(0,W-Wx.shape[1]))); Wy=np.pad(Wy,((0,0),(0,H-Wy.shape[1])))
n=np.asarray(Image.open('natief.png').convert('RGB')).astype(float); lum=n@[0.299,0.587,0.114]
r,g,b=n[...,0],n[...,1],n[...,2]
M={'D':(lum<95)&fig,'L':(b>r-30)&(b>g+8)&fig,'C':(r>200)&(g>190)&(b<190)&fig}
f=fig.astype(float); den=np.maximum(Wy@f@Wx.T,1e-9)
fr={k:(Wy@m.astype(float)@Wx.T)/den for k,m in M.items()}
print('    '+'  '.join('%-3d'%i for i in range(x0,x1)))
for j in range(y0,y1):
    print('%2d  '%j+'  '.join(''.join(str(min(9,int(fr[k][j,i]*10))) for k in 'DLC') for i in range(x0,x1)))
