# r11: keuring r10 (MOET 1-3 + MAG iris/band) toegepast door Claude, alleen benoemde pixels
from PIL import Image
im=Image.open('r10/welp_r10.png'); px=im.load()
E={ (13,31):4,(12,33):4,(10,33):2,(8,32):0,(9,32):2,  # neus driehoek, punt niet als stokje
    (11,39):12,(11,40):13,                  # tong breder/links
    (11,37):2,(12,36):1,(10,36):2,          # buitenrand dicht
    (20,27):6,(20,20):8 }                   # MAG: iris, bandeinde
for k,v in E.items(): px[k]=v
im.save('r11/welp_r11.png',transparency=0)
im2=Image.open('r11/welp_r11.png').convert('RGBA'); im2.resize((512,512),Image.NEAREST).save('r11/welp_r11_8x.png')
