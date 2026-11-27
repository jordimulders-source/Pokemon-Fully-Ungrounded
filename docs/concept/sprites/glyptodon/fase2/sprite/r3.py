# Ronde 3: vanaf r2. (1) losse zwarte pixels -> modus van de modelcellen; (2) lijnen rond het oog minder donker.
import numpy as np
from basis import png,PAL
from modus import modus
I=np.load('r2_I.npy').copy(); I0=I.copy(); nat=np.load('comp_nat.npy')
op=I>0; P=np.pad(op,1)
buiten=(I==1)&~(P[:-2,1:-1]&P[2:,1:-1]&P[1:-1,:-2]&P[1:-1,2:])
DONK=(I==1)|(I==10)   # zwart en de donkerste grijstint (op 8x allebei zwart)
binnen=DONK&~buiten
# losse donkere pixels: geïsoleerd, of een uitsteeksel van <=2 px dat niet aan de buitenlijn vastzit
def buren(y,x):
    return [(y+dy,x+dx) for dy in (-1,0,1) for dx in (-1,0,1) if (dy or dx) and 0<=y+dy<64 and 0<=x+dx<64 and DONK[y+dy,x+dx]]
los=set()
for y,x in zip(*np.where(binnen)):
    nb=buren(y,x)
    if len(nb)==0: los.add((y,x)); continue
    if len(nb)!=1: continue
    keten=[(y,x)]; vorige=(y,x); cur=nb[0]; ok=False
    while True:
        if buiten[cur]: ok=True; break             # vast aan de buitenlijn: houden
        nb2=[q for q in buren(*cur) if q not in keten]
        if len(buren(*cur))>=3 or len(nb2)!=1:   # knooppunt of einde
            if len(buren(*cur))<3: keten.append(cur)   # eind van een los stukje
            break
        keten.append(cur); cur=nb2[0]
        if len(keten)>2: ok=True; break           # doorlopende lijn >=3
    if not ok and len(keten)<=2: los.update(keten)
# bultjes: donkere binnenpixel waarvan alle donkere buren aan één kant liggen en samen al een lijn vormen
#  (2-3 buren, onderling verbonden, geen enkele buur aan de buitenlijn) -> geen eigen lijn, maar een uitsteeksel
bult=set()
for y,x in zip(*np.where(binnen)):
    nb=buren(y,x)
    if not (2<=len(nb)<=3): continue
    if any(buiten[q] for q in nb): continue
    dys={q[0]-y for q in nb}; dxs={q[1]-x for q in nb}
    eenkant= dys=={-1} or dys=={1} or dxs=={-1} or dxs=={1}
    if not eenkant: continue
    # buren moeten onderling verbonden zijn (lijn langs P), en P moet niet een hoek in een lijn zijn
    if len(nb)==2 and max(abs(nb[0][0]-nb[1][0]),abs(nb[0][1]-nb[1][1]))>1: continue
    bult.add((y,x))
los=sorted(p for p in set(los)|bult if not (40<=p[0]<=43 and 11<=p[1]<=16))   # oogzone: stap 2
n=len(los)
# regel B (op 8x lezen diagonaal-alleen-verbonden stukjes als losse stippen): binnen-donkere 4-verbonden stukjes van <=2 px
#  die niet (4-buren) aan de buitenlijn vastzitten
lab4=np.zeros((64,64),int); m4=0; B=set()
for y,x in zip(*np.where(binnen)):
    if lab4[y,x]: continue
    m4+=1; st=[(y,x)]; lab4[y,x]=m4; c=[]
    while st:
        a,b=st.pop(); c.append((a,b))
        for p_,q_ in ((a+1,b),(a-1,b),(a,b+1),(a,b-1)):
            if 0<=p_<64 and 0<=q_<64 and binnen[p_,q_] and not lab4[p_,q_]: lab4[p_,q_]=m4; st.append((p_,q_))
    vast=any(buiten[p_,q_] for a,b in c for p_,q_ in ((a+1,b),(a-1,b),(a,b+1),(a,b-1)) if 0<=p_<64 and 0<=q_<64)
    if len(c)<=2 and not vast: B.update(c)
