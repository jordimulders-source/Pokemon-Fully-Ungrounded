# Model = r8 (ogen, bolle achterlijfvorm) met strepen zoals r7 op het achterlijf (Jordi, 20 nov).
# Strepen = gebogen banden (ringen rond een punt links van het achterlijf), periode en tinten gemeten op r7.
import numpy as np
from PIL import Image
r8=np.array(Image.open('gemini/r8.png').convert('RGB')).astype(int)
r,g,b=r8[...,0],r8[...,1],r8[...,2]
v=r8.mean(-1)
neutral=(abs(r-g)<14)&(abs(g-b)<14)&(abs(r-b)<14)
H,W=v.shape; yy,xx=np.mgrid[0:H,0:W]
m=neutral&(v>25)&(v<215)&(xx>=566)&(xx<900)&(yy>=360)&(yy<720)
CX,CY,P,B=380,470,88,16          # ringcentrum, periode, blokgrootte
LIGHT=[(184,184,184),(160,160,160),(128,136,136)]   # r7-tinten licht (boven → onder)
DARK=[(64,64,64),(56,56,56),(32,32,32)]
ys,xs=np.where(m); top,bot=ys.min(),ys.max()
out=r8.copy()
for y,x in zip(ys,xs):
    bx,by=(x//B)*B+B/2,(y//B)*B+B/2
    d=np.hypot(bx-CX,(by-CY)*1.3)
    dark=((d-215)%P)<P/2
    t=(by-top)/(bot-top+1)+(bx-600)/900
    k=0 if t<0.45 else (1 if t<0.8 else 2)
    out[y,x]=(DARK if dark else LIGHT)[k]
Image.fromarray(out.astype('uint8')).save('model/model.png')
