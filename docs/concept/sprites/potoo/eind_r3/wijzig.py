# Eind r3: rechterrand vleugel (x45, y31-48 kaarsrecht) -> licht bolle curve. Zone x40-47, y28-50.
# Jordi (7 nov): "ja die mag wat minder kaarsrecht nog". Elke wijziging met controle op de oude waarde.
import numpy as np; from PIL import Image
im=Image.open('../eind_r2/potoo.png'); a=np.array(im); pal=im.getpalette()
# (x,y,oud,nieuw)  0=transparant 1=zwart 5/6=schaduwtinten vleugel
R=[]
# y31: rand 45->46
R+=[(45,31,1,6),(46,31,0,1)]  # 6, geen los 5-pixel boven de sikkel
# y32-37: rand 45->47 (top van de bolling), sikkel 5 op x46, 6 erbinnen
for y in range(32,38):
    R+=[(45,y,1,6),(46,y,0,5),(47,y,0,1)]
R+=[(44,36,5,6),(44,37,5,6)]
# y38-42: rand 45->46, sikkel 5 op x45, oude sikkel op x44 -> 6 (inkeping 4/3 op y41-42 blijft)
for y in range(38,43):
    R+=[(45,y,1,5),(46,y,0,1)]
R+=[(44,38,5,6),(44,39,5,6),(44,40,5,6)]
# y43-46: rand blijft 45
# y47-48: rand 45->44
R+=[(45,47,1,0),(44,47,5,1),(45,48,1,0),(44,48,4,1),(43,48,6,5)]
b=a.copy(); fout=[]
for x,y,old,new in R:
    assert 40<=x<=47 and 28<=y<=50
    if a[y,x]!=old: fout.append((x,y,int(a[y,x]),old)); continue
    b[y,x]=new
print('gewijzigd',int((b!=a).sum()),'afwijkend:',fout)
d=np.argwhere(b!=a)
buiten=[(x,y) for y,x in d if not(40<=x<=47 and 28<=y<=50)]
print('diff buiten zone x40-47 y28-50:',len(buiten))
if not fout:
    o=Image.fromarray(b,'P'); o.putpalette(pal); o.save('potoo.png',transparency=0)
