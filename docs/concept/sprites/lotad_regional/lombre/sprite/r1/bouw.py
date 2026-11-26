# Gaucho-Lombre r1: kale reductie (kaal.py: model 54x74 -> 42x57 door rijen/kolommen te schrappen) + mond + technische opschoning.
# Gebruik: python3 bouw.py  -> lombre_gaucho_A/B/C.png. Elke stap telt hoeveel pixels hij verandert t.o.v. de kale reductie.
import numpy as np; from PIL import Image
from gemeen import opslaan, NAAM, ROOD, OLIJF
LOMBRE='/home/user/Pokemon-Fully-Ungrounded/graphics/pokemon/lombre/anim_front_gba.png'
N4=((-1,0),(1,0),(0,-1),(0,1)); N8=[(dy,dx) for dy in (-1,0,1) for dx in (-1,0,1) if dy or dx]

def basis():
    """Alles behalve de mond: kale reductie, snavel weg, kopcontour waar de snavel hem bedekte, opschoning."""
    o=np.load('kaal.npy').copy(); kaal=o.copy(); tel={}
    def stap(n,v): tel[n]=tel.get(n,0)+int((v!=o).sum())
    # 1. snavel weg: alle snavelpixels (16) -> kop rood midden (4) = de kleur van het gezicht naast/boven de snavel in het model.
    #    Zwarte snavellijnen in het snavelvak (x18-29, y30-34: onderrand + mondstreep van de snavel) -> 4.
    v=o.copy(); o[o==16]=4
    for y in range(30,35):
        for x in range(18,30):
            if o[y,x]==1: o[y,x]=4
    stap('snavel weg -> gezicht (4)',v)
    # 2. kopcontour links-onder (in het model verborgen achter de snavel): voorkant x20 recht door tot rij 31, dan een
    #    boog naar de kin (21,32) (22,33) (23-26,34), aansluitend op de bestaande kinlijn (rood 2 op x27-29, rij 34).
    v=o.copy()
    XL={26:20,27:20,28:20,29:20,30:20,31:20,32:21,33:22,34:23}
    for y,xl in XL.items():
        o[y,:xl]=0; o[y,xl]=1
    o[34,23:27]=1
    # schaduwsikkel onderaan de kaak (Gen 3: licht linksboven, schaduw onder), in de modeltint rood donker
    for x in range(23,30): 
        if o[33,x]==4: o[33,x]=3
    o[32,22]=3
    stap('kopcontour + kaakschaduw',v)
    def g(y,x): return o[y,x] if 0<=y<64 and 0<=x<64 else 0
    def mat(y,x):   # materiaal van een pixel of (voor zwart) van zijn buren: 'r' rood, 'o' olijf
        k=o[y,x]
        if k in ROOD: return 'r'
        if k in OLIJF: return 'o'
        ms=['r' if o[y+dy,x+dx] in ROOD else 'o' for dy,dx in N8 if 0<=y+dy<64 and 0<=x+dx<64 and (o[y+dy,x+dx] in ROOD|OLIJF)]
        return max(set(ms),key=ms.count) if ms else None
    # 3. buitenlijn (zoals de gaucho-Lotad): rand die alleen boven/links aan de achtergrond grenst = lichte kant -> selout
    #    in de lijntint van het materiaal (rood 2, olijf 7); rechts/onder blijft zwart. Ogen/nagels/wit niet.
    v=o.copy(); nieuw=[]
    SEL={'r':2,'o':7}
    for y,x in zip(*np.where(o>0)):
        if o[y,x] in (11,12,13,15): continue
        bgR=g(y,x+1)==0; bgD=g(y+1,x)==0; bgL=g(y,x-1)==0; bgU=g(y-1,x)==0
        if not(bgR or bgD or bgL or bgU): continue
        if bgR or bgD:
            if o[y,x]!=1: nieuw.append((y,x,1))
        else:
            m=mat(y,x)
            if m: nieuw.append((y,x,SEL[m]))
    for y,x,k in nieuw: o[y,x]=k
    stap('buitenlijn (selout links/boven, zwart rechts/onder)',v)
    # 4. binnenlijnen: zwart dat niet aan de achtergrond grenst en maar aan één materiaal grenst -> lijntint (rood 2, olijf 6).
    #    Zwart tussen rood en olijf (vorm over vorm) blijft zwart. Kop rond oog/mond (x18-36, y22-35) niet aangeraakt.
    v=o.copy(); nieuw=[]
    for y,x in zip(*np.where(o==1)):
        if 18<=x<=36 and 22<=y<=35: continue
        if any(g(y+dy,x+dx)==0 for dy,dx in N8): continue
        ms={('r' if v[y+dy,x+dx] in ROOD else 'o' if v[y+dy,x+dx] in OLIJF else 'x') for dy,dx in N8 if v[y+dy,x+dx]!=1}
        if ms=={'r'}: nieuw.append((y,x,2))
        elif ms=={'o'}: nieuw.append((y,x,6))
    for y,x,k in nieuw: o[y,x]=k
    stap('binnenlijnen (zwart binnen één materiaal -> lijntint)',v)
    # 5. losse tintpixel (geen gelijke 8-buur; geen lijn, oog, mond, nagel) -> meest voorkomende 8-buurtint uit dezelfde groep (geen lijntinten).
    v=o.copy()
    for y,x in zip(*np.where(np.isin(o,[3,4,5,7,8,9,10]))):
        k=o[y,x]; nb=[g(y+dy,x+dx) for dy,dx in N8]
        if k in nb: continue
        grp=ROOD if k in ROOD else OLIJF
        kand=[b for b in nb if b in grp and b not in (2,6)]
        if kand: o[y,x]=max(set(kand),key=kand.count)
    stap('losse tintpixels',v)
    return o,kaal,tel

