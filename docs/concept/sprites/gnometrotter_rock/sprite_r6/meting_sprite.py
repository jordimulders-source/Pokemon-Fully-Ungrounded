# meting_sprite.py: zet de meting (meet6.npz) om in palette-indexen binnen het r5-silhouet -> M.npy / M.png.
# Groep uit model-familie/zone, lijn waar het model lijn heeft (lijnaandeel), tint uit de gemeten modelhelderheid (3 tinten).
import numpy as np; from PIL import Image
d=np.load('meet6.npz'); fam,zon,lf,hel=d['fam'],d['zon'],d['lf'],d['hel']
r5=Image.open('r5.png'); S=np.asarray(r5)>0
GR={'steen':(2,[(110,3),(140,4),(999,5)]),'licht':(4,[(160,12),(196,13),(999,14)]),
    'roze':(6,[(155,7),(178,8),(999,15)]),'blauw':(9,[(124,9),(150,10),(999,11)])}
LT=0.45; LR=0.18
def is_lijn(y,x):
    v=lf[y,x]
    if v>=LT: return True
    if v<LR: return False
    # kam: lokaal maximum horizontaal of verticaal (lijn op de pixel met de meeste modellijn, 1 px)
    h=v>=lf[y,x-1] and v>=lf[y,x+1]; w=v>=lf[y-1,x] and v>=lf[y+1,x]
    return h or w
def groep(y,x):
    f=fam[y,x]
    if f==3: return 'roze'
    if f==4: return 'blauw'
    if f==2: return 'licht' if zon[y,x] in (2,3,4) else 'steen'
    return None
def bouw():
    M=np.zeros((64,64),int); G=np.empty((64,64),object)
    for y,x in zip(*np.where(S)):
        g=groep(y,x); G[y,x]=g
        if g is None: M[y,x]=1; continue
        lijn,tn=GR[g]
        if is_lijn(y,x): M[y,x]=lijn if lf[y,x]<0.8 else 1
        else: M[y,x]=next(i for t,i in tn if hel[y,x]<t)
    return M,G
if __name__=='__main__':
    M,G=bouw(); np.save('M.npy',M)
    p=Image.fromarray(M.astype('uint8'),'P'); p.putpalette(r5.getpalette()); p.save('M.png',transparency=0)
