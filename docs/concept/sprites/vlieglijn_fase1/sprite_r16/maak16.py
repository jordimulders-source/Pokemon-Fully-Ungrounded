# r16 = r15 A_L2 + glas/LED-ogen (O1/O2) + zichtbaar gebogen onderrand (P1/P2)
# palet: index 7 (kabel donker 50,60,74) samengevoegd met 3 (60,60,66); 7 wordt licht paars (LED-kern)
import sys; sys.path.insert(0,'sprite_r14')
from lib import *
LP=(232,180,255)
def palet(im):
    p=im.getpalette(); p[7*3:7*3+3]=list(LP); im.putpalette(p)
R=[(18,29),(18,30),(17,31),(19,31),(16,32),(20,32),(16,33),(20,33)]
L=[(10,29),(10,30),(9,31),(11,31),(9,32),(12,32),(12,33)]
def glas(b):
    # rechteroog: glans linksboven, donker naar rechtsonder, lichte terugkaatssikkel onderlangs
    for p in ((18,28),(19,28),(17,29),(16,30),(16,31)): b[p]=3
    b[16,29]=4; b[18,28]=4
    for p in ((20,28),(21,28)): b[p]=2
    for p in ((17,34),(18,34),(19,34),(21,32),(21,33)): b[p]=3
    b[18,33]=2   # uit-lampje in de sikkel -> donker puntje
    # linkeroog (ver oog) gelijk
    b[10,28]=4; b[11,28]=3; b[9,29]=3; b[9,30]=3
    for p in ((10,34),(11,34),(12,31)): b[p]=3
    b[12,29]=2
def led(b,v):
    if v=='O1':   # lampjes: kern (licht) op 1-px afstand, paars ertussen als gloed
        kern={(18,29),(17,31),(19,31),(16,33),(20,33),(10,29),(9,31),(11,31),(12,33)}
        for p in R+L: b[p]=7 if p in kern else 13
    else:         # O2: hele ^ licht, paarse gloed lekt eronder op het glas
        for p in R+L: b[p]=7
        S=set(R+L)
        for (x,y) in R+L:
            q=(x,y+1)
            if q not in S and b[q] in (2,3,4): b[q]=13
def poten(b,v):
    # P1: randbelichting langs de onderkant van het borststuk, trap 1-4-6-2 (lager naar het midden)
    b[21,37]=3
    for x in (22,25): b[x,38]=3
    for x in (23,24): b[x,38]=4
    b[26,39]=3; b[31,39]=3
    for x in (27,28,29,30): b[x,39]=4
    b[32,38]=3; b[33,38]=3; b[32,39]=1; b[33,39]=1; b[32,40]=1; b[33,40]=1
    b[36,41]=3; b[37,41]=3          # achterlijf: rand loopt door onder de taille
    if v=='P2':   # voorstel Claude: grijs heupkopje bovenaan elke kabel
        for (x,y),c in (((24,39),5),((25,39),4),((28,40),5),((29,40),5),((30,40),4),
                        ((34,41),5),((35,41),4),((39,41),5),((40,41),5),((41,41),4)):
            b[x,y]=c
def maak(o,p):
    im=Image.open('sprite_r15/vlieg_r15_A_L2.png'); b=im.load()
    for x in range(64):
        for y in range(64):
            if b[x,y]==7: b[x,y]=3
    palet(im); glas(b); led(b,o); poten(b,p); return im
if __name__=='__main__':
    for o in ('O1','O2'):
        for p in ('P1','P2'):
            im=maak(o,p); n='sprite_r16/vlieg_r16_%s_%s'%(o,p)
            im.save(n+'.png',transparency=0); onbg(im).resize((512,512),Image.NEAREST).save(n+'_8x.png')
    im.save('sprite_r16/_pal.png',transparency=0)
    pal=im.getpalette()[:48]
    open('sprite_r16/normal.pal','w').write('JASC-PAL\n0100\n16\n'+''.join('%d %d %d\n'%tuple(pal[i*3:i*3+3]) for i in range(16)))
