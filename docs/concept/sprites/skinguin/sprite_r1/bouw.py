# Bouwt Skinguin A (en B) uit de kale reductie (kaal.txt). Stappen:
#  1 kaal -> eindpalet (zelfde vlakken, Gen 3-tinten)
#  2 opschonen: tintclusters < 3 px opgaan in de buren (ruis), binnen dezelfde kleurgroep
#  3 buitenlijn: randpixels -> lijn (lichtkant gekleurde selout, schaduwkant zwart); binnenlijnen in rood -> donkerrood
#  4 handreparaties (lijst FIX, elk benoemd) + muts-bovenlijn (MUTS)
#  5 variant B: verre poot + ski verschoven
import numpy as np, sys, json; from PIL import Image
o=np.loadtxt('kaal.txt',dtype=int); H,W=o.shape
# eindpalet
PAL=[(255,0,255),
 (24,16,32),     #1 zwart
 (112,24,40),    #2 rood lijn/selout
 (168,32,48),    #3 rood schaduw (eindkeuring DC: was 176,36,44)
 (224,64,56),    #4 rood midden (eindkeuring DC: was 216,56,56)
 (240,120,104),  #5 rood licht
 (248,248,248),  #6 wit
 (200,200,216),  #7 grijs licht
 (120,120,144),  #8 grijs donker (lijn/selout wit)
 (248,208,72),   #9 geel licht (Delibird-geel, hoofdtint van ski/snavel zoals in het model)
 (232,180,56),   #10 geel midden
 (208,148,44),   #11 geel schaduw
 (112,64,8),     #12 bruin lijn/selout geel
]
# kaal-index -> eind: 1 K,2 bruin,3 S,4 M,5 L,6 W,7 g,8 d,9 Y licht,10 y donker,11 o midden
MAP={0:0,1:1,2:12,3:3,4:4,5:5,6:6,7:7,8:8,9:9,10:11,11:10}
s=np.vectorize(MAP.get)(o)
# kaal-index 2 (modelkleur 66,48,48) is alleen bruin naast geel; elders (oog, wenkbrauw) is het zwart
for y,x in zip(*np.where(o==2)):
    if not any(o[yy,xx] in (9,10,11) for yy in range(max(0,y-1),min(H,y+2)) for xx in range(max(0,x-1),min(W,x+2))): s[y,x]=1
GROEP={3:'r',4:'r',5:'r',6:'w',7:'w',9:'y',10:'y',11:'y'}
# 2 ruis: tintclusters < 3 px (4-buren) -> meest voorkomende buurtint uit dezelfde groep
def clusters(a):
    seen=np.zeros_like(a,bool); out=[]
    for y in range(H):
        for x in range(W):
            if seen[y,x] or a[y,x] not in GROEP: continue
            v=a[y,x]; st=[(y,x)]; seen[y,x]=True; cl=[]
            while st:
                p=st.pop(); cl.append(p)
                for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                    q=(p[0]+dy,p[1]+dx)
                    if 0<=q[0]<H and 0<=q[1]<W and not seen[q] and a[q]==v: seen[q]=True; st.append(q)
            out.append((v,cl))
    return out
ruis=0
for it in range(3):
    for v,cl in clusters(s):
        if len(cl)>=3: continue
        from collections import Counter
        c=Counter()
        for y,x in cl:
            for dy,dx in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1)):
                q=(y+dy,x+dx)
                if 0<=q[0]<H and 0<=q[1]<W and s[q]!=v and GROEP.get(s[q])==GROEP[v]: c[s[q]]+=1
        if c:
            n=c.most_common(1)[0][0]
            for p in cl: s[p]=n; ruis+=1
