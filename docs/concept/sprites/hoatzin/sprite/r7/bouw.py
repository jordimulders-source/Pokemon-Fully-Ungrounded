# Hoatzin r7 = r6_K1 (kuif volledig, snavel r6) + afgeronde snavelpunt uit het model + teken halverwege model-B en de variant.
# Diff 0 buiten de snavelzone en de tekenzone t.o.v. hoatzin_r6_K1.png (bewezen onderaan).
import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from gemeen import *
R6=HIER+'/../r6/'
im=Image.open(R6+'hoatzin_r6_K1.png'); K1=np.array(im); PALR=im.getpalette()
V=np.array(Image.open(R6+'hoatzin_r6_variant_teken.png'))
a,c,L=laad()
o=K1.copy(); tel={}
def snavelzone(X,Yy): return 6<=X<=16 and 15<=Yy<=25 and not (X>=16 and Yy<=18)
def tekenzone(X,Yy): return 18<=X<=30 and 32<=Yy<=45
N4=((-1,0),(1,0),(0,-1),(0,1))
def fg(a_,y,x): return 0<=y<64 and 0<=x<64 and a_[y,x]>0
# --- 1. snavelpunt. r6 nam in de snavelzone alles vanaf 20 % modeldekking; aan de punt gaf dat de hoeken (7,23) 23 %, (7,24) 21 % en
#        (10,24) 39 % erbij, waardoor de onderkant van de punt een recht streepje van 4 px werd (x7-10, y24). Met de gewone drempel
#        (45 %) volgt de punt de modelomtrek: onderste rij alleen (8,24) 92 % en (9,24) 98 %, dus rond afgesloten.
#        Belijning zoals r5: zwart aan de schaduwkant (onder/rechts), selout (donkerste lijftint) aan de lichtkant (boven/links).
v=o.copy()
for X,Yy in ((7,23),(7,24),(10,24)): o[Yy,X]=0
for Yy in range(19,26):
    for X in range(6,13):
        if not o[Yy,X]: continue
        bgo=[not fg(o,Yy+dy,X+dx) for dy,dx in N4]   # boven, onder, links, rechts
        if not any(bgo): continue
        if bgo[1] or bgo[3]: o[Yy,X]=1                     # schaduwkant
        elif o[Yy,X]!=1: o[Yy,X]=2                         # lichtkant: selout
tel['snavelpunt']=int((v!=o).sum())
# Gemeten (modelkolommen, onderrand van de snavel in spritecoordinaten): x12,5 21,98 | x13 21,61 | x13,5 21,37 | x14 21,01 |
# x15-17 20,76 | x17,5-20,5 21,01 | x21 21,37. Van de kaak tot x21 ligt de modelrand binnen 0,25 px vlak, dus op 64 px blijft
# daar één rij zwart (y20, x14-20); het schuine stuk naar de punt (y21 x12-13, y22 x11, y23 x10) staat er al.

# --- 2. teken halverwege: hoofdversie = plek model B, variant = (-2,+1) naar de buikrand. Halverwege = (-1,+1)
#        (de helft van (-2,+1) = (-1,+0,5); afgerond langs de modelnormaal van de buikrand 0,78/-0,63 -> (-1,+1)).
#        Dezelfde 24 tekenpixels (lijst uit r1); de oude plek krijgt de lijftint die de variant daar al had; een verschoven pixel
#        die op de buitenlijn, de verre vleugel of achtergrond valt, valt weg (zoals in de variant).
TP=[(25,34),(25,35),(26,35),(25,36),(26,36),(27,36),(25,37),(26,37),(27,37),
    (21,36),(21,37),(22,37),(21,38),(22,38),(22,39),(24,38),
    (25,40),(26,40),(25,41),(26,41),(27,41),(25,42),(26,42),(27,42)]
DX,DY=-1,1
v=o.copy(); kleur={p:K1[p[1],p[0]] for p in TP}
for X,Yy in TP:
    nv=V[Yy,X]
    if nv not in LIJF:
        nb=[V[Yy+dy,X+dx] for dy in (-1,0,1) for dx in (-1,0,1) if V[Yy+dy,X+dx] in LIJF]
        nv=max(set(nb),key=nb.count)
    o[Yy,X]=nv
weg=0
for (X,Yy),k in kleur.items():
    X2,Y2=X+DX,Yy+DY
    binnen=K1[Y2,X2] in LIJF and all(fg(K1,Y2+dy,X2+dx) for dy,dx in N4) or (X2,Y2) in kleur
    if binnen and K1[Y2,X2]!=1: o[Y2,X2]=k
    else: weg+=1
tel['teken']=int((v!=o).sum())
# --- controle en opslaan ---
zone=np.array([[snavelzone(X,Yy) or tekenzone(X,Yy) for X in range(64)] for Yy in range(64)])
buiten=int((o!=K1)[~zone].sum())
out=Image.fromarray(o.astype('uint8'),'P'); out.putpalette(PALR); out.save(HIER+'/hoatzin_r7.png',transparency=0)
np.save(HIER+'/r7.npy',o)
print(tel,'teken weggevallen',weg,'van',len(TP),'| buiten de zones anders dan K1:',buiten,'| kleuren',len(set(o.ravel())-{0}))
