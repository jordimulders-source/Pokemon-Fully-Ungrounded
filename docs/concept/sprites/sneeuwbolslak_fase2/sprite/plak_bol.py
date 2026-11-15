# r8 (lijf/staart) + bol van r7 (Jordi 15 nov: "a, de bol van r7"); zelfde raster, 1-op-1.
import numpy as np; from PIL import Image
r7=np.array(Image.open('gemini/r7_gemini.png').convert('RGB')).astype(int)
r8=np.array(Image.open('gemini/r8_gemini.png').convert('RGB')).astype(int)
H,W,_=r8.shape; yy,xx=np.mgrid[0:H,0:W]
cx,cy=xx-370,yy-200  # cropcoördinaten
m=(cx>=0)&(cx<=350)&(cy>=0)&(cy<=305)
m&=~((cx>335)&(cy>150))   # staart
m&=~((cx<45)&(cy>265))    # kop/lijf linksonder
green=(abs(r7-np.array([128,230,136])).sum(2)<60)
use=m&~green
out=r8.copy(); out[use]=r7[use]
Image.fromarray(out.astype('uint8')).save('sprite/r8_bol_r7.png')
# groenige randpixels (anti-alias van r7's groene achtergrond) -> pixel van r8
o=np.array(Image.open('sprite/r8_bol_r7.png')).astype(int)
g=(o[...,1]-np.maximum(o[...,0],o[...,2])>25); print('groen weg:',g.sum())
o[g]=r8[g];  # zelfde raster: r8 heeft daar dezelfde omlijning op wit
Image.fromarray(o.astype('uint8')).save('sprite/r8_bol_r7.png')