np.savetxt('stap2.txt',s,fmt='%d')
print('ruis weg',ruis)
# 3 buitenlijn + binnenlijnen
BINNEN_ROOD=False   # binnenlijnen blijven zwart zoals het model (vleugel over lijf leest anders niet)
bg=(s==0)
SEL={'r':2,'w':8,'y':12}
def nb8(y,x):
    for dy in (-1,0,1):
        for dx in (-1,0,1):
            if dy or dx: yield dy,dx
lijn=0; t=s.copy()
for y in range(H):
    for x in range(W):
        v=s[y,x]
        if v==0: continue
        # buitennormaal uit de achtergrondburen
        ny=nx=0; rand=False
        for dy,dx in nb8(y,x):
            yy,xx=y+dy,x+dx
            b= not(0<=yy<H and 0<=xx<W) or bg[yy,xx]
            if b:
                ny+=dy; nx+=dx
                if abs(dy)+abs(dx)==1: rand=True
        if not rand: continue
        licht=(-ny-nx)>0   # normaal wijst naar linksboven
        if v in GROEP:
            t[y,x]=SEL[GROEP[v]] if licht else 1; lijn+=1
        elif v in (2,8,12) and not licht:
            t[y,x]=1; lijn+=1
        elif v==1 and licht:
            # zwarte lijn aan de lichtkant -> selout van de groep eronder/ernaast
            from collections import Counter
            c=Counter(GROEP[s[y+dy,x+dx]] for dy,dx in nb8(y,x) if 0<=y+dy<H and 0<=x+dx<W and s[y+dy,x+dx] in GROEP)
            if c: t[y,x]=SEL[c.most_common(1)[0][0]]; lijn+=1
# binnenlijnen: zwart dat niet aan de achtergrond grenst en alleen rood/lijn als buren heeft -> donkerrood
for y in range(H):
    for x in range(W):
        if s[y,x]!=1: continue
        nbv=[s[y+dy,x+dx] for dy,dx in nb8(y,x) if 0<=y+dy<H and 0<=x+dx<W]
        if 0 in nbv: continue
        if BINNEN_ROOD and all(v in (1,2,3,4,5) for v in nbv): t[y,x]=2; lijn+=1
s=t
np.savetxt('stap3.txt',s,fmt='%d'); print('lijn gewijzigd',lijn)
lijnraster=s.copy()
# 4a muts-bovenlijn (toegestane afwijking 1): lange rechte lijn -> licht gebogen boog, runs 1,1,1,2,2,2,3,6,8 oplopend naar de pompon
TOP={3:11,4:10,5:9,6:8,7:8,8:7,9:7,10:6,11:6,12:5,13:5,14:5,15:4,16:4,17:4,18:4,19:4,20:4,21:3,22:3,23:3,24:3,25:3,26:3,27:3,28:3}
muts=s.copy(); mutsn=0
for x,ty in TOP.items():
    col=s[:12,x]; oy=int(np.argmax(col>0))     # oude bovenrand
    new=s[:,x].copy()
    if ty<oy:   # rand omhoog: kolom 1 px uitbreiden, binnenpixel krijgt de tint van de rij eronder
        for y in range(ty,oy): new[y]=2
        new[oy]=s[oy+1,x]
    elif ty>oy:
        for y in range(oy,ty): new[y]=0
        new[ty]=2
    mutsn+=int((new!=s[:,x]).sum()); s[:,x]=new
