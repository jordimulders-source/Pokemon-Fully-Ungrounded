# r11 = r10B (patroon B, hoofd, band, lijfvlakken diff 0) met:
# 1. armen als ronde stenen staven: per rij doorsnede (bovenrand licht -> hooglicht -> schaduw onder), tint varieert langs de lengte
#    (aanzet bij de schouder in de schaduw van kop/lijf, bolling in het midden het lichtst, eindvlak met eigen licht en een randje);
#    nabije rechterarm staat aan de schaduwkant (licht linksboven) en is ±1 stap donkerder dan de linker.
# 2. punt als gehouwen piramide onder het blok: donkere bovenkant (schaduw van het lijf), voorvlak links licht, zijvlak/ribbe rechts donker;
#    de ribbe loopt van de lijfribbe (x20) schuin naar de top.
# 3. keurderpunten r8: nekbalk verloop licht->donker, ribbe x20 bovenaan 1 stap lichter, zijvlak lijf onderaan schaduw.
# Coördinaten = klassenraster (png = y+27, x+15); waarden = rampindex 0..8 (9 = zwart). Zwarte omlijning en silhouet blijven.
import sys; sys.path.insert(0,'gereedschap'); from r4lib import op, rgba
import numpy as np; from PIL import Image
src=np.array(Image.open('sprite_r10/baltoy_r10B.png')); PAL=Image.open('sprite_r10/baltoy_r10B.png').getpalette()
OY,OX=27,15
ZONES={
'linkerarm':{  # rij: {x: tint}
 19:{8:6,9:6},
 20:{6:5,7:4,8:5,9:6},
 21:{5:5,6:3,7:4,8:6,9:6},
 22:{4:5,5:2,6:3,7:5},
 23:{3:4,4:1,5:3,6:5},
 24:{2:4,3:1,4:2,5:5},
 25:{1:5,2:2,3:3,4:6},
 26:{0:5,1:2,2:3,3:5,4:6},       # einde van de staaf, randje x3-4
 27:{1:3,2:2,3:4},               # eindvlak (eigen licht linksboven)
 28:{2:4}},
'rechterarm':{
 20:{23:6,24:6},
 21:{23:6,24:5,25:4,26:4},
 22:{25:6,26:4,27:3,28:4},
 23:{26:6,27:4,28:2,29:3},
 24:{27:5,28:4,29:2,30:3},
 25:{28:6,29:4,30:2,31:3},
 26:{28:6,29:5,30:3,31:4},
 27:{29:6,30:5,31:4,32:4},       # randje voor het eindvlak
 28:{29:6,30:4,31:3,32:5},       # eindvlak
 29:{30:4,31:3,32:5},
 30:{30:5,31:6}},
'punt':{
 30:{16:5,17:6,18:6,19:7},       # bovenkant in de schaduw van het lijf
 31:{15:6,16:6,17:7,18:7,19:8},
 32:{15:2,16:2,17:3,18:4,19:6},  # voorvlak licht, ribbe/zijvlak rechts
 33:{16:1,17:2,18:4,19:6},
 34:{17:2,18:5}},
'keurderpunten':{
 17:{11:5,12:6,13:6,14:7},       # nekbalk licht links -> donker rechts
 18:{11:6,12:6,13:7,14:7},
 21:{20:7},                      # ribbe voor/zij bovenaan 1 stap lichter
 28:{21:7,22:7}},                # zijvlak lijf onderaan schaduw (rij 28 hoort niet bij patroon B)
}
def bouw():
    a=src.copy()
    for z,d in ZONES.items():
        for y,row in d.items():
            for x,v in row.items():
                assert src[y+OY,x+OX] not in (0,10), (z,y,x,src[y+OY,x+OX])   # nooit transparant of zwart overschrijven
                a[y+OY,x+OX]=v+1
    return a
if __name__=='__main__':
    a=bouw(); p='sprite_r11/baltoy_r11.png'; im=Image.fromarray(a,'P'); im.putpalette(PAL); im.save(p,transparency=0)
    op(rgba(Image.open(p)),(255,255,255,255),8).save('sprite_r11/baltoy_r11_8x.png')
    toeg={(y+OY,x+OX):z for z,d in ZONES.items() for y,r in d.items() for x in r}
    m=a!=src; ys,xs=np.nonzero(m); per={}
    for y,x in zip(ys,xs): per[toeg.get((y,x),'BUITEN')]=per.get(toeg.get((y,x),'BUITEN'),0)+1
    print('gewijzigd t.o.v. r10B:',m.sum(),per,'transparantie gelijk',bool(((a==0)==(src==0)).all()),'zwart gelijk',bool(((a==10)==(src==10)).all()))
    keys='0123456789'; R={11:'P',12:'R',13:'r'}
    txt=[]
    for y in range(36):
        txt.append(''.join('.' if a[y+OY,x+OX]==0 else R.get(int(a[y+OY,x+OX]),str(int(a[y+OY,x+OX])-1)) for x in range(34)))
    open('sprite_r11/baltoy_r11.txt','w').write('\n'.join(txt)+'\n')
