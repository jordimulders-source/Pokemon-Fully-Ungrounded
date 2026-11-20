# mat.npy -> P1 (Sigilyph: zwarte grond + groen + wit) en P2 (ons palet: blauw + rood + wit). Max 16 kleuren.
import numpy as np; from PIL import Image
o=np.load('mat.npy'); H,W=o.shape
r4=np.array([list(l.rstrip('\n')[3:]) for l in open('../sprite_r4/rollen_hand.txt') if l.strip()])
KL={'.':(0,0,0),'K':(16,14,22),'1':(30,28,44),'2':(48,46,70),'3':(76,74,108),'g':(128,126,166),
    'L':(246,236,202),'M':(228,208,158),'D':(186,156,104),'S':(126,94,54),
    'B':(80,120,200),'b':(44,66,140),'R':(214,66,58),'r':(140,36,40),'W':(248,248,248),
    'G':(56,160,72),'H':(40,104,56)}
P1={'k':'K','a':'3','A':'2','c':'1','n':'G','N':'G','m':'H'}
P2={'k':'K','a':'B','A':'B','c':'b','n':'R','N':'R','m':'r'}
def maak(naam,mp,p2=False):
    r=np.vectorize(lambda c: mp.get(c,c))(o)
    if not p2: r[r=='r']='K'   # P1: geen plek voor donkerrood (selout rode strepen wordt lijn)
    # lijnen in het bedekte deel (k) zijn in beide varianten zwart: een creme selout naast blauw/rood/groen leest als losse bruine streep   # P1: geen plek voor donkerrood (selout rode strepen wordt lijn)
    keys=['.']+sorted(set(r.ravel())-{'.'}); assert len(keys)<=16,(naam,keys)
    full=np.zeros((64,64),'uint8'); x0=(64-W)//2; y0=64-H
    for j in range(H):
        for i in range(W): full[y0+j,x0+i]=keys.index(r[j,i])
    im=Image.fromarray(full,'P'); flat=[v for k in keys for v in KL[k]]; im.putpalette(flat+[0]*(768-len(flat))); im.save(naam,transparency=0)
    print(naam,len(keys),'kleuren',keys)
maak('astro_P1.png',P1); maak('astro_P2.png',P2,True)
