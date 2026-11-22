# Model (1024²) op het spriteraster gelegd in de driehoekzone: model met rasterlijnen + spritecoördinaten naast r4B.
import numpy as np
from PIL import Image, ImageDraw
M=Image.open('referenties/gemini_gekozen_r1.png').convert('RGB'); a=np.array(M).astype(int)
bg=a.min(-1)>235; ys,xs=np.where(~bg); X0,Y0,X1,Y1=xs.min(),ys.min(),xs.max()+1,ys.max()+1
# sprite: figuur x4..59, y1..63
sx=(X1-X0)/56; sy=(Y1-Y0)/63
def m2s(x,y): return 4+(x-X0)/sx, 1+(y-Y0)/sy
x0,x1,y0,y1=18,42,28,52   # spritezone
Z=20
def model_zone():
    W=(x1-x0)*Z; H=(y1-y0)*Z
    out=Image.new('RGB',(W,H))
    for j in range(H):
        for i in range(W):
            sxp=x0+i/Z; syp=y0+j/Z
            mx=X0+(sxp-4)*sx; my=Y0+(syp-1)*sy
            out.putpixel((i,j),M.getpixel((int(mx),int(my))))
    return out
def sprite_zone(p):
    s=Image.open(p); s.save('/tmp/claude-0/s.png',transparency=0); s=Image.open('/tmp/claude-0/s.png').convert('RGBA')
    bgc=Image.new('RGBA',s.size,(200,225,205,255)); bgc.alpha_composite(s)
    return bgc.convert('RGB').crop((x0,y0,x1,y1)).resize(((x1-x0)*Z,(y1-y0)*Z),Image.NEAREST)
def grid(im):
    d=ImageDraw.Draw(im)
    for k in range(x1-x0+1): d.line([(k*Z,0),(k*Z,im.height)],fill=(255,0,0) if (x0+k)%5==0 else (120,120,120))
    for k in range(y1-y0+1): d.line([(0,k*Z),(im.width,k*Z)],fill=(255,0,0) if (y0+k)%5==0 else (120,120,120))
    for k in range(0,x1-x0,2): d.text((k*Z+2,2),str(x0+k),fill=(255,0,0))
    for k in range(0,y1-y0,2): d.text((2,k*Z+2),str(y0+k),fill=(255,0,0))
    return im
A=grid(model_zone()); B=grid(sprite_zone('sprite_r4/mug_r4B.png'))
v=Image.new('RGB',(A.width*2+20,A.height),'white'); v.paste(A,(0,0)); v.paste(B,(A.width+20,0)); v.save('raster/driehoek_model_vs_r4B.png')
