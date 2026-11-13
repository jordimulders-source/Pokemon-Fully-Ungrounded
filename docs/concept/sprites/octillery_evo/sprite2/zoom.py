# zoom.py raster x0 y0 x1 y1 uit.png [k] : model (met spriteraster) | sprite, k px per cel, met coordinaten
import cfg,sys
from PIL import Image,ImageDraw
a=cfg.read(sys.argv[1]); x0,y0,x1,y1=map(int,sys.argv[2:6]); k=int(sys.argv[7]) if len(sys.argv)>7 else 16
src=Image.open(cfg.MODEL).convert('RGB')
bx=cfg.X0+(x0-cfg.LEFT)*cfg.S; by=cfg.Y0+(y0-cfg.TOP)*cfg.S
w=x1-x0; h=y1-y0
m=src.crop((int(round(bx)),int(round(by)),int(round(bx+w*cfg.S)),int(round(by+h*cfg.S)))).resize((w*k,h*k),Image.LANCZOS)
s=cfg.rgba(a,(208,208,176,255)).crop((x0,y0,x1,y1)).resize((w*k,h*k),Image.NEAREST)
M=18
v=Image.new('RGB',(2*w*k+3*M,h*k+M),(255,255,255)); d=ImageDraw.Draw(v)
for im,ox in ((m,M),(s,2*M+w*k)):
    v.paste(im,(ox,M))
    for i in range(w+1): d.line([(ox+i*k,M),(ox+i*k,M+h*k)],fill=(0,0,0) if (x0+i)%5==0 else (150,150,150) if im is m else (190,190,160),width=1)
    for j in range(h+1): d.line([(ox,M+j*k),(ox+w*k,M+j*k)],fill=(0,0,0) if (y0+j)%5==0 else (150,150,150) if im is m else (190,190,160),width=1)
    for i in range(w):
        if (x0+i)%5==0: d.text((ox+i*k+1,3),str(x0+i),fill=(0,0,0))
    for j in range(h):
        if (y0+j)%5==0: d.text((ox-M+1 if im is m else ox-M+1,M+j*k+1),str(y0+j),fill=(0,0,0))
v.save(sys.argv[6])
