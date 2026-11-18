"""Vel: front (4x) naast icoon f1 (8x), even groot, voor kleine details. python3 front_icoon_8x.py uit.png soort ..."""
import sys,os,re,numpy as np
from PIL import Image,ImageDraw
def pal(p):
    L=open(p).read().split('\n'); n=int(L[2]); return [tuple(int(v) for v in L[3+k].split()[:3]) for k in range(n)]+[(0,0,0)]*(16-n)
IPI={}
for fn in os.listdir('src/data/pokemon/species_info'):
    for mm in re.finditer(r'\[SPECIES_([A-Z0-9_]+)\]\s*=\s*\{(.*?)\n    \},',open('src/data/pokemon/species_info/'+fn).read(),re.S):
        v=re.search(r'iconPalIndex = (?:P_GBA_STYLE_SPECIES_ICONS \? \d : )?(\d)',mm.group(2))
        if v: IPI[mm.group(1).lower()]=int(v.group(1))
def img(path,P,rows):
    a=np.array(Image.open(path))[:rows]; o=np.zeros(a.shape+(4,),np.uint8)
    for k in range(1,16): o[a==k]=P[k]+(255,)
    return Image.fromarray(o)
sps=sys.argv[2:]; C=3
W=Image.new('RGB',(C*540,((len(sps)+C-1)//C)*280),(115,197,164)); d=ImageDraw.Draw(W)
for n,sp in enumerate(sps):
    D=f'graphics/pokemon/{sp}'; fp=D+'/anim_front.png' if os.path.exists(D+'/anim_front.png') else D+'/front.png'
    f=img(fp,pal(D+'/normal.pal'),64).resize((256,256),Image.NEAREST)
    i=img(D+'/icon.png',pal(f'graphics/pokemon/icon_palettes/pal{IPI.get(sp,0)}.pal'),32).resize((256,256),Image.NEAREST)
    x,y=(n%C)*540,(n//C)*280; W.paste(f,(x,y+20),f); W.paste(i,(x+266,y+20),i); d.text((x+2,y+2),sp,fill=0)
W.save(sys.argv[1])
