"""Salticonda kleurronde 3d: vanaf kleur3.
- Hele sprite 3 px omlaag (DY=3); lijf, halsband, gezicht, neus/snuitfront, oog, wenkbrauw en wang alleen verschoven.
- De kuif van kleur3 ~1,2x in alle richtingen (vooral hoger), zelfde vorm: silhouet = kleur3-kuif geschaald om het
  anker (16,10) (voorkant kuif, ooghoogte), zie kuifsilhouet(); daarna per rij met de hand ingekleurd met de
  zouttextuur van 3b (okernaden g, lichte opstaande randen, korrels).
Tekens: . transparant | O K h omlijning | e d c b a zout | f g gezicht/naad | q r s t pekel."""
from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/salticonda/'
CH='.OKhedcbafgqrst'; I=CH.index
DY=3; S=1.2; AX,AY=16,10
def kuifmasker(x,y):               # zelfde masker als kuifmaat.py (kleur3-coordinaten)
    return y<20 and ((y<=5 and x>=13) or (6<=y<=9 and x>=21) or (y>=10 and x>=34))
def vast(x,y):                     # bevroren binnen het masker: wenkbrauw, oog, wang (kleur3-coordinaten)
    return (21<=x<=33 and 7<=y<=9) or (23<=x<=30 and y==6) or (25<=x<=27 and y==5) or (20<=x<=33 and 10<=y<=15) or (33<=x<=36 and 9<=y<=19)
# de kuif, met de hand op het geschaalde silhouet (nieuwe coordinaten): rij -> [(x0, tekens)]
KUIF={
 1:[(20,"hhhhhhh..hhhhhK")],
 2:[(17,"hhhabaabbbhhaababbKKKK")],
 3:[(15,"hhaaabbbbbbccgabbbabbccgKK")],
 4:[(15,"haababbbbbbcggabbbbbcccgaK")],
 5:[(13,"hhaabbbbbbbbcggcgabbbbccgacK")],
 6:[(12,"haabbbbbbbbcggaccgabbbcccgabKK")],
 7:[(12,"hbbbbbbbbbcgaabcccgabbbcgaggdeK")],
 8:[(12,"hheeeeeedbbbb"),(28,"bcgabbccgbaagK")],
 9:[(21,"ee"),(31,"abccgabbcceK")],
 10:[(34,"cgabbccceK")],
 11:[(34,"cgbccccdeK")],
 12:[(37,"bcccddeO")],
 13:[(37,"gbcccdeO")],
 14:[(37,"gbccccdeO")],
 15:[(37,"cgbcccdeO")],
 16:[(37,"cgbccdeO")],
 17:[(37,"cgggddeO")],
 18:[(37,"cgbbggeO")],
 19:[(37,"gcccbbbO")],
 20:[(37,"gddddeO")],
 21:[(37,"gddddeO")],
 22:[(37,"gddeeOO")],
}
def build():
    K3=Image.open(D+'kleur3/salticonda.png'); P=K3.load()
    out=Image.new('P',(64,64),0); out.putpalette(K3.getpalette()); Q=out.load()
    for x in range(64):
        for y in range(61):
            if P[x,y]!=0 and not (kuifmasker(x,y) and not vast(x,y)): Q[x,y+DY]=P[x,y]
    for y,segs in KUIF.items():
        for x0,t in segs:
            for i,ch in enumerate(t):
                x=x0+i
                if ch=='.': continue
                if Q[x,y]!=0: raise SystemExit('kuif over bevroren pixel %s'%((x,y),))
                Q[x,y]=I(ch)
    return out
def kuifsilhouet():
    """Het geschaalde kleur3-kuifsilhouet waarop KUIF getekend is (ter controle)."""
    P=Image.open(D+'kleur3/salticonda.png').load()
    k={(x,y) for x in range(64) for y in range(20) if P[x,y]!=0 and kuifmasker(x,y)}
    out=set()
    for X in range(64):
        for Y in range(24):
            y0=Y-DY; s=S if y0<=AY else S-0.12*(y0-AY)/9
            src=(int(round(AX+(X-AX)/s)),int(round(AY+(y0-AY)/S if y0<AY else y0)))
            if src in k: out.add((X,Y))
    return out
if __name__=='__main__':
    im=build(); im.save(D+'kleur3d/salticonda.png',transparency=0)
    Q=im.load()
    open(D+'kleur3d/salticonda_raster.txt','w').write('\n'.join(''.join(CH[Q[x,y]] for x in range(64)) for y in range(64))+'\n')
