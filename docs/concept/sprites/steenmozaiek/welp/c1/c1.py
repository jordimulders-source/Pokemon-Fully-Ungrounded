# c1: Chavin-gravure op de welp. Basis = p8 zonder lijfpatronen (basis.npy). Motieven staan hieronder met de hand als
# tekstraster (stempels). Tekens: g = groef, i = groef met inleg (B: lila), c = verhoogd hart (A: licht, B: creme),
# 3/4/5 = steentoon van het vlak zetten (facet), n = geen automatische lichtrand, . = niets.
# Lichtrand: elke vlakpixel direct onder of rechts van een groef wordt 1 toon lichter (licht linksboven).
import sys, numpy as np
from PIL import Image
B0=np.load('basis.npy'); P8=np.array(Image.open('../p8/welp_p8.png'))
S={}  # (x0,y0): regels
def stempel(x0,y0,txt):
    S[(x0,y0)]=[r for r in txt.strip('\n').split('\n')]
# ---------- motieven ----------
import motieven
for (x0,y0),txt in motieven.STEMPELS: stempel(x0,y0,txt)
def opbouw():
    base=B0.copy(); lay=np.full((64,64),'.',dtype='<U1')
    for (x0,y0),rows in S.items():
        for j,r in enumerate(rows):
            for i,ch in enumerate(r):
                if ch==' ' or ch=='.': continue
                y,x=y0+j,x0+i
                if ch in '345': base[y,x]=int(ch)
                else: lay[y,x]=ch
    return base,lay
# ---------- kleur ----------
GROEF={5:3,4:6,3:2,2:2}      # groef = donkere tint van het vlak
RAND ={3:4,4:5,5:14}         # lichtrand = 1 toon lichter
def kleur(var):
    base,lay=opbouw(); a=P8.copy()
    vlak=np.isin(P8,[3,4,5,6,7,8,9,11])  # schilderbaar: oude vlak/patroonpixels (lijnen 1/2, oog, mond, tong, tenen blijven)
    from basis import bevroren_kop
    vlak&=~bevroren_kop()
    a[vlak]=base[vlak]
    G=np.isin(lay,['g','i'])&vlak
    for y,x in zip(*np.where(G)):
        t=base[y,x]
        if var=='B' and lay[y,x]=='i': a[y,x]=8 if t==5 else 7
        else: a[y,x]=GROEF.get(t,2)
    for y,x in zip(*np.where(vlak&~G)):
        if lay[y,x]=='n': continue
        if lay[y,x]=='c': a[y,x]=11 if var=='B' else RAND.get(base[y,x],14); continue
        if (y>0 and G[y-1,x]) or (x>0 and G[y,x-1]):
            a[y,x]=RAND.get(base[y,x],base[y,x])
    return a
def pal(var):
    p=Image.open('../p8/welp_p8.png').getpalette()[:48]
    p[18:21]=[80,52,52]     # 6: groef op middentoon (A en B)
    return p
def bewaar(var):
    a=kleur(var); im=Image.fromarray(a.astype(np.uint8),'P'); im.putpalette(pal(var)+[0]*(768-48))
    im.save('welp_c1_%s.png'%var,transparency=0)
    im.convert('RGBA').resize((512,512),Image.NEAREST).save('welp_c1_%s_8x.png'%var)
    return a
if __name__=='__main__':
    for v in (sys.argv[1:] or ['A','B']): bewaar(v)
