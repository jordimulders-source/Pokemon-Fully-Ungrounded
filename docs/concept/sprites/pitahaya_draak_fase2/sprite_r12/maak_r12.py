# r12 op eind/pitahaya2_eind_plaatlicht.png: volume onderlijf + poten (Jordi 17 nov: "Je mag met kleur altijd van het model afwijken he").
# Vorm/silhouet ongewijzigd; alleen bestaande tinten; diff alleen in lijf (roze, x 22-51, rij 41-53) en poten (groen).
import numpy as np; from PIL import Image
B='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/pitahaya_draak_fase2/'
N='.KdrpPgGhHwWsv'; I={c:i for i,c in enumerate(N)}
src=Image.open(B+'eind/pitahaya2_eind_plaatlicht.png'); a0=np.array(src).astype(int); a=a0.copy(); LOG=[]
def zet(lst,c,oud,why):
    for x,y in lst:
        assert N[a[y,x]] in oud,(x,y,N[a[y,x]],c)
        if N[a[y,x]]!=c: LOG.append((x,y,N[a[y,x]],c,why)); a[y,x]=I[c]
# 1. Terminator lijf: licht (p) zakt mee met de buikronding (laag in het midden, hoger naar keel en romp; Shelgon/Lairon/Swampert).
T={28:44,29:45,30:45,31:46,32:46,33:46,34:46,35:46,36:46,37:46,38:45,39:45,40:45,41:45,42:44,43:44,44:43,45:43,46:43,47:43}
for x,t in T.items():
    for y in range(43,52):
        if N[a0[y,x]] in 'pr':
            zet([(x,y)],'p' if y<t else 'r','pr','terminator volgt de buikronding')
# 2. Slagschaduw d waar de dijen over het lijf vallen, rechts van de dij (licht linksboven): sikkel die aansluit op de bestaande d-keten.
zet([(32,46),(33,46)],'d','r','slagschaduw middelste dij, sluit aan op (33,47)-(36,50)')
zet([(45,45),(46,45),(47,46),(48,46),(49,46)],'d','r','slagschaduw achterste dij, sluit aan op (50,46)')
# 3. Dijen rond: licht linksboven (H), randlicht rechts terug naar h, schaduw G rechtsonder (Swampert/Salamence).
zet([(29,48),(30,48),(31,48),(29,49),(30,49)],'H','h','middelste dij: hooglicht linksboven')
zet([(30,47)],'H','h','middelste dij: bovenrand hooglicht (anders losse h)')
zet([(33,49),(34,50),(35,51),(36,51)],'h','H','middelste dij: randlicht rechts weg')
zet([(33,51),(34,51),(34,52),(35,52),(36,52)],'G','hH','middelste dij: schaduwsikkel rechtsonder')
zet([(42,47),(43,47),(41,48),(42,48),(43,48),(41,49)],'H','h','achterste dij: hooglicht linksboven')
zet([(41,47)],'H','h','achterste dij: bovenrand hooglicht (anders losse h)')
zet([(47,48),(47,49),(48,49),(47,50),(48,51)],'h','H','achterste dij: randlicht rechts weg')
zet([(46,50),(46,51),(47,51),(45,52),(46,52),(47,52)],'G','hG','achterste dij: schaduwsikkel rechtsonder')

# ---- asserts en opslaan ----
chg={(x,y) for y,x in zip(*np.where(a!=a0))}
assert ((a>0)==(a0>0)).all()
for x,y in chg: assert (N[a0[y,x]] in 'drpP' and 22<=x<=51 and 41<=y<=53) or N[a0[y,x]] in 'gGhH',(x,y)
def dam(a): return {(x,y) for y in range(63) for x in range(63) if (q:=a[y:y+2,x:x+2])[0,0]==q[1,1]!=q[0,1]==q[1,0] and 0 not in q}
def los(a): return {(x,y) for y in range(1,63) for x in range(1,63) if a[y,x] and all(a[y+dy,x+dx]!=a[y,x] for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)))}
print('diff',len(chg),'dambord nieuw',sorted(dam(a)-dam(a0)),'losse nieuw',sorted(los(a)-los(a0)))
for y in range(40,56): print('%2d '%y+''.join(N[v] for v in a[y,18:52])+'   '+''.join(N[v] for v in a0[y,18:52]))
im=Image.fromarray(a.astype('uint8'),'P'); im.putpalette(src.getpalette()); im.save('pitahaya2_r12.png',transparency=0)
r=im.convert('RGBA'); bg=Image.new('RGBA',(64,64),(232,234,238,255)); bg.alpha_composite(r); bg=bg.convert('RGB')
bg.resize((512,512),Image.NEAREST).save('pitahaya2_r12_8x.png')
open('pitahaya2_r12_afwijkingen.txt','w').write('x\ty\toud\tnieuw\treden\n'+'\n'.join('\t'.join(map(str,l)) for l in LOG)+'\n')
