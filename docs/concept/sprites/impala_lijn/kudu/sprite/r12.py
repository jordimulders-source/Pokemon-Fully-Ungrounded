# Ronde 12: B6a (r10) netter, minder rechte lijnen. Vorm en manier van B6a blijven; oog K4 blijft.
# Uitgangspunt is de png r10/kudu_r10_B6a.png zelf (niet opnieuw gebouwd). Alleen per pixel: trappen/rechte
# stukken in de omtrek van franje, nekmanen, halsstrook en schouder naar een curve; halsstrook 1 px meegebogen (2 px breed).
import numpy as np, r8lib as L
from PIL import Image
INV={v:k for k,v in L.PAL.items() if k!='.'}
def lees(pad):
    a=np.array(Image.open(pad).convert('RGBA')); OX=(64-L.W)//2; OY=64-L.H
    return [''.join('.' if a[OY+y,OX+x,3]==0 else INV[tuple(int(v) for v in a[OY+y,OX+x,:3])] for x in range(L.W)) for y in range(L.H)]
B6A=lees('r10/kudu_r10_B6a.png')
g=[list(r) for r in B6A]; LOG={}
def put(x,y,c,why):
    assert g[y][x]!=c,(x,y,c)
    LOG[(x,y)]=(g[y][x],c,why); g[y][x]=c
# 1 keelfranje: linkerrand x9 (r30-33, 4 recht) -> 9,9,9 | 8,8,8 | 9 | 10 (bolling begint 1 rij eerder);
#   rechterrand x12 (r30-34, 5 recht) en x13 (r35-38, 4 recht) -> 12,12,12 | 13,13,13 | 14,14 (volgt de gebogen halsstrook)
put(8,33,'d','franje: linkerrand buigt 1 px uit (bolling begint op rij 33); lichtkant d zoals rij 32/34')
put(9,33,'l','franje: vulling (was linkerrand), tint van de buren (l)')
put(12,33,'l','franje: vulling (was rechterrand), tint van de buren (l)')
put(13,33,'0','franje: rechterrand 1 px mee met de halsstrook (schaduwkant 0)')
put(12,34,'l','franje: vulling (was rechterrand), tint van kolom x12 eronder (l)')
put(13,34,'0','franje: rechterrand 1 px mee met de halsstrook (schaduwkant 0)')
put(13,36,'l','franje: vulling (was rechterrand), tint van de buur links (l)')
put(14,36,'0','franje: rechterrand 1 px mee met de halsstrook (schaduwkant 0)')
put(13,37,'l','franje: vulling (was rechterrand), tint van de buur links (l)')
put(14,37,'0','franje: rechterrand 1 px mee met de halsstrook (was D-slagschaduw, nu rand)')
# 2 halsstrook (2 px M) als boog: r28 x13(+x12 D) | r29 12-13 | r30-32 13-14 | r33-35 14-15 | r36-38 15-16 | r39 16-17
#   nekmanen-linkerrand (lichtkant d): x14 r28-29 | x15 r30-32 | x16 r33-35 | x17 r36-38 (was x15 r28-35, 8 recht)
put(14,28,'d','nekmanen: linkerrand 1 px naar links (boog begint onder de kaak)')
put(14,29,'d','nekmanen: linkerrand 1 px naar links (boog begint onder de kaak)')
put(15,28,'m','nekmanen: vulling (was rand), tint van de buur rechts (m)')
put(15,29,'m','nekmanen: vulling (was rand), tint van de buur rechts (m)')
for y in (33,34,35):
    put(15,y,'M','halsstrook 1 px meegebogen (lijftint M)')
    put(16,y,'d','nekmanen: linkerrand 1 px mee met de halsstrook (lichtkant d)')
for y in (36,37):
    put(16,y,'M','halsstrook 1 px meegebogen (lijftint M)')
    put(17,y,'d','nekmanen: linkerrand 1 px mee met de halsstrook (lichtkant d)')
put(17,35,'l','nekmanen: losse m-pixel (1 px vlakje na de randverschuiving) -> tint van de buren (l)')
put(16,38,'M','halsstrook 1 px meegebogen (lijftint M); de punt eindigt op (17,38) zoals in B6a')
# 3 schouderrand x26 (r32-36, 5 recht) -> ronde boog 25 | 26,26 | 27,27,27 | 26,26 | 25 | 24, slagschaduw D schuift mee
for y,c in ((34,'l'),(35,'l'),(36,'m')):
    put(26,y,c,'schouder: vulling (was rand), tint van de buur links')
    put(27,y,'0','schouder: rand 1 px naar buiten (boog; schaduwkant 0)')
    put(28,y,'D','schouder: slagschaduw D schuift mee (1 px naast de rand, zoals in B6a)')
for y in (37,38):
    put(25,y,'m','schouder: vulling (was rand), tint van de buur links (m)')
    put(26,y,'0','schouder: rand 1 px naar buiten (boog; schaduwkant 0)')
    put(27,y,'D','schouder: slagschaduw D schuift mee (1 px naast de rand, zoals in B6a)')
G=[''.join(r) for r in g]
if __name__=='__main__':
    L.toon(G,22,46,36)
