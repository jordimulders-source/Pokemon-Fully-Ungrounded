# vel.png: kop 12x r2 | A_sym | B_sym met hulplijn op de oogas (x=12, alleen in het vel); hele sprite 4x en 1x
import sys; sys.path.insert(0,'r1'); from pal import *
from PIL import ImageDraw
gs=[('r2',np.load('r2/r2.npy')),('A_sym',np.load('r2_maan/A_sym.npy')),('B_sym',np.load('r2_maan/B_sym.npy'))]; W=(255,255,255)
x0,y0,s=1,32,12
k=[naar_img(g[y0:56,x0:27],s,W).convert('RGB') for _,g in gs]
for im in k:
    d=ImageDraw.Draw(im); xa=int((12.5-x0)*s); d.line([(xa,0),(xa,im.height)],fill=(0,200,255),width=1)
h=[naar_img(g,4,W).convert('RGB') for _,g in gs]
V=Image.new('RGB',(3*(k[0].width+16),20+k[0].height+30+256+30+80),(225,225,225)); d=ImageDraw.Draw(V)
for i,(n,g) in enumerate(gs):
    x=i*(k[0].width+16); d.text((x+4,4),n+' kop 12x (blauw = oogas x12)',fill=(0,0,0)); V.paste(k[i],(x,20))
    y=20+k[0].height+30; d.text((x+4,y-16),n+' 4x',fill=(0,0,0)); V.paste(h[i],(x,y)); y+=276
    V.paste(naar_img(g,1,(248,248,248)).convert('RGB'),(x,y)); V.paste(naar_img(g,1,(40,40,48)).convert('RGB'),(x+72,y))
V.save('r2_maan/vel.png'); print(V.size)
