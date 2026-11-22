# Pinsir-evolutie r3: ALLEEN poten en onderlijf (y >= 36, x >= 14: arm met klauwen linksonder, twee benen, buik, staart).
# Alles daarboven en alle kaak- en dekschildpixels (+1 px eromheen) komen 1-op-1 uit r2 (script-check onderaan).
# Werkwijze (model overnemen, per onderdeel): voor elke spritecel in de zone is uit het 1024-model gemeten (gereedschap/model.py):
#   - zwartaandeel van de cel (modellijn) en
#   - gemiddelde helderheid van de niet-zwarte modelpixels in de cel.
# Op die metingen is per onderdeel (arm, hand, linkerdijplaat, linkerknieplaat, scheen/voet, buiksegmenten, onderarmstrook,
# middelste hand, rechterdij, rechterknie, scheen/voet, staart) een tekstraster opgezet (raster.txt): zwart op de modellijnen,
# binnen elke plaat de modelschaduw in de lijftinten 2-5 (modelhelderheid < 34 -> 2, < 51 -> 3, < 80 -> 4, >= 80 -> 5; de
# glans van het model = 5), zodat elk deel één omlijnde vorm is i.p.v. losse vlekken. Daarna:
#   1. buitenlijn Gen 3 (zoals r2 stap 5): randpixel met achtergrond onder/rechts -> zwart, alleen boven/links -> selout 3;
#   2. klauwen (klauwen.txt): klauwen zijn op 64 px 1-2 px breed en liggen op de rand; stap 1 maakte ze geheel zwart (r2-probleem).
#      Lichte klauwpixel (4/5, modelglans van de klauw) op de rand aan de lichtkant, zwart op de punt/schaduwkant.
# Bouwen: cd pinsir_evo && python3 sprite_r3/bouw.py [toon]
import sys, numpy as np
sys.path.insert(0,'gereedschap'); from model import *; from gemeen import *
from PIL import Image; from scipy import ndimage
UIT='sprite_r3'
R2=np.asarray(Image.open('sprite_r2/pinsir_evo_r2.png')).astype(int); o=R2.copy()
yy,xx=np.mgrid[:64,:64]
KEEP=ndimage.binary_dilation(np.isin(R2,list(KAAK|SCHILD)),structure=np.ones((3,3)))
E=(yy>=36)&(xx>=14)&(R2>0)&~KEEP           # bewerkbare zone
M={'K':1,'2':2,'3':3,'4':4,'5':5}
def lees(path):
    for ln in open(path):
        if ln.strip():
            Y,X0,s=ln.split()
            for i,ch in enumerate(s): yield int(Y),int(X0)+i,M[ch]
gezet=np.zeros((64,64),bool)
for Y,X,k in lees(UIT+'/raster.txt'):
    assert E[Y,X],('buiten de zone',X,Y); o[Y,X]=k; gezet[Y,X]=True
# niet in het raster = r2 gehouden: de rugstekels (53-54,37-38) en (55,43-44) aan de rand van het dekschild (geen onderlijf)
stap1=o.copy()
f=o>0
for Y,X in zip(*np.where(E)):
    bg=[not f[Y+dy,X+dx] if 0<=Y+dy<64 and 0<=X+dx<64 else True for dy,dx in ((-1,0),(1,0),(0,-1),(0,1))]
    if any(bg) and o[Y,X]!=1: o[Y,X]=1 if (bg[1] or bg[3]) else 3
n_rand=int((o!=stap1).sum())
stap2=o.copy()
for Y,X,k in lees(UIT+'/klauwen.txt'):
    assert E[Y,X] and o[Y,X]>0; o[Y,X]=k
n_klauw=int((o!=stap2).sum())
opslaan(o,UIT+'/pinsir_evo_r3.png')
if len(sys.argv)>1 and sys.argv[1]=='toon': toon(o,36,62,14,64)
# --- controles ---
print('diff met r2 boven y36:',int((o[:36]!=R2[:36]).sum()))
print('diff met r2 in kaak/dekschild (+1 px rand), x<14 en overal buiten de zone:',int((o[~E]!=R2[~E]).sum()))
print('silhouet-diff met r2:',int(((o>0)!=(R2>0)).sum()))
print('anders dan r2 (alleen in de zone):',int((o!=R2).sum()),'van',int(E.sum()),'zonepixels | stap buitenlijn:',n_rand,'| klauwen:',n_klauw)
# afwijking van de directe modelvertaling per cel (zwart >= 60 % -> K, anders helderheid -> 2..5), per onderdeel
a,c,fg=klassen(); L=a.mean(2); CEL=974/64; MX0,MY0=31,134; DY=13
def model_tint(Y,X):
    j=Y-DY; ya,yb=int(round(MY0+j*CEL)),int(round(MY0+(j+1)*CEL)); xa,xb=int(round(MX0+X*CEL)),int(round(MX0+(X+1)*CEL))
    cc=c[ya:yb,xa:xb]; ff=fg[ya:yb,xa:xb]; body=ff&(cc>=2)
    if (cc==1).mean()>=0.6 or not body.any(): return 1
    v=L[ya:yb,xa:xb][body].mean(); return 2 if v<34 else 3 if v<51 else 4 if v<80 else 5
DELEN=[('arm + hand links',lambda X,Y: X<=24 and Y>=42 and not (X>=22 and Y>=47)),('linkerbeen (dij, knie, scheen, voet)',lambda X,Y: 22<=X<=31 and Y>=45),
       ('buik + borst',lambda X,Y: 25<=X<=35 and Y<=48),('onderarmstrook + middelste hand',lambda X,Y: 32<=X<=40),
       ('rechterbeen (dij, knie, scheen, voet)',lambda X,Y: 40<=X<=50),('staart',lambda X,Y: X>=48)]
t={}
for Y,X in zip(*np.where(E)):
    if not gezet[Y,X]: continue
    if o[Y,X]!=model_tint(Y,X):
        d=next((n for n,fn in DELEN if fn(X,Y)),'rest'); t[d]=t.get(d,0)+1
print('pixels die afwijken van de directe modelvertaling (cel-zwart/cel-helderheid), per onderdeel:',t,'totaal',sum(t.values()))
