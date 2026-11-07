# Eind r4: bovenkant kop (rij y2 kaarsrecht x23-37) -> bolle koepel. Zone x18-42, y0-5.
# Jordi (7 nov): "het valt mij op dat de bovenkant een rechte lijn is, dat moet wat meer boller.
#  Houd voor de rest alles hetzelfde". Elke wijziging met controle op de oude waarde.
# Koepel (buitenlijn per rij): y2 x23-24 | y1 x25-27 | y0 x28-31 | y1 x32-34 | y2 x35-36 | y3 x37-38 (trappen 2-3-4-3-2-2),
#  symmetrisch rond x29,5 (oude rand y2 x23-36).
# Selout lichtkant 4 (hoekpixel 3 op x24 y2 blijft), rechts 4 -> 2 -> 1 zoals nu; binnen 8,
# schaduw 4 op x34 y2 (naast de zwarte rand, zoals x36 y3) (sluit aan op de bestaande 4-sikkel x36 y3 / x39 y4).
# Haartjes (4): oud y1 x24 en x26-28 -> nu y1 x23 en y0 x24-25: één streng schuin omhoog-links boven de nieuwe rand (poging 1 had y0 x25-26: las samen met de koepeltop als een nieuwe rechte lijn).
import numpy as np; from PIL import Image
im=Image.open('../eind_r3/potoo.png'); a=np.array(im); pal=im.getpalette()
R=[]  # (x,y,oud,nieuw)
# y0: haartjes x24-25 (schuin omhoog-links vanaf x23 y1, zoals in het model), buitenlijn x28-31
R+=[(24,0,0,4),(25,0,0,4)]+[(x,0,0,4) for x in range(28,32)]
# y1: haartje x23; oud haartje x24 weg; buitenlijn x25-27 (x26-27 waren al 4: haartjes worden rand);
#     x28 oud haartje -> binnen 8; binnen x29-31 = 8; buitenlijn x32-33 = 4, x34 = 2
R+=[(23,1,0,4),(24,1,4,0),(25,1,0,4),(28,1,4,8)]+[(x,1,0,8) for x in range(29,32)]
R+=[(32,1,0,4),(33,1,0,4),(34,1,0,2)]
# y2: oude rechte rand x25-33 (4) -> binnen 8; x34 (2) -> schaduw 4. x23 4, x24 3, x35-36 1 blijven.
R+=[(x,2,4,8) for x in range(25,34)]+[(34,2,2,4)]
b=a.copy(); fout=[]
for x,y,old,new in R:
    assert 18<=x<=42 and 0<=y<=5
    if a[y,x]!=old: fout.append((x,y,int(a[y,x]),old)); continue
    b[y,x]=new
print('wissels in lijst',len(R),'| gewijzigd',int((b!=a).sum()),'| afwijkende oude waarden:',fout)
d=np.argwhere(b!=a)
print('diff buiten zone x18-42 y0-5:',[(int(x),int(y)) for y,x in d if not(18<=x<=42 and 0<=y<=5)])
if not fout:
    o=Image.fromarray(b,'P'); o.putpalette(pal); o.save('potoo.png',transparency=0)