print('muts px',mutsn)
# 4b handreparaties (elk naar het model)
FIX=[(22,38,3,'eindkeuring MOET 2: los grijs pixel in het rood -> roodschaduw (canvas 39,25)'),(15,44,2,'eindkeuring MOET 3: zwarte binnenlijn in lichte veer -> donkerrood (canvas 45,18)'),(14,45,2,'eindkeuring MOET 3: zwarte binnenlijn in lichte veer -> donkerrood (canvas 46,17)'),(13,46,2,'eindkeuring MOET 3: zwarte binnenlijn in lichte veer -> donkerrood (canvas 47,16)'),(11,48,2,'eindkeuring MOET 3: zwarte binnenlijn in lichte veer -> donkerrood (canvas 49,14)'),(12,48,2,'eindkeuring MOET 3: zwarte binnenlijn in lichte veer -> donkerrood (canvas 49,15)'),(14,48,2,'eindkeuring MOET 3: zwarte binnenlijn in lichte veer -> donkerrood (canvas 49,17)'),(10,49,2,'eindkeuring MOET 3: zwarte binnenlijn in lichte veer -> donkerrood (canvas 50,13)'),(13,49,2,'eindkeuring MOET 3: zwarte binnenlijn in lichte veer -> donkerrood (canvas 50,16)'),(12,50,2,'eindkeuring MOET 3: zwarte binnenlijn in lichte veer -> donkerrood (canvas 51,15)'),(11,51,2,'eindkeuring MOET 3: zwarte binnenlijn in lichte veer -> donkerrood (canvas 52,14)'),(9,52,2,'eindkeuring MOET 3: zwarte binnenlijn in lichte veer -> donkerrood (canvas 53,12)'),(10,52,2,'eindkeuring MOET 3: zwarte binnenlijn in lichte veer -> donkerrood (canvas 53,13)'),(55,11,10,'eindkeuring KAN 4: ski geel licht -> midden (canvas 12,58)'),(55,12,10,'eindkeuring KAN 4: ski geel licht -> midden (canvas 13,58)'),(55,13,10,'eindkeuring KAN 4: ski geel licht -> midden (canvas 14,58)'),(55,14,10,'eindkeuring KAN 4: ski geel licht -> midden (canvas 15,58)'),(53,3,12,'eindkeuring KAN 5: zwart -> bruin lijn (canvas 4,56)'),(54,3,12,'eindkeuring KAN 5: zwart -> bruin lijn (canvas 4,57)'),(54,6,12,'eindkeuring KAN 5: zwart -> bruin lijn (canvas 7,57)'),(55,6,12,'eindkeuring KAN 5: zwart -> bruin lijn (canvas 7,58)'),(3,32,7,'eindkeuring KAN 6: pompon wit -> grijs licht (canvas 33,6)'),(3,33,7,'eindkeuring KAN 6: pompon wit -> grijs licht (canvas 34,6)'),(2,34,7,'eindkeuring KAN 6: pompon wit -> grijs licht (canvas 35,5)'),(4,21,5,'muts: glansband volgt de nieuwe boog'),(4,22,5,'idem'),(4,23,5,'idem'),(31,15,1,'borstlijn: zwart zoals het model (lijnregel gaf hier grijs, brak de lijn)'),(35,20,1,'idem, modelzwart terug'),(36,19,1,'dij onder de buik ligt in de schaduw: modelzwart terug i.p.v. rode selout'),(37,19,1,'idem'),(38,20,1,'idem'),(39,20,1,'idem'),(13,22,1,'keuring MOET 1: witte restpixel van de spleet muts/vleugel gesloten met lijnkleur'),(17,26,4,'keuring MOET 2: losse zwarte pixel in rood -> roodtint van de buren'),(12,17,8,'keuring KAN: punt van de wenkbrauwpluk zwart -> grijze lijn van wit, sluit diagonaal aan op (11,18)'),(54,48,11,'keuring KAN: los bruin pixel in nabije ski -> buurtint (lijn eindigt op (53,50))'),(53,7,9,'rode ruispixel midden in de ski (Gemini-artefact) -> geel van de buren')]
for (y,x,v,why) in FIX: s[y,x]=v
np.savetxt('A.txt',s,fmt='%d')
def save(a,naam,ox=1,oy=None):
    hh,ww=a.shape; oy=64-hh if oy is None else oy
    full=np.zeros((64,64),int); full[oy:oy+hh,ox:ox+ww]=a
    im=Image.fromarray(full.astype('uint8'),'P'); pal=[v for c in PAL for v in c]; im.putpalette(pal+[0]*(48-len(pal))); im.save(naam,transparency=0,bits=4)
    return full