B={p for p in B if not (40<=p[0]<=43 and 11<=p[1]<=16)} - set(los)
los_A=set(los); los=sorted(set(los)|B)
TONEN={'g':None}
def kleur(y,x):
    w=modus(x,y,nat); w.pop('.',None); w.pop('#',None)
    if not w: return None
    k=max(w,key=w.get)
    if k=='g':  # grijs: tint per helderheid uit de grijze cellen
        from reduceer import X0,Y0,s,LEFT,TOP
        ya=Y0+(y-TOP)*s; xa=X0+(x-LEFT)*s
        cs=[nat[yy,xx] for yy in range(int(ya),int(np.ceil(ya+s))) for xx in range(int(xa),int(np.ceil(xa+s))) if 0<=yy<100 and 0<=xx<100 and nat[yy,xx].mean()>=45 and abs(int(nat[yy,xx][0])-int(nat[yy,xx][2]))<16]
        c=np.median(np.array(cs),0)
        return [10,11,12,13][int(np.argmin([((np.array(PAL[i])-c)**2).sum() for i in (10,11,12,13)]))]
    return int(k)
opg=[]; gehouden=[]
for y,x in los:
    v=kleur(y,x)
    if v is None: gehouden.append((x,y)); continue
    I[y,x]=v; opg.append((x,y,v))
print('regel A',len(los_A),'regel B',len(B)); print('los:',sorted((x,y,int(I0[y,x])) for y,x in los)); print('binnen-zwart',binnen.sum(),'componenten',n,'opgeruimd',len(opg),'geen modelkleur (blijft zwart)',gehouden)
np.save('r3_opg.npy',np.array([(x,y) for x,y,v in opg]))
# 2. OOG: zwarte lijnpixels die (4-buren) aan het oranje grenzen, behalve de wenkbrauw erboven (rij 40, model daar puur zwart ~5)
#    model links/onder/rechts van het oog: (12,4,3) (37,34,32) (25,17,11) (45,31,29) -> donkerste grijstint 10 (46,46,48)
oranje=[(y,x) for y,x in zip(*np.where((I==14)|(I==15)))]
oog=set()
for y,x in oranje:
    for dy,dx in ((0,1),(0,-1),(1,0),(-1,0)):
        p=(y+dy,x+dx)
        if I[p]==1 and p[0]!=40: oog.add(p)
for p in oog: I[p]=10
print('oog: zwart -> 10:',sorted((x,y) for y,x in oog))
np.save('r3_I.npy',I); png(I,'r3.png'); png(I,'r3_8x.png',8)
# overzicht: r3 op 8x, opgeruimde pixels rood omrand, oogpixels blauw omrand
from PIL import Image,ImageDraw
im=Image.open('r3.png').convert('RGBA'); bg=Image.new('RGBA',(64,64),(255,255,255,255)); bg.alpha_composite(im)
r2=Image.open('r2.png').convert('RGBA'); bg2=Image.new('RGBA',(64,64),(255,255,255,255)); bg2.alpha_composite(r2)
o=Image.new('RGB',(64*8*2+16,64*8+20),(235,235,235)); d=ImageDraw.Draw(o)
d.text((4,2),'r2 (8x): rood = los (8-verbonden regel), oranje = los (regel B: diagonaal-stipjes), blauw = oog',fill=0); d.text((64*8+12,2),'r3 (8x)',fill=0)
for i,b in enumerate((bg2,bg)):
    o.paste(b.convert('RGB').resize((512,512),Image.NEAREST),(4+i*(512+8),16))
for X,Y,v in opg:
    col=(255,0,0) if (Y,X) in los_A else (255,150,0)
    for i in (0,1): d.rectangle([4+i*520+X*8,16+Y*8,4+i*520+X*8+7,16+Y*8+7],outline=col,width=2)
for Y,X in oog:
    for i in (0,1): d.rectangle([4+i*520+X*8,16+Y*8,4+i*520+X*8+7,16+Y*8+7],outline=(0,90,255),width=2)
o.save('opgeruimd_r3.png')
