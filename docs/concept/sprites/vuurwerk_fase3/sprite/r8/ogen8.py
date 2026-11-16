# r8 punt 2 (na Jordi: "het linkeroog is sowieso een blur ... r5 115% nog het beste alleen die heeft dus geen pupil"):
# basis = r5 115% geel (het r5-oog blijft, vorm/plek/hoek uit het model) + vlamtong (vlam8.py). Per probeersel alleen:
#  NABIJ OOG (r5): pupil erin. Donkerste plek in het modeloog (1024 px, >= 0,3 px van de ooglijnen): r4 (13,8;22,05) ->
#    r5 (12,9;22,5) -> pixel (12,22). Varianten: 1 px of 2 px, bijna-zwart (1) of het modelrood (11); eventueel gesloten
#    rand rechtsonder ((13,23),(14,22) -> 2, niet uit het model: daar is het model licht).
#  VER OOG (links, op het model in r5-coordinaten op 64x bekeken, warpmodel.py): buitenste ooglijn = de bruine diagonaal
#    (5,19)-(6,23) (staat al in r5); bovenrand = de tan lijn (6,2-7,0; 19,2-21) -> (7,21) = 2; binnenkant = het lichte vlak
#    tussen die lijnen x 6,5-9, y 20,5-23 -> (8,21),(7,22),(8,22) geel 13 (3 px: kleiner dan het nabije oog, perspectief);
#    pupil = de rode streep van het model (9,2-9,6; 21,6-22,9) -> (9,22) (en (9,21) blijft het modelrood 11).
#    Onderrand (7,23),(8,23) -> 2: NIET uit het model (daar is het licht); nodig om het oog dicht te maken.
import json, numpy as np; from PIL import Image
from vlam8 import vlam
PAL=json.load(open('palet.json'))
basis=vlam(np.asarray(Image.open('../r5/sprite_115_geel.png')).astype(int))
VER={(7,21):2,(8,21):13,(7,22):13,(8,22):13,(7,23):2,(8,23):2}
NIET_MODEL={(7,23),(8,23)}
P={
 'a':dict(ver_pupil={(9,22):1}, nabij_pupil={(12,22):1}, dicht=False),                       # 1 px zwart, beide ogen
 'b':dict(ver_pupil={(9,22):1}, nabij_pupil={(12,22):1}, dicht=True),                        # a + nabij oog gesloten
 'c':dict(ver_pupil={(9,21):1,(9,22):1}, nabij_pupil={(12,22):1,(13,22):1}, dicht=False),    # 2 px pupillen
 'd':dict(ver_pupil={(9,22):11}, nabij_pupil={(12,22):11}, dicht=False),                     # pupillen in het modelrood
 'e':dict(ver_pupil={(9,22):1}, nabij_pupil={(13,22):1}, dicht=True),                        # voorstel: b, nabije pupil 1 px naar rechts (minder scheel)
}
def maak(o):
    a=basis.copy(); nm=set(NIET_MODEL)
    for p,v in VER.items(): a[p[1],p[0]]=v
    for d in (o['ver_pupil'],o['nabij_pupil'],o.get('glans',{})):
        for p,v in d.items(): a[p[1],p[0]]=v
    if o['dicht']:
        for p in ((13,23),(14,22)): a[p[1],p[0]]=2; nm.add(p)
    if o.get('glans'): nm|=set(o['glans'])
    return a,nm
if __name__=='__main__':
    HX='.123456789ABCDEF'; r5=np.asarray(Image.open('../r5/sprite_115_geel.png')).astype(int)
    for k,o in P.items():
        a,nm=maak(o); im=Image.fromarray(a.astype('uint8'),'P'); im.putpalette(sum(PAL,[])+[0]*(768-48)); im.save('sprite_%s.png'%k,transparency=0)
        print(k,'diff t.o.v. r5 115%:',int((a!=r5).sum()),'(waarvan vlamtong 3) | niet uit het model:',sorted(nm))
        for y in range(19,25): print('   %2d'%y,''.join(HX[v] for v in a[y,3:17]))
