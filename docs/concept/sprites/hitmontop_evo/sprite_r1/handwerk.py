# Handwerk bovenop raster_draft.txt: per rij (x0, "pixels") met de hand geplaatst; '.' = transparant maken,
# '_' = laten staan. Resultaat: raster.txt (daarna nog los met de hand bijgewerkt).
rows=[list(r.rstrip('\n')) for r in open('raster_draft.txt')]
def seg(y,x0,s):
    for i,c in enumerate(s):
        if c!='_': rows[y][x0+i]=c
E={}
def add(y,x0,s): E.setdefault(y,[]).append((x0,s))
# --- nabije voet (Hitmontop linkervoet, met de hand kleiner nagetekend; zool-kussen, 3 klauwen, witte wikkel)
add(0,9,"dc")
add(1,8,"dc1f")
add(2,4,"98877cf")
add(3,3,"9866666d")
add(4,2,"986555666f")
add(5,1,"98653335669f")
add(6,1,"8653333456698")
add(7,0,"f8665334566c1")
add(8,0,"f8766544667c1")
add(9,0,"fc977666678ff")
add(10,0,"f1cf7777798f")
add(11,0,"f11df99988f")
add(12,1,"ffd11ff")
add(13,3,"ff")
# enkel (bruin) + zoom van de broek
add(6,13,"fff")
add(7,13,"1345")
add(8,13,"1345")
add(9,13,"f455")
add(10,13,"_fff")
add(7,17,"9"); add(8,17,"9"); add(9,17,"9"); add(10,17,"f")
# --- verre voet (Hitmontop rechtervoet, kleiner, zijaanzicht, klauwen naar rechtsboven)
add(0,54,"99988ff")
add(1,53,"9666667c11f")
add(2,50,"dcf766667911f")
add(3,51,"df776677c1f")
add(4,52,"f97777889cf")
add(5,53,"f9c118ff")
add(6,55,"f345f")
add(7,55,"f9998f")
# --- romp, hals, vrije arm (bovenarm langs de bovenflank, elleboog bij de taille, hand op de buik),
#     cordão met knoop en twee hangende einden, schouder + bovenkant steunarm. Per rij met de hand.
def clr(y,x0,x1):
    for x in range(x0,x1+1): rows[y][x]='.'
for y in range(22,48): clr(y,20,61)
R={
22:[(42,"ff"),(44,"9"+"7"*10+"88f")],
23:[(41,"523f"),(45,"7"*10+"88f")],
24:[(40,"52334f"),(46,"7"*8+"88f")],
25:[(39,"5233334f"),(47,"7"*6+"88f")],
26:[(38,"52334"),(43,"5"),(44,"334f"),(48,"777788f")],
27:[(37,"52334"),(42,"53"),(44,"5555"),(48,"ab778f")],
28:[(36,"52334"),(41,"53"),(43,"52233f"),(49,"ab7f")],
29:[(35,"52334"),(40,"53"),(42,"5222233f"),(50,"af")],
30:[(34,"52334"),(39,"533"),(42,"5222233f"),(50,"faaf")],
31:[(33,"5ab34"),(38,"5333"),(42,"5322333f"),(50,"fabbf")],
32:[(32,"523ab"),(37,"53333"),(42,"5333334f"),(51,"fafbf")],
33:[(31,"52334"),(36,"5333333"),(43,"f3334f"),(51,"fafbf")],
34:[(30,"52334"),(35,"533333344"),(44,"ffff"),(51,"fafbf")],
35:[(29,"52334"),(34,"53333333344f"),(51,"fafbf")],
36:[(28,"52334"),(33,"53333333344f"),(51,"faff")],
37:[(27,"52334"),(32,"533333333344f"),(51,"faf")],
38:[(28,"334"),(31,"53333333334 4f".replace(' ','')),(51,"fbf")],
39:[(28,"34"),(30,"5333333333344f"),(52,"f")],
40:[(27,"443333333334 4f".replace(' ',''))],
41:[(26,"4444333333334 4f".replace(' ',''))],
42:[(24,"44333333333334 4f".replace(' ',''))],
43:[(23,"4433333333333334f")],
44:[(22,"ffffffffff53344f")],
45:[(32,"52334f")],
46:[(32,"5234f")],
47:[(32,"faabf"),(37,"f")],
}
for y,l in R.items():
    for x0,s_ in l: add(y,x0,s_)
# --- steunarm (recht omlaag) met prajiad en witte polswikkel (Hitmontop-pols)
add(48,32,"fbbbf"); add(48,37,"af")
add(49,32,"5234f"); add(49,37,"bf")
add(50,32,"5234f"); add(50,37,"f")
add(51,32,"5234f")
add(52,32,"5234f")
add(53,32,"f1d1f")
add(54,32,"fcddf")
# steunhand = Hitmontop-hand (orig. x9-16, y28-35) pixel voor pixel
add(55,30,"__5555__")
add(56,30,"_52233f_")
add(57,30,"5222233f")
add(58,30,"5222233f")
add(59,30,"5322333f")
add(60,30,"5333334f")
add(61,30,"_f3334f_")
add(62,30,"__ffff__")
for y,l in E.items():
    for x0,s in l: seg(y,x0,s)
from kop import kop
k=kop()
for y in range(26):
    for x in range(42):
        if k[y][x] and 0<=x-3<64: rows[y+20][x-3]='%x'%k[y][x]
# alles 1 px naar rechts en 1 px omlaag (marge boven/links)
rows=[['.']*64]+[['.']+r[:63] for r in rows[:63]]
open('raster.txt','w').write('\n'.join(''.join(r) for r in rows)+'\n')
