# r7: alleen de kop van de kleine geest (zone x21-30, y3-13). Rest = r6 (bevroren).
# Kopvlak egaal lichaamsgroen (5); ogen op de modelplekken (natief x36-38 / x39-42, y9-11 -> sprite x22-24 / x26-29, y3-5)
# met witte glimp linksboven; 1 rij lichaamsgroen ertussen; mond = D van het model (natief x35-42, y12-16 -> x21-29, y7-12):
# hoekje linksboven, linkerrand recht, onderrand recht, rechterkant schuin omhoog, gesloten donkere rand.
# A: binnenkant lichtgroen (model). B: Weepinbell-opbouw: lichte lip langs de rand, donkere binnenkant.
from PIL import Image; import numpy as np
im=Image.open('sprite_r6/sprite.png'); pal=im.getpalette(); base=np.array(im)
W,D,M,L,K=13,6,5,2,1   # glimp, donker, lichaam, licht, zwart
def maak(var):
    a=base.copy()
    for y in range(3,13):
        for x in range(21,31):
            if not (x==21 and y==12): a[y,x]=M          # egaal kopvlak (lobplooi op (21,12) blijft)
    for x in range(22,27): a[13,x]=M                      # lichaam onder de mond
    for y in range(3,6):
        for x in list(range(22,25))+list(range(26,30)): a[y,x]=D   # ogen
    a[3,22]=W; a[3,26]=W                                  # glimp linksboven
    rand=[(x,7) for x in range(21,30)]+[(22,y) for y in range(8,12)]+[(29,y) for y in range(8,11)] \
        +[(27,11),(28,11)]+[(x,12) for x in range(22,27)]
    binnen=[(x,y) for y in range(8,11) for x in range(23,29)]+[(x,11) for x in range(23,27)]
    for p in rand: a[p[1],p[0]]=D
    rs=set(rand)
    for (x,y) in binnen:
        if var=='A': a[y,x]=L
        else:
            lip=any((x+dx,y+dy) in rs for dx,dy in((1,0),(-1,0),(0,1),(0,-1)))
            a[y,x]=L if lip else K
    o=Image.fromarray(a.astype('uint8'),'P'); o.putpalette(pal); o.save('sprite_r7/sprite_%s.png'%var,transparency=0)
    d=(a!=base); Y,X=np.mgrid[0:64,0:64]; zone=(X>=21)&(X<=30)&(Y>=3)&(Y<=13)
    print(var,'anders binnen kopzone',int((d&zone).sum()),'| buiten kopzone',int((d&~zone).sum()))
    print('\n'.join('%2d '%y+''.join('.' if v==0 else '%X'%v for v in a[y,14:40]) for y in range(0,15)))
for v in 'AB': maak(v)
