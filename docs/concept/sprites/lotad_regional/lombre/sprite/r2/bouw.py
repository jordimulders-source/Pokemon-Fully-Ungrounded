# Gaucho-Lombre r2: basis = r1 A5 (mondvorm A5 blijft). Alleen het hoofd: (1) kop rond de mond consistent, (2) ver oog
# leesbaarder, (3) nabij oog = Gen 3-Lombre-oog, bozer. Varianten A/B/C verschillen alleen in het nabije oog.
# Elke wijziging staat hieronder als losse pixel met reden; de rest van de sprite blijft pixelgelijk aan A5 (controle onderaan).
import numpy as np; from PIL import Image
from gemeen import opslaan
A5=np.array(Image.open('../r1/lombre_gaucho_A5.png')).astype(int)
W,K,R2,R3,R4=15,1,2,3,4   # wit, zwart, rood lijn, rood donker, rood midden

# (1) hoofd consistent
HOOFD=[((28,20),K,'voorkant lip: de omtrek loopt nu in één zwarte lijn van de lippunt naar de kaak (was rest oude kopcontour, rood lijn)'),
       ((27,21),K,'bovenlijn van de lip sluit aan op de kopomtrek (was een los stukje gezicht tussen omtrek en lijn)'),
       ((26,21),R4,'dubbele rode lijn naast het verre oog -> gezicht (de omtrek is x20)')]
HOOFD+=[((33,x),R3,'schaduwsikkel onderaan de kaak in rood donker, zoals de rest van de kop (kaak was één vlak midden)') for x in range(23,31)]
HOOFD+=[((34,x),K,'kinlijn één doorlopende zwarte lijn (was zwart en rood lijn om en om)') for x in range(27,30)]
# (2) ver oog: wit 2 hoog met zwarte stip rechtsboven (naar de kijker), zoals de gaucho-Lotad (wit + stip); los van de omtrek
VER=[((24,21),R4,'zwart boven het verre oog -> gezicht, zodat het oog niet in de zwarte omtrek verdwijnt'),
     ((25,21),W,'ver oog wit (was al wit, model)'),((26,21),W,'ver oog wit, 2e pixel (nieuw)'),((25,22),K,'ver oog stip (was al zwart, model)')]
# (3) nabij oog: eerst het modeloog (x29-34, y25-28) leeg naar gezicht, dan het Gen 3-Lombre-oog.
LEEG=[((y,x),R4,'modeloog weg -> gezicht') for y in range(25,29) for x in range(29,35)]
# Lombre-oog = anim_front_gba.png frame 1, x28-33 y22-25 (wit d, zwart 1). Ongespiegeld: de ooglidlijn zakt naar de voorkant
# (naar de snuit) = boze blik; gespiegeld zou hij naar achter zakken (Lombre's vriendelijke blik).
LOMBRE_OOG={(25,32):W,(25,33):W,(25,34):K,
            (26,29):K,(26,30):W,(26,31):W,(26,32):K,(26,33):K,(26,34):K,
            (27,29):W,(27,30):K,(27,31):K,(27,32):W,(27,33):W,
            (28,30):W,(28,31):W,(28,32):W}
def oog(extra=()):
    d=dict(LOMBRE_OOG)
    for p,k,_ in extra: d[p]=k
    return [(p,k,'Lombre-oog' if p in LOMBRE_OOG else '') for p,k in d.items()]
VAR={
 'A':oog(),
 'B':oog([((26,30),K,'boos: wit boven het ooglid vooraan weg (ooglid dicht vooraan)'),((26,31),R4,'idem, gezicht')]),
 'C':oog([((26,30),R4,'boos: wit boven het ooglid vooraan -> gezicht'),((26,31),R4,'idem')]
        +[((24,x),R2,'wenkbrauw: modelbrauw (rood donker) een tint donkerder, rood lijn') for x in range(29,33)]),
}
if __name__=='__main__':
    log=open('pixels.txt','w')
    basis=A5.copy()
    for (y,x),k,r in HOOFD+VER+LEEG:
        if basis[y,x]!=k or r: pass
        basis[y,x]=k
    for (y,x),k,r in HOOFD+VER:
        log.write('basis (%d,%d) %d->%d  %s\n'%(x,y,A5[y,x],k,r))
    for n,lst in VAR.items():
        o=basis.copy()
        for (y,x),k,r in lst: o[y,x]=k
        opslaan(o,'lombre_gaucho_r2_%s.png'%n)
        d=np.argwhere(o!=A5); 
        buiten=[(x,y) for y,x in d if not(18<=x<=36 and 22<=y<=35)]
        print(n,'verschil met A5: %d px, buiten het hoofdvak x18-36 y22-35: %d'%(len(d),len(buiten)),'kleuren',len(set(o.ravel())))
        for y,x in d: log.write('%s (%d,%d) %d->%d\n'%(n,x,y,A5[y,x],o[y,x]))
