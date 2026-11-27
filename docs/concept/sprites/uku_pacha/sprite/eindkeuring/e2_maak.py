# Eindkeuring stap 2: ruispixel + tintladders (meer contrast) -> uku_pacha_e.png
from lib import *
R=lees('raster_e1.txt')
R[47][25]='b'
# vleugelpunt ligt vóór de geest: rand naar de geest (onder/rechts = schaduwkant) blijft zwart
for x,y in [(53,31),(54,32),(52,32),(53,32),(51,33),(50,33),(49,34)]: R[y][x]='K'
# hals/kronkel binnen het vleugelvak: lijn in de eigen donkerste tint n, niet vleugelblauw
for x,y in [(36,35),(38,35),(41,41),(42,41)]: R[y][x]='n'   # los m-pixeltje tussen twee lijnpixels -> vlak eronder (b)
schrijf(R,'raster_e.txt')
PAL_E=dict(PAL)
# lichaamsladder n-d-s-m: stappen 28/29/37 i.p.v. 28/23/27 (n en d iets blauwer: hue shift naar de schaduw)
PAL_E['n']=(32,44,70); PAL_E['d']=(60,72,98); PAL_E['s']=(84,104,136); PAL_E['m']=(114,138,168)
png(R,'uku_pacha_e.png',PAL_E)
# controles
from PIL import Image
im=Image.open('uku_pacha_e.png'); pal=im.getpalette()
c=lambda x,y: tuple(pal[3*im.getpixel((x,y)):3*im.getpixel((x,y))+3])
print('linkeroog', [ (xy,c(*xy)) for xy in [(10,16),(10,17),(11,16),(11,17)]])
print('rechteroog',[ (xy,c(*xy)) for xy in [(38,5),(39,5),(40,5)]])
print('kleuren',len(set(im.getdata())), im.size, im.mode, im.info)
O=Image.open('../r7/uku_pacha_r7A.png')
d=[(x,y) for y in range(64) for x in range(64) if (im.getpixel((x,y))==0)!=(O.getpixel((x,y))==0)]
print('alpha-wijzigingen',len(d),d)
d2=sum(1 for y in range(64) for x in range(64) if im.getpixel((x,y))!=O.getpixel((x,y)))
print('pixels met andere index',d2)
