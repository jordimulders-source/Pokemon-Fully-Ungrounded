# Ronde 6 (2 ogen) op r5 I1A: onderkop = licht/schaduw van Gemini r7 (per pixel r7-toon -> dichtstbijzijnde steentint) + een paar
# doorlopende cracks uit de 3-ogenbasis; rode lijn na boog 2 vloeiend naar horizontaal (H1-H3); neusvarianten a-c.
import os, sys, numpy as np
from PIL import Image
H=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,os.path.join(H,'../r5')); import r5
U=r5.U; PAL=r5.PAL
R5=np.array(Image.open(os.path.join(H,'../r5/claydol_2ogen_r5.png'))).astype(int)
E=np.array(Image.open(os.path.join(H,'../../claydol_gemini_r3/r5/claydol_g3r5_paletB.png'))).astype(int)
RED=(8,9)

# ---- r7 op ons raster (16 px-cellen, mediaan van het binnenste 8x8) -> onze steentinten ----
C=np.load(os.path.join(H,'r7cel.npy')); L=C.sum(2)/3
def toon(l):                       # r7-niveaus 162 / 130 / 110 / 96-77 -> 3 / 4 / 5 / 6
    return 3 if l>=146 else 4 if l>=120 else 5 if l>=102 else 6
T=np.vectorize(toon)(L)
slecht=np.zeros((64,64),bool)
room=(L>=185)
for y in range(18,33):            # r7-ogen (crème + 1 cel ring), r7-mond, r7-rood: geen steen, vullen vanuit de buren
    for x in range(9,40):
        if room[max(0,y-1):y+2,max(0,x-1):x+2].any(): slecht[y,x]=True
slecht|=(C[...,0]-C[...,1]>60)
slecht[31,19:26]|=(L[31,19:26]<100)
for y,x in zip(*np.where(slecht)):
    for d in [1,2,3,4,5,6,7,8]:
        cand=[(y+d,x),(y,x+d),(y,x-d),(y-d,x)]
        ok=[c for c in cand if 0<=c[0]<64 and 0<=c[1]<64 and not slecht[c]]
        if ok: T[y,x]=T[ok[0]]; break

# ---- zones ----
def oogmasker(S):
    m=np.zeros((64,64),bool); cr=(S==1); cr[:19]=False; cr[32:]=False; cr[:,:11]=False; cr[:,40:]=False
    for y,x in zip(*np.where(cr)): m[y-2:y+3,x-2:x+3]=True
    return m
def onderzone():
    z=np.zeros((64,64),bool)
    for y in range(28,37):
        x0=11 if y<=30 else max([x for x in range(9,18) if R5[y,x]==7]+[12])+1
        x1=min([x for x in range(40,56) if R5[y,x]==7]+[51])
        z[y,x0:x1]=True
    for y in range(16,32):         # rechts van het rechteroog
        z[y,38:(50 if y<20 else 51)]=True
    z&=(R5!=7)&(R5>0)
    return z
ZON=onderzone()
ZALL=r5.Z|ZON
RAND=[(y,50) for y in range(16,20) if R5[y,50] in RED]   # oud lijneinde op de donkere koprand -> koprand (6, zoals (17,50))
ZALL[tuple(np.array(RAND).T)]=True

# ---- cracks: doorlopende cracklijnen uit de onderkop van de 3-ogenbasis (palet B), eigen plek / rechts 2 kol mee met het oog ----
CR={'C3 onder linkeroog':[(30,19),(31,18),(32,17),(32,20),(33,18),(33,19),(34,19),(35,19)],
    'C2 onder rechteroog':[(y,x-1) for y,x in [(28,39),(29,39),(30,38),(30,40),(31,39),(31,41),(32,38),(32,41),(33,37)]],
    'C4 midden-rechts':[(y,x-1) for y,x in [(32,33),(33,32),(33,34),(34,32),(34,34),(35,32),(35,35),(36,31),(36,34)]]}
for k,v in CR.items():
    for p in v:
        src=(p[0],p[1]+1) if k!='C3 onder linkeroog' else p
        assert E[src]==6, (k,p)

# ---- rode lijn ----
BOOG1=[(16,x) for x in range(15,19)]+[(17,x) for x in range(14,20)]+[(18,13),(18,14),(19,13)]
V_R7=[(18,18),(18,19),(18,20),(19,19),(19,20),(20,20),(20,21),(21,21),(21,22),(22,22),(22,23),(22,24),(23,22),(23,23),
      (21,24),(21,25),(20,25),(20,26),(19,26),(19,27),(18,27),(18,28)]
