# 2-ogenvariant van claydol_g3r5_paletB (Claydol regional): alleen bestaande pixels, verplaatst als asset.
# Bandindeling (rijen):  A 12-18 voorhoofd + rode lijn | B 19-31 ogen + neus | C 32-36 onderkop (neusrug loopt door)
import os, numpy as np
from PIL import Image
HIER=os.path.dirname(os.path.abspath(__file__))
BASIS=os.path.join(HIER,'../claydol_gemini_r3/r5/claydol_g3r5_paletB.png')
im0=Image.open(BASIS); PAL=im0.getpalette(); E=np.array(im0).astype(int)

def F_vul(y,x,d,x0):
    """Vrijgekomen plek rechts (waar oog 3 zat): kop-assets uit de sprite zelf, zelfde kolombreedte.
       rij 19-25 <- voorhoofd onder de punt (rij 7-13, kol 27..): steen 4/5 met reliëfblokjes (lichter, boven)
       rij 26-31 <- onderkop rechts (rij 31-36, kol 36..): reliëf in schaduw 5/6 (donker, onder/rechts)"""
    if (y,x)==(19,50): return (19,50)            # eind rode lijn blijft
    if y in (19,20) and x==51: return (y,x)      # donkere koprand onder kransbolletje
    if y==30 and x>=51: return (y,x)             # buitenlijn kop
    if y==31 and x>=48: return (y,x)
    if y<=25: return (y-12, x-x0+27)
    return (y+5, x-x0+36)

def bouw(d, links, smal=None):
    """d: ogen+neus d kolommen naar rechts. links: d bronkolommen (brug tussen oog 2 en 3, kol 40/41) voor de strook links van oog 1.
       smal: kolom in oog 2 die geschrapt wordt (verre oog 1 kolom smaller), of None."""
    S=E.copy(); bron={}
    def put(y,x,s,w):
        S[y,x]=E[s]
        if s!=(y,x): bron[(y,x)]=(s,w)
    ns=1 if smal is not None else 0
    # A: kolom 20 (top boog 1) d x herhalen; boog 2 eventueel 1 smaller (kol 33); top boog 3 (vanaf 43) d-ns kolommen schrappen
    for y in range(12,19):
        mid=[c for c in range(21,43) if not (smal is not None and c==33)]
        src=list(range(0,21))+[20]*d+mid+list(range(43+d-ns,64))
        for x,s in enumerate(src): put(y,x,(y,s),'A')
    # B: blok 11..39 (oog 1 met ring, neus, oog 2 met ring) d naar rechts
    for y in range(19,32):
        x_l=13 if y==31 else 11                       # rij 31: kol 11-12 = rand kransbolletje, blijft
        blok=[c for c in range(x_l,40) if c!=smal]
        for i,c in enumerate(blok): put(y,x_l+d+i,(y,c),'B')
        for i in range(d): put(y,x_l+i,(y,links[i]),'B-links')
        x0=x_l+d+len(blok)
        for x in range(x0,52): put(y,x,F_vul(y,x,d,x0),'F')
    # C: onderkop: kolom 21 d x herhalen, d kolommen effen schaduw (kol 40..) schrappen
    for y in range(32,37):
        src=list(range(0,22))+[21]*d+list(range(22,40))+list(range(40+d,64))
        for x,s in enumerate(src): put(y,x,(y,s),'C')
    for k in [k for k in bron if S[k]==E[k]]: del bron[k]
    return S,bron

def save(S,pad,schaal=8):
    im=Image.fromarray(S.astype(np.uint8),'P'); im.putpalette(PAL); im.save(pad+'.png',transparency=0)
    im.resize((64*schaal,64*schaal),Image.NEAREST).save(pad+'_8x.png',transparency=0)

def rgba(S):
    im=Image.fromarray(S.astype(np.uint8),'P'); im.putpalette(PAL); im.info['transparency']=0; return im.convert('RGBA')

VARIANTEN={'A':dict(d=3,links=[40,41,40]), 'B':dict(d=4,links=[40,41,40,41]), 'C':dict(d=4,links=[40,41,40,41],smal=33)}

if __name__=='__main__':
    for n,kw in VARIANTEN.items():
        S,bron=bouw(**kw); save(S,os.path.join(HIER,'claydol_2ogen_'+n))
        alpha=((S>0)!=(E>0)).sum(); ch=(S!=E)
        ys,xs=np.where(ch)
        print(n,kw,'| alpha-diff',alpha,'| gewijzigd',ch.sum(),'| rijen',ys.min(),ys.max(),'kol',xs.min(),xs.max(),
              '| per band', {w:sum(1 for k,(s,ww) in bron.items() if ww==w and S[k]!=E[k]) for w in ['A','B','B-links','F','C']},
              '| buiten sprite:',0)
        assert alpha==0
        assert (S[37:]==E[37:]).all() and (S[:12]==E[:12]).all()
