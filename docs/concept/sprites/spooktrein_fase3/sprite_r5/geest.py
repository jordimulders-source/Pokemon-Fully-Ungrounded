# r5 = r4 + kleine geest 1-op-1 uit het natieve model (niet verkleind, dus ±1/3 groter), alleen palet-kwantisering.
# Jordi: "bij de kleine geest is het belangrijk dat de mond volledig klopt" / "als dat niet lukt, moet die groter worden".
from PIL import Image; import numpy as np
s=Image.open('sprite_r4/sprite.png'); pal=s.getpalette(); a=np.array(s)
n=np.array(Image.open('model/natief.png').convert('RGB')).astype(int)
DX,DY=-15,-6
GROEN=[2,3,4,5,6]; IJZER=[1,7,8,9,10,11,12]
pal[13*3:13*3+3]=[232,248,232]  # glimp in de ogen (model: wit)
P=np.array(pal[:16*3]).reshape(16,3)
# oude geest weg (alleen groen boven de schoorsteen)
for y in range(0,14):
    for x in range(64):
        if a[y,x] in GROEN: a[y,x]=0
for y in range(6,21):
    for x in range(26,64):
        c=n[y,x]; ty,tx=y+DY,x+DX
        if not(0<=ty<64 and 0<=tx<64): continue
        if c.min()>225:
            # wit: glimp als het omringd is door geest
            nb=[n[y+dy,x+dx] for dy,dx in((1,0),(-1,0),(0,1),(0,-1))]
            if sum(v.min()<=225 for v in nb)>=3: a[ty,tx]=13
            continue
        if not (c[1]>c[0]+30): continue   # alleen geest-groen
        k=GROEN[int(np.argmin(((P[GROEN]-c)**2).sum(1)))]
        if a[ty,tx] in IJZER and ty>=13: continue
        a[ty,tx]=k
o=Image.fromarray(a.astype('uint8'),'P'); o.putpalette(pal); o.save('sprite_r5/sprite.png',transparency=0)
o2=Image.open('sprite_r5/sprite.png').convert('RGBA'); bg=Image.new('RGBA',(64,64),(255,255,255,255)); bg.alpha_composite(o2)
bg.convert('RGB').resize((512,512),Image.NEAREST).save('sprite_r5/sprite_8x.png')
c=bg.crop((8,0,50,18)).resize((42*16,18*16),Image.NEAREST); c.save('sprite_r5/geest_16x.png')
