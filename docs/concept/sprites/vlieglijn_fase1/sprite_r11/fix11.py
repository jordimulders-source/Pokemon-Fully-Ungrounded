# r11 = r10 + zwevend voetje donkerder (Jordi, 20 nov: "Het zwevend voetje moet donkerder qua schaduw").
# Index 8 (kwam maar 2x voor, in de bocht van de achterpoot) wordt een extra donkere koperschaduw.
from PIL import Image
im=Image.open('sprite_r10/vlieg_r10.png'); a=im.load()
a[41,41]=7; a[41,42]=7                       # oude index-8-pixels -> kabeltint
a[39,53]=15; a[40,53]=8; a[40,54]=8          # voetje: donker koper + nieuwe diepe schaduw
pal=im.getpalette(); pal[8*3:8*3+3]=[92,38,22]; im.putpalette(pal)
im.save('sprite_r11/vlieg_r11.png',transparency=0)
p=open('sprite_r10/normal.pal').read().splitlines(); p[3+8]='92 38 22'
open('sprite_r11/normal.pal','w').write('\r\n'.join(p)+'\r\n')
im2=Image.open('sprite_r11/vlieg_r11.png').convert('RGBA')
bg=Image.new('RGBA',im2.size,(255,255,255,255)); bg.alpha_composite(im2)
bg.convert('RGB').resize((512,512),Image.NEAREST).save('sprite_r11/vlieg_r11_8x.png')
bg.convert('RGB').crop((22,34,50,62)).resize((28*16,28*16),Image.NEAREST).save('sprite_r11/poten_16x.png')
