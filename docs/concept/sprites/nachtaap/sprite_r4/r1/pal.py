# Gedeeld: palet (oude sprite) en hulpfuncties
from PIL import Image; import numpy as np
def lees_pal(p='referenties/oude_normal.pal'):
    l=open(p).read().split('\n')[3:19]; return [tuple(map(int,x.split())) for x in l]
PAL=lees_pal()
def naar_img(g,schaal=1,bg=None):
    h,w=g.shape; out=np.zeros((h,w,4),'uint8')
    for y in range(h):
        for x in range(w):
            v=g[y,x]
            if v>0: out[y,x]=PAL[v]+(255,)
            elif bg: out[y,x]=bg+(255,)
    im=Image.fromarray(out,'RGBA')
    return im.resize((w*schaal,h*schaal),Image.NEAREST) if schaal>1 else im
S='.123456789ABCDEF'
def toon(g,x0=0,x1=64,y0=0,y1=64):
    for y in range(y0,y1): print('%2d '%y+''.join(S[v] for v in g[y,x0:x1]))
