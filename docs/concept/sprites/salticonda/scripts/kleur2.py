"""Salticonda kleurronde 2: 3/4-lijf (onderlaag2) + handgetekende kop/hals (KOPPEN) + staart.
Tekens = palet van de Silicobra-Uyuni (zie kleur1.py)."""
import math, sys
from PIL import Image
sys.path.insert(0,'/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/salticonda/scripts')
import onderlaag2
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/salticonda/'
CH='.OKhedcbafgqrst'
PAL=Image.open(D+'../silicobra_uyuni/af/silicobra_uyuni.png').getpalette()[:48]

def body():
    px=onderlaag2.render()
    C={}; coil={}
    for (x,y),(dep,ci,l,b) in px.items():
        coil[(x,y)]=ci
        C[(x,y)]='a' if l>0.86 else 'b' if l>0.64 else 'c' if l>0.42 else 'd' if l>0.16 else 'e'
    # gleuven: pekelringen op de lagere winding, direct onder de hogere
    for (x,y),ci in list(coil.items()):
        if ci==0 and False: pass
    for (x,y),ci in coil.items():
        up=[coil.get((x,y-k)) for k in (1,2,3)]
        for k,u in enumerate(up):
            if u is not None and u>ci:
                C[(x,y)]={0:'r',1:'s',2:'t'}[k]
                break
    for (x,y),ci in coil.items():   # slagschaduw: onderste rij van de hogere winding
        if C[(x,y)] in 'abc' and coil.get((x,y+1)) is not None and coil[(x,y+1)]<ci: C[(x,y)]='d'
    return C,coil

def render(C):
    im=Image.new('P',(64,64),0); im.putpalette(PAL+[0]*(768-48))
    for p,c in C.items():
        if c!='.': im.putpixel(p,CH.index(c))
    return im
if __name__=='__main__':
    C,_=body()
    render(C).convert('RGB').resize((384,384),Image.NEAREST).save(sys.argv[1])
