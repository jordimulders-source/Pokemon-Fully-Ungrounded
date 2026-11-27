# Varianten op r5b: alleen de maan verschuiven (omhoog / links / linksboven). Alleen verplaatsen.
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
s=Image.open('r5/regicosmo_r5b.png'); a=np.array(s)
lab,n=ndimage.label(a>0,structure=np.ones((3,3)))
objs=ndimage.find_objects(lab)
# maan = deel rechts met middelpunt-y tussen 38 en 52
maan=[i for i in range(n) if objs[i][1].start>40 and 36<(objs[i][0].start+objs[i][0].stop)/2<54][0]
M=lab==maan+1; rest=(a>0)&~M
d=ndimage.distance_transform_cdt(~rest,metric='chessboard')
vs=[('omhoog1',0,-1),('omhoog2',0,-2),('omhoog3',0,-3),('links1',-1,0),('links2',-1*2,0),('linksboven1',-1,-1),('linksboven2',-2,-2),('lb_2op1links',-1,-2)]
tiles=[('r5b',a)]
yy,xx=np.nonzero(M)
for naam,dx,dy in vs:
    out=a.copy(); out[M]=0; out[yy+dy,xx+dx]=a[yy,xx]
    gap=d[yy+dy,xx+dx].min()-1
    o=Image.fromarray(out,'P'); o.putpalette(s.getpalette()); o.save(f'r6/r6_{naam}.png',transparency=0)
    tiles.append((f'{naam} (ruimte {gap}px)',out))
S=4; W=64*S
vel=Image.new('RGB',(3*(W+12)+12,3*(W+34)+12),(200,200,200)); dr=ImageDraw.Draw(vel)
pal=np.array(s.getpalette()[:48]).reshape(16,3)
for k,(t,arr) in enumerate(tiles):
    rgb=pal[arr].astype('uint8'); rgb[arr==0]=255
    im=Image.fromarray(rgb).resize((W,W),Image.NEAREST)
    x=12+(k%3)*(W+12); y=12+(k//3)*(W+34)
    dr.text((x,y),t,fill=(0,0,0)); vel.paste(im,(x,y+16))
vel.save('r6/vel_maan.png')
