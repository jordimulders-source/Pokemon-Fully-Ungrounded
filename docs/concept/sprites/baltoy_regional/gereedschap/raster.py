# Hulpvel: huidige sprite (tekst) met rasternummers op 16x naast het natieve model met de geschrapte rijen/kolommen gemarkeerd.
import sys, numpy as np; from PIL import Image, ImageDraw
sys.path.insert(0,'gereedschap'); import schrap as S
from bouw_pal import PAL
txt=sys.argv[1]; y0,y1,x0,x1=map(int,sys.argv[2:6]); out=sys.argv[6]
g=[r for r in open(txt).read().split()]
Z=16
a=Image.new('RGB',((x1-x0)*Z+30,(y1-y0)*Z+20),'white'); d=ImageDraw.Draw(a)
for y in range(y0,y1):
    for x in range(x0,x1):
        c=g[y][x]; col=PAL[c] if c!='.' else (255,255,255)
        d.rectangle([30+(x-x0)*Z,20+(y-y0)*Z,30+(x-x0+1)*Z-1,20+(y-y0+1)*Z-1],fill=col,outline=(225,225,225) if c=='.' else None)
for x in range(x0,x1): d.text((30+(x-x0)*Z+3,4),str(x%100),fill=(0,0,200))
for y in range(y0,y1): d.text((2,20+(y-y0)*Z+3),str(y),fill=(0,0,200))
# model: kies de natieve rijen/kolommen die overblijven
kk,rr,rows,cols,*_=S.schrap_zones(48)
keepr=[i for i in range(S.H) if i not in rows]; keepc=[i for i in range(S.W) if i not in cols]
ny0,ny1=keepr[y0],keepr[min(y1,len(keepr))-1]+1; nx0,nx1=keepc[x0],keepc[min(x1,len(keepc))-1]+1
m=Image.fromarray(S.rgb[ny0:ny1,nx0:nx1].astype('uint8'))
sc=a.height/m.height
m=m.resize((int(m.width*sc),int(m.height*sc)),Image.NEAREST)
v=Image.new('RGB',(a.width+m.width+20,a.height),'white'); v.paste(a,(0,0)); v.paste(m,(a.width+20,0)); v.save(out)
