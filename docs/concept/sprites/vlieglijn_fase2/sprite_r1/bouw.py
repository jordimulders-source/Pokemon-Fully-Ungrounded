# mug r1: kale reductie (kaal2.txt, uit het model berekend) -> technische opschoning -> benoemde reparaties per zone.
# Elke reparatie staat hieronder als (zone, x, y, teken, reden). Tekens: zie txt.py.
import numpy as np
from collections import Counter
from txt import CH
a=np.loadtxt('kaal2.txt',dtype=int); H,W=a.shape
G={2:'c',3:'g',4:'g',5:'g',6:'p',7:'p',8:'p',9:'l',10:'l',11:'l',12:'y',13:'y',14:'e',15:'e'}
N8=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
def clusters(a,v):
    seen=np.zeros_like(a,bool); res=[]
    for y,x in zip(*np.where(a==v)):
        if seen[y,x]: continue
        st=[(y,x)]; seen[y,x]=True; c=[]
        while st:
            p=st.pop(); c.append(p)
            for dy,dx in N8:
                q=(p[0]+dy,p[1]+dx)
                if 0<=q[0]<H and 0<=q[1]<W and not seen[q] and a[q]==v: seen[q]=True; st.append(q)
        res.append(c)
    return res
# ---- 1. vlekjes < 3 px binnen een kleurgroep (niet zwart/oog/geel/hooglicht w)
for it in range(2):
    for v in (3,4,6,7,8,9,10,11):
        for c in clusters(a,v):
            if len(c)>=3: continue
            nb=Counter()
            for y,x in c:
                for dy,dx in N8:
                    q=(y+dy,x+dx)
                    if 0<=q[0]<H and 0<=q[1]<W and G.get(a[q])==G[v] and a[q]!=v: nb[a[q]]+=1
            if nb:
                t=nb.most_common(1)[0][0]
                for p in c: a[p]=t
stap_vlek=a.copy()
# ---- 2. randpass: elke buitenrandpixel wordt lijn; lucht rechts/onder = zwart, alleen boven/links = selout van de groep
SEL={'g':2,'c':2,'p':6,'l':1,'y':12,'e':1}
m=a>0; b=a.copy()
def lucht(y,x): return not(0<=y<H and 0<=x<W) or not m[y,x]
for y in range(H):
    for x in range(W):
        if not m[y,x]: continue
        bo,on,li,re=lucht(y-1,x),lucht(y+1,x),lucht(y,x-1),lucht(y,x+1)
        if not(bo or on or li or re): continue
        if on or re: b[y,x]=1; continue
        if a[y,x]!=1 and a[y,x] in G: g=G[a[y,x]]
        else:
            nb=Counter(G[a[q]] for q in ((y+1,x),(y,x+1),(y+1,x+1),(y+1,x-1),(y-1,x+1)) if 0<=q[0]<H and 0<=q[1]<W and a[q] in G)
            if not nb: continue
            g=nb.most_common(1)[0][0]
        b[y,x]=SEL[g]
# losse selout (geen andere selout als 8-buur) -> zwart; losse zwarte randpixel tussen selout aan de lichtkant -> selout
a=b
def rand(y,x): return m[y,x] and any(lucht(y+dy,x+dx) for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)))
for y in range(H):
    for x in range(W):
        if a[y,x] in (2,6,12) and rand(y,x) and not any(0<=y+dy<H and 0<=x+dx<W and rand(y+dy,x+dx) and a[y+dy,x+dx]==a[y,x] for dy,dx in N8):
            a[y,x]=1
