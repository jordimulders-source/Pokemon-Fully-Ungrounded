# Voorstel koeienvanger (keurder, 16 nov): r11 als basis, alleen x0-25 / y42-61 (feitelijk rijen 48-58, x0-23).
# Vormen uit het model (natief.png, 99x99; sprite x ~ (nx-9)*0.744, y ~ (ny-73)*0.744+52.5):
#  - 5 platen: lichte wig links (lichte rand + roestblad), grijze plaat die naar de punt linksonder loopt,
#    smalle middentand (roest onderaan), brede rechterplaat (roestvlek, ondiepe groef); groen tussen/onder bleef.
#  - spleten waaieren naar de punt: links leunen ze naar rechts (omlaag), rechts naar links (V van een koeienvanger).
#  - licht linksboven: lichte rand/bovenkanten in 7, vlak 11, schaduwkant 12, spleten/onderrand zwart; selout links = donkerroest 9.
# Paletindexen: 0 transp, 1 zwart, 7 licht, 8 roest, 9 donkerroest, 10 lichtgrijs (ongebruikt), 11 grijs, 12 donkergrijs; groen = 2-6,13.
from PIL import Image; import numpy as np
import os; os.chdir(os.path.dirname(os.path.abspath(__file__)))
im=Image.open('sprite.png'); r11=np.array(im); a=r11.copy()
G={2,3,4,5,6,13}
K={'.':0,'1':1,'7':7,'8':8,'9':9,'A':10,'B':11,'C':12,'g':None}
RIJ={ #   x: 000000000011111111112222
      #      012345678901234567890123
    47: '.177C977B999g',
    48: '.977C8BB7799977999977BC1',
    49: '.977C8BBBB717BBC177BBBC1',
    50: '.977C88BBBC17BBC1BBBCBC1',
    51: '.977C88BBBC17BBC188BCBC1',
    52: '9877C89BBBC17BC1B88CBBC1',
    53: '9877C9BBBBC1789CB88CBCC1',
    54: '.977C1BBBC1g1891BBBCBCC1',
    55: '.977C1BBB1gg1891111111111',
    56: '..177BBC11gg891gggg....g',
    57: '...17BBC1ggg11gggg.....g',
    58: '...17BC111gggggggg......',
}
for y,s in RIJ.items():
    for x,c in enumerate(s[:24]):
        v=K[c]
        if v is None: assert r11[y,x] in G,(x,y); continue
        assert r11[y,x] not in G,('groen overschreven',x,y)
        a[y,x]=v
d=(a!=r11)
assert all(0<=x<=25 and 42<=y<=61 for y,x in zip(*np.where(d))),'buiten de zone'
assert all(a[y,x]==r11[y,x] for y in range(64) for x in range(64) if r11[y,x] in G or a[y,x] in G),'groen gewijzigd'
out=Image.fromarray(a,'P'); out.putpalette(im.getpalette()); out.save('voorstel.png',transparency=0)
rgba=out.convert('RGBA')
for z in (8,16):
    b=Image.new('RGBA',rgba.size,(255,255,255,255)); b.alpha_composite(rgba)
    b.convert('RGB').resize((64*z,64*z),Image.NEAREST).save('voorstel_%dx.png'%z)
print('gewijzigd t.o.v. r11:',int(d.sum()),'px; groen gewijzigd: 0')
for y in range(44,61): print('%2d '%y+''.join('g' if v in G else '.' if v==0 else '%X'%v for v in a[y,:26]))
