# Stap 2: vlam. Basis stap1.png. Palet: index 7 (was ongebruikt 'L') wordt rood (225,58,73) uit fase 3.
# A = alleen kleur (lint: roze bij de armen -> rood waar het lint achter de pijl langs is gegaan, zoals fase 3 kleurt na een kruising;
#     kieuwen/sprieten: donker bij de basis, licht/creme naar de top, zoals de vlamtongen bij de kop van fase 3).
# B = A + vlamtongetjes langs de buitenrand van het lint (vorm van fase 3: punt in selout-kleur, daaronder selout+vlak).
import sys; sys.path.insert(0,'../r10'); from txt import CH
import numpy as np; from PIL import Image
S=Image.open('stap1.png'); a=np.array(S); pal=S.getpalette()[:48]
pal[7*3:7*3+3]=[225,58,73]; CH2=CH[:7]+'r'+CH[8:]; I={c:i for i,c in enumerate(CH2)}
def ch(r,c): return CH2[A[r,c]]
A=a.copy()
# pijl-pixels binnen de pijlkolommen (23-29) die NIET het voorlangs lopende lint zijn
band=set()
for r in range(27,35):
    for c in range(22,30):
        if CH2[a[r,c]] in 'dsm': band.add((r,c))
band|={(30,25),(31,24),(32,23),(33,22)}
def lint(r,c):
    if r<21 or a[r,c]==0: return False
    if r<=22 and c>=35: return False                    # kin/kop
    if 23<=c<=29 and r<=41 and (r,c) not in band: return False   # pijl
    if r in (41,42) and c in (23,29): return False     # ring
    return CH2[a[r,c]] in 'dsmlc#'
def rood(r,c): return (r>=38 and c>=29) or r>=42      # na de kruising achter de pijl: rechterband onder + staart
for r in range(64):
    for c in range(64):
        if lint(r,c) and rood(r,c):
            v=CH2[a[r,c]]
            if v=='s': A[r,c]=I['r']      # vlak -> rood (fase 3 r)
            elif v=='m': A[r,c]=I['l']    # lichtkant -> licht (fase 3 heeft lichte zalm op rood; l is de dichtstbijzijnde)
# staartpunt (rij 53-61): vlak/licht -> rood, creme kern -> licht (donkerder naar de staart, kern blijft het lichtst)
for r in range(53,62):
    for c in range(20,32):
        if A[r,c]==I['l']: A[r,c]=I['r']
        elif A[r,c]==I['c']: A[r,c]=I['l']
# kieuwen/sprieten (gills): basis donkerder, top licht/creme
GILL=[ # (r,c,nieuw) -- per frond: top -> creme c, midden licht l, basis -> m (fase 3: vlamtong creme/roze, donkerder waar hij vastzit)
 (3,34,'c'),(4,33,'c'),(7,33,'m'),(7,34,'m'),          # sprietje boven: top creme, basis roze
 (6,30,'c'),                                          # klein sprietje links ervan: top creme
 (13,48,'c'),(14,44,'m'),(15,44,'m'),(15,45,'m'),     # kieuw 1 (boven): punt creme, basis m
 (17,43,'m'),(17,44,'m'),(18,43,'s'),(18,47,'c'),(18,48,'c'),(19,47,'c'),  # kieuw 2: basis m/s, top creme
 (21,43,'m'),(21,44,'c'),                             # kieuw 3 (onder)
]
for r,c,v in GILL: A[r,c]=I[v]
def save(arr,fn):
    im=Image.fromarray(arr.astype('uint8'),'P'); im.putpalette(pal+[0]*(768-48)); im.save(fn,transparency=0)
save(A,'A.png')
# ---- B: vlamtongetjes (fase 3: punt in donkere tint/selout, daaronder selout + vlak; 1 px breed, 2-3 rijen)
Bv=A.copy()
TONG=[ # (r,c,nieuw, waar)
 # T1 linkerlint (roze), dunne punt links-omhoog vanaf de bult bij rij 37 (zoals de losse punten in fase 3 rij 2-4)
 (36,18,'d','T1'),(35,17,'d','T1 punt'),
 # T2 rechterband (rood, schaduwkant), wijst rechts-omhoog: twee diagonale paren donker+lijn zoals fase 3 (rij 17-18, kol 49-52)
 (39,33,'d','T2'),(39,34,'#','T2'),(38,34,'d','T2 punt'),(38,35,'#','T2 punt'),
 # T3 staart (rood, lichtkant), wijst links-omhoog
 (46,23,'d','T3 punt'),
 # T4 rechterband boven (roze, schaduwkant), wijst rechts-omhoog, zelfde vorm als T2
 (25,35,'d','T4'),(24,36,'#','T4 punt'),(47,22,'d','T3'),(47,23,'l','T3 vlak'),
]
for r,c,v,w in TONG: Bv[r,c]=I[v]
save(Bv,'B.png')
