# Hulpmiddel: sprite (npy of png) op 8x naast het natieve model op dezelfde schaal. Gebruik: python3 toon.py bestand uit.png [x0 y0 x1 y1 schaal]
import sys, numpy as np; from PIL import Image
from gemeen import rgb
f=sys.argv[1]; o=np.load(f) if f.endswith('.npy') else np.array(Image.open(f))
nat=np.asarray(Image.open('natief.png'))[1:92,13:88]   # figuur 75x91
box=[int(v) for v in sys.argv[3:7]] if len(sys.argv)>6 else [0,0,64,64]; S=int(sys.argv[7]) if len(sys.argv)>7 else 8
a=Image.fromarray(rgb(o,bg=(255,255,255))).crop(box); a=a.resize((a.width*S,a.height*S),Image.NEAREST)
# model op dezelfde plek: sprite-figuur x7-57, y1-62 <-> natief 75x91
X0,Y0=6,1; sx=75/51; sy=91/62
m=Image.fromarray(nat).resize((round(51*S),round(62*S)),Image.NEAREST)
mm=Image.new('RGB',(64*S,64*S),'white'); mm.paste(m,(X0*S,Y0*S)); mm=mm.crop([v*S for v in box])
c=Image.new('RGB',(a.width*2+16,a.height),'white'); c.paste(a,(0,0)); c.paste(mm,(a.width+16,0)); c.save(sys.argv[2])
