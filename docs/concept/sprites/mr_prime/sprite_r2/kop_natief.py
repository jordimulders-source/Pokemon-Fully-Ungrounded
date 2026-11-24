# r2, op het natieve raster (natief_stok.png -> natief_kop.png), alleen modelpixels:
# a) linker (grijze) ring weg: buitenste ringpixels rond (82.5,62.5), straal 4.4-6.4 -> wit (de witte modelkleur eronder)
# b) voorhoofd: de witte modelrij onder de hoedrand (rij 56) 5x dupliceren in de kopkolommen; alles erboven
#    (r9-hoed/lokken, worden toch vervangen) schuift 5 natieve px = 2 spritepx omhoog.
from PIL import Image; import numpy as np
a=np.asarray(Image.open('natief_stok.png').convert('RGB')).copy(); L=a.astype(int).mean(axis=2)
n=0
for y in range(56,69):
    for x in range(76,90):
        d=((x-82.5)**2+(y-62.5)**2)**.5
        if 4.4<=d<=6.4 and 30<=L[y,x]<235: a[y,x]=255; n+=1
print('linkerring weg',n,'px')
b=a.copy(); X0,X1,K=60,140,5
b[0:56-K,X0:X1]=a[K:56,X0:X1]
for k in range(K): b[56-K+k,X0:X1]=a[56,X0:X1]
Image.fromarray(b).save('natief_kop.png')
# c) hand over de stok (opdracht coordinator r2): in de handschoenrijen worden stokpixels die binnen de
#    handschoenomtrek (tussen de meest linkse en meest rechtse handschoenpixel van die rij) liggen wit = de witte
#    vulkleur van de handschoen in het model. Boven en onder de hand blijft de stok.
c=np.asarray(Image.open('natief_kop.png').convert('RGB')).copy(); L=c.astype(int).mean(axis=2); m=0
for y in range(82,102):
    g=[x for x in range(30,56) if 95<=L[y,x]<250]
    if len(g)<2: continue
    for x in range(min(g)+1,max(g)):
        if L[y,x]<95 and abs(x-(36.5+0.74*(y-82)))<=6: c[y,x]=255; m+=1   # alleen de stok, niet de vingerlijnen
Image.fromarray(c).save('natief_kop.png'); print('stokpixels onder de hand -> handschoenwit',m)