# Gen 3-Lombre-mond, gespiegeld (Lombre kijkt naar rechts, dit model naar links). Kleuren: Lombre 7 (lip) -> 12 (Lotad-snavel midden),
# b (lip licht) -> 13 (Lotad-snavel licht), 1 (zwart) blijft zwart, 4 (Lombre-onderkaak) -> 4 (gezicht rood midden).
# Lombre-gezichtstinten (a,9,8,d,5,6,e) worden niet overgenomen (daar blijft ons gezicht).
def lombre_mond(r0=23,r1=29,kaak=4):
    L=np.array(Image.open(LOMBRE))[:64]; p=L[r0:r1+1,30:46][:,::-1]   # kolom c = Lombre x45-c
    M={7:12,0xb:13,1:1,4:kaak}
    return [(r0+j,c,M[int(p[j,c])]) for j in range(p.shape[0]) for c in range(p.shape[1]) if int(p[j,c]) in M]

def plak(o,mond,dx,dy,schaal=(1,1)):
    """schaal=(sy,sx) met elk 1 of 1,5. Bij 1,5: 3x opblazen en dan exact 2x verkleinen (zwart wint bij >= de helft,
    anders de meerderheid), zodat lijnen 1 px blijven (zelfde regel als de kale reductie van de Lotad).
    Lege cellen (waar Lombre gezicht heeft) worden niet geplakt."""
    o=o.copy(); sy,sx=schaal
    d={(r,c):k for r,c,k in mond}; rs=[r for r,_,_ in mond]; cs=[c for _,c,_ in mond]
    R0,C0=min(rs),min(cs); h=max(rs)-R0+1; w=max(cs)-C0+1
    fy=3 if sy!=1 else 1; fx=3 if sx!=1 else 1; ry=2 if sy!=1 else 1; rx=2 if sx!=1 else 1
    big=np.full((fy*h,fx*w),-1)
    for (r,c),k in d.items(): big[fy*(r-R0):fy*(r-R0)+fy,fx*(c-C0):fx*(c-C0)+fx]=k
    for j in range(fy*h//ry):
        for i in range(fx*w//rx):
            b=big[ry*j:ry*j+ry,rx*i:rx*i+rx].ravel(); b=b[b>=0]
            if len(b)*2<ry*rx: continue
            if (b==1).sum()*2>=ry*rx: k=1
            else:
                v,n=np.unique(b,return_counts=True); k=v[n.argmax()]
            if o[R0+dy+j,C0+dx+i] in (11,15): continue   # oog (oogwit/wit) blijft het model
            o[R0+dy+j,C0+dx+i]=k
    return o

VARIANTEN={  # naam: (dx, dy, schaal (y,x), kaakkleur) ; Lombre-kolom c -> x = c+dx, Lombre-rij r -> y = r+dy
 'A':(17,4,(1,1),4),     # 1-op-1, lip direct onder de ogen, punt 2 px voor de kopvoorkant (zoals bij Lombre); onderkaak = gezicht rood
 'B':(17,4,(1,1),13),    # als A, maar de Lombre-onderkaak (bij Lombre lichter dan het gezicht) ook in Lotad-snavel licht
 'C':(16,5,(1,1.5),4),   # alleen in de breedte 1,5x (lip zo breed als de modelsnavel), 1 rij lager en 1 px verder naar voren (vrij van het oog)
}
def sluit(o):
    """Na het plakken: figuurpixel die rechts/onder aan de achtergrond grenst en geen lijn is -> zwart (buitenlijn dicht)."""
    o=o.copy()
    for y,x in zip(*np.where(o>0)):
        if o[y,x] in (1,2,6,7): continue
        if (x+1<64 and o[y,x+1]==0) or (y+1<64 and o[y+1,x]==0) or o[y,x-1]==0 or o[y-1,x]==0: o[y,x]=1
    return o

if __name__=='__main__':
    import sys
    o,kaal,tel=basis(); opslaan(o,'zonder_mond.png'); np.save('zonder_mond.npy',o)
    print('basis: afwijking van de kale reductie per stap',tel,'totaal',int((o!=kaal).sum()))
    for n,(dx,dy,s,kk) in VARIANTEN.items():
        v=plak(o,lombre_mond(kaak=kk),dx,dy,s); v=sluit(v); opslaan(v,'lombre_gaucho_%s.png'%n)
        ys,xs=np.where(v>0)
        print(n,'maat %dx%d px %d kleuren incl. transparant %d | mondpixels %d'%(xs.max()-xs.min()+1,ys.max()-ys.min()+1,(v>0).sum(),len(set(v.ravel())),int((v!=o).sum())))
