# r12 = r11 met: (1) stekel weer als stekel: r10B/r8-tinten (donkere band onder het lijf, licht voorvlak dat naar de tip smal uitloopt,
# donkere rechterkant), tip helder; (2) de twee 'mond'-pixels onder de neus (klassen (15,12) en (15,14)) -> omringende gezichtstint.
# Alles verder diff 0 t.o.v. r11. Coördinaten = klassenraster (png = y+27, x+15), waarden = rampindex.
import sys; sys.path.insert(0,'gereedschap'); from r4lib import op, rgba
import numpy as np; from PIL import Image
src=np.array(Image.open('sprite_r11/baltoy_r11.png')); PAL=Image.open('sprite_r11/baltoy_r11.png').getpalette(); OY,OX=27,15
VAR={
 'r10B':{30:{16:5,17:6,18:6,19:7},31:{15:7,16:8,17:8,18:8,19:8},32:{15:1,16:3,17:3,18:4,19:4},33:{16:2,17:3,18:3,19:5},34:{17:3,18:5}},
 'spits':{30:{16:5,17:6,18:6,19:7},31:{15:7,16:8,17:8,18:8,19:8},32:{15:2,16:2,17:3,18:4,19:6},33:{16:2,17:2,18:4,19:6},34:{17:1,18:5}},
}
KEUZE=sys.argv[1] if len(sys.argv)>1 else 'spits'
ZONES={'stekel':VAR[KEUZE],'mond':{15:{12:2,14:3}}}
def bouw():
    a=src.copy()
    for z,d in ZONES.items():
        for y,row in d.items():
            for x,v in row.items():
                assert src[y+OY,x+OX] not in (0,10),(z,y,x); a[y+OY,x+OX]=v+1
    return a
if __name__=='__main__':
    a=bouw(); p='sprite_r12/baltoy_r12.png'; im=Image.fromarray(a,'P'); im.putpalette(PAL); im.save(p,transparency=0)
    op(rgba(Image.open(p)),(255,255,255,255),8).save('sprite_r12/baltoy_r12_8x.png')
    R={11:'P',12:'R',13:'r'}
    open('sprite_r12/baltoy_r12.txt','w').write('\n'.join(''.join('.' if a[y+OY,x+OX]==0 else R.get(int(a[y+OY,x+OX]),str(int(a[y+OY,x+OX])-1)) for x in range(34)) for y in range(36))+'\n')
    toeg={(y+OY,x+OX):z for z,d in ZONES.items() for y,r in d.items() for x in r}; m=a!=src; per={}
    for y,x in zip(*np.nonzero(m)): per[toeg.get((y,x),'BUITEN')]=per.get(toeg.get((y,x),'BUITEN'),0)+1
    print(KEUZE,'gewijzigd t.o.v. r11:',int(m.sum()),per,'transparantie gelijk',bool(((a==0)==(src==0)).all()),'zwart gelijk',bool(((a==10)==(src==10)).all()))