stap_rand=a.copy()
# ---- 3. benoemde reparaties (alleen naar het model gemeten; zie dekking.py / ntxt.py)
REP=[]
def P(zone,x,y,ch,reden): REP.append((zone,x,y,ch,reden))
# ogen: per cel de meerderheid in het model (dekking.py 12 21 24 28)
P('kop/vizier',21,22,'E','oog dichtbij: model violet 26 / zwart 23 / antraciet; reductie gaf paars P (1 px) -> violet, wenkbrauw /')
P('kop/vizier',16,24,'k','oog ver: model antraciet 41 > zwart 29 > roze 16 > violet 14')
P('kop/vizier',21,24,'e','oog dichtbij: model 44% lichtroze + lichtviolette tussentint (q) tegen 53% violet incl. die tussentint; roze leest op 1x')
P('kop/vizier',15,26,'#','vizier: model zwart 48; reductie gaf los donkerpaars pixel')
P('kop/vizier',15,19,'q','koepelband: model lichtpaars (157,102,169) met zwart; reductie gaf oogviolet E door hoge verzadiging')
P('kop/vizier',20,20,'d','koepelrand: model 4/9 zwart + paars/blauwgrijs; los indigo-pixel l -> buurtint d')
P('naald',12,32,'k','naald voor de klauw: model heeft hier de antraciet linkerrand van de naald (natief k tussen geel gewricht en naaldwit); reductie gaf d')
P('naald',11,33,'k','idem rij 33: model k tussen indigo klauwdeel en naaldwit; naald houdt 2 px vulling (g+d)')
for x,y,c in [(15,27,'g'),(16,27,'d'),(17,27,'g'),(18,27,'d'),(15,28,'g'),(16,28,'g'),(17,28,'g'),(18,28,'d'),(15,29,'g'),(16,29,'g'),(17,29,'k'),
 (14,30,'w'),(15,30,'g'),(16,30,'d'),(13,31,'w'),(14,31,'g'),(15,31,'d'),(13,32,'g'),(14,32,'g'),(12,33,'w'),(13,33,'d'),
 (11,34,'w'),(12,34,'d'),(10,35,'w'),(11,35,'d'),(9,36,'w'),(10,36,'d'),(8,37,'w'),(9,37,'g'),(8,38,'g'),(7,39,'g'),(6,40,'g'),(5,41,'d')]:
    if CH[a[y,x]]!=c: P('naald',x,y,c,'naaldvolume: meest voorkomende modeltint in de cel i.p.v. vlakgemiddelde (licht linksboven, schaduw rechtsonder)')
P('borststuk',27,29,'P','borststuk: model 6/9 donker + lichtpaars; los indigo L -> donkerpaars (zelfde kleurgroep)')
P('achterlijf',46,43,'p','achterlijf: model 3/6 paars (119,72,131) + donkerpaars; los indigo L -> paars')
P('vleugels',35,23,'y','geel accent vleugelaanzet: model 1,1 spritepx (2 lichtgele modelpixels in deze cel); van 1 naar 2 px')
P('vleugels',36,23,'Y','idem, model 2 licht + 2 donker geel; Y blijft')
for zone,x,y,ch,_ in REP: a[y,x]=CH.index(ch)
# vleugels en koepel: vlaktint = meest voorkomende modeltint (het gemiddelde trok dunne lijnen erin -> spikkels), daarna de lange modeladers terug
from modus import modus
from aders import aders
res=modus(a)
for z in ('vleugels','kop/vizier'):
    for x,y,c in res.get(z,[]):
        REP.append((z,x,y,c,'vlaktint: meest voorkomende modeltint in de cel i.p.v. vlakgemiddelde')); a[y,x]=CH.index(c)
for x,y in aders(12):
    if a[y,x] in (4,5): REP.append(('vleugels',x,y,'d','ader: lange modelader (>=12 natieve px) als doorlopende lijn')); a[y,x]=3
np.savetxt('mug_r1.idx',a,fmt='%d')
open('mug_r1.txt','w').write('# mug r1, 64x64, tekens = paletindex: '+' '.join(f'{c}={i}' for i,c in enumerate(CH))+'\n'+'\n'.join(''.join(CH[v] for v in r) for r in a)+'\n')
open('reparaties.txt','w').write('\n'.join(f'{z}: ({x},{y}) -> {c}  {r}' for z,x,y,c,r in REP)+'\n')
k=np.loadtxt('kaal2.txt',dtype=int)
print('afwijkend van kale reductie:',(a!=k).sum(),' waarvan vlekjes',(stap_vlek!=k).sum(),' rand',(stap_rand!=stap_vlek).sum(),' reparaties',(a!=stap_rand).sum())
