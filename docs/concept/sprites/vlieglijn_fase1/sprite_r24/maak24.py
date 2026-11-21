# r24 = r23 L12 + (1) rechte lijnen uit Jordi's krabbel breken met randpixels, (2) kleur/schaduwronde.
# Jordi: "Niks hertekenen, behalve wat pixelwerk om rechte lijnen iets minder recht te maken"
import sys
from PIL import Image
H='.123456789abcdef'
src=Image.open('../sprite_r23/vlieg_r23_L12.png'); im=src.copy(); a=im.load()
def put(y,x,s):
    for i,ch in enumerate(s):
        if ch==' ': continue
        a[x+i,y]=H.index(ch)
# --- A kop-bovenrand (rij 23 x13-20): 8 recht -> 6-3-1-1
put(23,19,'..'); put(24,19,'11')
# --- B vizier rechterrand (x22 rij 28-33): bolling 1-1-2-2-1
put(27,21,'5'); put(28,21,'15'); put(30,22,'21'); put(31,22,'21')
# --- C naad borststuk/achterlijf + strepen (gebogen ')') + rechterrand achterlijf
R={
30:"3331333366663331",
33:"22221663366653333551",
34:"222221663355533335531",
35:"2222216633555533355531",
36:"2222216533555533355531",
37:"22231555335553335555331",
38:"22311553355553335553331",
40:"314414453311333344422241",
41:"314491451993133244222241",
44:"9113931444193114922291.",
45:"93139311441ab12222221.",
}
for y,s in R.items(): put(y,30,s)
# --- poten: kabels een heel lichte bocht
for y in (50,51,52):  # poot 1 (x18-21) rij 50-52 1 px naar links
    row=[a[x,y] for x in range(17,22)]
put(50,17,'3931.'); put(51,17,'3931.'); put(52,17,'3931')
put(50,22,'1931.'); put(51,21,'1')  # teen van poot 2 houdt zijn bovenrand   # poot 2 rij 50 1 px naar links
for y in (54,55,56): put(y,30,'.1931')  # poot 3 rij 54-56 1 px naar rechts
# --- KLEUR: borststuk licht linksboven met bolle terminator, sikkel rechtsonder; achterlijf: licht neemt naar rechts af
K={
32:(25,"3333333221"),
33:(25,"333333222"),
34:(24,"33333222222"),
35:(23,"333222222222"),
37:(33,"2"), 38:(32,"2"),
34.5:(49,"2"),
}
for y,(x,s) in K.items():
    if y==34.5: put(34,49,'2'); continue
    put(y,x,s)
put(35,49,'22'); put(36,49,'42'); put(37,48,'4422'); put(38,47,'44222')
im.save(sys.argv[1] if len(sys.argv)>1 else 'vlieg_r24_geo.png',transparency=0)
