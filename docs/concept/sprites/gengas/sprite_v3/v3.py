# v3 = v2 + reparaties uit keuring v2 (sprite_v2/keuring/KEURING_v2.md). Alles komt uit het model:
#   Q  = model_64_geschrapt gekwantiseerd met het v3-palet (u = wig erbij, w eruit)
#   QS = Q met het gezichtsblok (model rij 28-45, kol 8-27) verschoven +1 rij / +5 kol (zoals v2)
#   N  = het natieve model (74x74) gekwantiseerd, voor de krul
# Elke zone staat hieronder met zijn grenzen; vel.py/diff.py bewijzen dat daarbuiten niets veranderde.
import sys, os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from gemeen import *
from pal import PAL,CH
D=os.path.dirname(os.path.abspath(__file__))+'/'
a=model(); bg=achtergrond(a)
q,_=dichtst(a,PAL[1:]); q=q+1; q[bg]=0
Q=[[CH[v] for v in r] for r in q]
def QS(y,x): return Q[y-1][x-5]
nat=np.asarray(Image.open(M+'gekozen_v3_natief.png').convert('RGB')).astype(float)
n,_=dichtst(nat,PAL[1:]); N=[[CH[v+1] for v in r] for r in n]
R=[list(l.rstrip('\n').replace('w','v')) for l in open(D+'../sprite_v2/raster.txt')][:64]
ZONES={}; log=[]
def zet(y,x,c,zone):
    ZONES.setdefault(zone,set()).add((y,x))
    if R[y][x]!=c: log.append(f'{zone}: ({y},{x}) {R[y][x]}->{c}'); R[y][x]=c

# ---------- palet: w (kern lichtvlek) -> v gebeurt hierboven bij het inlezen (zone P) ----------
for y,l in enumerate(open(D+'../sprite_v2/raster.txt')):
    for x,c in enumerate(l.rstrip('\n')):
        if c=='w': ZONES.setdefault('P lichtvlekkern w->v (paletruil)',set()).add((y,x))

# ---------- MOET 1: wit gat tussen rookarm en rechtermaan = achtergrond (model 255) ----------
for x in (51,52): zet(22,x,'.','M1 gat rookarm')

# ---------- MOET 5 + MAG streep + MOET 3 + MOET 2: gezichtszone opnieuw uit het model ----------
Z='M5/M3/M2 gezichtsnaden'
# rij 25-28 links: de gedempte wig (u) van het model op zijn eigen plek (model kol 10-13)
for y in range(25,29):
    for x in range(10,14):
        if Q[y][x]=='u': zet(y,x,'u',Z)
zet(27,9,'a',Z); zet(28,9,'r',Z)          # rand onder de wig zoals het model (rij 27 'Ka', rij 28 'Kr')
# gezichtsblok rij 30-46, kol 13-32: model verschoven (ogen, masker MET wig u, grijns), rimpixels niet
for y in range(30,47):
    for x in range(13,33):
        c=QS(y,x)
        if x==13 and c=='K': continue      # silhouetrand van het model schuift niet mee
        zet(y,x,c,Z)
# MAG lichte streep: rij 29 droeg een verschoven kopie van modelrij 28 (dubbele streep). Rij 29 wordt de
# overgang: alleen het stuk dat rij 28 (kol 14-23) met de wigtop op rij 30 (kol 20-26) verbindt blijft licht.
for x in range(13,33):
    c=QS(29,x)
    if x<19: zet(29,x,'u' if c=='u' else 'b',Z)      # modelrand-wig (u) links van het oog, verder masker
    elif x<=23: zet(29,x,'l',Z)                        # verbinding streep -> wigtop
    elif c in 'K': zet(29,x,c,Z)                       # wenkbrauw rechteroog
    else: zet(29,x,'b',Z)
# vrijgekomen strook links (kol 8-12): modelband van dezelfde rijen. Rij 29-32: de u-wig van rij 25-28 loopt langs
# de rand naar beneden en versmalt zoals in het model (u op kol 11-13 -> 12 -> 12); rij 33-36 masker.
strook={29:'rbuuu',30:'rbbuu',31:'rbbbu',32:'abbbu',33:'abbbb',34:'bbbbb',35:'bbbbb',36:'abbbb',
        37:'llabb',38:'lllll',39:'lllll',40:'lllll',41:'Klllll'[1:],42:'lllll',43:'lllll',44:'lllll'}
# rij 36-38: maskerrand schuin naar de mondhoek (36,8) -> (37,10) -> (38,14) (MOET 3)
for y,s in strook.items():
    for i,c in enumerate(s):
        x=8+i
        if R[y][x] in 'K' and x<=9: continue
        zet(y,x,c,Z)
zet(37,13,'b',Z); zet(37,14,'a',Z); zet(38,13,'l',Z); zet(38,14,'a',Z)
# rij 45-46 links: de m-band van het model op zijn eigen plek ('Klmllm', 'Krmmmm') -> overgang l->m->r naar de rand
for x,c in zip(range(10,15),'lmllm'): zet(45,x,c,Z)
for x,c in zip(range(11,16),'rmmmm'): zet(46,x,c,Z)
zet(47,12,'u',Z)  # model 'Ku' (was b bij gebrek aan u)
# MOET 2: rechts van de grijns (rij 42-47) weer het model op zijn eigen plek: bandgrens diagonaal
grijns_eind={42:30,43:29,44:28,45:28,46:26}
for y,xe in grijns_eind.items():
    for x in range(xe+1,34): zet(y,x,Q[y][x],Z)
# Gengar-vorm uit v2 opnieuw: pupil rechteroog, bovenlip als doorlopende lijn, tandschaduw één tint
for (y,x),c in {(34,27):'K',(34,28):'K',(35,28):'K',(38,14):'K',(38,15):'K',(39,16):'K',(39,17):'K',(40,18):'K',(40,19):'K',
                (39,14):'H',(39,15):'H',(40,16):'H',(39,30):'H',(35,26):'R'}.items(): zet(y,x,c,Z)

# ---------- MOET 4: krul = de spiraal van het natieve model, zonder geschrapte rij/kolommen ----------
# natief rij 38-45 -> sprite rij 32-39 (natief rij 46, effen l, valt nu af i.p.v. 40); natief kol 43-51 -> sprite
# kol 36-44 (natief kol 42 en 52, effen, vallen af i.p.v. 45 en 50). Lijn in één tint b.
Z4='M4 krul'
for i in range(8):
    for j in range(9):
        c=N[38+i][43+j]
        zet(32+i,36+j,'b' if c=='a' else c,Z4)

open(sys.argv[1] if len(sys.argv)>1 else D+'raster.txt','w').write('\n'.join(''.join(r) for r in R)+'\n')
open(D+'raster.txt.log','w').write('\n'.join(log)+'\n')
import json; json.dump({k:sorted(v) for k,v in ZONES.items()},open(D+'zones.json','w'))
print(len(log),'wijzigingen')
