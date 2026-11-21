# hulpbeeld: klassenraster 64x64 (npy) op 10x met rasterlijnen/coördinaten naast het natieve model op dezelfde schaal en plaats
import numpy as np, sys, json; from PIL import Image, ImageDraw
from palet import pal
o=np.load(sys.argv[1]); fam=np.load(sys.argv[2]) if sys.argv[2]!='-' else None; z=10
F,OY,OX=2.9,0,0.97; pl=json.load(open('plaats.json'))
P=pal(sys.argv[4] if len(sys.argv)>4 else 'model'); H,W=o.shape
im=Image.new('RGB',(W*z*2+60,H*z+20),'white'); d=ImageDraw.Draw(im)
for y in range(H):
    for x in range(W):
        v=o[y,x]; c=P[v] if v else (235,235,235)
        if fam is not None and v==1 and fam[y,x]>0: c=[(0,0,0),(0,90,0),(150,110,0),(140,40,60)][fam[y,x]]
        d.rectangle([30+x*z,20+y*z,30+x*z+z-1,20+y*z+z-1],fill=c,outline=(200,200,200))
for x in range(0,W,5): d.text((30+x*z,4),str(x),fill='black')
for y in range(0,H,5): d.text((2,20+y*z),str(y),fill='black')
n=Image.open('natief.png'); s=z/F
nm=n.resize((int(200*s),int(200*s)),Image.NEAREST)
X0=60+W*z; im.paste(nm,(int(X0+(pl['dx']*z)-OX*s),int(20+pl['dy']*z-OY*s)))
d.rectangle([W*z+30,0,W*z+58,H*z+20],fill='white')
for x in range(0,W,5): d.line([X0+x*z,20,X0+x*z,25],fill='red')
for y in range(0,H,5): d.line([X0,20+y*z,X0+5,20+y*z],fill='red')
im.save(sys.argv[3])
