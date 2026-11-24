# r4: tekstraster <-> png, palet, 8x-render. Tekens: . K D d m M l h R r  (zie klassen.py)
import numpy as np; from PIL import Image
S='.KDdmMlhRr'
# palet: modelkleuren (klassen.py), lijn K iets warmer; kleur mag naar Gen 3 afwijken
PAL={'.':(255,255,255),'K':(32,26,30),'D':(66,57,52),'d':(104,93,80),'m':(126,115,99),'M':(150,139,120),'l':(186,175,155),'h':(212,204,184),'R':(214,86,84),'r':(164,48,56)}
def lees(p): return [r for r in open(p).read().split() if r and not r[0].isdigit()]
def png(g,uit,canvas=64):
    H,W=len(g),len(g[0]); keys=list(PAL); full=np.zeros((canvas,canvas),'uint8')
    x0=(canvas-W)//2; y0=canvas-H-1
    for y,r in enumerate(g):
        for x,c in enumerate(r): full[y0+y,x0+x]=keys.index(c)
    im=Image.fromarray(full,'P'); im.putpalette([v for k in keys for v in PAL[k]]+[0]*(768-3*len(keys))); im.save(uit,transparency=0)
    return Image.open(uit)
def rgba(pim):
    a=np.array(pim); pal=np.array(pim.getpalette()[:768]).reshape(-1,3)
    rgb=pal[a].astype('uint8'); al=np.where(a>0,255,0).astype('uint8'); return Image.fromarray(np.dstack([rgb,al]),'RGBA')
def op(im,bg,z):
    b=Image.new('RGBA',im.size,bg); b.alpha_composite(im); return b.convert('RGB').resize((im.width*z,im.height*z),Image.NEAREST)