V_B=[(18,19),(18,20),(19,20),(19,21),(20,21),(20,22),(21,22),(21,23),(21,24),(20,24),(20,25),(19,25),(19,26),(18,26),(18,27),(18,28)]
TOP2=[(16,x) for x in range(29,34)]+[(17,x) for x in range(28,34)]
def staart(h):
    """na de top van boog 2: (donker, licht) -- licht = rij onder een horizontaal stuk, zoals onder de boogtoppen"""
    if h=='H1':   # op tophoogte door, zakt in 2 treden naar de rand
        dk=[(16,x) for x in range(33,42)]+[(17,x) for x in range(42,47)]+[(18,x) for x in range(47,50)]
        lt=[(17,x) for x in range(34,42)]+[(18,x) for x in range(42,47)]+[(19,x) for x in range(47,50)]
    elif h=='H2': # rechterarm daalt tot halve hoogte (rij 19), dan horizontaal, licht afzakkend
        dk=[(17,34),(18,34),(18,35)]+[(19,x) for x in range(36,45)]+[(20,x) for x in range(45,49)]+[(21,49),(21,50)]
        lt=[(19,35)]+[(20,x) for x in range(36,45)]+[(21,x) for x in range(45,49)]+[(22,49),(22,50)]
    else:         # H3: zachte bocht, treden 1-1-2-3, dan horizontaal op rij 20, licht afzakkend
        dk=[(17,34),(18,35),(19,36),(19,37),(20,38),(20,39),(20,40)]+[(20,x) for x in range(41,46)]+[(21,x) for x in range(46,50)]+[(22,50)]
        lt=[(18,34),(19,35),(20,36),(20,37)]+[(21,x) for x in range(38,46)]+[(22,x) for x in range(46,50)]
    return dk,lt
def lijn(h,n):
    lp={}
    for p in BOOG1+(V_B if n=='b' else V_R7)+TOP2: lp[p]=9
    for x in range(15,19): lp[(17,x)]=8
    for x in range(29,34): lp[(17,x)]=8
    dk,lt=staart(h)
    for p in dk: lp[p]=9
    for p in lt: lp.setdefault(p,8)
    return lp

def bouw(h='H1',n='a'):
    S=R5.copy(); bron={}
    oogL=np.zeros((64,64),bool)
    for y,x in zip(*np.where(np.isin(R5,(1,2)))):
        if 20<=y<=31 and 11<=x<=22: oogL[y-2:y+3,x-2:x+3]=True
    oogL[:,23:]=False
    # 1. rechteroog 1 px naar rechts (U5 kol 32-43 -> 27-38), neus (U5 kol 27-30 -> 23-26), rij 18-31
    for y in range(18,32):
        for i,s in enumerate(range(32,44)):
            if ZALL[y,27+i]: S[y,27+i]=U[y,s]; bron[(y,27+i)]='rechteroog +1'
        if n in ('a','c'):
            for i,s in enumerate(range(27,31)): S[y,23+i]=U[y,s]; bron[(y,23+i)]='neus'
    if n=='b':                      # neus met kap op rij 22 i.p.v. 20: 2 gelijke rugrijen (U5 26, 27) geschrapt
        rows=[r for r in range(20,32) if r not in (26,27)]
        for i,s in enumerate(rows):
            for j,c in enumerate(range(27,31)): S[22+i,23+j]=U[s,c]; bron[(22+i,23+j)]='neus'
        for y in (18,19,20,21):
            for x in range(23,27): S[y,x]=T[y,x]; bron[(y,x)]='r7-toon'
    if n=='a':                      # binnenkant V boven de punt: zoals r5 (steen 2 rijen hoger)
        for (y,x) in [(20,22),(20,23),(20,24),(21,23)]: S[y,x]=S[y-2,x]; bron[(y,x)]='V-binnen'
    if n=='c':                      # neusvorm uit r7 met onze tinten (zonder r7-mond)
        for y in range(18,32):
            for x in range(23,27): S[y,x]=T[y,x]; bron[(y,x)]='r7-neus'
    oogR=oogmasker(S); oogR[:,:27]=False
    # 2. onderkop + rechterkant: r7-licht/schaduw
    for y,x in zip(*np.where(ZON)):
        if oogR[y,x] or oogL[y,x] or (23<=x<=26 and y<=31): continue
        S[y,x]=T[y,x]; bron[(y,x)]='r7-toon'
    # 3. cracks
    for k,v in CR.items():
        for p in v:
            if ZON[p] and not oogR[p] and not oogL[p]: S[p]=6; bron[p]='crack '+k.split()[0]
    # 4. rood dat niet meer op de lijn ligt -> r7-toon; dan de lijn
    lp=lijn(h,n)
    for p in RAND:
        if p not in lp: S[p]=R5[17,50]; bron[p]='rood weg -> koprand'
    for y,x in zip(*np.where(ZALL & np.isin(S,RED))):
        if (y,x) not in lp: S[y,x]=T[y,x]; bron[(y,x)]='rood weg -> r7-toon'
    for p,c in lp.items():
        assert ZALL[p] and S[p] not in (1,2), ('lijn in oog/buiten zone',p)
        S[p]=c; bron[p]='lijn'
    # controles
    assert ((S>0)==(R5>0)).all(), 'silhouet'
    assert not ((S!=R5)&~ZALL).any(), 'buiten kopzone'
    k=np.zeros((64,64),bool); k[20:32,11:23]=True; k&=np.isin(R5,(1,2)); k=np.array([[k[max(0,y-1):y+2,max(0,x-1):x+2].any() for x in range(64)] for y in range(64)]); k&=~np.isin(R5,RED)
    assert (S[k]==R5[k]).all(), 'linkeroog (creme + ring 1 px)'
    m=oogmasker(R5); m[:,:26]=False
    ys,xs=np.where(m)
    assert all(S[y,x+1]==R5[y,x] for y,x in zip(ys,xs) if R5[y,x]==1), 'rechteroog'
    return S,bron

