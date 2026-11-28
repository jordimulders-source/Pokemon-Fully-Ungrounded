"""Grid (tekst) -> icon PNG (pal0) + vel 8x naast front en Banette/Shuppet. python3 render.py grid.txt naam"""
import sys,numpy as np
from PIL import Image
D='docs/concept/sprites/banette_evo/'
K={'.':0,'O':15,'o':14,'g':1,'G':2,'W':3,'r':6,'p':11,'k':10,'y':5,'b':4}
IP=np.array([[int(v) for v in l.split()[:3]] for l in open('graphics/pokemon/icon_palettes/pal0.pal').read().split('\n')[3:19]])
def lees(fn):
    L=[l.rstrip('\n') for l in open(fn) if not l.startswith('#')]
    g=np.zeros((64,32),np.uint8)
    for y,l in enumerate(L[:64]):
        for x,c in enumerate(l[:32]): g[y,x]=K[c]
    return g
def rgb(a,bg=(115,197,164)):
    o=IP[a].astype(np.uint8); o[a==0]=bg; return Image.fromarray(o)
if __name__=='__main__':
    g=lees(sys.argv[1]); naam=sys.argv[2]
    im=Image.fromarray(g,'P'); im.putpalette(IP.flatten().tolist()+[0]*720)
    im.info['transparency']=0; im.save(D+f'icoon/{naam}.png',transparency=0)
    fr=Image.open(D+'af/shuppetto.png').convert('RGBA').resize((256,256),Image.NEAREST)
    W=Image.new('RGB',(256*3+256+40,256+260),(115,197,164))
    W.paste(fr,(0,0),fr); W.paste(rgb(g[:32]).resize((256,256),Image.NEAREST),(266,0)); W.paste(rgb(g[32:]).resize((256,256),Image.NEAREST),(532,0))
    # 1x en buren op 4x
    bur=[]
    for s in ['banette','shuppet','dusclops','dragapult','voltorb']:
        a=np.array(Image.open(f'graphics/pokemon/{s}/icon.png'))[:32]
        import re
        bur.append(a)
    P0=IP
    x=0
    for a in [g[:32]]+bur[:2]+[g[:32]]+bur[2:]:
        W.paste(rgb(a).resize((128,128),Image.NEAREST),(x,266)); x+=130
    for i,a in enumerate([g[:32]]+bur[:2]):
        W.paste(rgb(a),(800+i*34,10))
    W.save(D+f'icoon/{naam}_vel.png')
