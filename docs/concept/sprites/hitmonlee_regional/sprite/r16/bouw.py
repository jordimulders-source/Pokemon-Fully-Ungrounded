# r16 (Jordi over r15/ek3): "daar zijn de benen gewoon een normale vorm alsof ze getaped zijn, dus alleen binnen de lijnen
# zie je die golven" · "met geel heb ik getoond hoe je dan een beenvorm kan maken ... de groene lijnen twijfel ik of die
# niet te recht zijn" · "nee de gele lijnen zijn een indicatie" · "maak het netjes".
# Basis = r15 (= ek3). Benen: gladde 1-px omtrek, ligging/breedte uit het model (uniform gefit, subpixelranden, curven
# volgens Dragonfly Cave), ringen binnenin met de r15-ringtabellen. Groene plekken a-f: gemeten in het model.
from PIL import Image; import numpy as np
D='docs/concept/sprites/hitmonlee_regional/'
ek=Image.open(D+'eindkeuring/ek2.png'); e=np.array(ek)
r15=np.array(Image.open(D+'sprite/r15/r15.png')); r=r15.copy()
ZONE={}
def zet(y,x,v,why):
    if r[y,x]!=v: r[y,x]=v; ZONE[(y,x)]=why

def been(naam,omtrek,eindrijen,T1,TM,TE,vrij=()):
    """omtrek: y->(L,R). eindrijen s: boog-uiteinden (raken de omtrek), middenlijn op s+1.
    T1 = gewone ringrij, TM = rij met middenlijn, TE = rij met de uiteinden (r15-tabellen, per breedte)."""
    for y,(L,R) in omtrek.items():
        for x in range(L-3,R+4):
            if r[y,x]!=0 and x not in vrij: zet(y,x,0,naam+': oude omtrek')
        zet(y,L,2,naam+': gladde omtrek (selout lichtkant)'); zet(y,R,1,naam+': gladde omtrek (zwart schaduwkant)')
        w=R-L-1
        T=TE if y in eindrijen else (TM if (y-1) in eindrijen else T1)
        for i,v in enumerate(T[w]): zet(y,L+1+i,v,naam+': ring binnenin (r15-tabel, breedte %d)'%w)

# --- trapbeen. Model (schaal 0,424, subpixel): links 42,3 42,4 41,8 41,8 41,9 41,8 42,0 41,8 41,6 41,4 41,0 40,5 39,8 39,6
#     (rij 11-24), rechts 49,0 ... 48,6 48,4 48,1 48,1 47,3 47,1 46,4 (rij 11-25). Gerasterd als curve 8-3-2-2 (links) en 9-3-3 (rechts).
KB={}
for y in range(12,24):
    # Jordi's gele indicatie: een doorlopende, gelijkmatige buiging (geen lange verticale stukken). Model en indicatie
    # liggen hier binnen ~0,8 px van elkaar; gekozen: links 42/41/40 met runs 6-5-3 (dan 39,38 van ek2: 2-2),
    # rechts 48/47/46 met runs 8-5-4 (dan 45: 2).
    L=42 if y<=15 else (41 if y<=20 else 40)
    R=48 if y<=16 else (47 if y<=21 else 46)
    KB[y]=(L,R)
T1={5:[15,7,6,5,4],6:[15,7,6,6,5,4]}
TM={5:[8,3,2,2,5],6:[8,3,2,2,2,5]}
TE={5:[2,6,5,4,2],6:[2,6,5,5,4,2]}
del KB[23]   # rij 23 = begin doorschijnend deel: alleen omtrek (40,46 = ek2) en de middenlijn van r15 blijven
been('trapbeen',KB,[13,16,19,22],T1,TM,TE)

# --- standbeen. Model (schaal 0,432): links 50,7 51,4 51,1 51,6 51,2 51,3 51,0 50,5 49,6 (rij 45-53), rechts 57,1-57,6 (rij 44-53), 57,6 / 58,1 (rij 54-55).
SB={}
for y in range(44,54):
    SB[y]=(51 if y<=51 else 50, 56 if y<=47 else 57)
S1={4:[7,6,5,4],5:[7,6,5,5,4],6:[7,6,6,5,5,4]}
SM={4:[8,3,2,4],5:[8,3,2,2,4],6:[8,3,2,2,2,4]}
SE={4:[2,5,4,2],5:[2,5,5,4,2],6:[2,5,5,4,4,2]}
been('standbeen',SB,[45,48,51],S1,SM,SE)
# bovenkant voet rij 54: model rechts 57,6 -> rechterrand 57 (was 56; sloot niet aan op rij 53/55)
zet(54,56,3,'standbeen/voet: rechterrand rij 54 naar model'); zet(54,57,1,'standbeen/voet: rechterrand zwart')
# rij 42-43 (aansluiting onder de romp) blijven; rechterrand 56 loopt door tot rij 47, dan 57 t/m de voet (rij 54-55), 58 (rij 56)
# rij 53 links 50 sluit aan op de voet (rij 54 links 50)

