# r7 = r6 + kleine DFC-reparaties (eindkeuring 19 nov). Draaien vanuit deze map: python3 bouw.py
from PIL import Image; import numpy as np
r6=Image.open('../r6/lama.png'); a=np.array(r6); O=a.copy()
fix={
 # 1. open rand: bovenste pixel linkerkwastje zonder omlijning (licht rood op de buitenrand)
 (11,5):1,
 # 2. open rand onder de buik tussen de achterpoten (licht/midden bruin op de buitenrand, schaduwkant -> zwart)
 (40,48):1, (41,49):1, (42,50):1, (43,50):1, (44,50):1, (45,50):1,
 # 3. verre voorpoot: bovenkant lag in de lichtste tint (6/5) direct onder de buik -> slagschaduw (3), zoals de nabije poot (20,48)
 (22,48):3, (23,48):3, (24,48):3, (25,48):3,
}
for (x,y),v in fix.items():
    assert a[y,x]!=0, (x,y); O[y,x]=v
pal=r6.getpalette()[:48]
# 4. kleurramp vacht: hooglicht 6 (231,181,128) lag maar ~22 helderheid boven 5; nu ~34 (Gen 3: 30-40)
pal[6*3:6*3+3]=[238,192,140]
out=Image.fromarray(O,'P'); out.putpalette(pal); out.save('lama.png',transparency=0)
assert ((O>0)==(a>0)).all(), 'alfa-diff'
print('alfa-diff 0; pixels veranderd:',(O!=a).sum())
with open('normal.pal','w',newline='\r\n') as f:
    f.write('JASC-PAL\n0100\n16\n'+''.join('%d %d %d\n'%tuple(pal[i:i+3]) for i in range(0,48,3)))
