# r16 op de schaal van Jordi's krabbel (10,02 px/spritepixel, offset 8,3), met zijn gele en groene lijnen erover.
import numpy as np; from PIL import Image
D='docs/concept/sprites/hitmonlee_regional/'
S,OX,OY=10.02,8.0,3.0
k=np.array(Image.open(D+'jordi/krabbel_benen.png').convert('RGB')).astype(int)
R,G,B=k[...,0],k[...,1],k[...,2]
yel=(R>160)&(G>190)&(B<140)&(G>R)&(G-B>60)          # Jordi's geel (201,218,82)
grn=(G>195)&(G-R>80)&(G-B>60)                 # Jordi's groen
r16=Image.open(D+'sprite/r16/r16.png').convert('RGBA'); a=np.array(r16)
H,W=k.shape[:2]; out=np.zeros((H,W,3),np.uint8); out[:]=(152,208,160)
ys,xs=np.mgrid[0:H,0:W]
sx=np.floor((xs-OX)/S).astype(int); sy=np.floor((ys-OY)/S).astype(int)
ok=(sx>=0)&(sx<64)&(sy>=0)&(sy<64)
px=np.zeros((H,W,4),np.uint8); px[ok]=a[sy[ok],sx[ok]]
m=px[...,3]>0; out[m]=px[m][:,:3]
# raster lichtjes
out[((xs-OX)%S<1)|((ys-OY)%S<1)]=(out[((xs-OX)%S<1)|((ys-OY)%S<1)]*0.85).astype(np.uint8)
out[yel]=(255,230,0); out[grn]=(0,230,90)
Image.fromarray(out).save(D+'sprite/r16/overlay_krabbel.png')