def save(S,pad):
    im=Image.fromarray(S.astype(np.uint8),'P'); im.putpalette(PAL); im.save(pad+'.png',transparency=0)
    im.resize((512,512),Image.NEAREST).save(pad+'_8x.png',transparency=0)
rgba=r5.rgba
COMBI=[(h,n) for h in ('H1','H2','H3') for n in ('a','b','c')]
if __name__=='__main__':
    from collections import Counter
    for h,n in COMBI:
        S,b=bouw(h,n); save(S,os.path.join(H,'claydol_2ogen_r6_%s%s'%(h,n)))
        print(h+n,'diff t.o.v. r5:',(S!=R5).sum(),dict(Counter(b[k].split(' ')[0] for k in b if S[k]!=R5[k])))

KEUZE=('H3','b')
def vel():
    from PIL import ImageDraw
    S,_=bouw(*KEUZE); save(S,os.path.join(H,'claydol_2ogen_r6'))
    r7=Image.open(os.path.join(H,'../../gemini/claydol_r7_2ogen.png')).convert('RGBA').resize((512,512),Image.NEAREST)
    W=3*522+10; v=Image.new('RGBA',(W,2000),(255,255,255,255)); d=ImageDraw.Draw(v)
    for i,(t,im) in enumerate([('r6 keuze %s%s (H3 zachte bocht, neus b)'%KEUZE,rgba(S).resize((512,512),Image.NEAREST)),
                               ('r5 (I1A)',rgba(R5).resize((512,512),Image.NEAREST)),('Gemini r7',r7)]):
        d.text((10+i*522,3),t,fill='black'); v.alpha_composite(im,(10+i*522,16))
    y=540; d.text((10,y),'kop 12x: r6 keuze | r5',fill='black'); y+=14
    for i,X in enumerate([S,R5]): v.alpha_composite(rgba(X).crop((8,9,56,38)).resize((48*12,29*12),Image.NEAREST),(10+i*(48*12+10),y))
    y+=29*12+10
    for i,X in enumerate([S,R5]):
        for j,bg in enumerate([(248,248,240,255),(40,40,48,255)]):
            t=Image.new('RGBA',(80,80),bg); t.alpha_composite(rgba(X),(8,8)); v.alpha_composite(t,(10+i*200+j*90,y))
    d.text((410,y+30),'1x licht/donker: r6 keuze | r5',fill='black')
    y+=96; d.text((10,y),'alle varianten 4x  (H1 = tophoogte, H2 = halve hoogte, H3 = zachte bocht 1-1-2-3;  a = volle neus + V erover, b = V-punt boven de neus, c = neusvorm r7)',fill='black'); y+=14
    for i,(h,n) in enumerate(COMBI):
        X,_=bouw(h,n); x=10+(i%5)*266; yy=y+(i//5)*270
        v.alpha_composite(rgba(X).resize((256,256),Image.NEAREST),(x,yy+12)); d.text((x,yy),h+n+('  <- keuze' if (h,n)==KEUZE else ''),fill='black')
    v=v.crop((0,0,W,y+2*270+10)); v.save(os.path.join(H,'vel.png'))
if __name__=='__main__': vel()
