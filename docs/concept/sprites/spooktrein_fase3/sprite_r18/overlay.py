# Overlay: geprojecteerde modelpixels (natief.png) op een sprite, koeienvanger-uitsnede.
# rood = modellijn (lum<80), cyaan = licht (lum>150), groen ring = modelgroen.
import sys; sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/spooktrein_fase3/sprite_r18')
from proj import *
from PIL import ImageDraw
def overlay(src,out,Z=24,box=(0,42,28,61),groen=True):
    x0,y0,x1,y1=box
    im=Image.open(src).convert('RGBA')
    c=im.crop(box).resize(((x1-x0)*Z,(y1-y0)*Z),Image.NEAREST)
    bg=Image.new('RGBA',c.size,(255,255,255,255)); bg.alpha_composite(c); c=bg
    d=ImageDraw.Draw(c)
    for x in range(x1-x0+1): d.line((x*Z,0,x*Z,c.size[1]),fill=(200,200,200,255))
    for y in range(y1-y0+1): d.line((0,y*Z,c.size[0],y*Z),fill=(200,200,200,255))
    G=N[...,1]>N[...,0]+20
    for ny in range(55,90):
      for nx in range(3,46):
        if min(N[ny,nx])>215: continue
        X,Y=n2s(nx+0.5,ny+0.5); px,py=(X-x0)*Z,(Y-y0)*Z
        if G[ny,nx]:
            if groen: d.ellipse((px-3,py-3,px+3,py+3),outline=(0,160,0))
        elif LUM[ny,nx]<80: d.ellipse((px-4,py-4,px+4,py+4),fill=(255,0,0))
        elif LUM[ny,nx]>150: d.ellipse((px-3,py-3,px+3,py+3),fill=(0,200,255))
    for x in range(x1-x0): d.text((x*Z+3,2),str((x+x0)%10),fill=(0,0,255))
    for y in range(y1-y0): d.text((2,y*Z+3),str(y+y0),fill=(0,0,255))
    c.save(out)
if __name__=='__main__': overlay(sys.argv[1],sys.argv[2])
