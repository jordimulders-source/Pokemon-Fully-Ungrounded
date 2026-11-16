import sys; sys.path.insert(0,'sprite_r1')
from groepen import laad; import numpy as np; from PIL import Image, ImageDraw
a,lum,g=laad('sprite_r2/natief.png')
im=Image.open('sprite_r2/pitahaya_r2.png'); S=np.array(im); H=S>0
TH=int(sys.argv[1]) if len(sys.argv)>1 else 85
def edge(x,y): return any(not H[y+dy,x+dx] for dy,dx in((1,0),(-1,0),(0,1),(0,-1)))
face=lambda x,y: 18<=x<=34 and 22<=y<=34
mis=[];ext=[]
for y in range(6,37):
  for x in range(14,48):
    if not H[y,x] or edge(x,y) or face(x,y): continue
    r=3*(y+2); c=1+3*(x+1); b=lum[r:r+3,c:c+3]; gb=g[r:r+3,c:c+3]
    nd=((b<TH)&(gb!=0)&(gb!=4)).sum()   # donker, niet groen
    ndg=((b<60)&(gb!=0)).sum()
    isl=S[y,x] in (1,2)
    if nd>=2 and not isl and S[y,x] in (3,4,5): mis.append((x,y,nd))
    if isl and nd<=1: ext.append((x,y,int(S[y,x]),nd))
print('model-naad, sprite vlak:',len(mis),mis)
print('sprite naad/lijn, model geen:',len(ext),ext)
