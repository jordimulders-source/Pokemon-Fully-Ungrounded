# omtrek.py sprite.png uit.png x0 y0 x1 y1 z : sprite op z-voud met de modelomtrek (masker alpha>=0.45, rood) en modelrand op subpixel (blauw) erover. Meting.
import sys,json,numpy as np; from PIL import Image, ImageDraw
G='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/hitmontop_evo/sprite_gemini/ronde3/gereedschap/'
k=json.load(open(G+'kader.json')); X0,Y0,s=k['x0'],k['y0'],k['s']
x0,y0,x1,y1,z=map(int,sys.argv[3:8])
mo=np.asarray(Image.open(G+k['model']).convert('RGBA'))[...,3]>0
sp=Image.open(sys.argv[1]).convert('RGBA'); b=Image.new('RGBA',sp.size,(152,208,160,255)); b.alpha_composite(sp)
im=b.convert('RGB').crop((x0,y0,x1,y1)).resize(((x1-x0)*z,(y1-y0)*z),Image.NEAREST); d=ImageDraw.Draw(im)
# modelmasker op z-resolutie
H,W=mo.shape
for py in range(0,(y1-y0)*z,2):
  for px in range(0,(x1-x0)*z,2):
    mx=int(X0+(x0+px/z)*s); my=int(Y0+(y0+py/z)*s)
    mx2=int(X0+(x0+(px+2)/z)*s); my2=int(Y0+(y0+(py+2)/z)*s)
    if 0<=my<H and 0<=mx<W and 0<=my2<H and 0<=mx2<W:
      if mo[my,mx]!=mo[my,mx2] or mo[my,mx]!=mo[my2,mx]: d.rectangle([px,py,px+1,py+1],fill=(255,0,0))
for x in range(x0,x1+1): d.line([((x-x0)*z,0),((x-x0)*z,4)],fill=(0,0,0))
for x in range((x0+4)//5*5,x1,5): d.text(((x-x0)*z+2,6),str(x),fill=(0,0,0))
for y in range((y0+4)//5*5,y1,5): d.text((2,(y-y0)*z+2),str(y),fill=(0,0,0))
im.save(sys.argv[2])
