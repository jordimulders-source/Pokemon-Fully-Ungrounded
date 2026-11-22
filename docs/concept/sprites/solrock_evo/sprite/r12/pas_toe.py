# Ronde 12: eindkeuring r11 B (MOET + MAG), per script.
from PIL import Image
im=Image.open('r11/B.png'); px=im.load(); pal=im.getpalette()
for p in [(40,31),(40,32),(39,33),(40,33),(39,34),(44,32)]: px[p]=15
px[43,34]=2
pal[3*3:3*3+3]=[94,90,112]; pal[2*3:2*3+3]=[30,28,48]
for p in [(39,21),(40,21),(41,21)]: px[p]=3
px[19,44]=1; px[21,46]=1
im.putpalette(pal); im.save('r12/sprite.png',transparency=0)