# --- (b) overgang voet -> trapbeen: model rij 10 donker op kol 41-43 en 46-48, licht 44-45; rij 11 donker over de hele breedte
#     = een boog (uiteinden 1 rij hoger). Zelfde bouw als de ringbogen.
zet(10,43,2,'(b) enkel: boog-uiteinde links (model rij 10 kol 43 = 19)'); zet(10,47,2,'(b) enkel: boog-uiteinde rechts (model 10)')
zet(11,43,8,'(b) enkel: onder het boog-uiteinde = lichtkant van de eerste ring'); zet(11,47,5,'(b) enkel: idem schaduwkant')

# --- (a) lijn binnen de trapvoet: model donkerrode plooi: bovenrand rij 4 (kol 37-40), rij 5 (41-43), rij 6 (44-48) = schuin, trapjes 2-3-4.
#     ek3 had de bovenrand recht op rij 5/6 (kol 40-43) en stopte op kol 43.
for y,x in [(4,39),(4,40),(5,41),(5,42),(5,43),(6,44),(6,45),(6,46),(6,47)]:
    zet(y,x,3,'(a) plooi trapvoet schuin zoals het model (lum 78-93)')

# --- (f) overgang ring -> doorschijnend deel: model-lijn (natief rij 59-63) loopt van (41,25,6) omhoog-links en recht naar (45,6, 26,5);
#     geen verticale lijn omlaag. ek3: L met een verticaal stuk kol 41 rij 26-27 -> weg (beige van de buren).
zet(26,41,14,'(f) verticale lijn weg (model kol 41 rij 26 = 92/147, geen lijn)'); zet(27,41,14,'(f) idem (model 117/173)')

# --- (c) onderrand romp boven de verre hand: model onderrand 44,8 45,1 45,6 46,0 46,4 46,5 46,9 46,9 47,3 (kol 22-34) = ek3 (runs 3-4-6).
#     De zwarte lijn liep daarna door in de naad met de verre arm (kol 35-36): 8 px recht. Naad = binnenlijn in donkerrood.
zet(46,35,2,'(c) naad romp/verre arm: binnenlijn donkerrood i.p.v. zwart (zwarte onderrand stopt op kol 34)')
zet(46,36,2,'(c) idem')
zet(48,36,1,'(c) linkerrand verre arm 47-48-49 als 1-1-1 trap (model kol 36 onderrand 48,8)')

# --- (d) overgang romp -> standbeen: model onderrand 44,4 43,9 43,7 43,4 43,2 43,0 42,8 42,8 43,2 43,6 (kol 42-51): boog van 0,7 px.
#     kol 45 (43,4) -> rij 43 erbij: boog 4-4 i.p.v. 3-5.
zet(43,45,1,'(d) onderrand kruis: kol 45 een rij lager (model 43,41)'); zet(42,45,12,'(d) binnenkant (zoals 42,44)')

# --- (e) pols nabije arm: model ringlijn loopt schuin (rij 50 kol 10-11 = 48/63, kol 13 rij 49 = 23); ek3 recht op rij 50 kol 10-12.
zet(49,12,13,'(e) polsring: lijn schuin omhoog naar rechts zoals het model'); zet(50,12,15,'(e) onder de lijn: creme zoals rij 51')

np.save(D+'sprite/r16/idx.npy',r)
im=Image.fromarray(r.astype('uint8'),'P'); im.putpalette(ek.getpalette())
im.save(D+'sprite/r16/r16.png',transparency=0)
im.convert('RGBA').resize((512,512),0).save(D+'sprite/r16/r16_8x.png')
prev={}
for l in open(D+'sprite/r15/log.txt'):
    xy=l.split(')')[0][1:]; x,y=map(int,xy.split(',')); prev[(y,x)]=l.split('  ',1)[1].strip()
with open(D+'sprite/r16/log.txt','w') as f:
    for y,x in zip(*np.where(r!=e)):
        f.write('(%d,%d) %d -> %d  %s\n'%(x,y,e[y,x],r[y,x],ZONE.get((y,x)) or ('r15: '+prev.get((y,x),'?'))))
print((r!=e).sum(),'px t.o.v. ek2;',(r!=r15).sum(),'t.o.v. r15; kleuren',len(set(r.ravel())-{0}))
