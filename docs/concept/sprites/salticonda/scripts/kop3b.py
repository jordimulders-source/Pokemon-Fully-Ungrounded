"""Salticonda kleurronde 3b: vanaf kleur3 alleen de kroon en de snuit opnieuw (met de hand, per rij in globale coordinaten).
Bevroren (wordt na het tekenen letterlijk uit kleur3 teruggezet, dus kan niet per ongeluk veranderen):
oog x20-33 y10-14 + x23-30 y15 | wenkbrauw x21-33 y7-9 + x23-30 y6 + x25-27 y5 | wang/gezichtslijn x33-36 y9-19 |
halsband en lijf: alle rijen >= 20 | alles buiten x0-47 y0-25.
Tekens: . transparant | O K h omlijning | e d c b a zout | f g gezicht | q r s t pekel."""
from PIL import Image
D='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/salticonda/'
CH='.OKhedcbafgqrst'
# rij -> lijst van (x, tekens); alles in rij 0-19 wat hier niet staat en niet bevroren is, wordt transparant
NIEUW = {
 # kroon: 5 zoutplaten (voorhoofd, top, achter-boven, achter-midden, achter-onder), naden in warm oker g, lichte opstaande randen
 1: [(26,"hhhhK")],
 2: [(22,"hhhhaababKK")],
 3: [(18,"hhhhagabbbbbccgKK")],
 4: [(16,"hhaabbbcgabbbbcgbbcKK")],
 5: [(5,"hhhhh"),(15,"heeeeebbbb"),(28,"bcgaggbccKK")],
 6: [(4,"haaaaah"),(13,"hhaaaafeee"),(31,"baaggcddK")],
 7: [(3,"haaaaabchh"),(13,"aaaaaaaa"),(34,"aaggcdK")],
 8: [(3,"haOOaaKcha"),(13,"aaaaaaaa"),(34,"daabggeK")],
 9: [(4,"hcccccbb"),(12,"baaaaaaaa"),(37,"baabcK")],
 10:[(5,"haaaaaaaaaaaaaaa"),(37,"cbbccdO")],
 11:[(5,"haaaaaaaaaaaaaaa"),(37,"gcccddeO")],
 12:[(5,"haaaaaaaaaaaaaaa"),(37,"gggdddeO")],
 13:[(5,"Kaaaaaaaaaaaaaaf"),(37,"gbbggdcbK")],
 14:[(6,"haageeeeffaaaff"),(37,"gccbbggO")],
 15:[(6,"Keefffffeefffffff"),(37,"cgcccbdO")],
 16:[(7,"Keffffffeeeffffffffffff"),(37,"cgddddeO")],
 17:[(8,"Keffffffeeefffffffffff"),(37,"cgdddeeO")],
 18:[(8,"Kffffffffffe"),(37,"gdddeeeO")],
 19:[(9,"KKOgfffffff"),(37,"gddeeeeO")],
}
def frozen(x,y):
    if y>=20 or x>47 or y>25: return True
    if 20<=x<=33 and 10<=y<=14: return True
    if 23<=x<=30 and y==15: return True
    if 21<=x<=33 and 7<=y<=9: return True
    if 23<=x<=30 and y==6: return True
    if 25<=x<=27 and y==5: return True
    if 33<=x<=36 and 9<=y<=19: return True
    return False
def build():
    K3=Image.open(D+'kleur3/salticonda.png'); P=K3.load()
    out=K3.copy(); Q=out.load()
    # rijen 0-19: kroon- en snuitzone leeg; behalve wat in kleur3 tussen snuit en oog/wang al goed stond (x 19-36 rij 10-19 links van het oog blijft kleur3)
    for y in range(0,20):
        for x in range(0,48):
            if not frozen(x,y): Q[x,y]=0
    # wat de snuitrijen niet raken tussen x=20 en de wang (onder het oog, rij 15-19) komt uit kleur3
    for y in range(15,20):
        for x in range(20,33): Q[x,y]=P[x,y]
    for y,segs in NIEUW.items():
        for x0,t in segs:
            for i,ch in enumerate(t):
                x=x0+i
                if not frozen(x,y) and ch!='C': Q[x,y]=CH.index(ch)
    for x in range(64):
        for y in range(64):
            if frozen(x,y): Q[x,y]=P[x,y]
    return out
if __name__=='__main__':
    im=build(); im.save(D+'kleur3b/salticonda.png',transparency=0)
    Q=im.load()
    open(D+'kleur3b/salticonda_raster.txt','w').write('\n'.join(''.join(CH[Q[x,y]] for x in range(64)) for y in range(64))+'\n')