if __name__=='__main__' and len(sys.argv)>1 and sys.argv[1]=='tussen':
    save(s,'stap3.png'); Image.open('stap3.png').convert('RGB').resize((512,512),Image.NEAREST).save('stap3_8x.png')

# 5 opslaan A
A=s.copy(); save(A,'skinguin_A.png')
# 6 variant B: verre poot + ski (los onderdeel vanaf rij 41, floodfill vanaf de verre ski) naar rechts, schuin aflopend zodat de dij-aansluiting blijft
from collections import deque
m=np.zeros_like(A,bool); q=deque([(51,10)])
while q:
    y,x=q.popleft()
    if 0<=y<H and 0<=x<W and y>=41 and not m[y,x] and A[y,x]!=0 and A[y,x] not in (2,3,4,5):
        m[y,x]=True; q.extend([(y+1,x),(y-1,x),(y,x+1),(y,x-1)])
SHIFT=lambda y: 0 if y<=42 else (1 if y<=45 else 2)
B=A.copy(); B[m]=0
for y,x in zip(*np.where(m)): B[y,x+SHIFT(y)]=A[y,x]
# naad: geelpixels van de verschoven poot die nu aan de achtergrond grenzen krijgen een lijn (zelfde regel als stap 3)
naad=[]
for y in range(41,47):
    for x in range(W):
        if B[y,x] not in (9,10,11): continue
        nbg=[(dy,dx) for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)) if B[y+dy,x+dx]==0]
        if nbg:
            ny=sum(d[0] for d in nbg); nx=sum(d[1] for d in nbg)
            B[y,x]=12 if nx<0 else 1; naad.append((y,x,int(B[y,x])))
print('naad',naad)
np.save('poot_masker.npy',m)
np.savetxt('B.txt',B,fmt='%d')
save(B,'skinguin_B.png')
# bewijs: diff A<->B alleen binnen het pootgebied
d=np.argwhere(A!=B); print('diff A-B',len(d),'rijen',d[:,0].min(),d[:,0].max(),'kolommen',d[:,1].min(),d[:,1].max())
buiten=[(y,x) for y,x in d if not (m[y,x] or (x>=1 and m[y,x-SHIFT(y)]) or (x>=2 and m[y,x-2]) )]
print('diff buiten verre poot+ski (incl. verschoven plek):',len(buiten))

with open('normal.pal','w') as f:
    f.write('JASC-PAL\r\n0100\r\n16\r\n')
    for c in PAL+[(0,0,0)]*(16-len(PAL)): f.write('%d %d %d\r\n'%c)
# afwijking t.o.v. de kale reductie (kaal.txt in eindpalet = stap 1), per zone en per stap
k1=np.vectorize(MAP.get)(o)
st2=np.loadtxt('stap2.txt',dtype=int); st3=np.loadtxt('stap3.txt',dtype=int)
def zone(y,x):
    if y>=41 or (y>=36 and x<=27 and A[y,x] in (9,10,11,12)) or (A[y,x] in (9,10,11,12) and y>=30): return 'poten+ski'
    if y<=11 and x<=36: return 'muts+pompon'
    if x<=14 and 11<y<=30: return 'gezicht (oog/snavel/wenkbrauw)'
    return 'lijf+vleugels'
from collections import defaultdict
tel=defaultdict(lambda: defaultdict(int))
for y in range(H):
    for x in range(W):
        z=zone(y,x)
        if k1[y,x]!=st2[y,x]: tel[z]['ruis']+=1
        if st2[y,x]!=st3[y,x]: tel[z]['lijn']+=1
        if st3[y,x]!=A[y,x]: tel[z]['muts/hand']+=1
        if k1[y,x]!=A[y,x]: tel[z]['totaal']+=1
for z in tel: print(z,dict(tel[z]))
