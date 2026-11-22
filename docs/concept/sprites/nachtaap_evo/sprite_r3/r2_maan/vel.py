# vel: kop 12x r2 | A | B ; hele sprite 4x en 1x (licht en donker) van alle drie
import sys; sys.path.insert(0,'r1'); from pal import *
from PIL import ImageDraw
gs=[('r2',np.load('r2/r2.npy')),('A',np.load('r2_maan/A.npy')),('B',np.load('r2_maan/B.npy'))]; W=(255,255,255)
k=[naar_img(g[32:56,1:27],12,W).convert('RGB') for _,g in gs]
h=[naar_img(g,4,W).convert('RGB') for _,g in gs]
V=Image.new('RGB',(3*(k[0].width+16),20+k[0].height+30+256+30+80),(225,225,225)); d=ImageDraw.Draw(V)
for i,(n,g) in enumerate(gs):
    x=i*(k[0].width+16); d.text((x+4,4),n+' kop 12x',fill=(0,0,0)); V.paste(k[i],(x,20))
    y=20+k[0].height+30; d.text((x+4,y-16),n+' 4x',fill=(0,0,0)); V.paste(h[i],(x,y))
    y+=256+20
    V.paste(naar_img(g,1,(248,248,248)).convert('RGB'),(x,y)); V.paste(naar_img(g,1,(40,40,48)).convert('RGB'),(x+72,y))
V.save('r2_maan/vel.png'); print(V.size)
