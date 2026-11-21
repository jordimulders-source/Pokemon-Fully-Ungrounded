# hulpbeeld: uitsnede (y0,y1,x0,x1) van een of meer klassenrasters (palet A) en het model op dezelfde schaal, z-voudig, met raster
import sys, numpy as np; from PIL import Image, ImageDraw; from palet import pal
from modeltoon import r,c,DY,DX
nat=Image.open('natief.png').convert('RGB')
p=pal('A_donker'); z=12
def img(a): return Image.fromarray(np.array([(255,255,255)]+p[1:],dtype='uint8')[a])
out=sys.argv[1]; y0,y1,x0,x1=map(int,sys.argv[2:6]); fs=sys.argv[6:]
ims=[img(np.load(f)).crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST) for f in fs]
# model: natieve cellen van spritepixel (y,x) = rij r[y-DY], kol c[x-DX]; 2 microcellen per spritepixel -> exacte uitsnede
ra=r[y0-DY] if y0-DY>=0 else r[0]; ca=c[x0-DX] if x0-DX>=0 else c[0]
m=nat.crop((ca,ra,ca+(x1-x0)*2,ra+(y1-y0)*2)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST); ims.append(m)
W=Image.new('RGB',(sum(i.width+12 for i in ims),ims[0].height+16),(200,200,200)); d=ImageDraw.Draw(W); x=0
for i,im in enumerate(ims):
    dd=ImageDraw.Draw(im)
    for k in range(0,im.width,z): dd.line([(k,0),(k,im.height)],fill=(180,180,180))
    for k in range(0,im.height,z): dd.line([(0,k),(im.width,k)],fill=(180,180,180))
    W.paste(im,(x,16)); d.text((x+2,2),(fs+['model'])[i]+' y%d x%d'%(y0,x0),fill='black'); x+=im.width+12
W.save(out)
