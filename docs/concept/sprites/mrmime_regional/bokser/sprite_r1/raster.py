# Toont sprite (npy-raster of png) en model per spritecel naast elkaar met coordinaten. Gebruik: raster.py IN.npy|png UIT.png [y0 y1 x0 x1] [schaal]
import sys; from PIL import Image, ImageDraw; import numpy as np
sys.path.insert(0,'.'); from palet import PAL, TONEN
IN,UIT=sys.argv[1],sys.argv[2]
if IN.endswith('.npy'): g=np.load(IN)
else: g=np.asarray(Image.open(IN))
if g.shape==(64,64): OFF=(0,0)
y0,y1,x0,x1=(map(int,sys.argv[3:7]) if len(sys.argv)>6 else (0,g.shape[0],0,g.shape[1]))
Z=int(sys.argv[7]) if len(sys.argv)>7 else 14
m=Image.open('../r12.png').convert('RGB')
# model-uitsnede die overeenkomt met het 43x63-raster: natief (12..72, 5..93), pitch 10.24, fase 9.25
p=10.24; ph=9.25+1; s=88/63
def mod_xy(i,j): return (ph+(12+i*s)*p, ph+(5+j*s)*p)
ox,oy=(int(sys.argv[8]),int(sys.argv[9])) if len(sys.argv)>9 else (0,0)  # verschuiving sprite t.o.v. 43x63
w=(x1-x0)*Z; h=(y1-y0)*Z
o=Image.new('RGB',(2*w+20,h+16),(255,255,255)); d=ImageDraw.Draw(o)
for j in range(y0,y1):
    for i in range(x0,x1):
        v=int(g[j,i]); c=(200,230,200) if v==0 else TONEN[v]
        d.rectangle([(i-x0)*Z,16+(j-y0)*Z,(i-x0+1)*Z-1,16+(j-y0+1)*Z-1],fill=c)
        a0=mod_xy(i-ox,j-oy); a1=mod_xy(i-ox+1,j-oy)
        crop=m.crop((int(a0[0]),int(a0[1]),int(a1[0]),int(a0[1]+s*p))).resize((Z,Z),Image.NEAREST)
        o.paste(crop,(w+20+(i-x0)*Z,16+(j-y0)*Z))
for i in range(x0,x1):
    if i%2==0: d.text(((i-x0)*Z+1,2),str(i%100),fill=(255,0,0)); d.text((w+20+(i-x0)*Z+1,2),str(i%100),fill=(255,0,0))
for j in range(y0,y1):
    if j%2==0: d.text((w+2,16+(j-y0)*Z),str(j),fill=(255,0,0))
for k in range(x0,x1+1):
    d.line([((k-x0)*Z,16),((k-x0)*Z,16+h)],fill=(180,180,255)); d.line([(w+20+(k-x0)*Z,16),(w+20+(k-x0)*Z,16+h)],fill=(255,150,150))
for k in range(y0,y1+1):
    d.line([(0,16+(k-y0)*Z),(w,16+(k-y0)*Z)],fill=(180,180,255)); d.line([(w+20,16+(k-y0)*Z),(2*w+20,16+(k-y0)*Z)],fill=(255,150,150))
o.save(UIT)
