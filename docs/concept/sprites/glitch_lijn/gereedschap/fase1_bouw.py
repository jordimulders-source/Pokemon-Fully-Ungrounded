"""Fase 1 glitch-lijn: hoop 8x8-rommeltegels met vaag gezicht (test, Claude 25 nov)."""
import random, sys
from PIL import Image
W=(255,255,255)
def tile(r,pal,mode):
    t=Image.new('RGB',(8,8),W)
    for y in range(8):
        for x in range(8):
            if mode=='stripe': c=pal[(y//2)%len(pal)] if r.random()<.85 else W
            elif mode=='check': c=pal[0] if (x//2+y//2)%2 else pal[1]
            elif mode=='bits': c=r.choice(pal+[W])
            elif mode=='bars': c=pal[2] if y in (2,3) or y in (6,) else (pal[0] if r.random()<.7 else W)
            else: c=pal[0]
            t.putpixel((x,y),c)
    return t
def build(layout,pal,eye,seed,face):
    r=random.Random(seed); im=Image.new('RGB',(64,64),W)
    rows=[l.ljust(8) for l in layout]
    for ty,row in enumerate(rows):
        for tx,ch in enumerate(row):
            if ch=='#': im.paste(tile(r,pal,r.choice(['stripe','check','bits','bars','bits'])),(tx*8,ty*8))
            elif ch=='o': im.paste(tile(r,pal,'solid'),(tx*8,ty*8))
    (ex1,ey1),(ex2,ey2),(mx,my,mw)=face
    for (ex,ey),shape in (((ex1,ey1),[(0,0),(1,0),(2,1),(1,1),(3,2)]),((ex2,ey2),[(2,0),(1,0),(0,1),(1,1),(-1,2)])):
        for dx,dy in shape:
            for a in range(2):
                for b in range(2): im.putpixel((ex+dx*2+a-2,ey+dy*2+b),eye)
    for i in range(mw):
        y=my+(0 if (i//3)%2==0 else 3)+((i%3) if (i//3)%2==0 else -(i%3))
        for b in range(2): im.putpixel((mx+i,y+b),eye)
    return im
L1=["   ##   ","  ####  ","  #oo## ","  #oo## "," #####  ","########","  ####  ","  #  ## "]
L2=["    ##  ","   ###  ","  #ooo##","  #ooo# ","#####   ","  ######","  ###   ","   ##   "]
L3=["   ###  ","  ##### "," ##oo## "," ##oo#  ","  ######","######  ","   ###  ","  ## #  "]
P=[[(40,40,70),(90,70,140),(20,20,30)],[(30,60,70),(60,140,150),(15,25,30)],[(60,30,70),(150,60,150),(25,15,30)]]
E=[(250,230,40),(250,230,40),(250,240,80)]
F=[((22,24),(40,24),(18,36,26)),((28,22),(46,22),(24,34,28)),((22,24),(38,24),(18,36,24))]
out=[build(L,p,e,i*7+1,f) for i,(L,p,e,f) in enumerate(zip([L1,L2,L3],P,E,F))]
sh=Image.new('RGB',(72*3+8,80),(230,230,230))
for i,im in enumerate(out): sh.paste(im,(8+i*72,8)); im.save(f'{sys.argv[1]}/v{i+1}.png')
sh.resize((sh.size[0]*4,sh.size[1]*4),Image.NEAREST).save(f'{sys.argv[1]}/vel_v1-3.png')
